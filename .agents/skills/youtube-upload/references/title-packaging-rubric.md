# Title Packaging Rubric

Use this reference when generating or reviewing titles and thumbnail hook text for
YouTube videos. Apply all rules to both the primary language title and the localized
(Korean or English) title.

## Pass / Fail Rules

A title passes if ALL eight rules are satisfied.

**Rule 1 — Delivery test**: Every specific outcome promised in the title is
demonstrably delivered in the video. If the title says "in 5 minutes," the core
technique is fully demonstrable in ≤5 minutes.

**Rule 2 — Specificity test**: A viewer predicts ≥70% of the video's content
from the title alone. Generic hooks fail; specific, named-tool hooks pass.
Example: "Obsidian Kanban Plugin Changed How I Track Projects" passes;
a vague all-caps opener claiming one unnamed thing "changes everything" fails.

**Rule 3 — No manufactured urgency**: Remove phrases such as "BEFORE IT'S TOO
LATE," "RIGHT NOW," "HURRY," or "IMMEDIATELY" unless an actual time-bounded
reason exists in the video.

**Rule 4 — No impossible-outcome framing**: Remove metaphorical hyperbole
(e.g., implying passive sleep-time coding) unless the video is literally about
that outcome. A CI/CD automation video may use "Your Tests Run While You Sleep"
because that is accurate.

**Rule 5 — Casing sanity check**: No all-caps words other than acronyms (API,
CLI, AI) or proper tool names. Capitalize at most one word for emphasis.

**Rule 6 — Power word ceiling**: Maximum 2 power words per title. Count from
this list: Ultimate, Secret, Hack, Instantly, Game-Changer, Proven, Finally,
Never, Always, Must, Best, Only, Worst, Shocking, Unbelievable, Crazy, Insane.

**Rule 7 — Length check**: Title is ≤90 characters. The first 50 characters
carry the complete hook; the remaining characters add a niche qualifier, year,
or tool name for search.

**Rule 8 — Bilingual package complement check**: Review the English title,
Korean title, and rendered thumbnail together. Both titles must accurately
promise the same underlying video in natural language. Thumbnail hook text must
add a verified when/how/scale dimension rather than repeat or translate either
title. If the title names a setup, the thumbnail can add its verified time or
number of steps.

The package does not pass from text alone: inspect the rendered thumbnail for
legibility, clipping, contrast, and Hangul tofu. Record which final image was
reviewed.

## Rewrite Patterns: Sensational → Honest-Compelling

Each pattern below shows the bad-pattern type, a representative "After" rewrite,
and why the rewrite passes the rubric.

**EN — Vague all-caps superlative** (fails Rules 1, 2, 5)
- Pattern: all-caps opener claiming one unnamed thing transforms the viewer's workflow
- After: `The Obsidian Plugin That Replaced My Whole Note System`
- Why: names a verifiable claim and includes the tool for search; viewer predicts content.

**EN — Impossible-outcome framing** (fails Rules 1, 4)
- Pattern: implies passive automation during sleep as the hook when the video is a workflow tutorial
- After: `I Let Claude AI Write My Boilerplate for 30 Days — Here's What Happened`
- Why: the 30-day experiment frame is honest and creates a genuine curiosity gap.

**EN — Unanchored speed multiplier** (fails Rules 1, 2, 5)
- Pattern: all-caps N-times-faster claim with no baseline or named tool
- After: `Cursor AI Cut My Debugging Time in Half — Here's the Setup`
- Why: "Half" is specific and achievable; tool name and "Setup" anchor the promise.

**EN — Broad tutorial with all-caps superlative** (fails Rules 2, 5, 6)
- Pattern: "THE ULTIMATE [X] (You Won't Believe This)"
- After: `My Obsidian Dev Setup: 7 Plugins I Use Every Single Day`
- Why: a specific number and authentic daily use signal genuine expertise.

**KO — Manufactured urgency** (fails Rule 3)
- Pattern: `이걸 모르면 개발자 인생 끝납니다 | AI 도구 충격 공개`
- After: `개발자가 매일 쓰는 AI 도구 5개 — 실제 사용 후기`
- Why: "인생 끝납니다" (your developer life is over) is manufactured urgency. The
  rewrite uses a specific count (5개) and signals personal experience (사용 후기).

**KO — Vague curiosity trap** (fails Rule 2)
- Pattern: `이것만 알면 됩니다 | 절대 알려주지 않는 Obsidian 비법`
- After: `Obsidian Dataview로 TODO 자동 정리하는 법 (5분 설정)`
- Why: "절대 알려주지 않는 비법" (secrets they never share) is a Clicktrap pattern.
  The rewrite names the tool, outcome, and a verifiable time-compression promise.

## Thumbnail Hook Text Rules

1. **Maximum 4 words** (3 preferred; 5 as absolute ceiling).
2. **Complement the title**: title carries the searchable what; thumbnail text
   adds the when, how, or scale — not a repeat of the title.
3. **No shock-bait phrases**: banned terms include SHOCKING, INSANE, CRAZY,
   UNBELIEVABLE, GAME CHANGER, MIND BLOWN, YOU WON'T BELIEVE.
4. **Bold Title Case or ALL CAPS acceptable** for thumbnail text only — short
   bursts of 2–4 words at thumbnail scale are standard practice.
5. **Specific over vague**: "In 15 Min" beats "FAST"; "7 Plugins" beats
   "BEST SETUP"; "Free" beats "AMAZING."

## Synthetic bilingual before/after package

The following is **illustrative only, not evidence of a real execution or
review**.

**Before (fails Rules 1, 2, 3, 5, and 8)**

- EN title: `THIS AI CHANGES EVERYTHING — WATCH NOW`
- KO title: `이 AI 모르면 끝납니다 — 지금 보세요`
- Thumbnail: `AI CHANGES EVERYTHING`
- Failure: neither title identifies the delivered workflow; the Korean title
  adds unsupported urgency; the thumbnail simply repeats the vague English
  claim.

**After (passes only if the synthetic video really demonstrates the claim)**

- EN title: `Build an Obsidian Weekly Review with GJC`
- KO title: `GJC로 Obsidian 주간 리뷰 만드는 법`
- Thumbnail: `15분 설정`
- Evidence expected: the final video shows the named workflow in both language
  packages and completes setup within 15 minutes; the rendered thumbnail is
  legible. The titles carry the searchable what, while the thumbnail adds a
  verified time dimension.

Compliant examples for dev/tech content:

| Hook text | Why it works |
|-----------|-------------|
| `In 15 Min` | Specific time-compression promise |
| `Step by Step` | Format signal; sets accurate expectation |
| `2x Faster` | Quantified outcome — only use if accurate |
| `Worth It?` | Honest question the video genuinely answers |
| `Free Tool` | Literal attribute |
| `My Setup` | Personal authenticity signal |
| `7 Plugins` | Specific number |
| `15분 완성` (KO) | "15 minutes to complete" — time-compression |
| `무료 도구` (KO) | "Free tool" — literal attribute |
| `실제 사용` (KO) | "Actually using it" — authenticity signal |

## Title Length Guidance

| Discovery pathway | Recommended chars | Rationale |
|------------------|-------------------|-----------|
| Search-led (primary for <1K subs) | 40–55 | Keyword front-loaded; top-ranked videos average 47–48 chars |
| Browse / suggested feed | 55–70 | Thumbnail carries visual load; title adds context |
| Hard cap | 90 | Existing repo limit; covers mobile truncation |

Front-load the primary keyword in the first 0–5 words for search-led discoverability.

## Bilingual Note

Apply all eight rules to both the primary language title and the localized title.
Do not grade them independently and then assume the package works: compare their
promises with each other, the transcript/final master, and the rendered thumbnail.
Korean title conventions:
- Front-load the 핵심 키워드 (keyword)
- Use a specific number where possible (same +20–30% CTR effect as English)
- Pipe separator `|` is standard: "Obsidian 완전 정복 | 개발자를 위한 노트 시스템"
- Plain form (기본형 / 명사형) — no honorifics in titles
- Age-segmented tone: 30+ dev audience responds well to trust-based language with
  concrete expectations ("개발자를 위한 Obsidian 완전 가이드: 실제 사용 중인 플러그인 7개")

## Diagnostic Table: Common Failure Patterns

| Title pattern type | Fails rule(s) | Fix direction |
|--------------------|--------------|---------------|
| Vague all-caps superlative (unnamed thing "changes everything") | 1, 2, 5 | Name the specific thing that changes; drop all-caps |
| Unanchored Nx-speed claim with no baseline | 1, 2, 5 | Replace with specific multiplier + comparison context |
| Passive sleep-time automation hook (impossible framing) | 1, 4 | Rephrase to describe the actual automation that happens |
| Korean manufactured urgency ("인생 끝납니다"-style) | 3 | Replace urgency with specific outcome + social proof |
| Korean vague curiosity trap ("이것만 알면 됩니다"-style) | 2 | Name the tool, outcome, and time investment |

## Sources

- Research report: `.omc/research/youtube-title-best-practices-2026-06.md` — 2026-06-11
- [LaunchLens — "YouTube Algorithm Secrets 2025"](https://launchlens.tech/blog/youtube-algorithm-secrets-2025) — satisfaction-weighted discovery, clickbait decay, delivery mismatch detection
- [Colin & Samir — "The New Rules of YouTube from Paddy Galloway"](https://www.colinandsamir.com/resources/the-new-rules-of-youtube-from-paddy-galloway) — 70% compelling rule, curiosity gap reframing
- [Briggsby / Justin Briggs — "Reverse-Engineering YouTube Search"](https://www.briggsby.com/reverse-engineering-youtube-search) — title length and ranking data; keyword placement
- [humbleandbrag.com — "YouTube Title Best Practices"](https://humbleandbrag.com/blog/youtube-title-best-practices) — ALL CAPS guidance, power word ceiling, number CTR data
- [FluxNote — "YouTube Title Formulas 2026"](https://fluxnote.io/guides/how-to-write-viral-youtube-titles-2026) — specific vs generic outcome CTR comparison
- [SNS핫딜 — "2025 유튜브 제목으로 조회수 올리는 공식"](https://xn--sns-h84mk60k.com/blog/youtube-ab-test-guide) — Korean CTR formula, sensationalism warning
- [YouTube Help — "Thumbnail & title tips"](https://support.google.com/youtube/answer/12340300) — official ALL CAPS guidance and accuracy policy
- [ContentGuaranteed — "Using Text in Thumbnails Effectively"](https://www.contentguaranteed.com/?p=1322) — role of thumbnail text vs title
- [YouTube Blog KO — "2025년 한국 유튜브 트렌드"](https://blog.youtube/intl/ko-kr/culture-and-trends/year-on-youtube-2025-korea/) — authenticity over sensationalism in KO YouTube 2025
