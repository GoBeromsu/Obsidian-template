# Upload Validation Policy

This policy defines what must NOT appear in publicly uploaded YouTube content.
It is consumed by `scripts/validate.py` and applied to the transcript + generated
metadata (title/description/tags) before upload.

The validator is a **safety net**, not a guarantee. It flags likely violations
based on this ruleset; the creator is still responsible for final review.

Each rule has a `severity`:
- **high** — block the operation
- **medium** — contributes to the blocking threshold
- **low** — surface as advisory only

The validator runs through an authenticated non-Anthropic GJC CLI route and
returns a JSON report with `passed: bool`, input-binding and runtime evidence,
and `violations: [{rule, severity, quote, category, suggestion}]`. No Anthropic
key is required or supported.

The operation is blocked when ANY `severity: high` violation is found, OR when
2+ `severity: medium` violations are found. No upload or metadata/localization
mutation occurs at any privacy level. Private is merely the uploader's default
after a successful review, never a violation fallback.

---

## Category 1: 사람 (People)

**Rule 1.1 — Identifiable colleague/director/student mentions** (`severity: high`)

Do not mention specific co-workers, directors, managers, or students in a way
that could be linked back to them. This includes referring to them by role at a
named company ("내 디렉터", "팀의 ML 리드"), by personal traits, or in
combination with other context that narrows identification.

- **Negative example**: "when my director said we should ship Solar Pro 3 by..."
- **Negative example**: "내 디렉터가 그러는데..."
- **Negative example**: "함께 일하는 ML 엔지니어가 어제 평가에서..."
- **Positive example**: "함께 일하는 분이 좋은 피드백을 줬다"
- **Positive example**: "동료들과 논의한 결과..."
- **Positive example (public-facing role)**: "Upstage CEO 김성훈 대표님이 공개 발표에서..."

**Rule 1.2 — Student/cohort identifying details** (`severity: high`)

Do not disclose specific numbers of students, cohort sizes, scholarship counts,
or anything that could de-anonymize a specific class or program participant.

- **Negative example**: "30명 학생을 가르치는데..."
- **Negative example**: "JNU x Upstage 스킬톤에서 학생 7명이..."
- **Positive example**: "최근 강의를 진행하면서..."
- **Positive example**: "공개된 스킬톤 행사에 참여했다"

---

## Category 2: 회사 제품 (Company Products)

**Rule 2.1 — Evaluative statements about Solar / Upstage products** (`severity: high`)

Do not make evaluative, comparative, or quality-judgment statements about Solar,
Upstage products, or internal model performance. Technical facts (architecture,
API usage, what you built) are OK; subjective judgments ("better than", "worse
than", "quality is bad") are not.

- **Negative example**: "Solar API quality is not great"
- **Negative example**: "Solar Pro 3는 OpenAI보다 못하다"
- **Negative example**: "Solar embedding이 별로다"
- **Positive example**: "Solar embedding을 Hermes Agent에 사용했다"
- **Positive example**: "Solar Pro 3로 이런 워크플로우를 구현했다"
- **Positive example (objective fact)**: "Solar는 한국어 컨텍스트에 최적화되어 있다"

**Rule 2.2 — Unreleased product roadmap leaks** (`severity: high`)

Do not mention unreleased features, upcoming model versions, internal roadmap,
or pre-announcement product details.

- **Negative example**: "Solar Pro 4 곧 나올 건데..."
- **Negative example**: "내년에 우리가 출시할 모델은..."
- **Positive example**: "이미 공개된 Solar Pro 2 모델은..."

---

## Category 3: 운영 디테일 (Operational Details)

**Rule 3.1 — Internal budget / credit / compensation numbers** (`severity: high`)

Do not disclose specific dollar amounts, credit grants, freelance rates,
budgets, or compensation details tied to internal operations.

- **Negative example**: "$70 크레딧을 받았다"
- **Negative example**: "이 프로젝트 예산이 500만원이라..."
- **Positive example**: "충분한 API 크레딧이 있다"
- **Positive example**: "예산을 효율적으로 사용하고 있다"

**Rule 3.2 — Internal schedules / deadlines / working hours** (`severity: medium`)

Do not disclose specific internal deadlines, work hours, or schedule details
that imply how a private team operates.

- **Negative example**: "9시 30분까지 이 PR 끝내야 해서..."
- **Negative example**: "마감이 다음 주 월요일이라 야근 중"
- **Positive example**: "최근 집중해서 작업 중"
- **Positive example**: "공개 데모 일정에 맞춰 준비 중"

**Rule 3.3 — Confidential customer / partner names** (`severity: high`)

Do not mention specific customer names, partner contract details, or B2B deal
specifics unless they are already publicly announced.

- **Negative example**: "X 회사가 우리 API를 쓰는데 만족도가 별로..."
- **Positive example**: "공식 파트너십이 발표된 Y 회사와..."

---

## Self-criticism / professional tone (Category 4 — `severity: medium`)

Avoid extended self-deprecation, profanity, or non-professional rants that
could affect long-term channel perception. Casual energy is fine; sustained
negative self-talk or off-brand outbursts are flagged.

- **Negative example**: "I'm so stupid for not figuring this out earlier..."
- **Negative example**: 욕설 (fuck, shit, 등) reaching 3+ instances
- **Positive example**: "처음엔 헤맸지만 결국 이렇게 풀었다"

---

## ASR caveat

The transcript is produced by automatic speech recognition (mlx-audio /
Qwen3-ASR). It may contain phonetically-similar misspellings (e.g., "Obstage"
for "Upstage", "LMS" for "Hermes"). When evaluating rules, consider phonetic
neighbors and the surrounding context — do NOT rely on exact string match.

## Output shape

The validator returns a single JSON object on stdout:

```json
{
  "passed": false,
  "violations": [
    {
      "rule": "1.1",
      "category": "사람",
      "severity": "high",
      "quote": "when my director said we should...",
      "suggestion": "Generalize to '함께 일하는 분' or remove the attribution"
    }
  ],
  "checked_text_length": 3421,
  "input_digest": "sha256:<digest-of-complete-bound-input>",
  "review": {
    "backend": "gjc",
    "provider": "openai-codex",
    "model": "gpt-5.6-sol",
    "response_id": "<non-empty-runtime-response-id>",
    "stop_reason": "stop"
  }
}
```

`passed` is `true` if and only if there are zero `severity: high` violations
AND fewer than 2 `severity: medium` violations.

The SHA-256 digest binds the complete transcript, canonical metadata, and exact
policy. The `review` object identifies the actual completed GJC response and
must match the requested provider/model. Missing, malformed, truncated,
digest-mismatched, or provider-mismatched evidence fails closed. The examples
above are synthetic schema illustrations, not real execution receipts.

Exit `0` means the bound review completed and passed. Exit `2` means the bound
review completed but crossed the violation threshold and stops before mutation.
Exit `1` means input, backend, runtime, or evidence failure and also stops before
mutation. Never reinterpret either nonzero exit as permission to upload
privately.

## Validator report shape

The script writes a JSON report to stdout:

```json
{
  "passed": false,
  "violations": [
    {"rule": "1.1", "category": "사람", "severity": "high",
     "quote": "...", "suggestion": "..."}
  ],
  "checked_text_length": 3421,
  "input_digest": "sha256:<digest-of-complete-bound-input>",
  "review": {
    "backend": "gjc",
    "provider": "openai-codex",
    "model": "gpt-5.6-sol",
    "response_id": "<non-empty-runtime-response-id>",
    "stop_reason": "stop"
  }
}
```

The digest binds the complete transcript, canonical metadata, and exact policy;
the response identity proves which completed GJC response supplied the verdict.
Missing, malformed, truncated, digest-mismatched, or provider-mismatched evidence
fails closed. The validator never includes private source text or raw backend
output in an error report.
