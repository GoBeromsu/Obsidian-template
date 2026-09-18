---
created_by: agent
authorship: agent
---
# 템플릿

[English](README.md) · [한국어](README.ko.md)

관련: [Start (English)](../../README.md) · [시작 (한국어)](../../README.ko.md) · [Placement Guide](../01%20Guideline/01.%20Placement%20Guide.md) · [배치 가이드](../01%20Guideline/01.%20Placement%20Guide.ko.md) · [Agent contract](AGENTS.md)

이들은 [Templater](https://github.com/SilentVoid13/Templater) 템플릿입니다. `periodic-notes` 플러그인은 이 템플릿의 플러그인 ID 목록에 없고 사용하지 않습니다.

`community-plugins.json`에 `templater-obsidian`(또는 Dataview, Excalidraw, Minimal Theme Settings)이 적혀 있어도 그 플러그인을 **설치하지 않습니다**. 이 볼트는 `.obsidian/plugins/templater-obsidian/data.json`과 `.obsidian/plugins/obsidian-excalidraw-plugin/data.json`에 허용 목록 플러그인 **설정**을 포함합니다. 그 파일은 경로·폴더 템플릿 설정이며 플러그인 바이너리가 아닙니다. `.obsidian/themes/`는 포함되지 않습니다. `<% %>` 템플릿이 실행되려면 먼저 Templater를 설치하고 켜십시오.

## `auto/`와 `manual/`

| 폴더 | 역할 |
| --- | --- |
| `auto/` | 주기 템플릿. Templater **Folder templates**(Dashboard 제외, 미리 로드됨)가 매핑된 폴더에 파일이 생길 때 이 파일을 적용합니다. |
| `manual/` | 필요할 때 쓰는 템플릿. Templater 삽입 모달에서 호출합니다. |

`auto/`는 폴더 이름이지 자동 실행기가 아닙니다. Templater가 설치·활성화되어 있지 않으면 이 템플릿 안의 어떤 것도 이 파일들을 실행하지 않습니다. 핵심 Daily notes는 `.obsidian/core-plugins.json`에서 **켜져 있고** `.obsidian/daily-notes.json`이 있습니다. Templater 폴더 규칙은 `.obsidian/plugins/templater-obsidian/data.json`에 있습니다. Templater를 설치하고 켜기 전에는 `10. Time/` 아래에 파일을 만들어도 이 템플릿이 적용되지 않습니다.

포함된 템플릿 파일은 모두 `*.template.md` 접미사를 씁니다.

- `auto/Daily Note.template.md`
- `auto/Weekly Notes.template.md`
- `auto/Monthly Notes.template.md`
- `auto/Quarterly Notes.template.md`
- `auto/Yearly Note.template.md`
- `auto/Dashboard.template.md`
- `manual/note.template.md`
- `manual/task.template.md`
- `manual/project.template.md`
- `manual/log.template.md`
- `manual/video.template.md`
- `manual/book.template.md`

## 엔진 설정 (Daily notes와 Templater 폴더 규칙은 미리 로드됨)

핵심 Daily notes 설정과 최소 Templater 폴더 템플릿 목록은 이미 포함된 JSON에 있습니다. 그것은 설정이지 라이브 플러그인 설치가 아니며, 검증된 Obsidian 실행이라는 주장도 아닙니다. 핵심 Templates는 `core-plugins.json`에서 켜져 있지만 `templates.json`은 없고, Templater와 혼동하지 마십시오.

### Templater (설치는 여전히 필요)

1. Templater를 설치하고 켭니다. 플러그인 바이너리가 없으면 `data.json`은 아무 것도 하지 않습니다.
2. **Template folder location**은 `90. Settings/02 Templates`로 미리 로드되어 있습니다(볼트 상대 경로). 삽입 모달이 보는 폴더이며, `auto/`와 `manual/`이 그 아래에 있습니다.
3. **새 파일 생성 시 실행**은 폴더 모드로 미리 로드되어 있습니다(`trigger_on_file_creation_mode: folder`). 아래 목록의 폴더에서만 Templater가 실행됩니다.
4. **Folder templates**는 다음 행만 미리 로드되어 있습니다.

| 폴더 | 템플릿 |
| --- | --- |
| `10. Time/01 Daily Notes` | `90. Settings/02 Templates/auto/Daily Note.template.md` |
| `10. Time/02 Weekly Notes` | `90. Settings/02 Templates/auto/Weekly Notes.template.md` |
| `10. Time/03 Monthly Notes` | `90. Settings/02 Templates/auto/Monthly Notes.template.md` |
| `10. Time/05 Quarterly Notes` | `90. Settings/02 Templates/auto/Quarterly Notes.template.md` |
| `10. Time/04 Yearly Notes` | `90. Settings/02 Templates/auto/Yearly Note.template.md` |

`10. Time/06 Dashboard`에는 폴더 템플릿을 **추가하지 마십시오**. Daily 훅이 `tp.file.create_new`와 `auto/Dashboard.template.md`로 대시보드를 한 번만 만듭니다. 그 폴더를 매핑하면 Dashboard 템플릿이 두 번 적용됩니다.

같은 파일에 폴더 템플릿과 다른 적용 수단이 함께 걸리면 Templater가 두 번 실행될 수 있습니다. 폴더마다 적용 수단을 하나만 고르십시오.

### 핵심 Daily notes (미리 로드됨)

핵심 **Daily notes**는 켜져 있습니다. `.obsidian/daily-notes.json`은 다음과 같습니다.

- New file location: `10. Time/01 Daily Notes`
- Date format: `YYYY-MM-DD` (Daily 템플릿이 그 제목을 파싱합니다)
- Template file: 비움 (핵심 템플릿 없음). Templater의 Daily 폴더 템플릿이 `auto/Daily Note.template.md`를 적용합니다. Daily notes 템플릿 칸을 채우지 마십시오. 두 엔진이 함께 돌 수 있습니다.

핵심 Daily notes는 일일 파일만 만듭니다. 주·월·분기·연·대시보드 노트는 만들지 않습니다. Daily 템플릿 훅이 일일 노트가 쓰인 뒤 없는 대시보드를 만듭니다.

## 명령과 실습 예

일반 예제 날짜: **2026-01-15** (어제 `2026-01-14`, 내일 `2026-01-16`, ISO 주 `2026-03W`, 월 `2026-01`). 이 날짜는 문서용 예시일 뿐이며, Obsidian UI에서 끝까지 실행했다는 주장이 아닙니다.

1. **날짜가 있는 Daily 노트 만들기.** 볼트 날짜가 그날이면 명령 팔레트 → **Daily notes: Open today's daily note**. 시계와 관계없이 예제 날짜를 쓰려면 `10. Time/01 Daily Notes/2026-01-15.md`를 그 폴더에 만들어 Daily 폴더 템플릿이 돌게 합니다.
2. **연결된 대시보드.** Daily 템플릿이 끝난 뒤 없는 파일을 만들려고 합니다.
   - `10. Time/06 Dashboard/2026-01-14 Dashboard.md`
   - `10. Time/06 Dashboard/2026-01-15 Dashboard.md`
   - `10. Time/06 Dashboard/2026-01-16 Dashboard.md`
   `tp.file.create_new`로 `auto/Dashboard.template.md`를 사용합니다. `2026-03W`, `2026-01`, `2026-Q1`, `2026`은 **만들지 않습니다**.
3. **할 일 시연.** `15. Work/04 Tasks/2026-01-15 Example task.md`를 만듭니다. 명령 팔레트 → **Templater: Insert Template** → `manual/task.template.md`. Dashboard **Today**와 **Due soon**에 걸리도록 `plan: 2026-01-15` 그리고/또는 `due: 2026-01-15`를 넣고, **Delegation**에는 `gtd: delegation`을 넣습니다. `done: false`로 둡니다.
4. **그날 대시보드 열기.** `10. Time/06 Dashboard/2026-01-15 Dashboard.md`를 엽니다. 핵심 Bases **Tasks** 뷰가 `type == "task"`와 그 필드로 거릅니다. 그 대시보드는 폴더 매핑되지 않으므로 Daily 훅이 Templater를 한 번만 적용합니다.
5. **Sample Project 허브.** 수동 템플릿은 파일을 만들지 않고 자동으로 실행되지 않습니다. 폴더 `15. Work/01 Project/Sample Project`를 만든 뒤, 빈 노트 이름을 `Sample Project`로 하여 `15. Work/01 Project/Sample Project/Sample Project.md`를 만듭니다. 명령 팔레트 → **Templater: Insert Template** → `manual/project.template.md`. 정규 [`../../Me.md`](../../Me.md)를 검토한 뒤 Context에 그 노트 위키링크를 붙이십시오 (미해결 자리표시를 남기지 마십시오). Objective, Success criteria, Constraints, Next action을 채웁니다. `15. Work/01 Project`에는 폴더 템플릿이 없습니다.
6. **날짜가 있는 프로젝트 로그.** 빈 노트 이름을 `2026-01-15 Sample Project log`로 하여 `15. Work/01 Project/Sample Project/2026-01-15 Sample Project log.md`를 만듭니다. 명령 팔레트 → **Templater: Insert Template** → `manual/log.template.md`. `project: ["[[Sample Project]]"]`로 둡니다 (목록 안의 인용된 허브 위키링크). Observations, Decision, Next action을 채웁니다. `## Thinking`은 비워 두십시오. 사람 전용입니다.
7. **프로젝트 소유 할 일 연결.** 허브 옆에 별도 할 일을 만들고 `manual/task.template.md`를 삽입한 뒤 `project: ["[[Sample Project]]"]`로 두어 Dashboard Tasks가 소유 프로젝트를 보이게 합니다. 3단계의 소유 프로젝트 없는 할 일은 `04 Tasks`에 둡니다. 허브의 Linked logs 섹션에 로그의 위키링크를 추가합니다. 위키링크는 허브나 로그를 만들지 않습니다.

일일 노트의 체크박스는 일일 노트에 남깁니다. Dashboard **Overdue**는 `10. Time/01 Daily Notes`에 대한 Dataview `TASK` 질의이며 Dataview 설치가 필요합니다.

**Templater 없이 일반 마크다운.** Templater가 없으면 `<% %>`는 실행되지 않습니다. 렌더되지 않은 `<% %>`를 노트에 복사해 유효한 마크다운처럼 쓰지 마십시오. 같은 YAML 키를 손으로 쓰십시오: `type: project` 또는 `type: log`, `created_by: user`, `authorship: user`, 인용 없는 ISO `date_created` / `date_modified` (예: `2026-01-15`), 로그는 인용된 허브 위키링크를 넣을 때까지 `project: []`. 본문에서는 Templater 식이 아니라 템플릿의 절 제목을 복사하십시오.

## 탐색과 생성

프론트매터와 본문의 위키링크(`week`, `month`, `year`, `quarter`, 이전/다음 주기, 대시보드 `up` 등)는 **탐색**입니다. 대상 노트를 만들지 않습니다.

계획 계층은 연 → 분기 → 월 → 주 → 일입니다. 주기 노트는 그 사슬을 명시적 위키링크로 가리킵니다. 자동 주기 연쇄 생성은 없습니다.

방금 연 노트 외에, 포함된 생성기는 Daily 템플릿뿐입니다. 일일 노트가 쓰인 뒤 어제·오늘·내일 대시보드만 만들려고 합니다.

## 제목 형식

제목 형식은 스크립트가 `tp.file.title`에서 파싱하는 값입니다. 제목 없는 채 만든 뒤 이름 바꾸는 경쟁 상태에서는 "지금"으로 떨어집니다.

| 주기 | 폴더 | 제목 형식 | 예 |
| --- | --- | --- | --- |
| 일 | `10. Time/01 Daily Notes` | `YYYY-MM-DD` | `2026-01-15` |
| 주 | `10. Time/02 Weekly Notes` | ISO 주년 `GGGG-WW` 뒤에 `W` | `2026-03W` |
| 월 | `10. Time/03 Monthly Notes` | `YYYY-MM` | `2026-01` |
| 분기 | `10. Time/05 Quarterly Notes` | `YYYY-Qn` | `2026-Q1` |
| 연 | `10. Time/04 Yearly Notes` | `YYYY` | `2026` |
| 대시보드 | `10. Time/06 Dashboard` | `YYYY-MM-DD Dashboard` | `2026-01-15 Dashboard` |

주는 ISO 주(월요일–일요일)이며 Daily의 `week` 값(`GGGG-WW` 뒤에 `W`)과 같습니다. 일요일 시작 주를 쓰지 말고, 일요일을 다음 주에 넣지 마십시오. 일일 노트는 `week`를 그 제목으로 쓰므로, 주간 노트를 만들 때 같은 제목을 쓰십시오.

## YAML 규칙

각 템플릿이 이미 넣는 필드를 재사용하십시오. 개인 메타데이터 스키마를 덮어씌우지 마십시오.

- 키는 `snake_case`입니다 (`created_by`, `date_created`, `date_modified`).
- 위키링크 값은 인용된 YAML 문자열입니다. 예: `week: "[[2026-03W]]"`, `up: "[[2026-01-15 Dashboard]]"`.
- 일반 ISO 날짜는 인용하지 않습니다. 예: `date_created: 2026-01-15`.
- 사람용 스탬프는 `created_by: user`, `authorship: user`로 유지합니다.

현재 키를 유지합니다. Daily (`up`, `week`, `month`, `type`, `created_by`, `authorship`, `tags`); Weekly (`created_by`, `authorship`, `tags`, `month`, `quarter`, `roundup`, `type`); Monthly (`year`, `quarter`, `created_by`, `authorship`, `tags`); Quarterly (`year`, `quarter`, `created_by`, `authorship`, `tags`, `type`); Yearly (`created_by`, `authorship`, `tags`, `type`); Dashboard (`aliases`, `created_by`, `authorship`, `tags`, `type`, `week`); `manual/note.template.md` (`type`, `created_by`, `authorship`, `date_created`, `date_modified`, `tags`, `aliases`); `manual/task.template.md` (`aliases`, `type`, `done`, `gtd`, `project`, `plan`, `due`, `date_created`, `date_modified`, `date_finished`, `created_by`, `authorship`, `tags`); `manual/project.template.md` (`type`, `created_by`, `authorship`, `date_created`, `date_modified`, `tags`, `aliases`); `manual/log.template.md` (`type`, `created_by`, `authorship`, `date_created`, `date_modified`, `project`, `tags`, `aliases`).

## `auto/` — 주기 노트

Dashboard를 제외한 모든 행의 Templater 폴더 템플릿은 미리 로드되어 있습니다. Dashboard 파일은 폴더 매핑이 아니라 Daily 훅이 만듭니다.

| 템플릿 | 폴더 | 제목 형식 | 폴더 템플릿? |
| --- | --- | --- | --- |
| `auto/Daily Note.template.md` | `10. Time/01 Daily Notes` | `YYYY-MM-DD` | 예 |
| `auto/Weekly Notes.template.md` | `10. Time/02 Weekly Notes` | `GGGG-WW` 뒤에 `W` (예: `2026-03W`) | 예 |
| `auto/Monthly Notes.template.md` | `10. Time/03 Monthly Notes` | `YYYY-MM` | 예 |
| `auto/Quarterly Notes.template.md` | `10. Time/05 Quarterly Notes` | `YYYY-Qn` (예: `2026-Q1`) | 예 |
| `auto/Yearly Note.template.md` | `10. Time/04 Yearly Notes` | `YYYY` | 예 |
| `auto/Dashboard.template.md` | `10. Time/06 Dashboard` | `YYYY-MM-DD Dashboard` | **아니요** (Daily 훅만) |

이식성을 위해 이 템플릿의 섹션 제목은 영어입니다. 넣는 프론트매터는 사람이 만든 노트용입니다 (`created_by: user`, `authorship: user`). 평범한 템플릿 사용에 두 번째 메타데이터 계약을 얹지 마십시오.

## 내장 Bases와 Dataview

`90. Settings/05 Bases/`는 빈 채로 제공됩니다. 있는 뷰는 주기 템플릿에 **내장**되어 있습니다.

| 위치 | 내용 | 필요 | 노트를 만드나? |
| --- | --- | --- | --- |
| Weekly `Daily Notes` | 해당 주 날짜 범위의 `10. Time/01 Daily Notes` 파일 Core Bases **표** | 핵심 Bases (`core-plugins.json`에서 이미 켜짐); 맞는 일일 파일 | 아니요 |
| Monthly `Weeks in This Month` | 주간 계획 태그가 있고 `month` 속성이 월 제목을 포함하는 노트의 Core Bases **표** | 핵심 Bases; 필터에 맞는 주간 노트 | 아니요 |
| Quarterly `Months in Quarter` | `10. Time/03 Monthly Notes`의 월간 계획 노트 Core Bases **표** | 핵심 Bases; 맞는 월간 파일 | 아니요 |
| Dashboard `Tasks` | `type == "task"`와 `done`, `plan`, `due`, `gtd`, `project`로 거른 Core Bases **표** | 핵심 Bases; 해당 속성을 가진 할 일 노트 | 아니요 |
| Dashboard `Timeline` | Created Today, Modified Today라는 Core Bases **표** | 핵심 Bases | 아니요 |
| Dashboard `Overdue` | `10. Time/01 Daily Notes`에 대한 Dataview `TASK` 질의 | Dataview 설치 및 활성화 | 아니요 |

`auto/Dashboard.template.md`의 Dashboard **Tasks** 뷰(`manual/task.template.md`의 이 필드와 맞출 것):

| 뷰 | 필터 |
| --- | --- |
| Today | `type == "task"`이고 `done != true`이며 (`plan`이 오늘 이하 ISO 날짜이거나 `due`가 오늘 이하 ISO 날짜) |
| Due soon | `type == "task"`이고 `done != true`이며 `due`가 있음 |
| Delegation | `type == "task"`이고 `gtd == "delegation"`이며 `done != true` |

`scheduled` 키는 없습니다. `plan`과 `due`는 `YYYY-MM-DD`로 씁니다. 할 일 템플릿의 기본 `gtd`는 `inbox`입니다. `project`는 목록이며 빈 `[]`도 유효합니다.

이 템플릿에는 사용자 정의 Bases `type: timeline` 뷰가 없고, timeline-for-bases(또는 동등) 플러그인 ID도 없습니다. 간트나 타임라인 막대를 기대한 경우 제외되어 있습니다. Dashboard Timeline 섹션은 일반 표입니다. 빈 폴더는 빈 뷰를 만듭니다. 이 중 어느 것도 Obsidian UI에서 끝까지 검증했다는 주장이 아닙니다.

연간 노트는 이전/다음과 분기 위키링크만 있습니다. 내장 Base는 없습니다.

## `manual/` — 필요할 때

`manual/note.template.md`는 일반 새 노트 템플릿입니다. `manual/task.template.md`는 Dashboard Tasks와 필드가 맞는 할 일 노트입니다. `manual/project.template.md`는 프로젝트 허브입니다 (`type: project`, `status` 없음). `manual/log.template.md`는 날짜가 있는 로그입니다 (`type: log`, 인용된 허브 위키링크용 `project: []`). `manual/video.template.md`(`type: video`, `author`·`source_url`·`date_published`·`image`)와 `manual/book.template.md`(`type: book`, `author`·`status`·`total_page`·`cover_url`)는 자료 노트용이며, `90. Settings/05 Bases/Video.base`와 `Books.base`가 그 속성 이름을 읽습니다. 템플릿과 Base의 속성 이름을 같게 유지하십시오. 이름이 다르면 Base 화면이 비어 보입니다. 파일을 만들고 이름을 지은 뒤 Templater 삽입 모달에서 호출합니다. 파일·폴더·다른 노트를 만들지 않고 자동으로 실행되지 않습니다. `15. Work/01 Project`와 `15. Work/04 Tasks`에는 폴더 템플릿이 없습니다.

## 그림

Excalidraw 그림과 에셋은 `90. Settings/07 Excalidraw`에 둡니다. Handbook이 아니고 Collections 목록도 아닙니다. 허용 목록 Excalidraw `data.json`은 폴더 경로 설정입니다 (`folder`, 라이브러리·스크립트·폰트 하위 경로). 플러그인 경로 이전은 상위 작업이 맡습니다. 그 설정이 적용되려면 Excalidraw 플러그인을 설치하십시오. 이 템플릿은 Excalidraw 바이너리를 포함하지 않습니다.
