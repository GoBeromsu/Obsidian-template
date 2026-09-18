# Transcript and qualitative analysis lessons

Use this when channel analysis needs to explain why a video performed the way it did.

## Why transcripts matter

Metrics show where attention changed; transcripts and notes explain why. For Beomsu's videos, inspect:

- first 15 seconds: promise, outcome, and visual proof
- first 30 seconds: whether context is too long
- topic shifts: whether chapters match viewer intent
- moments before average view duration: likely CTA/drop-off placement
- repeated fillers or unclear English phrasing in English videos
- screen-recording clarity: large text, narrated transitions, visible outcome

## Source order

Prefer sources in this order:

1. Existing Ataraxia upload note transcript and `## Feedback`.
2. Original local mp4 transcript from upload pipeline if available.
3. YouTube page transcript extraction for published videos.
4. External transcript skills/tools only when local/vault sources are missing.

## Lessons absorbed from shared transcript skills

From `baoyu-youtube-transcript` and Hermes' bundled YouTube transcript docs:

- Accept multiple input forms: full watch URL, youtu.be, embed, Shorts, or raw 11-character video ID.
- Prefer cached transcript artifacts when repeatedly analyzing the same video.
- Request language priority explicitly, usually `en,ko` for Beomsu's channel.
- Include timestamps for diagnosis; plain text is less useful for retention analysis.
- Chapter segmentation is useful even when the original description has no chapters; infer topic shifts.
- If direct transcript extraction fails, retry with another method before giving up: InnerTube/youtube-transcript-api, then `yt-dlp`, optionally browser cookies if needed.
- Distinguish no captions, private/deleted/unavailable, requested language missing, and bot/IP block. Each implies a different next step.

## Analysis rubric

When reviewing an underperforming video:

1. Locate the average view duration and first retention cliff if available.
2. Read transcript around the opening and around the drop-off point.
3. Check whether the title promise appears on-screen quickly.
4. Identify dead air, setup friction, or terminology overload.
5. Produce 2-4 edit/format changes and one title/thumbnail hypothesis.

## English-delivery feedback

For English videos, reuse the `youtube-upload` feedback structure if detailed language coaching is requested:

- CEFR estimate
- good patterns
- awkward-but-not-wrong paraphrase candidates
- objectively wrong expression corrections

Do not mix English coaching into every channel strategy report; include it only when it explains retention or when the user asks for delivery feedback.
