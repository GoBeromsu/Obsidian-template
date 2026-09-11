---
created_by: agent
authorship: agent
---
# 템플릿

[English](README.md) · [한국어](README.ko.md)

관련: [Start (English)](../../README.md) · [시작 (한국어)](../../README.ko.md) · [Placement Guide](../01%20Guideline/01.%20Placement%20Guide.md) · [배치 가이드](../01%20Guideline/01.%20Placement%20Guide.ko.md) · [Agent contract](AGENTS.md)

이들은 [Templater](https://github.com/SilentVoid13/Templater) 템플릿입니다. `periodic-notes` 플러그인은 이 템플릿의 플러그인 ID 목록에 없고 사용하지 않습니다.

`community-plugins.json`에 `templater-obsidian`(또는 Dataview, Excalidraw, Minimal Theme Settings)이 적혀 있어도 그 플러그인을 **설치하지 않습니다**. 이 볼트는 `.obsidian/plugins/` 디렉터리와 `.obsidian/themes/` 디렉터리를 **포함하지 않습니다**. `<% %>` 템플릿이 실행되려면 먼저 Templater를 설치하십시오.

## `auto/`와 `manual/`

| 폴더 | 역할 |
| --- | --- |
| `auto/` | 주기 템플릿. Templater **Folder templates**(또는 동등한 생성 시 삽입 경로)를 이 파일에 연결합니다. |
| `manual/` | 필요할 때 쓰는 템플릿. Templater 삽입 모달에서 호출합니다. |

`auto/`는 폴더 이름이지 자동 실행기가 아닙니다. 이 템플릿 안에는 이 파일들을 스스로 실행하는 장치가 없습니다. 핵심 Daily notes는 현재 `.obsidian/core-plugins.json`에서 **꺼져 있고**, Templater `data.json`과 핵심 `daily-notes.json`도 포함되어 있지 않습니다. Templater를 설치하고 아래 정확한 경로를 설정하기 전에는 `10. Time/` 아래에 파일을 만들어도 이 템플릿이 적용되지 않습니다.

포함된 템플릿 파일은 모두 `*.template.md` 접미사를 씁니다.

- `auto/Daily Note.template.md`
- `auto/Weekly Notes.template.md`
- `auto/Monthly Notes.template.md`
- `auto/Quarterly Notes.template.md`
- `auto/Yearly Note.template.md`
- `auto/Dashboard.template.md`
- `manual/note.template.md`

## 엔진 설정 (미리 로드되지 않음)

이 템플릿은 Templater `data.json`과 핵심 `daily-notes.json`을 포함하지 않습니다. 핵심 Daily notes는 `.obsidian/core-plugins.json`에서 **꺼져 있습니다**. 핵심 Templates는 거기에서 켜져 있지만 `templates.json`은 없고, Templater와 혼동하지 마십시오. 아래 단계는 파일이 맞춰 쓰인 설정이며, 검증된 라이브 볼트라는 주장이 아닙니다.

### Templater

1. Templater를 설치하고 켭니다.
2. **Template folder location**을 `90. Settings/02 Templates`로 둡니다(볼트 상대 경로). 삽입 모달이 보는 폴더이며, `auto/`와 `manual/`이 그 아래에 있습니다.
3. **Trigger Templater on new file creation**을 켭니다.
4. 아래 표에서 실제로 해당 폴더에 파일을 떨어뜨려(또는 먼저 그 위치에 파일을 만드는 명령으로) 생성하는 행마다 **Folder templates**를 추가합니다.

같은 파일에 폴더 템플릿과 다른 적용 수단이 함께 걸리면 Templater가 두 번 실행될 수 있습니다. 폴더마다 적용 수단을 하나만 고르십시오.

### 핵심 Daily notes (선택)

Obsidian의 Daily notes 명령이 필요할 때만 씁니다. 켜기 전에는 꺼져 있습니다.

1. 핵심 **Daily notes** 플러그인을 켭니다.
2. New file location: `10. Time/01 Daily Notes`
3. Date format: `YYYY-MM-DD` (Daily 템플릿이 그 제목을 파싱합니다)
4. Template file: Templater 폴더 템플릿이 이미 `10. Time/01 Daily Notes`를 가리키면 비워 둡니다. 그렇지 않으면 `90. Settings/02 Templates/auto/Daily Note.template.md`로 둡니다.

핵심 Daily notes는 일일 파일만 만듭니다. 주·월·분기·연·대시보드 노트는 만들지 않습니다.

## 탐색과 생성

프론트매터와 본문의 위키링크(`week`, `month`, `year`, `quarter`, 이전/다음 주기, 대시보드 `up` 등)는 **탐색**입니다. 대상 노트를 만들지 않습니다.

계획 계층은 연 → 분기 → 월 → 주 → 일입니다. 주기 노트는 그 사슬을 명시적 위키링크로 가리킵니다. 자동 주기 연쇄 생성은 없습니다.

방금 연 노트 외에, 포함된 생성기는 Daily 템플릿뿐입니다. 일일 노트가 쓰인 뒤 없는 파일을 만들려고 합니다.

- 어제·오늘·내일의 `10. Time/06 Dashboard/YYYY-MM-DD Dashboard.md`

Templater `tp.file.create_new`로 `auto/Dashboard.template.md`를 사용합니다. 주·월·분기·연 노트는 **만들지 않습니다**.

`10. Time/06 Dashboard`에도 Templater 폴더 템플릿을 걸면, Daily 훅이 만든 대시보드가 두 번 처리될 수 있습니다. 이중 처리를 감수하지 않는 한 Daily 훅과 Dashboard 폴더 템플릿을 함께 쓰지 마십시오.

## 제목 형식

제목 형식은 스크립트가 `tp.file.title`에서 파싱하는 값입니다. 제목 없는 채 만든 뒤 이름 바꾸는 경쟁 상태에서는 "지금"으로 떨어집니다.

| 주기 | 폴더 | 제목 형식 | 예 |
| --- | --- | --- | --- |
| 일 | `10. Time/01 Daily Notes` | `YYYY-MM-DD` | `2026-09-11` |
| 주 | `10. Time/02 Weekly Notes` | ISO 주년 `GGGG-WW` 뒤에 `W` | `2026-37W` |
| 월 | `10. Time/03 Monthly Notes` | `YYYY-MM` | `2026-09` |
| 분기 | `10. Time/05 Quarterly Notes` | `YYYY-Qn` | `2026-Q1` |
| 연 | `10. Time/04 Yearly Notes` | `YYYY` | `2026` |
| 대시보드 | `10. Time/06 Dashboard` | `YYYY-MM-DD Dashboard` | `2026-09-11 Dashboard` |

주는 ISO 주(월요일–일요일)이며 Daily의 `week` 값(`GGGG-WW` 뒤에 `W`)과 같습니다. 일요일 시작 주를 쓰지 말고, 일요일을 다음 주에 넣지 마십시오. 일일 노트는 `week`를 그 제목으로 쓰므로, 주간 노트를 만들 때 같은 제목을 쓰십시오.

## YAML 규칙

각 템플릿이 이미 넣는 필드를 재사용하십시오. 개인 메타데이터 스키마를 덮어씌우지 마십시오.

- 키는 `snake_case`입니다 (`created_by`, `date_created`, `date_modified`).
- 위키링크 값은 인용된 YAML 문자열입니다. 예: `week: "[[2026-37W]]"`, `up: "[[2026-09-11 Dashboard]]"`.
- 일반 ISO 날짜는 인용하지 않습니다. 예: `date_created: 2026-09-11`.
- 사람용 스탬프는 `created_by: user`, `authorship: user`로 유지합니다.

현재 키를 유지합니다. Daily (`up`, `week`, `month`, `type`, `created_by`, `authorship`, `tags`); Weekly (`created_by`, `authorship`, `tags`, `month`, `quarter`, `roundup`, `type`); Monthly (`year`, `quarter`, `created_by`, `authorship`, `tags`); Quarterly (`year`, `quarter`, `created_by`, `authorship`, `tags`, `type`); Yearly (`created_by`, `authorship`, `tags`, `type`); Dashboard (`aliases`, `created_by`, `authorship`, `tags`, `type`, `week`); `manual/note.template.md` (`type`, `created_by`, `authorship`, `date_created`, `date_modified`, `tags`, `aliases`).

## `auto/` — 주기 노트

Templater 폴더 템플릿(또는 동등한 생성 시 삽입 경로)을 이 파일에 연결합니다.

| 템플릿 | 폴더 | 제목 형식 |
| --- | --- | --- |
| `auto/Daily Note.template.md` | `10. Time/01 Daily Notes` | `YYYY-MM-DD` |
| `auto/Weekly Notes.template.md` | `10. Time/02 Weekly Notes` | `GGGG-WW` 뒤에 `W` (예: `2026-37W`) |
| `auto/Monthly Notes.template.md` | `10. Time/03 Monthly Notes` | `YYYY-MM` |
| `auto/Quarterly Notes.template.md` | `10. Time/05 Quarterly Notes` | `YYYY-Qn` (예: `2026-Q1`) |
| `auto/Yearly Note.template.md` | `10. Time/04 Yearly Notes` | `YYYY` |
| `auto/Dashboard.template.md` | `10. Time/06 Dashboard` | `YYYY-MM-DD Dashboard` |

이식성을 위해 이 템플릿의 섹션 제목은 영어입니다. 넣는 프론트매터는 사람이 만든 노트용입니다 (`created_by: user`, `authorship: user`). 평범한 템플릿 사용에 두 번째 메타데이터 계약을 얹지 마십시오.

## 내장 Bases와 Dataview

`90. Settings/05 Bases/`는 빈 채로 제공됩니다. 있는 뷰는 주기 템플릿에 **내장**되어 있습니다.

| 위치 | 내용 | 필요 | 노트를 만드나? |
| --- | --- | --- | --- |
| Weekly `Daily Notes` | 해당 주 날짜 범위의 `10. Time/01 Daily Notes` 파일 Core Bases **표** | 핵심 Bases (`core-plugins.json`에서 이미 켜짐); 맞는 일일 파일 | 아니요 |
| Monthly `Weeks in This Month` | 주간 계획 태그가 있고 `month` 속성이 월 제목을 포함하는 노트의 Core Bases **표** | 핵심 Bases; 필터에 맞는 주간 노트 | 아니요 |
| Quarterly `Months in Quarter` | `10. Time/03 Monthly Notes`의 월간 계획 노트 Core Bases **표** | 핵심 Bases; 맞는 월간 파일 | 아니요 |
| Dashboard `Tasks` | `type == "task"`로 거른 Core Bases **표** | 핵심 Bases; 해당 속성을 가진 할 일 노트 | 아니요 |
| Dashboard `Timeline` | Created Today, Modified Today라는 Core Bases **표** | 핵심 Bases | 아니요 |
| Dashboard `Overdue` | `10. Time/01 Daily Notes`에 대한 Dataview `TASK` 질의 | Dataview 설치 및 활성화 | 아니요 |

이 템플릿에는 사용자 정의 Bases `type: timeline` 뷰가 없고, timeline-for-bases(또는 동등) 플러그인 ID도 없습니다. 간트나 타임라인 막대를 기대한 경우 제외되어 있습니다. Dashboard Timeline 섹션은 일반 표입니다. 빈 폴더는 빈 뷰를 만듭니다. 이 중 어느 것도 Obsidian UI에서 끝까지 검증했다는 주장이 아닙니다.

연간 노트는 이전/다음과 분기 위키링크만 있습니다. 내장 Base는 없습니다.

## `manual/` — 필요할 때

`manual/note.template.md`는 일반 새 노트 템플릿입니다. Templater 삽입 모달에서 호출합니다.
