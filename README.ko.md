---
created_by: gjc
authorship: agent
---

# Ataraxia 볼트 템플릿

[English](README.md)

개인 지식 시스템에서 가져온 휴대용 Obsidian 볼트 골격입니다. 번호가 붙은 PARA와 비슷한 배치, 노트당 하나의 정식 위치, `90. Settings` 아래의 시스템 규칙을 유지합니다. 개인 노트, 자격 증명, 플러그인 캐시, 플러그인 바이너리, 테마 바이너리, 기기별 상태는 포함하지 않습니다.

이 폴더를 Obsidian에서 새 볼트로 여세요. `00. Inbox`에 캡처한 뒤 [90. Settings/01 Guideline/01. Placement Guide.ko.md](90.%20Settings/01%20Guideline/01.%20Placement%20Guide.ko.md)로 각 노트를 배치합니다. 주기 노트 템플릿은 `90. Settings/02 Templates`에 있습니다. 홈 노트, 인덱스, 독립 Bases 파일은 비어 있는 자리만 있으므로 직접 채우면 됩니다.

## 루트

루트 10개를 제공합니다. 개인 볼트에만 있는 추가 루트는 이 템플릿의 일부가 아닙니다.

- `00. Inbox` — 미분류 캡처. 목적지가 분명해지면 바로 옮깁니다.
- `10. Time` — 주기 계획과 회고(일간, 주간, 월간, 분기, 연간, 대시보드).
- `15. Work` — 종료 조건이 있는 프로젝트, 지속 영역, 끝난 작업, 할 일.
- `30. Literature Notes` — 외부 자료에서 나온 생각(연구, 리뷰, 회의).
- `40. Permanent Notes` — 그 자체로 서는 아이디어와 원칙.
- `50. AI` — 소유 프로젝트가 없는 AI 생성·합성 자료.
- `70. Collections` — 사람, 프롬프트, 콘텐츠 맵, 음악, 장소, Excalidraw 그림, 조직, GitHub, 채널 등 재사용 목록. `70. Collections/06 Excalidraw`는 빈 폴더로 있습니다.
- `80. References` — 책, 논문, 첨부 파일.
- `85. Raw` — 누가, 무엇이 캡처했든 외부 원본.
- `90. Settings` — 볼트 규칙, 템플릿, 홈, 인덱스, Bases.

## 포함된 설정과 직접 설치해야 하는 것

`.obsidian/community-plugins.json`은 플러그인 **ID** 목록입니다. 플러그인을 설치하지 않습니다. 이 템플릿에는 `.obsidian/plugins/` 디렉터리가 없습니다.

`.obsidian/appearance.json`은 `cssTheme`을 `Minimal`로 두고, `.obsidian/snippets/` 아래 함께 제공되는 스니펫 두 개를 켭니다. `.obsidian/themes/` 디렉터리는 없으므로 Minimal은 직접 추가하기 전(또는 테마를 바꾸기 전)까지 설치되지 않습니다. `obsidian-minimal-settings`도 ID만 있습니다.

`.obsidian/core-plugins.json`은 코어 Bases와 코어 Templates 플러그인을 켜고 **Daily notes는 끕니다**. `.obsidian/daily-notes.json`은 없습니다. Templater 설정도 포함되지 않습니다(`templater-obsidian`은 ID만 있습니다).

`90. Settings/02 Templates/auto/Daily Note.template.md`는 **포함되어 있습니다**. 이 템플릿으로 일간 노트를 만들면 어제·오늘·내일의 빠진 대시보드를 만들 수 있습니다. 주간, 월간, 분기, 연간 노트는 만들지 않습니다. 주기 템플릿의 위키링크는 탐색용입니다.

## 일간·주간 이름 규칙

일간 노트 제목은 `10. Time/01 Daily Notes`에서 `YYYY-MM-DD`입니다. 주간 노트 제목은 `10. Time/02 Weekly Notes`에서 ISO 주 연도 `GGGG-WW` 뒤에 `W`를 붙인 형식입니다(예: `2026-37W`). 일간 노트는 `week`에 그 주간 제목을 씁니다. 주간 노트를 만들 때 같은 이름을 사용하세요.

자동 주기 연쇄는 없습니다. 주기 템플릿의 위키링크는 탐색용입니다.

폴더, 형식, Templater 단계는 [90. Settings/02 Templates/README.ko.md](90.%20Settings/02%20Templates/README.ko.md)에 있습니다.

## 시작 방법

1. 이 디렉터리를 복사하거나 클론한 뒤 Obsidian 볼트로 엽니다.
2. 첫 노트를 두기 전에 [90. Settings/01 Guideline/01. Placement Guide.ko.md](90.%20Settings/01%20Guideline/01.%20Placement%20Guide.ko.md)를 읽습니다.
3. 실제로 쓸 커뮤니티 플러그인과 테마만 설치합니다. Obsidian에서 플러그인은 **설정 → 커뮤니티 플러그인**, 테마는 **외관 → 테마**로 설치합니다. `auto/`와 `manual/` 템플릿을 실행하려면 [Templater](https://github.com/SilentVoid13/Templater)가 필요합니다. 대시보드 Overdue 쿼리에는 Dataview가 필요합니다. Excalidraw는 `70. Collections/06 Excalidraw`에 그림을 둘 때만 필요합니다. [Minimal](https://github.com/kepano/obsidian-minimal) 테마는 `appearance.json`에 이름만 있고 파일은 없습니다. `community-plugins.json`의 ID는 설치를 대신하지 않습니다.
4. Templater를 설정하고, Daily notes 명령을 쓰려면 코어 Daily notes를 켠 뒤 설정합니다. 정확한 폴더, 형식, 템플릿 경로는 [90. Settings/02 Templates/README.ko.md](90.%20Settings/02%20Templates/README.ko.md)에 있습니다.
5. 미분류 캡처는 `00. Inbox`에 둡니다.
6. 노트의 소유자가 있으면 `15. Work/01 Project` 또는 `15. Work/02 Area` 아래에 작업을 만듭니다.
7. 캡처한 원본은 `85. Raw`에, 시스템 파일은 `90. Settings`에 둡니다.

이 단계는 설정 안내입니다. 주기 노트 생성, Bases 보기, 테마 모양이 Obsidian에서 끝까지 검증되었다는 주장이 아닙니다.
