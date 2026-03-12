# 🌾 생물자원가공공학 및 실습 (Biomaterial Handling & Processing)

본 저장소(Repository)는 **생물자원가공공학 및 실습** 교과의 주차별 프로그래밍 과제 및 데이터 분석 실습 코드를 통합 관리하기 위한 공식 포트폴리오(또는 제공용) 최상위 루트 공간입니다.

> 📌 **[English Version](../en/README.md)** is also available for international students.

## 📌 저장소 목적 및 구성
본 과목에서는 수확 후 농산물 및 다양한 생물자원의 물리적, 광학적, 역학적 특성을 이해하고 이를 디지털 이미지 프로세싱(OpenCV) 등의 프로그래밍 기술을 활용하여 정량적으로 분석하는 실습을 진행합니다.

학생들은 매주 새롭게 제공되는 실습 주제별 **폴더(예: `week2`, `week3`...)** 내용물을 본인의 로컬 PC로 다운로드(Clone)하고 IDE에서 실습을 진행한 후, 각자의 GitHub 저장소에 변경/추가된 결과물을 `git add/commit/push` 하여 1학기 학습 이력을 누적해 나갑니다.

---

## 📂 주차별 실습 내용 요약

### [Week 01] 오리엔테이션 및 실습 기초 환경 구축
- 파이썬 및 GitHub 계정 세팅, 로컬 개발 환경(VS Code 등) 기초 설정 및 저장소 생성

### [Week 02] 기하학적 형태 지표(원형도, 구형도) 분석 알고리즘 구현
디지털 이미지 프로세싱 기초 기법들을 익히고, 영상을 활용해 사과 표본의 핵심 물리적 특성인 **원형도(Circularity)와 구형도(Sphericity)**를 산출합니다.
- **[A군] 정상 사과 데이터 ([`apple_side_A.png`](week2/apple_side_A.png), [`apple_top_A.png`](week2/apple_top_A.png))**: 둥글고 대칭에 가까운 정상 표본
- **[B군] 10% 왜곡 사과 데이터 ([`apple_side_B.png`](week2/apple_side_B.png), [`apple_top_B.png`](week2/apple_top_B.png))**: 한쪽 축이 일그러진 비대칭 표본
- **주요 학습 스크립트**:
  - [`step1_preprocess.py`](week2/step1_preprocess.py): 이미지 로딩 및 그레이스케일, 블러 노이즈 제거 전처리
  - [`step2_contour.py`](week2/step2_contour.py): Otsu 알고리즘 이진화 및 객체 윤곽선(Contour) 분리
  - [`step3_shape_analysis.py`](week2/step3_shape_analysis.py): 분리된 영상의 기하 특성(둘레, 면적) 추출 및 수식 기반 형태 지표(%, Circularity) 산출 및 시각화
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week2/02주차_실습_원형도_구형도.md)**

### [Week 03] 수치 적분 기반 체적 및 표면적 추정 알고리즘 구현
아보카도 레퍼런스 이미지에서 OpenCV로 프로파일을 자동 추출하고, 큐빅 스플라인 보간 후 회전체의 체적(`V = π∫r²dx`)을 Simpson/Trapezoidal 수치 적분으로 산출합니다.
- **실습 대상 시료**: 아보카도(Hass) 정면 뷰 레퍼런스 이미지 ([`avocado_front_view.png`](week3/images/avocado_front_view.png))
- **주요 학습 스크립트**:
  - [`avocado_profile.py`](week3/avocado_profile.py): (**신규**) 이미지 로드 → OpenCV 윤곽선 검출 → 프로파일 데이터 자동 추출
  - [`step1_interpolation.py`](week3/step1_interpolation.py): 이미지 기반 프로파일 추출 + 큐빅 스플라인 보간, 3패널 시각화
  - [`step2_volume.py`](week3/step2_volume.py): 회전체 체적 수치 적분 (Simpson vs. Trapezoidal), 분할 수별 수렴 분석
  - [`step3_3d_visualization.py`](week3/step3_3d_visualization.py): 원본 이미지 → 3D 회전체 재구성 → 2D 프로파일 3패널 시각화
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week3/03주차_실습_체적_표면적.md)**

### [Week 04] 밀도 측정, 공극률 산출 및 3D 가상 패킹 시뮬레이션
생물자원의 핵심 물리적 특성인 **진밀도(True Density), 겉보기 밀도(Bulk Density), 공극률(Porosity)**의 개념을 이해하고, 파이썬 기반 데이터 증강 및 3D 공간 시뮬레이션을 통해 정량적으로 평가합니다.
- **실습 대상 시료**: 아보카도(Hass) 및 사과 표본 (크기, 무게 가상 데이터 활용)
- **주요 학습 스크립트**:
  - [`step1_density_porosity.py`](week4/step1_density_porosity.py): 밀도/공극률 산출 수식(체적 차감 방식 vs 밀도 비율 방식) 교차 검증 및 3D 가상 패킹(산물과 공극의 시각화) 구현.
  - [`step2_advanced_apple.py`](week4/step2_advanced_apple.py): 제공된 기본 구조를 활용해, 주어진 사과 표본 데이터(기하학적 제원 및 무게)를 입력하여 심화 연산과 3D 가상 패킹 코드를 스스로 완성해보는 Advanced 과제.
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week4/04주차_실습_밀도_공극률.md)**

### [Week 05] (이후 실습 내용 지속 업데이트 예정)
- (차주 업데이트...)

---

## 👩‍🏫 실습 준비 공통 가이드 (환경 설정 및 코드 실행)
본 실습은 개인 PC에서 파이썬과 외부 라이브러리(OpenCV, Numpy)가 설치된 환경을 전제로 합니다. 학습을 시작하기 전 아래 단계를 수행하세요.

### 1. 베이스코드 및 데이터 다운로드 (Clone)
학생들은 매주 교수진이 배포하는 베이스 코드와 영상 데이터가 포함된 본 저장소를 자신의 로컬 PC로 가져와야 합니다.
- **[방법 1] Git 명령어 (권장)**: 터미널에서 해당 저장소를 통째로 다운로드(Clone)합니다.
   ```bash
   git clone [제공된_실습_레포지토리_주소.git]
   ```
- **[방법 2] AI IDE 프롬프트 활용**: Cursor 또는 Antigravity 같은 AI 기반 IDE를 사용 중인 경우 별도 명령어 없이 채팅 창에 바로 입력을 할 수 있습니다.
  - *예) "이 GitHub 저장소([레포지토리_주소])를 C 드라이브 밑에 biomaterial-handling 폴더로 통째로 복제해서 열어줘."*
- **[방법 3] 다운로드**: GitHub 웹페이지 우상단 `Code` 버튼 > `Download ZIP`으로 압축을 풀어 지정 폴더에 저장합니다.

### 2. IDE (통합 개발 환경) 실행 및 폴더 로드
1. VS Code, Cursor, Antigravity 등 본인에게 익숙한 에디터를 켭니다.
2. 항상 상단 메뉴의 **`File` > `Open Folder...` (폴더 열기)**를 눌러 **본 최상위 디렉터리(`biomaterial-handling/`) 전체**를 열어주세요. 
   *(하위 주차 폴더만 개별로 열 경우 파이썬 터미널 실행 시 상대 경로 인식에 오류가 생길 수 있습니다.)*

### 3. 파이썬 필수 환경 설치 및 포트폴리오 갱신
1. IDE 내부 터미널을 엽니다. (예: VS Code의 경우 `` Ctrl + ` ``)
2. 실습에 필요한 OpenCV 및 Numpy 패키지를 설치합니다.
   ```bash
   pip install opencv-python numpy
   ```
3. 각 주차별로 작성된 스크립트 코드명(예: `python step1_preprocess.py`)을 입력하여 터미널에서 구동 성능을 확인해 봅니다.
4. **결과물 업데이트**: 실습을 끝낸 후에는 반드시 이 `README.md` 문서를 스스로 수정하고(`git add/commit`), 본인의 GitHub 저장소에 `push`하여 과제 해결 이력을 본인의 포트폴리오로 누적 관리하십시오.
5. 학습 중 코딩 지식이 필요하거나 이해가 되지 않을 때는 AI 도구(ChatGPT, Antigravity 등)에 자유롭게 문의하여 해결책을 도출해 보시길 권장합니다.

---

## 4. 실습 결과물 버전 관리 및 GitHub 제출 가이드 (주석 기반 폴더 관리)

학생들은 매주 새로운 저장소(Repository)를 만들 필요 없이, **하나의 마스터 저장소(예: `biomaterial-handling`) 내에 주차별(week02, week03...) 폴더를 생성하여 과제를 누적 관리**해야 합니다.

### 4-1. 프로젝트 Git 저장소 초기화 (최초 1회만 수행)
내 컴퓨터의 학습용 최상위 폴더(예: `C:\biomaterial-handling`) 내에서 명령 프롬프트(또는 터미널)를 엽니다.
1. `git init` : 현재 최상위 폴더를 로컬 Git 저장소로 초기화합니다.
2. (GitHub 웹사이트) `biomaterial-handling` 이름으로 새 Repository를 생성합니다.
3. `git remote add origin https://github.com/[본인아이디]/biomaterial-handling.git` : 원격 저장소 주소를 연동합니다.

> 💡 **[AI Prompt 대안] Cursor / Antigravity 등 활용 시**
> 터미널 명령이 어렵다면, 해당 폴더를 IDE에서 연 상태에서 **직접 AI에게 요청**할 수도 있습니다.
> - *"현재 열린 폴더를 로컬 Git 저장소로 초기화해 주고, 방금 내가 만든 GitHub의 `[본인아이디]/biomaterial-handling` 주소로 origin 원격을 연결해 줘."*

### 4-2. 주차별(Week) 과제 폴더 생성 및 소스코드 저장
매주 새로운 실습이 주어질 때마다 최상위 폴더 내에 해당 주차의 폴더를 만들고 그 안에 코드를 저장합니다.
1. 이번 주 과제 폴더 생성: `week02` (다음 주는 `week03`)
2. `week02` 폴더 내에 방금 작성한 파이썬 스크립트(`step1`, `step2`, `step3`), 원본 이미지(`apple_side_A.png`), 그리고 결과 창 캡처 이미지를 모두 복사/저장합니다.

### 4-3. GitHub 원격 저장소로 과제 Push (매주 수행)
폴더 정리가 끝났다면 최상위 경로 터미널에서 아래 명령을 통해 추가된 주차별 코드만 깃허브에 올립니다.
1. `git add .` : 변경되거나 새롭게 추가된 주차별 폴더(week02 등) 전체를 스테이징(Staging)
2. `git commit -m "Add week02 shape analysis python scripts"` : 주차별 스냅샷 저장
3. `git push -u origin main` : (최초 시에만 `-u origin main` 사용, 이후엔 `git push`만 입력)
   - **주의**: 비밀번호 대신 **개인 액세스 토큰 (PAT, Personal Access Token)** 사용을 권장합니다.

> 💡 **[AI Prompt 대안] 매주 간편한 커밋 & 푸시 요령**
> - *"새롭게 만든 `week02` 폴더의 코드 내용들을 모두 스테이징(add) 하고 'Add week02 shape analysis python scripts' 라는 메시지로 커밋해 줘. 그 후에 origin main으로 push까지 한 번에 완료해 줘."*

### 4-4. 메인 README.md 작성 (협업/평가용)
최상위 폴더에 있는 `README.md` 문서를 매주 업데이트하여 학위/과제 포트폴리오를 구성합니다.
- **프로젝트 개요**: 본인의 이름 / 학번 / 생물자원가공공학 과제 레포지토리임을 명시
- **주차별 업데이트 내역**: 
  - `[Week 02]` 사과 윤곽선 인식 및 원형도/구형도 산출 스크립트 개발 완료
  - `[Week 03]` 수치 적분 기반 아보카도 체적/표면적 추정 실습 진행
  - `[Week 04]` 농산물 밀도/공극률 산출 및 3D 가상 패킹 구현
  - `[Week 05]` (차주 진행 시 업데이트)

---
*과제 제출 완료 후, 본인의 GitHub 저장소 URL(예: `https://github.com/아이디/biomaterial-handling/tree/main/ko/week02`)을 조교/교수에게 제출하여 최종 성적에 반영합니다.*
