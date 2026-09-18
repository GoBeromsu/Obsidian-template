#!/usr/bin/env python3
"""Fetch Beomsu YouTube upload stats from Ataraxia notes + YouTube Data API.

Default output: JSON summary.
Use --discord for a compact Discord-friendly Markdown report.
This script intentionally avoids printing OAuth secrets.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import os
import re
import statistics
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

VAULT = Path(os.environ.get('OBSIDIAN_VAULT_PATH') or Path.home() / 'Obsidian/Ataraxia').expanduser()
YOUTUBE_DIR = VAULT / '15. Work/02 Area/Youtube'
CONFIG_DIR = Path.home() / '.config/youtube-upload'

FM_RE = re.compile(r'^---\n(.*?)\n---\n', re.S)


def parse_frontmatter(text: str) -> dict:
    match = FM_RE.match(text)
    if not match:
        return {}
    data = {}
    lines = match.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.startswith(' '):
            i += 1
            continue
        if ':' not in line:
            i += 1
            continue
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()
        if value == '':
            arr = []
            j = i + 1
            while j < len(lines) and (lines[j].startswith('  ') or lines[j].startswith('\t')):
                item = lines[j].strip()
                if item.startswith('- '):
                    arr.append(item[2:].strip().strip('"\''))
                j += 1
            data[key] = arr
            i = j
            continue
        data[key] = value.strip('"\'')
        i += 1
    return data


def topic_bucket(title: str, text: str) -> str:
    s = (title + ' ' + text[:2500]).lower()
    if any(w in s for w in ['hermes', 'claude', 'agent', 'openclaw', 'ai agent', 'closed-loop', 'harness']):
        return 'AI agents / Hermes'
    if any(w in s for w in ['obsidian', 'second-brain', 'second brain', 'vault', 'pkm', 'knowledge']):
        return 'Obsidian / PKM'
    if any(w in s for w in ['daily log', 'sprint', 'hackathon', 'progress', 'solo founder']):
        return 'Daily build log'
    if any(w in s for w in ['english', 'speaking', 'pronunciation']):
        return 'English practice'
    return 'Other'


def parse_iso_duration(value: str | None) -> int | None:
    if not value:
        return None
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', value)
    if not match:
        return None
    h = int(match.group(1) or 0)
    m = int(match.group(2) or 0)
    s = int(match.group(3) or 0)
    return h * 3600 + m * 60 + s


def collect_records() -> list[dict]:
    records = []
    for path in YOUTUBE_DIR.glob('*.md'):
        text = path.read_text(encoding='utf-8', errors='ignore')
        fm = parse_frontmatter(text)
        tags = fm.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        if fm.get('type') != 'video' or not any('youtube/uploaded' in str(tag) for tag in tags):
            continue
        video_id = fm.get('video_id')
        if not video_id:
            src = fm.get('source', '')
            match = re.search(r'(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})', src)
            video_id = match.group(1) if match else None
        if not video_id:
            continue
        title = fm.get('title') or path.stem
        try:
            note_duration = float(fm.get('duration_seconds') or 0) or None
        except ValueError:
            note_duration = None
        records.append({
            'video_id': video_id,
            'note_title': title,
            'note_date': (fm.get('date_published') or '')[:10],
            'language': fm.get('language', 'unknown') or 'unknown',
            'note_duration': note_duration,
            'path': str(path.relative_to(VAULT)),
            'topic': topic_bucket(title, text),
        })
    return records


def refresh_access_token() -> str:
    credentials_path = CONFIG_DIR / 'credentials.json'
    token_path = CONFIG_DIR / 'token.json'
    if not credentials_path.exists() or not token_path.exists():
        raise SystemExit(f'Missing OAuth files under {CONFIG_DIR}')
    credentials = json.loads(credentials_path.read_text())['installed']
    token = json.loads(token_path.read_text())
    payload = urllib.parse.urlencode({
        'client_id': credentials.get('client_id') or token.get('client_id'),
        'client_secret': credentials.get('client_secret') or token.get('client_secret'),
        'refresh_token': token['refresh_token'],
        'grant_type': 'refresh_token',
    }).encode()
    request = urllib.request.Request('https://oauth2.googleapis.com/token', data=payload, method='POST')
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            refreshed = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode('utf-8', 'replace'))
            err = body.get('error') or f'HTTP {exc.code}'
            desc = body.get('error_description') or 'OAuth refresh failed'
        except Exception:
            err = f'HTTP {exc.code}'
            desc = 'OAuth refresh failed'
        raise SystemExit(f'YouTube OAuth refresh failed safely: {err}: {desc}. Re-run auth-only with the required scopes; do not print token contents.')
    token['token'] = refreshed['access_token']
    token['expiry'] = (dt.datetime.utcnow() + dt.timedelta(seconds=refreshed.get('expires_in', 3600))).isoformat('T') + 'Z'
    token_path.write_text(json.dumps(token, indent=2))
    return refreshed['access_token']


def api_get(access_token: str, url: str, params: dict) -> dict:
    full = url + '?' + urllib.parse.urlencode(params)
    request = urllib.request.Request(full, headers={'Authorization': f'Bearer {access_token}'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def group_stats(group: list[dict]) -> dict:
    if not group:
        return {}
    views = [item['views'] for item in group]
    velocities = [item['views_per_day'] for item in group if item.get('views_per_day') is not None]
    durations = [item['duration_sec'] / 60 for item in group if item.get('duration_sec')]
    return {
        'count': len(group),
        'views_total': sum(views),
        'views_avg': round(sum(views) / len(views), 1),
        'views_median': statistics.median(views),
        'views_per_day_avg': round(sum(velocities) / len(velocities), 2) if velocities else None,
        'duration_min_avg': round(sum(durations) / len(durations), 1) if durations else None,
        'likes_total': sum(item['likes'] for item in group),
        'comments_total': sum(item['comments'] for item in group),
    }


def fetch_summary() -> dict:
    records = collect_records()
    access_token = refresh_access_token()
    now = dt.datetime.now(dt.timezone.utc)

    items = []
    ids = [record['video_id'] for record in records]
    for i in range(0, len(ids), 50):
        response = api_get(access_token, 'https://www.googleapis.com/youtube/v3/videos', {
            'part': 'snippet,statistics,contentDetails,status',
            'id': ','.join(ids[i:i+50]),
            'maxResults': 50,
        })
        items.extend(response.get('items', []))

    api_by_id = {item['id']: item for item in items}
    for record in records:
        item = api_by_id.get(record['video_id'])
        if not item:
            record['api_found'] = False
            continue
        record['api_found'] = True
        stats = item.get('statistics', {})
        snippet = item.get('snippet', {})
        details = item.get('contentDetails', {})
        record['yt_title'] = snippet.get('title')
        record['published_at'] = snippet.get('publishedAt')
        record['views'] = int(stats.get('viewCount', 0))
        record['likes'] = int(stats.get('likeCount', 0))
        record['comments'] = int(stats.get('commentCount', 0))
        record['duration_sec'] = parse_iso_duration(details.get('duration')) or record['note_duration']
        try:
            published_at = dt.datetime.fromisoformat(record['published_at'].replace('Z', '+00:00'))
            age_days = max((now - published_at).total_seconds() / 86400, 0.01)
        except Exception:
            age_days = None
        record['age_days'] = round(age_days, 2) if age_days else None
        record['views_per_day'] = round(record['views'] / age_days, 2) if age_days else None
        record['like_rate_pct'] = round(100 * record['likes'] / record['views'], 2) if record['views'] else 0
        record['comment_rate_pct'] = round(100 * record['comments'] / record['views'], 2) if record['views'] else 0

    channel = None
    channel_response = api_get(access_token, 'https://www.googleapis.com/youtube/v3/channels', {
        'part': 'snippet,statistics',
        'mine': 'true',
    })
    if channel_response.get('items'):
        item = channel_response['items'][0]
        stats = item.get('statistics', {})
        channel = {
            'title': item['snippet'].get('title'),
            'customUrl': item['snippet'].get('customUrl'),
            'subscriberCount': int(stats.get('subscriberCount', 0)),
            'viewCount': int(stats.get('viewCount', 0)),
            'videoCount': int(stats.get('videoCount', 0)),
            'hiddenSubscriberCount': stats.get('hiddenSubscriberCount'),
        }

    found = [record for record in records if record.get('api_found')]
    by_topic = collections.defaultdict(list)
    by_language = collections.defaultdict(list)
    by_month = collections.defaultdict(list)
    for record in found:
        by_topic[record['topic']].append(record)
        by_language[record['language']].append(record)
        by_month[(record.get('published_at') or record['note_date'])[:7]].append(record)

    return {
        'collected_at': now.isoformat(),
        'channel': channel,
        'records_total': len(records),
        'api_found': len(found),
        'api_missing': [record['video_id'] for record in records if not record.get('api_found')],
        'overall': group_stats(found),
        'by_topic': {key: group_stats(value) for key, value in sorted(by_topic.items())},
        'by_language': {key: group_stats(value) for key, value in sorted(by_language.items())},
        'by_month': {key: group_stats(value) for key, value in sorted(by_month.items())},
        'top_by_views': sorted(found, key=lambda record: record['views'], reverse=True)[:10],
        'top_by_velocity': sorted(found, key=lambda record: record.get('views_per_day') or 0, reverse=True)[:10],
        'recent': sorted(found, key=lambda record: record.get('published_at') or '', reverse=True)[:10],
    }


def discord_report(summary: dict) -> str:
    channel = summary.get('channel') or {}
    overall = summary.get('overall') or {}
    lines = []
    lines.append('형님, YouTube ops 스냅샷입니다.')
    lines.append('')
    lines.append('**현재 채널**')
    lines.append(f"- 구독자: {channel.get('subscriberCount', 'unknown')}")
    lines.append(f"- 전체 조회수: {channel.get('viewCount', 'unknown')}")
    lines.append(f"- 전체 영상: {channel.get('videoCount', 'unknown')}")
    lines.append('')
    lines.append('**분석 대상**')
    lines.append(f"- Obsidian 업로드 노트: {summary.get('records_total')}개")
    lines.append(f"- API 조회 성공: {summary.get('api_found')}개")
    lines.append(f"- 평균 조회수: {overall.get('views_avg')}")
    lines.append(f"- 중앙값 조회수: {overall.get('views_median')}")
    lines.append(f"- 평균 속도: {overall.get('views_per_day_avg')} views/day")
    lines.append('')
    lines.append('**지금 반응 빠른 영상 Top 5**')
    for idx, item in enumerate(summary.get('top_by_velocity', [])[:5], start=1):
        title = item.get('yt_title') or item.get('note_title')
        lines.append(f'{idx}. {title}')
        lines.append(f"   - views: {item.get('views')}")
        lines.append(f"   - speed: {item.get('views_per_day')}/day")
        lines.append(f"   - topic: {item.get('topic')}")
    lines.append('')
    lines.append('**한 줄 결론**')
    lines.append('> 누적 검증은 Obsidian/PKM, 최근 모멘텀은 Hermes/AI Agent 쪽인지 확인하세요.')
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--discord', action='store_true', help='print Discord-friendly markdown instead of JSON')
    parser.add_argument('--output', help='optional path to save JSON summary')
    args = parser.parse_args()

    summary = fetch_summary()
    if args.output:
        Path(args.output).write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    if args.discord:
        print(discord_report(summary))
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
