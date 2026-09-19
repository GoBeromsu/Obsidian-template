#!/usr/bin/env python3
"""Print YouTube metadata, chapters, and transcript as JSON for a video note.

Usage: python3 fetch_youtube_meta.py <youtube-url-or-id>
Fields: video_id, title, author, description, source_url, image, date_published, duration_seconds, language, chapters, transcript
Sources: oEmbed (title, author, thumbnail) + watch page ld+json / player response + transcript/subtitles via youtube_transcript_api or yt-dlp fallback.
"""
import json, re, sys, urllib.parse, urllib.request, subprocess

def video_id(arg: str) -> str:
    m = re.search(r'(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})', arg)
    if m: return m.group(1)
    if re.fullmatch(r'[A-Za-z0-9_-]{11}', arg): return arg
    sys.exit(f'cannot find a video id in: {arg}')

def get(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept-Language': 'ko,en'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', 'replace')

def format_timestamp(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def parse_time_str(t_str: str) -> float:
    parts = [int(p) for p in t_str.split(':')]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0.0

def fetch_transcript_items(vid: str):
    # Method 1: youtube_transcript_api
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        ytt = YouTubeTranscriptApi()
        ts = ytt.fetch(vid, languages=['ko', 'en'])
        items = [{'start': x.start, 'duration': x.duration, 'text': x.text.strip()} for x in ts if x.text.strip()]
        if items:
            return items
    except Exception:
        pass

    # Method 2: yt-dlp json dump (extract auto/manual subtitles json3)
    try:
        res = subprocess.run(['yt-dlp', '--dump-json', '--skip-download', f'https://www.youtube.com/watch?v={vid}'],
                             capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        subs = data.get('subtitles') or {}
        auto_subs = data.get('automatic_captions') or {}
        tracks = (subs.get('ko') or subs.get('en') or auto_subs.get('ko') or auto_subs.get('en') or [])
        json3 = next((t for t in tracks if t.get('ext') == 'json3'), None)
        if json3:
            req = urllib.request.Request(json3['url'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as r:
                sub_data = json.loads(r.read().decode('utf-8'))
            items = []
            for event in sub_data.get('events', []):
                t_start = event.get('tStartMs', 0) / 1000.0
                d_dur = event.get('dDurationMs', 0) / 1000.0
                segs = event.get('segs', [])
                text = ''.join(s.get('utf8', '') for s in segs).strip()
                if text and text != '\n':
                    items.append({'start': t_start, 'duration': d_dur, 'text': text})
            if items:
                return items
    except Exception:
        pass

    return []

def build_formatted_transcript(items, chapters):
    if not items:
        return ''
    out_lines = []
    ch_idx = 0
    num_chapters = len(chapters)
    current_p = []
    current_time = 0.0

    ch_times = [parse_time_str(c['time']) for c in chapters] if chapters else []

    for item in items:
        t_start = item['start']
        text = item['text']
        if not text:
            continue

        if num_chapters > 0:
            while ch_idx + 1 < num_chapters and t_start >= ch_times[ch_idx + 1]:
                if current_p:
                    out_lines.append(f"**{format_timestamp(current_time)}** " + " ".join(current_p))
                    current_p = []
                ch_idx += 1
                c_time = chapters[ch_idx]['time']
                c_title = chapters[ch_idx]['title']
                out_lines.append(f"\n### {c_time} {c_title}\n")
                current_time = t_start

            if ch_idx == 0 and not out_lines:
                c_time = chapters[0]['time']
                c_title = chapters[0]['title']
                out_lines.append(f"### {c_time} {c_title}\n")
                current_time = t_start

        if not current_p:
            current_time = t_start
            current_p.append(text)
        elif t_start - current_time > 40 or len(" ".join(current_p)) > 250:
            out_lines.append(f"**{format_timestamp(current_time)}** " + " ".join(current_p))
            current_p = [text]
            current_time = t_start
        else:
            current_p.append(text)

    if current_p:
        out_lines.append(f"**{format_timestamp(current_time)}** " + " ".join(current_p))

    return "\n\n".join(out_lines).strip()

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    vid = video_id(sys.argv[1]); url = f'https://www.youtube.com/watch?v={vid}'
    o = json.loads(get('https://www.youtube.com/oembed?url=' + urllib.parse.quote(url, safe='') + '&format=json'))
    meta = {'video_id': vid, 'title': o.get('title', ''), 'author': o.get('author_name', '').strip(),
            'description': '', 'source_url': url, 'image': f'https://img.youtube.com/vi/{vid}/maxresdefault.jpg',
            'date_published': '', 'duration_seconds': '', 'language': '',
            'chapters': [], 'transcript': ''}
    try:
        html = get(url)
        m = re.search(r'"uploadDate":"(\d{4}-\d{2}-\d{2})', html) or re.search(r'"publishDate":"(\d{4}-\d{2}-\d{2})', html)
        if m: meta['date_published'] = m.group(1)
        m = re.search(r'"lengthSeconds":"(\d+)"', html)
        if m: meta['duration_seconds'] = int(m.group(1))

        m_resp = re.search(r'ytInitialPlayerResponse\s*=\s*({.+?});(?:var|\n|</script>)', html)
        if m_resp:
            pr = json.loads(m_resp.group(1))
            full_desc = pr.get('videoDetails', {}).get('shortDescription', '')
            for line in full_desc.split('\n'):
                m_ch = re.match(r'^(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$', line.strip())
                if m_ch:
                    meta['chapters'].append({'time': m_ch.group(1), 'title': m_ch.group(2).strip()})

        m = re.search(r'"shortDescription":"((?:[^"\\]|\\.)*)"', html)
        if m:
            first = json.loads('"' + m.group(1) + '"').split('\n')[0]
            first = re.sub(r'https?://\S+', '', first).strip(' -:|·')
            meta['description'] = first[:200]
        m = re.search(r'"defaultAudioLanguage":"([a-zA-Z-]+)"', html)
        if m: meta['language'] = m.group(1).split('-')[0]
    except Exception as e:  # metadata beyond oEmbed is best effort
        meta['warning'] = f'watch page not parsed: {e}'

    # Fetch transcript
    items = fetch_transcript_items(vid)
    if items:
        meta['transcript'] = build_formatted_transcript(items, meta['chapters'])

    print(json.dumps(meta, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
