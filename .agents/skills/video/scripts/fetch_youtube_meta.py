#!/usr/bin/env python3
"""Print YouTube metadata as JSON for a video note. Standard library only.

Usage: python3 fetch_youtube_meta.py <youtube-url-or-id>
Fields: video_id, title, author, description, source_url, image, date_published, duration_seconds, language
Sources: oEmbed (title, author, thumbnail) + watch page ld+json / player response (uploadDate, lengthSeconds, description).
"""
import json, re, sys, urllib.parse, urllib.request

def video_id(arg: str) -> str:
    m = re.search(r'(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})', arg)
    if m: return m.group(1)
    if re.fullmatch(r'[A-Za-z0-9_-]{11}', arg): return arg
    sys.exit(f'cannot find a video id in: {arg}')

def get(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'ko,en'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', 'replace')

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    vid = video_id(sys.argv[1]); url = f'https://www.youtube.com/watch?v={vid}'
    o = json.loads(get('https://www.youtube.com/oembed?url=' + urllib.parse.quote(url, safe='') + '&format=json'))
    meta = {'video_id': vid, 'title': o.get('title', ''), 'author': o.get('author_name', '').strip(),
            'description': '', 'source_url': url, 'image': f'https://img.youtube.com/vi/{vid}/maxresdefault.jpg',
            'date_published': '', 'duration_seconds': '', 'language': ''}
    try:
        html = get(url)
        m = re.search(r'"uploadDate":"(\d{4}-\d{2}-\d{2})', html) or re.search(r'"publishDate":"(\d{4}-\d{2}-\d{2})', html)
        if m: meta['date_published'] = m.group(1)
        m = re.search(r'"lengthSeconds":"(\d+)"', html)
        if m: meta['duration_seconds'] = int(m.group(1))
        m = re.search(r'"shortDescription":"((?:[^"\\]|\\.)*)"', html)
        if m: meta['description'] = json.loads('"' + m.group(1) + '"').split('\n')[0][:200]
        m = re.search(r'"defaultAudioLanguage":"([a-zA-Z-]+)"', html)
        if m: meta['language'] = m.group(1).split('-')[0]
    except Exception as e:  # metadata beyond oEmbed is best effort
        meta['warning'] = f'watch page not parsed: {e}'
    print(json.dumps(meta, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
