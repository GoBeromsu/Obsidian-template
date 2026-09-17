---
created_by: agent
authorship: agent
---

<div align="center">
  <h1>Obsidian Template</h1>
  <p><strong>노트에는 제자리를. 생각에는 연결을.</strong></p>
  <p>PARA의 정리, 제텔카스텐의 연결, 일상과 장기 계획까지 — 사람과 AI 에이전트가 함께 쓰는 Obsidian 템플릿.</p>
  <p>
    <a href="README.md">English</a> ·
    <strong>한국어</strong>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Obsidian-7C3AED?style=flat&amp;logo=obsidian&amp;logoColor=white" alt="Obsidian" />
    <img src="https://img.shields.io/badge/Markdown-000000?style=flat&amp;logo=markdown&amp;logoColor=white" alt="Markdown" />
    <img src="https://img.shields.io/badge/EN%20%7C%20KO-bilingual-1F6FEB?style=flat" alt="Bilingual English and Korean" />
  </p>
  <p>
    <a href="90.%20Settings/01%20Guideline/01.%20Placement%20Guide.ko.md">배치</a>
    ·
    <a href="90.%20Settings/01%20Guideline/02.%20Writing%20and%20AI.ko.md">글쓰기와 AI</a>
    ·
    <a href="90.%20Settings/02%20Templates/README.ko.md">템플릿</a>
    ·
    <a href="90.%20Settings/01%20Guideline/03.%20Agent%20Skills.ko.md">에이전트 스킬</a>
    ·
    <a href="AGENTS.md">에이전트 가이드라인</a>
  </p>
</div>

## 정리에 쓰는 시간은 줄이고, 생각은 이어가세요

남의 개인 노트 대신, 바로 시작할 수 있는 구조를 가져오세요. ZIP을 받아 **새** 볼트로 폴더를 열고, 일반 마크다운부터 쓰면 됩니다. Git과 커뮤니티 플러그인은 필요할 때까지 선택 사항입니다. 노트마다 제자리를 정하고, 프로젝트를 넘어 아이디어를 연결하고, 연간 목표부터 오늘의 계획까지 이어갑니다. 사람과 에이전트가 같은 배치 규칙을 사용합니다.

- **노트당 하나의 위치.** 누가 썼는지, 어떤 도구가 수집했는지가 아니라 노트가 무엇인지로 둡니다.
- **PARA와 제텔카스텐.** 프로젝트·영역은 문헌 노트 및 상록 아이디어와 분리합니다.
- **회고 방식과 맞는 계획 사슬.** 폴더 번호는 이름표이고, 계층은 주기 사슬입니다.
- **처음부터 휴대 가능하게.** 개인 노트, 자격 증명, 플러그인 캐시, 플러그인 바이너리, 테마 바이너리, 기기별 상태는 포함하지 않습니다.

## 기능

| 기능 | 제공 |
| --- | --- |
| 번호 매긴 PARA 배치 | 루트 10개, 노트당 정식 경로 하나 |
| 제텔카스텐 구분 | 출처에서 나온 생각은 문헌 노트, 그 자체로 서는 아이디어는 영구 노트 |
| 주기 계획 | 연·분기·월·주·일·대시보드용 Templater `auto/` 노트 |
| 에이전트가 읽는 규칙 | 볼트 루트, Settings, Templates의 중첩 `AGENTS.md` |
| 임베디드 보기 | 주기 템플릿의 코어 Bases 표, 대시보드 Overdue는 Dataview 필요 |
| 에이전트 스킬 | 포함된 `obsidian` 스킬 하나; Claude Code, Codex, Antigravity에서 모두 동작 |
| 빈 자리 | 홈, 인덱스, 독립 Bases 폴더는 직접 채웁니다 |

## 수집에서 작업까지

이것은 배치 모델이며 자동 파이프라인이 아닙니다. 노트를 옮겨 주지 않습니다. 웹의 Gemini는 이 볼트에 자동으로 접근하지 않습니다.

**수집** (`00. Inbox`) → **원본** (`85. Raw`) · **해석** (`30. Literature Notes`) · **아이디어** (`40. Permanent Notes`) · **작업** (`15. Work`)

누가 수집했든 원본은 Raw에 둡니다. 소유자가 있을 때만 프로젝트 또는 영역 아래에 작업을 만듭니다. 첫 노트를 두기 전에 [배치 가이드](90.%20Settings/01%20Guideline/01.%20Placement%20Guide.ko.md)를 읽으십시오. 공개 AI 채팅으로 글을 쓸 때는 [글쓰기와 AI](90.%20Settings/01%20Guideline/02.%20Writing%20and%20AI.ko.md)를 보십시오.

## 루트

루트 10개를 제공합니다. 개인 볼트에만 있는 추가 루트는 이 템플릿의 일부가 아닙니다.

| 루트 | 역할 |
| --- | --- |
| `00. Inbox` | 미분류 캡처 |
| `10. Time` | 일간, 주간, 월간, 분기, 연간, 대시보드 |
| `15. Work` | 프로젝트, 영역, 아카이브, 할 일 |
| `30. Literature Notes` | 외부 자료에서 나온 연구, 리뷰, 회의 |
| `40. Permanent Notes` | 그 자체로 서는 아이디어와 원칙 |
| `50. AI` | 소유 프로젝트가 없는 AI 생성·합성 자료 |
| `70. Collections` | 사람, 프롬프트, MoC, 음악, 장소, 조직, GitHub, 채널 |
| `80. References` | 책, 논문, 첨부 파일 |
| `85. Raw` | 캡처한 외부 원본 |
| `90. Settings` | 규칙, 템플릿, 홈, 인덱스, Bases, Excalidraw |

`90. Settings/07 Excalidraw`는 그림과 에셋의 정규 폴더입니다.

## 시간

계획 계층은 **Year → Quarter → Month → Week → Day**입니다. 폴더 번호가 그 계층이 아닙니다.

일간 제목은 `YYYY-MM-DD`입니다. 주간 제목은 ISO 주 연도 `GGGG-WW` 뒤에 `W`를 붙인 형식입니다(예: `2026-37W`). 주기 위키링크는 탐색용입니다. 일간 노트를 만들면 어제·오늘·내일의 빠진 대시보드를 만들 수 있고, 주·월·분기·연 노트는 만들지 않습니다.

할 일 노트는 `manual/task.template.md`의 `type`, `done`, `gtd`, `project`, `plan`, `due` 필드(날짜 스탬프 포함)를 써서 대시보드 질의와 맞춥니다. 형식, ISO 주, 엔진 매핑, 그 필드: [배치 가이드](90.%20Settings/01%20Guideline/01.%20Placement%20Guide.ko.md) · [템플릿](90.%20Settings/02%20Templates/README.ko.md) **엔진 설정**.

## 시작하기

1. **ZIP 받기 (Git 불필요)**

   GitHub 저장소 페이지에서 **Code → Download ZIP**을 선택합니다. 압축을 풉니다. Obsidian에서 **Open folder as vault**를 고르고, `.obsidian`과 번호 매긴 루트가 들어 있는 압축 해제 폴더를 선택합니다.

   **새** 볼트로 여십시오. 이미 있는 볼트에 이 파일들을 합치지 마십시오.

   숨김 폴더 `.obsidian`은 그대로 두십시오. 숨김 파일을 표시해 확인하고, 누락되었다면 점(.)으로 시작하는 폴더를 보존하는 도구로 ZIP을 다시 푸십시오. 그 폴더는 휴대용 설정이며 플러그인 바이너리가 아닙니다.

2. **선택: Git으로 클론**

   ```sh
   git clone https://github.com/GoBeromsu/Obsidian-template.git
   ```

   클론한 폴더를 같은 방식으로 새 볼트로 엽니다. 디렉터리를 복사해도 같습니다.

3. **먼저 마크다운을 쓰고, 플러그인은 필요할 때 설치**

   일반 마크다운 수업은 커뮤니티 플러그인 없이 됩니다. 커뮤니티 플러그인은 필요할 때만 **설정 → 커뮤니티 플러그인**에서 설치합니다. `auto/` 폴더 템플릿을 적용하거나 `manual/` 템플릿을 삽입하려면 [Templater](https://github.com/SilentVoid13/Templater)가 필요합니다. 대시보드 Overdue 쿼리를 쓰려면 Dataview를 설치합니다. `community-plugins.json`의 ID는 설치를 대신하지 않습니다.

4. **엔진 설정 확인 (템플릿을 쓸 때)**

   코어 Daily notes는 켜져 있습니다. 일·주·월·분기·연용 Templater 폴더 템플릿은 `data.json`으로 포함되어 있으며, 플러그인 바이너리가 아닙니다. [템플릿](90.%20Settings/02%20Templates/README.ko.md) **엔진 설정**을 따르십시오. 코어 Bases는 이미 켜져 있습니다.

5. **수집한 뒤 배치**

   먼저 [배치 가이드](90.%20Settings/01%20Guideline/01.%20Placement%20Guide.ko.md)를 읽습니다. 미분류 캡처는 `00. Inbox`에 둡니다. 노트의 소유자가 있으면 `15. Work/01 Project` 또는 `15. Work/02 Area` 아래에 작업을 만듭니다. 시스템 파일은 `90. Settings`에 둡니다.

이 단계는 설정 안내입니다. 주기 노트 생성, Bases 보기, 테마 모양이 Obsidian에서 끝까지 검증되었다는 주장이 아닙니다.

## 첫 수업

볼트를 연 뒤의 짧은 경로입니다. 자세한 내용: [글쓰기와 AI](90.%20Settings/01%20Guideline/02.%20Writing%20and%20AI.ko.md).

1. 쓰기 전에 [초보 문법](90.%20Settings/01%20Guideline/02.%20Writing%20and%20AI.ko.md#초보-문법)에서 Markdown 기본 여섯 가지와 짧은 예시를 읽습니다.
2. 볼트 루트의 [`Me.md`](Me.md)를 편집합니다. 다섯 개의 `##` 섹션으로 된 한 장의 워크시트입니다: **Summary Statement**(나는 누구이고 지금 무엇을 하는지), **First Principles**(내가 판단 기준으로 삼는 가치나 원칙), **How I Think**(언제, 어떻게 사고 방법을 쓰는지 — 상향식, 하향식, 첫 원칙 사고는 선택적 예시이지 정해진 단계나 고정된 신념이 아닙니다), **Working Preferences**(AI 가 나와 협업할 때 원하는 방식), **나에게 영향을 주는 사람**(나에게 영향을 준 사람의 이름만 — 에세이나 기본으로 채워진 이름은 없습니다). 정식 `Me` 노트는 이것 하나입니다. 일반적인 사실만 적으십시오. 비밀, 자격 증명, 기기 경로는 넣지 마십시오.

   각 섹션은 **(작성 안내)**로 표시된 한국어 `> 역할:` 인용구로 시작합니다. 이 줄은 무엇을 적을지 알려주는 안내이며, 채워진 답이 아닙니다. 그 아래에 자신의 답을 자기 말로 적으십시오. 외부 출처를 인용할 때는 출처를 밝힌 `>` 인용을 쓰고, 인용을 지어내지 마십시오. 섹션을 채운 뒤에는 프런트매터의 `authorship`을 `mixed`로 바꾸십시오(`created_by: agent`는 유지).
3. 웹의 Gemini에는 **정제된 발췌만** 공유합니다. 텍스트는 직접 붙여 넣습니다. Gemini는 이 볼트에 자동으로 접근하지 않습니다.
4. Gemini에게 확인 질문을 **정확히 세 개** 하고 기다리도록 요청합니다. 직접 답한 뒤 초안을 요청합니다. 초안을 검토하고 **채택한 답만** `Me.md`의 해당 섹션에 직접 저장합니다.
5. `70. Collections/03 MoC`에 자신만의 Map of Content (MOC)를 만듭니다. `Me.md`에 방금 적은 내용과 관련된 기존 노트를 골라, 각 링크마다 짧은 이유를 답니다. 이는 사람이 직접 큐레이션한 목차이지, 자동 생성 색인이나 프로젝트 허브가 아닙니다.

채워 넣은 `Me.md`와 연결한 노트는 비공개로 취급하십시오. **Git이나 공유에서 자동 제외되지 않습니다.** 공개 저장소에 올리지 마십시오.

### 파일 세 개, 역할 세 개

[`Me.md`](Me.md)는 한 사람으로서의 정체성과 선호를 담습니다. [`AGENTS.md`](AGENTS.md)는 이 저장소의 규칙을 담습니다. [`CLAUDE.md`](CLAUDE.md)는 이 두 파일을 가리키는 단순한 포인터이며, 어느 쪽 내용도 중복하지 않습니다. 에이전트는 사용자 맥락을 위해 루트 `Me.md`를 먼저 읽고, 그다음 해당하는 `AGENTS.md` 계약을 읽습니다. `Me.md`를 읽는다고 해서 자동 통합이나 확장된 권한이 생기지 않습니다 — 각 섹션에는 이미 **(작성 안내)**로 표시된 `> 역할:` 안내 줄이 있으며, 그 아래의 빈 답변 칸은 채워지지 않은 알 수 없는 것이지 채택자에 대한 사실이 아닙니다.

## 에이전트 가이드라인

노트를 만들거나 옮기기 전에 가장 가까운 계약을 읽으십시오. 사람용 가이드는 영어/한국어 쌍이며, 어느 언어도 다른 언어보다 우선하지 않습니다.

| 계층 | 역할 |
| --- | --- |
| [볼트](AGENTS.md) | 루트 10개 지도와 볼트 전역 규칙 |
| [Settings](90.%20Settings/AGENTS.md) | 배치 SSOT, 빈 홈/인덱스/Bases, 설정 계층 규칙 |
| [Templates](90.%20Settings/02%20Templates/AGENTS.md) | `auto/`와 `manual/`, 제목 형식, 탐색과 생성 |

<details>
<summary>플러그인, 테마, 설정 한계</summary>

`.obsidian/community-plugins.json`은 플러그인 **ID** 목록입니다. 플러그인 ID와 포함된 `data.json`은 설정이지 설치가 아닙니다. 바이너리(`main.js`, `manifest.json`)는 `.obsidian/plugins/`에서 확인하십시오. 플러그인 디렉터리나 `data.json`만으로는 패키지가 설치된 것이 아닙니다.

`.obsidian/appearance.json`은 `cssTheme`을 `Minimal`로 두고, `.obsidian/snippets/` 아래 함께 제공되는 스니펫 두 개를 켭니다. `.obsidian/themes/` 디렉터리는 없습니다. 그 테마를 쓰려면 [Minimal](https://github.com/kepano/obsidian-minimal)을 직접 설치하거나 테마를 바꾸십시오. `obsidian-minimal-settings`도 ID만 있습니다.

`.obsidian/core-plugins.json`은 코어 Bases, 코어 Templates, **Daily notes**를 켭니다. `.obsidian/daily-notes.json`이 포함됩니다(폴더 `10. Time/01 Daily Notes`, 형식 `YYYY-MM-DD`, 템플릿은 비워 두어 Templater가 적용). 일·주·월·분기·연용 Templater 폴더 템플릿은 `.obsidian/plugins/templater-obsidian/data.json`에 있습니다. 그 파일은 플러그인 바이너리가 아닙니다. 코어 Templates는 `<% %>` 파일의 엔진이 아닙니다.

Excalidraw 그림은 `90. Settings/07 Excalidraw`에 둡니다. `.obsidian/plugins/obsidian-excalidraw-plugin/data.json`은 경로 설정이며 설치가 아닙니다. `periodic-notes` 플러그인은 ID 목록에 없고 사용하지 않습니다.

</details>

<details>
<summary>주기 링크는 연쇄 생성하지 않습니다</summary>

주기 템플릿의 위키링크는 탐색용입니다. 자동 주기 연쇄는 없습니다.

포함된 일간 템플릿은 어제·오늘·내일의 빠진 대시보드를 만들 수 있습니다. 주간, 월간, 분기, 연간 노트는 만들지 않습니다. 대시보드 질의용 할 일 필드(`type`, `done`, `gtd`, `project`, `plan`, `due`)는 `manual/task.template.md`에 있습니다. [템플릿](90.%20Settings/02%20Templates/README.ko.md) **엔진 설정**을 보십시오.

코어 Daily notes는 켜져 있으며 일간 파일만 만듭니다.

</details>
