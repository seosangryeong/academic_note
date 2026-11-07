# 학업 프로젝트 노트

사이트: https://seosangryeong.github.io/academic_note/

대학교·대학원 수업과 대회에서 한 프로젝트 기록을 한 사이트로 모은 저장소입니다.

- 대학원: 과학기술연합대학원대학교(UST) 인공지능학과
- 대학교: 한국기술교육대학교(KOREATECH) 메카트로닉스공학과 생산시스템

왼쪽에는 프로젝트의 기록 목록, 오른쪽에는 프로젝트 목록이 있습니다.

기록은 **Markdown**으로 쓰고, `build.py`가 HTML로 바꿉니다. push하면 GitHub Actions가 빌드해서 배포합니다. `_site/`는 커밋하지 않습니다.

| 프로젝트 | 폴더 |
| --- | --- |
| 거대언어모델기반 로봇제어 이론 및 실습 (대학원 수업) | `projects/llm-robot/` |
| 유공압실습, PLC실습 (대학교 수업) | `projects/plc/` |
| R-BIZ 챌린지 우주 탐사 로버 | `projects/rbiz/` |

## 미리 보기

```bash
python3 build.py && python3 check_site.py     # 필요: pip install markdown
python3 -m http.server -d _site 8080           # http://localhost:8080
```

## 기록 쓰기

- 프로젝트마다 `notes/`에 기록(`00-index.md`가 개요, 나머지는 파일 이름 순서), `assets/`에 사진을 둡니다.
- 기록 맨 위에 `title`, `nav`(왼쪽 목록 이름), `date`를 적습니다. 쓸 수 있는 상자(`!!! summary`, `!!! issue`, `??? 원리` 등)는 `build.py` 위쪽 설명과 기존 기록을 참고하세요.
- 새 프로젝트는 `projects/<이름>/notes`, `projects/<이름>/assets`를 만들고 `build.py`의 `PROJECTS`와 `home.md` 목록에 한 줄씩 추가합니다.

## 구성

| 파일 | 내용 |
| --- | --- |
| `home.md` | 첫 화면 소개 (`{{period:slug}}`는 `build.py`의 기간으로 바뀜) |
| `projects/` | 프로젝트별 기록과 사진 |
| `build.py` | Markdown → `_site/` (홈 + 프로젝트별 폴더), 프로젝트 순서·기간 |
| `styles.css` | 스타일 |
| `check_site.py` | 깨진 링크 검사 |
| `.github/workflows/site.yml` | push·수동 실행 시 빌드·검사·GitHub Pages 배포 |
