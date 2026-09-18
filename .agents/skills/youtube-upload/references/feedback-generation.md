# Feedback generation

Own the Feedback-section trigger, language branch, required fields, templates, and output file.

### 5.5. Generate Feedback section

From the transcript, generate the `## Feedback` content yourself (do NOT call a
separate script — same pattern as Step 2 metadata generation). Use
`assets/note-template.md` as the structural template and
`references/youtube-best-practices.md` as the rubric.

**Language branch**: If the transcript language is NOT `en`, set the entire
`### English (CEFR Assessment)` body to a single italic placeholder
(`*N/A — non-English video*`) — the paraphrase/correction guidance only makes
sense for English-spoken videos. Still fill in `### YouTube (Content Assessment)`
and `### Action Items` normally.

For English videos, the section MUST contain (in this exact order):

- `### English (CEFR Assessment)` with:
  - `**Level**: A1-C2` estimate
  - `**Youglish 추천**: 3-5 words`
  - `#### 잘한 점` — 2-5 nested bullets, each with a sub-bullet citing a
    transcript moment when useful
  - `#### 아쉬운 점` — 2-5 nested bullets, high-level patterns only (specific
    fixes go under 영어 표현 교정)
  - `#### Paraphrase 추천` — target 3-7 entries. Each entry MUST follow this
    nested-bullet shape exactly:
    ```
    - 원문: "<verbatim phrase from transcript>"
      - 대안1: "<more natural rewrite>"
      - 대안2: "<alternative tone/register>"   # optional but encouraged
      - 왜: <1-line rationale>
    ```
    Pick phrases that are NOT grammatically wrong but feel awkward, repetitive,
    or low-register for YouTube delivery.
  - `#### 영어 표현 교정` — target 3-7 entries. Each entry MUST follow this
    nested-bullet shape exactly:
    ```
    - "<wrong phrase>" → "<corrected phrase>"
      - 이유: <grammar rule or usage convention>
    ```
    Pick phrases that are objectively wrong (grammar, article, tense, collocation).
- `### YouTube (Content Assessment)` — keep the existing template structure
  unchanged (잘한 점 / 아쉬운 점, flat bullets).
- `### Action Items` — 2-5 task checkboxes synthesizing the most actionable
  items from both English and YouTube sections.

**Two placeholders, two distinct cases** — do not mix:
- Whole-subsection skip (non-English video): set the entire `### English`
  body to `*N/A — non-English video*` (handled by the language branch above).
- Individual zero-candidate H4 (e.g., no Paraphrase candidates found in an
  English video): emit a single italic bullet inside that H4:
  `- *없음 — 검토할 만한 항목이 발견되지 않았습니다*`

For videos longer than 1 hour, warn the user that Feedback generation adds an
extra 1-2 minutes on top of the transcription wait.

Save the rendered Feedback markdown (everything from `### English` through the
end of `### Action Items`) to `/tmp/yt_upload_feedback.md` for use in Step 6.
