# /// script
# requires-python = ">=3.10"
# dependencies = ["google-auth>=2.0", "requests>=2.0"]
# ///
"""YouTube channel analytics collector for Beomsu's channel.

Secret-safe: never prints access/refresh tokens or credential JSON.
Writes a JSON report and optionally prints a compact Discord-friendly summary.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import time
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

TOKEN_PATH = Path.home() / ".config" / "youtube-upload" / "token.json"
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]
YOUTUBE_ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
YOUTUBE_VIDEOS = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNELS = "https://www.googleapis.com/youtube/v3/channels"
EXPECTED_CHANNEL_TITLE = "Beomsu Koh | 고범수"
KEYWORD_TERMS = [
    "notion", "obsidian", "pkm", "vault", "moc", "graph", "plugin", "note",
    "hermes", "agent", "agents", "ai", "claude", "openclaw", "clawhip",
    "omx", "omc", "qmd", "codex", "gemini", "llm", "wiki", "discord",
    "daily log", "second brain", "music", "cover", "ccm", "sync",
]


def load_creds(token_path: Path) -> Credentials:
    if not token_path.exists():
        raise SystemExit(f"Missing token file: {token_path}")
    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds.valid:
        creds.refresh(Request())
        token_path.write_text(creds.to_json(), encoding="utf-8")
        token_path.chmod(0o600)
    return creds


class Client:
    def __init__(self, creds: Credentials):
        self.creds = creds

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.creds.token}"}

    def get_json(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        response = requests.get(url, params=params, headers=self.headers, timeout=60)
        try:
            data = response.json()
        except Exception:
            data = {"raw": response.text[:1000]}
        if response.status_code >= 400:
            return {"_error": {"status_code": response.status_code, "body": data}}
        return data

    def analytics(self, name: str, params: dict[str, Any]) -> dict[str, Any]:
        data = self.get_json(YOUTUBE_ANALYTICS, params)
        if "_error" in data:
            return {"name": name, "error": data["_error"], "rows": []}
        headers = [h["name"] for h in data.get("columnHeaders", [])]
        rows = [dict(zip(headers, row)) for row in data.get("rows", [])]
        return {"name": name, "headers": headers, "rows": rows}

    def channels_mine(self) -> dict[str, Any]:
        return self.get_json(YOUTUBE_CHANNELS, {"part": "snippet,statistics", "mine": "true", "maxResults": 50})

    def videos(self, ids: list[str]) -> dict[str, dict[str, Any]]:
        out: dict[str, dict[str, Any]] = {}
        unique = [x for x in dict.fromkeys(ids) if x]
        for i in range(0, len(unique), 50):
            data = self.get_json(YOUTUBE_VIDEOS, {
                "part": "snippet,statistics,contentDetails,status",
                "id": ",".join(unique[i:i + 50]),
                "maxResults": 50,
            })
            for item in data.get("items", []):
                snippet = item.get("snippet", {})
                stats = item.get("statistics", {})
                out[item["id"]] = {
                    "id": item["id"],
                    "title": snippet.get("title"),
                    "channelTitle": snippet.get("channelTitle"),
                    "publishedAt": snippet.get("publishedAt"),
                    "publicViewsNow": int(stats.get("viewCount", 0)),
                    "publicLikesNow": int(stats.get("likeCount", 0)) if "likeCount" in stats else None,
                    "publicCommentsNow": int(stats.get("commentCount", 0)) if "commentCount" in stats else None,
                    "privacyStatus": item.get("status", {}).get("privacyStatus"),
                }
        return out


def topic_of(title: str | None) -> str:
    text = (title or "").lower()
    if any(k in text for k in ["obsidian", "pkm", "vault", "moc", "graph", "notion", "second brain", "plugin", "note"]):
        return "Obsidian / PKM"
    if any(k in text for k in ["hermes", "agent", "claude", "openclaw", "clawhip", "omx", "omc", "qmd", "codex", "gemini", "llm", "wiki", "discord"]):
        return "AI agents / Hermes"
    if "daily log" in text or "sprint" in text:
        return "Daily build log"
    if any(k in text for k in ["english", "pronunciation", "speaking"]):
        return "English practice"
    return "Other"


def pct(num: float, den: float) -> float:
    return round(num / den * 100, 1) if den else 0.0


def rank(rows: list[dict[str, Any]], metric: str, *, min_views: int = 0, reverse: bool = True) -> list[dict[str, Any]]:
    xs = [r for r in rows if (r.get("views") or 0) >= min_views and isinstance(r.get(metric), (int, float))]
    return sorted(xs, key=lambda r: r.get(metric) or 0, reverse=reverse)


def aggregate_keywords(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    agg: dict[str, dict[str, Any]] = {}
    for term in KEYWORD_TERMS:
        agg[term] = {"count": 0, "views": 0, "watch_minutes": 0, "subscribers_gained": 0, "weighted_retention_num": 0.0}
    for row in rows:
        title = (row.get("title") or "").lower()
        views = row.get("views") or 0
        for term in KEYWORD_TERMS:
            if term in title:
                cur = agg[term]
                cur["count"] += 1
                cur["views"] += views
                cur["watch_minutes"] += row.get("estimatedMinutesWatched") or 0
                cur["subscribers_gained"] += row.get("subscribersGained") or 0
                cur["weighted_retention_num"] += (row.get("averageViewPercentage") or 0) * views
    result = {}
    for term, cur in agg.items():
        if cur["count"]:
            cur["weighted_average_view_percentage"] = round(cur["weighted_retention_num"] / cur["views"], 1) if cur["views"] else 0
            del cur["weighted_retention_num"]
            result[term] = cur
    return dict(sorted(result.items(), key=lambda item: item[1]["views"], reverse=True))


def enriched_video(row: dict[str, Any]) -> dict[str, Any]:
    """Add packaging/strategy efficiency metrics without mutating the source row."""
    out = dict(row)
    views = out.get("views") or 0
    out["subscribers_per_1000_views"] = round((out.get("subscribersGained") or 0) * 1000 / views, 2) if views else 0.0
    out["likes_per_1000_views"] = round((out.get("likes") or 0) * 1000 / views, 2) if views else 0.0
    out["comments_per_1000_views"] = round((out.get("comments") or 0) * 1000 / views, 2) if views else 0.0
    return out


def diagnosis_buckets(rows: list[dict[str, Any]], *, min_views: int = 20) -> dict[str, Any]:
    """Create strategy buckets inspired by external marketing-skill audit playbooks.

    These are not hard facts like Analytics API rows; they are deterministic heuristics
    for deciding whether to repackage, make a sequel, tighten retention, or mine comments.
    """
    eligible = [enriched_video(r) for r in rows if (r.get("views") or 0) >= min_views]
    if not eligible:
        return {"min_views": min_views, "note": "not enough videos above threshold"}

    view_median = statistics.median([r.get("views") or 0 for r in eligible])
    retention_values = [r.get("averageViewPercentage") or 0 for r in eligible]
    retention_median = statistics.median(retention_values)
    high_retention_cutoff = max(45.0, retention_median)
    weak_retention_cutoff = min(35.0, retention_median)

    def slim(r: dict[str, Any]) -> dict[str, Any]:
        keys = [
            "video", "title", "topic", "publishedAt", "views", "estimatedMinutesWatched",
            "averageViewDuration", "averageViewPercentage", "subscribersGained",
            "subscribers_per_1000_views", "likes_per_1000_views", "comments_per_1000_views",
            "publicViewsNow", "publicLikesNow", "publicCommentsNow",
        ]
        return {k: r.get(k) for k in keys if k in r}

    high_retention_low_views = [
        r for r in eligible
        if (r.get("averageViewPercentage") or 0) >= high_retention_cutoff and (r.get("views") or 0) <= view_median
    ]
    high_views_low_retention = [
        r for r in eligible
        if (r.get("views") or 0) >= view_median and (r.get("averageViewPercentage") or 0) <= weak_retention_cutoff
    ]
    subscriber_efficiency = [r for r in eligible if (r.get("subscribersGained") or 0) > 0]
    engagement_efficiency = [r for r in eligible if (r.get("likes") or 0) or (r.get("comments") or 0)]

    return {
        "min_views": min_views,
        "view_median": view_median,
        "retention_median": round(retention_median, 1),
        "high_retention_cutoff": round(high_retention_cutoff, 1),
        "weak_retention_cutoff": round(weak_retention_cutoff, 1),
        "high_retention_low_views__repackage_or_distribute": [slim(r) for r in sorted(high_retention_low_views, key=lambda r: (r.get("averageViewPercentage") or 0), reverse=True)[:10]],
        "high_views_low_retention__tighten_hook_or_promise": [slim(r) for r in sorted(high_views_low_retention, key=lambda r: (r.get("views") or 0), reverse=True)[:10]],
        "subscriber_efficiency_best__series_candidates": [slim(r) for r in sorted(subscriber_efficiency, key=lambda r: (r.get("subscribers_per_1000_views") or 0), reverse=True)[:10]],
        "engagement_efficiency_best__comment_mining_candidates": [slim(r) for r in sorted(engagement_efficiency, key=lambda r: ((r.get("comments_per_1000_views") or 0), (r.get("likes_per_1000_views") or 0)), reverse=True)[:10]],
    }


def retention_points(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {}
    points = {}
    for target in [0.0, 0.25, 0.5, 0.75, 0.95]:
        nearest = min(rows, key=lambda r: abs(float(r.get("elapsedVideoTimeRatio", 0)) - target))
        points[str(target)] = {
            "elapsedVideoTimeRatio": nearest.get("elapsedVideoTimeRatio"),
            "audienceWatchRatio": nearest.get("audienceWatchRatio"),
            "relativeRetentionPerformance": nearest.get("relativeRetentionPerformance"),
        }
    return points


def load_public_summary(path: str | None) -> dict[str, Any] | None:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def verified_channel(response: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    """Return the sole expected mine=true channel or a safe stop reason."""
    if "_error" in response:
        return None, "Could not verify the OAuth channel identity."
    items = response.get("items")
    if not isinstance(items, list) or len(items) != 1:
        return None, "OAuth channel lookup did not return exactly one channel."
    item = items[0]
    if not isinstance(item, dict):
        return None, "OAuth channel lookup returned an unreadable channel."
    title = item.get("snippet", {}).get("title")
    if title != EXPECTED_CHANNEL_TITLE:
        return None, "OAuth channel does not match the required creator channel."
    stats = item.get("statistics", {})
    return {
        "title": title,
        "customUrl": item.get("snippet", {}).get("customUrl"),
        "subscriberCount": int(stats.get("subscriberCount", 0)),
        "viewCount": int(stats.get("viewCount", 0)),
        "videoCount": int(stats.get("videoCount", 0)),
    }, None


def write_stopped_artifact(output: str, start: date, end: date, days: int,
                           reason: str) -> None:
    artifact = {
        "status": "stopped",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "period": {"startDate": start.isoformat(), "endDate": end.isoformat(), "days": days},
        "channel": {},
        "reports": {},
        "retention_curves": {},
        "derived": {},
        "caveats": [reason],
    }
    Path(output).write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")


def compact_report(out: dict[str, Any]) -> str:
    lines: list[str] = []
    channel = out.get("channel") or {}
    overall = (out.get("reports", {}).get("overall", {}).get("rows") or [{}])[0]
    traffic = out.get("derived", {}).get("traffic_source_share", [])
    retention = out.get("derived", {}).get("retention_best_min20_views", [])
    subs = out.get("derived", {}).get("subscriber_gain_best", [])
    keywords = out.get("derived", {}).get("keyword_proxy", {})
    buckets = out.get("derived", {}).get("diagnosis_buckets", {})
    lines.append("형님, YouTube Analytics API 분석 스냅샷입니다.")
    lines.append("")
    lines.append("**채널**")
    lines.append(f"- title: {channel.get('title', 'unknown')}")
    lines.append(f"- subscribers: {channel.get('subscriberCount', 'unknown')}")
    lines.append(f"- views: {channel.get('viewCount', 'unknown')}")
    lines.append(f"- videos: {channel.get('videoCount', 'unknown')}")
    lines.append("")
    lines.append("**최근 기간 전체**")
    lines.append(f"- views: {overall.get('views')}")
    lines.append(f"- watch time: {overall.get('estimatedMinutesWatched')} min")
    lines.append(f"- avg view duration: {overall.get('averageViewDuration')} sec")
    lines.append(f"- avg view %: {round(overall.get('averageViewPercentage') or 0, 1)}%")
    lines.append(f"- subscribers: +{overall.get('subscribersGained')} / -{overall.get('subscribersLost')}")
    lines.append("")
    lines.append("**유입 경로 Top**")
    for r in traffic[:5]:
        lines.append(f"- {r.get('insightTrafficSourceType')}: {r.get('views')} views ({r.get('view_share_pct')}%), watch {r.get('watch_share_pct')}%, AVD {r.get('averageViewDuration')}s")
    lines.append("")
    lines.append("**리텐션 좋은 영상**")
    for idx, r in enumerate(retention[:5], 1):
        lines.append(f"{idx}. {r.get('title')}")
        lines.append(f"   - retention {round(r.get('averageViewPercentage') or 0, 1)}%, AVD {r.get('averageViewDuration')}s, views {r.get('views')}, subs +{r.get('subscribersGained')}")
    lines.append("")
    lines.append("**구독 전환 영상**")
    for idx, r in enumerate(subs[:5], 1):
        lines.append(f"{idx}. +{r.get('subscribersGained')} subs | {r.get('views')} views | {r.get('title')}")
    lines.append("")
    lines.append("**키워드 proxy**")
    for term, r in list(keywords.items())[:8]:
        lines.append(f"- {term}: {r.get('views')} views / +{r.get('subscribers_gained')} subs / weighted retention {r.get('weighted_average_view_percentage')}%")
    if buckets and not buckets.get("note"):
        lines.append("")
        lines.append("**전략 진단 버킷**")
        repackage = buckets.get("high_retention_low_views__repackage_or_distribute", [])
        tighten = buckets.get("high_views_low_retention__tighten_hook_or_promise", [])
        series = buckets.get("subscriber_efficiency_best__series_candidates", [])
        if repackage:
            lines.append("- repackage/distribute 후보: " + "; ".join((r.get("title") or r.get("video") or "unknown")[:48] for r in repackage[:3]))
        if tighten:
            lines.append("- hook/promise 점검 후보: " + "; ".join((r.get("title") or r.get("video") or "unknown")[:48] for r in tighten[:3]))
        if series:
            lines.append("- series 후보: " + "; ".join((r.get("title") or r.get("video") or "unknown")[:48] for r in series[:3]))
    if out.get("reports", {}).get("search_terms", {}).get("error"):
        lines.append("- exact search terms: API query unavailable; use Studio export for exact terms.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect YouTube Analytics API channel report")
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--output", default="/tmp/youtube_channel_analysis.json")
    parser.add_argument("--token", default=str(TOKEN_PATH))
    parser.add_argument("--public-summary", help="Optional JSON output from fetch_youtube_stats.py")
    parser.add_argument("--retention-limit", type=int, default=12)
    parser.add_argument("--discord", action="store_true")
    args = parser.parse_args()

    end = date.today()
    start = end - timedelta(days=args.days)
    creds = load_creds(Path(args.token).expanduser())
    client = Client(creds)
    try:
        channel, channel_error = verified_channel(client.channels_mine())
    except requests.RequestException:
        channel_error = "Could not verify the OAuth channel identity."
    if channel_error:
        write_stopped_artifact(args.output, start, end, args.days, channel_error)
        print(f"STOPPED: {channel_error}", file=sys.stderr)
        return 1

    common = {"ids": "channel==MINE", "startDate": start.isoformat(), "endDate": end.isoformat()}

    reports = {
        "overall": client.analytics("overall", {**common, "metrics": "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments,shares"}),
        "by_video": client.analytics("by_video", {**common, "dimensions": "video", "metrics": "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments,shares", "sort": "-views", "maxResults": 200}),
        "traffic_source": client.analytics("traffic_source", {**common, "dimensions": "insightTrafficSourceType", "metrics": "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage", "sort": "-views"}),
        "subscribed_status": client.analytics("subscribed_status", {**common, "dimensions": "subscribedStatus", "metrics": "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage", "sort": "-views"}),
        "country": client.analytics("country", {**common, "dimensions": "country", "metrics": "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage", "sort": "-views", "maxResults": 50}),
        "day": client.analytics("day", {**common, "dimensions": "day", "metrics": "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage", "sort": "day"}),
    }

    # Try exact search terms; keep the error as a caveat when unsupported.
    # Do not pass maxResults here: in this environment the API reports a misleading
    # FIELD_UNKNOWN_VALUE for max-results before returning the real unsupported-query
    # caveat. Keep the exact failure in the JSON so reports stay honest.
    reports["search_terms"] = client.analytics("search_terms", {**common, "dimensions": "insightTrafficSourceDetail", "filters": "insightTrafficSourceType==YT_SEARCH", "metrics": "views,estimatedMinutesWatched,averageViewDuration", "sort": "-views"})

    by_video = reports["by_video"].get("rows", [])
    meta = client.videos([row.get("video") for row in by_video])
    for row in by_video:
        m = meta.get(row.get("video"), {})
        row.update(m)
        row["title"] = row.get("title") or row.get("video")
        row["topic"] = topic_of(row.get("title"))

    overall = (reports["overall"].get("rows") or [{}])[0]
    total_views = overall.get("views") or 0
    total_watch = overall.get("estimatedMinutesWatched") or 0
    traffic_share = []
    for row in reports["traffic_source"].get("rows", []):
        copy = dict(row)
        copy["view_share_pct"] = pct(copy.get("views") or 0, total_views)
        copy["watch_share_pct"] = pct(copy.get("estimatedMinutesWatched") or 0, total_watch)
        traffic_share.append(copy)

    topic_agg: dict[str, dict[str, Any]] = defaultdict(lambda: {"count": 0, "views": 0, "watch_minutes": 0, "subscribers_gained": 0, "weighted_retention_num": 0.0})
    for row in by_video:
        topic = row.get("topic") or "Other"
        views = row.get("views") or 0
        cur = topic_agg[topic]
        cur["count"] += 1
        cur["views"] += views
        cur["watch_minutes"] += row.get("estimatedMinutesWatched") or 0
        cur["subscribers_gained"] += row.get("subscribersGained") or 0
        cur["weighted_retention_num"] += (row.get("averageViewPercentage") or 0) * views
    for cur in topic_agg.values():
        cur["weighted_average_view_percentage"] = round(cur["weighted_retention_num"] / cur["views"], 1) if cur["views"] else 0
        del cur["weighted_retention_num"]

    selected_ids: list[str] = []
    def add_video(video_id: str | None) -> None:
        if video_id and video_id not in selected_ids:
            selected_ids.append(video_id)

    for row in rank(by_video, "views")[:5]:
        add_video(row.get("video"))
    for row in rank(by_video, "averageViewPercentage", min_views=20)[:5]:
        add_video(row.get("video"))
    public_summary = load_public_summary(args.public_summary)
    if public_summary:
        for item in public_summary.get("top_by_velocity", [])[:5]:
            add_video(item.get("video_id"))

    retention = {}
    for video_id in selected_ids[: max(args.retention_limit, 0)]:
        report = client.analytics(f"retention_{video_id}", {**common, "dimensions": "elapsedVideoTimeRatio", "filters": f"video=={video_id}", "metrics": "audienceWatchRatio,relativeRetentionPerformance", "sort": "elapsedVideoTimeRatio"})
        rows = report.get("rows", [])
        retention[video_id] = {
            "title": meta.get(video_id, {}).get("title") or video_id,
            "row_count": len(rows),
            "points": retention_points(rows),
            "error": report.get("error"),
        }
        time.sleep(0.05)

    derived = {
        "traffic_source_share": traffic_share,
        "retention_best_min20_views": rank(by_video, "averageViewPercentage", min_views=20)[:10],
        "retention_weak_min20_views": rank(by_video, "averageViewPercentage", min_views=20, reverse=False)[:10],
        "watch_time_best": rank(by_video, "estimatedMinutesWatched")[:10],
        "subscriber_gain_best": rank(by_video, "subscribersGained")[:10],
        "keyword_proxy": aggregate_keywords(by_video),
        "topic_agg": dict(sorted(topic_agg.items(), key=lambda item: item[1]["views"], reverse=True)),
        "diagnosis_buckets": diagnosis_buckets(by_video),
    }

    out = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "period": {"startDate": start.isoformat(), "endDate": end.isoformat(), "days": args.days},
        "channel": channel,
        "reports": reports,
        "retention_curves": retention,
        "derived": derived,
        "public_summary": public_summary,
        "caveats": [
            "Exact search terms are included only if the Analytics API returns rows; otherwise use Studio export.",
            "CTR/impressions require Studio export in this environment unless future API queries prove otherwise.",
            "averageViewPercentage above 100% usually indicates replays/short-form behavior.",
        ],
    }
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.discord:
        print(compact_report(out))
    else:
        print(f"WROTE {args.output}")
        print(compact_report(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
