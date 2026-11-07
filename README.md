# 학업 프로젝트 노트

사이트: https://seosangryeong.github.io/academic_note/

대학교·대학원 수업과 대회에서 한 프로젝트 기록을 한 사이트로 모은 저장소입니다.

- 대학원: 과학기술연합대학원대학교(UST) 인공지능학과
- 대학교: 한국기술교육대학교(KOREATECH) 메카트로닉스공학과 생산시스템

왼쪽에는 프로젝트의 기록 목록, 오른쪽에는 프로젝트 목록이 있습니다.

기록은 **Markdown**으로 쓰고, `build.py`가 HTML로 바꿉니다. push하면 GitHub Actions가 빌드해서 배포합니다. `_site/`는 커밋하지 않습니다.

| 구분 | 폴더 | 내용 |
| --- | --- | --- |
| 대학원 수업 | `projects/grad/` | 거대언어모델기반 로봇제어 이론 및 실습, 컴퓨터비전을 위한 수학적 기법, 딥러닝 / 고급 딥러닝, 패턴인식 및 기계학습 |
| 대학교 수업 | `projects/undergrad/` | 캡스톤디자인(졸업작품: 테니스공 수거 로봇), 생산계획 및 관리, PLC실습, 유공압실습 |
| 대회 | `projects/contest/` | R-BIZ 챌린지 우주 탐사 로버 |

## 미리 보기

```bash
python3 build.py && python3 check_site.py     # 필요: pip install markdown
python3 -m http.server -d _site 8080           # http://localhost:8080
```

## 기록 쓰기

- 기록 맨 위에 `title`, `nav`(왼쪽 목록 이름), `date`를 적습니다. 쓸 수 있는 상자(`!!! summary`, `!!! issue`, `??? 원리` 등)는 `build.py` 위쪽 설명과 기존 기록을 참고하세요.
- 새 수업이나 대회는 해당 구분 폴더(`grad`, `undergrad`, `contest`)의 `notes/`에 기록 파일을 하나 추가하고 사진은 같은 폴더의 `assets/`에 넣은 뒤, `home.md` 목록에 한 줄 추가합니다. 왼쪽 목록 순서는 파일 이름 순서이고, `00-index.md`가 그 구분의 첫 페이지입니다.
- 구분 자체를 새로 만들 때만 `build.py`의 `PROJECTS`에 한 줄 추가합니다.

## 구성

| 파일 | 내용 |
| --- | --- |
| `home.md` | 첫 화면 소개 (`{{period:slug}}`는 `build.py`의 기간으로 바뀜) |
| `projects/` | 프로젝트별 기록과 사진 |
| `build.py` | Markdown → `_site/` (홈 + 프로젝트별 폴더), 프로젝트 순서·기간 |
| `styles.css` | 스타일 |
| `check_site.py` | 깨진 링크 검사 |
| `.github/workflows/site.yml` | push·수동 실행 시 빌드·검사·GitHub Pages 배포 |
