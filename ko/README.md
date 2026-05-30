# 🌾 생물자원가공공학 및 실습 (Biomaterial Handling & Processing)

> **Author / Rights Holder:** 전북대학교 생물산업기계공학과 유동수 (ryudongsoo@jbnu.ac.kr)

본 저장소(Repository)는 **생물자원가공공학 및 실습** 교과의 주차별 프로그래밍 과제 및 데이터 분석 실습 코드를 통합 관리하기 위한 공식 포트폴리오(또는 제공용) 최상위 루트 공간임

> 📌 **[English Version](../en/README.md)** is also available for international students.

## 📌 저장소 목적 및 구성
본 과목에서는 수확 후 농산물 및 다양한 생물자원의 물리적, 광학적, 역학적 특성을 이해하고 이를 디지털 이미지 프로세싱(OpenCV) 등의 프로그래밍 기술을 활용하여 정량적으로 분석하는 실습을 진행함

학생들은 매주 새롭게 제공되는 실습 주제별 **폴더(예: `week2`, `week3`...)** 내용물을 본인의 로컬 PC로 다운로드(Clone)하고 IDE에서 실습을 진행한 후, 각자의 GitHub 저장소에 변경/추가된 결과물을 `git add/commit/push` 하여 1학기 학습 이력을 누적해 나갑니다.

---

## 📂 주차별 실습 내용 요약

### [Week 01] 오리엔테이션 및 실습 기초 환경 구축
- 파이썬 및 GitHub 계정 세팅, 로컬 개발 환경(VS Code 등) 기초 설정 및 저장소 생성
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](실습_환경_설정_가이드.md)**

### [Week 02] 기하학적 형태 지표(원형도, 구형도) 분석 알고리즘 구현
디지털 이미지 프로세싱 기초 기법들을 익히고, 영상을 활용해 사과 표본의 핵심 물리적 특성인 **원형도(Circularity)와 구형도(Sphericity)**를 산출함
- **[A군] 정상 사과 데이터 ([`apple_side_A.png`](week2/images/apple_side_A.png), [`apple_top_A.png`](week2/images/apple_top_A.png))**: 둥글고 대칭에 가까운 정상 표본
- **[B군] 10% 왜곡 사과 데이터 ([`apple_side_B.png`](week2/images/apple_side_B.png), [`apple_top_B.png`](week2/images/apple_top_B.png))**: 한쪽 축이 일그러진 비대칭 표본
- **주요 학습 스크립트**:
  - [`step1_preprocess.py`](week2/step1_preprocess.py): 이미지 로딩 및 그레이스케일, 블러 노이즈 제거 전처리
  - [`step2_contour.py`](week2/step2_contour.py): Otsu 알고리즘 이진화 및 객체 윤곽선(Contour) 분리
  - [`step3_shape_analysis.py`](week2/step3_shape_analysis.py): 분리된 영상의 기하 특성(둘레, 면적) 추출 및 수식 기반 형태 지표(%, Circularity) 산출 및 시각화
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week2/02주차_실습_원형도_구형도.md)**

### [Week 03] 수치 적분 기반 체적 및 표면적 추정 알고리즘 구현
아보카도 레퍼런스 이미지에서 OpenCV로 프로파일을 자동 추출하고, 큐빅 스플라인 보간 후 회전체의 체적(`V = π∫r²dx`)을 Simpson/Trapezoidal 수치 적분으로 산출함
- **실습 대상 시료**: 아보카도(Hass) 정면 뷰 레퍼런스 이미지 ([`avocado_front_view.png`](week3/images/avocado_front_view.png))
- **주요 학습 스크립트**:
  - [`avocado_profile.py`](week3/avocado_profile.py): (**신규**) 이미지 로드 → OpenCV 윤곽선 검출 → 프로파일 데이터 자동 추출
  - [`step1_interpolation.py`](week3/step1_interpolation.py): 이미지 기반 프로파일 추출 + 큐빅 스플라인 보간, 3패널 시각화
  - [`step2_volume.py`](week3/step2_volume.py): 회전체 체적 수치 적분 (Simpson vs. Trapezoidal), 분할 수별 수렴 분석
  - [`step3_3d_visualization.py`](week3/step3_3d_visualization.py): 원본 이미지 → 3D 회전체 재구성 → 2D 프로파일 3패널 시각화
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week3/03주차_실습_체적_표면적.md)**

### [Week 04] 밀도 측정, 공극률 산출 및 3D 가상 패킹 시뮬레이션
생물자원의 핵심 물리적 특성인 **진밀도(True Density), 겉보기 밀도(Bulk Density), 공극률(Porosity)**의 개념을 이해하고, 파이썬 기반 데이터 증강 및 3D 공간 시뮬레이션을 통해 정량적으로 평가함
- **실습 대상 시료**: 아보카도(Hass) 및 사과 표본 (크기, 무게 가상 데이터 활용)
- **주요 학습 스크립트**:
  - [`step1_density_porosity.py`](week4/step1_density_porosity.py): 밀도/공극률 산출 수식(체적 차감 방식 vs 밀도 비율 방식) 교차 검증 및 3D 가상 패킹(산물과 공극의 시각화) 구현.
  - [`step2_advanced_apple.py`](week4/step2_advanced_apple.py): 제공된 기본 구조를 활용해, 주어진 사과 표본 데이터(기하학적 제원 및 무게)를 입력하여 심화 연산과 3D 가상 패킹 코드를 스스로 완성해보는 Advanced 과제.
  - [`step3_random_packing.py`](week4/step3_random_packing.py): (**신규**) 배열 적재(Ordered)와 무작위 적재(Random) 알고리즘 비교를 통해 산물 밀도 저하 원인을 확인하는 3D 시뮬레이션.
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week4/04주차_실습_밀도_공극률.md)**

### [Week 05] 유변학적 특성 분석 및 이송 공정 최적화 시뮬레이션
파이프라인 이송 중 발생하는 마찰 점성 저항(Pressure Drop)과 펌프 동력 비용, 그리고 열교환을 위한 가열 에너지 간의 트레이드오프 관계를 아레니우스 모델 및 하겐-푸아죄유 방정식으로 규명함
- **실습 대상 시료**: 맑은 사과 농축액 (사과즙) 데이터
- **주요 학습 스크립트**:
  - [`step1_viscosity_optimization.py`](week5/step1_viscosity_optimization.py): 뉴턴 유체 점도-온도 반비례 모델 정적 시각화 및 최저 총비용 교차점 도출
  - [`step2_interactive_simulation.py`](week5/step2_interactive_simulation.py): 파라미터(유속, 내경, 단가) 실시간 조작에 반응하는 최적 온도 U-커브 애니메이션 (Slider UI)
  - [`step3_pipe_diameter_simulation.py`](week5/step3_pipe_diameter_simulation.py): 파이프 직경 확대에 따른 펌핑 비용 하락 vs 기본 설비 단가 급증 교차 마진 도출
  - [`step4_reynolds_simulation.py`](week5/step4_reynolds_simulation.py): 레이놀즈 수 상승에 따른 층류/난류 상태 전이 및 믹싱 강제 와류 동적 파티클 애니메이션
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week5/05주차_실습_유변학적특성.md)**

### [Week 06] 비뉴턴 유체의 복합 거동 분석 및 유동 모델 피팅
비뉴턴 유체(전단 담화, 전단 농화, 빙햄 플라스틱)의 거동을 Power Law 및 Herschel-Bulkley 모델로 피팅하고, 겉보기 점도 및 항복 응력 시뮬레이터를 구현
- **주요 학습 스크립트**:
  - [`step1_powerlaw_curve_fit.py`](week6/step1_powerlaw_curve_fit.py): Power Law 곡선 피팅 역산
  - [`step2_apparent_viscosity.py`](week6/step2_apparent_viscosity.py): 겉보기 점도 슬라이더 시뮬레이터
  - [`step3_herschel_bulkley_yield.py`](week6/step3_herschel_bulkley_yield.py): Herschel-Bulkley 항복 응력 분석
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week6/06주차_실습_비뉴턴유체.md)**

### [Week 07] 점탄성 특성 — 크리프와 응력 이완
점탄성 모델(Maxwell, Kelvin-Voigt, Burgers)의 크리프 및 응력 이완 시뮬레이션과 4-파라미터 역산 피팅 실습
- **실습 대상 시료**: 사과(Fuji) 텍스처 애널라이저 응력 이완 및 크리프 데이터
- **주요 학습 스크립트**:
  - [`step1_maxwell_relaxation.py`](week7/step1_maxwell_relaxation.py): Maxwell 응력 이완 시뮬레이션 (3가지 η 비교)
  - [`step2_burgers_creep_fit.py`](week7/step2_burgers_creep_fit.py): Burgers 4-파라미터 크리프 곡선 피팅
  - [`step3_viscoelastic_simulator.py`](week7/step3_viscoelastic_simulator.py): 인터랙티브 점탄성 시뮬레이터 (모델 전환 + 듀얼 플롯)
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week7/07주차_실습_점탄성특성.md)**

### [Week 08] 중간고사
- 2~7주차 범위 종합 평가

### [Week 09] 접촉 응력과 헤르츠 이론 — 기계적 특성 I
곡면 생물자원의 접촉 역학(Hertz Contact Theory)을 기반으로 접촉 반경, 최대 응력, 압력 분포를 Python으로 분석하고, 선별기 롤러 재질 최적화 시뮬레이션 수행
- **실습 대상 시료**: 사과(Fuji) 텍스처 애널라이저 압축 데이터
- **주요 학습 스크립트**:
  - [`step1_hertz_calculator.py`](week9/step1_hertz_calculator.py): 헤르츠 접촉 응력 계산기 (4종 접촉면 재질 비교)
  - [`step2_pressure_distribution.py`](week9/step2_pressure_distribution.py): 접촉 압력 분포 3D 시각화 + 깊이별 응력 프로파일
  - [`step3_hertz_contact_simulator.py`](week9/step3_hertz_contact_simulator.py): 인터랙티브 접촉 시뮬레이터 (슬라이더 + 라디오 버튼)
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week9/09주차_실습_접촉응력_헤르츠이론.md)**


### [Week 11] 광학적 특성과 색채 공학 — 자동 선별
디지털 카메라로 촬영된 농산물 이미지에서 색채 공간(HSV, CIE Lab) 특성을 분석하고 머신비전 기반의 자동 선별 메커니즘을 구현함
- **주요 학습 스크립트**:
  - `step1_color_sorting.py`: BGR 색 공간을 HSV 및 CIE Lab으로 변환, 색상 임계값을 통한 토마토의 숙도(Red) 영역 추출 및 비교 시각화
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week11/11주차_실습_광학적특성_색채공학.md)**

### [Week 12] 광학적 특성 II — 내부 품질 평가 및 분광 분석
근적외선(NIR) 흡광도 스펙트럼 데이터를 기반으로 다변량 데이터 분석 기법을 적용하여 생물체의 내부 당도(Brix)를 비파괴적으로 예측함
- **주요 학습 스크립트**:
  - `step1_spectroscopy_plsr.py`: 파장별 스펙트럼 데이터 전처리(SNV, Savitzky-Golay 1차 미분) 및 부분 최소 자승 회귀(PLSR) 모델 학습, 예측 오차 분석(R², RMSE) 시각화
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week12/12주차_실습_광학적특성_분광분석.md)**

### [Week 10] 충격 특성과 손상 예측 모델링 — 기계적 특성 II
오픈소스 물리 분석 도구인 Tracker 비디오 분석 소프트웨어를 활용하여 생물체의 낙하 충격 거동을 추적하고, 파이썬 기반으로 반발 계수 산출 및 한계 손상 에너지(Bio-yield) 초과 여부를 시뮬레이션함
- **주요 학습 스크립트**:
  - [`step1_impact_analysis.py`](week10/step1_impact_analysis.py): 낙하 높이 및 충돌 시간 기반 반발 계수·최대 충격력 산출 및 손상 예측 시뮬레이션
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week12/12주차_실습_광학적특성_분광분석.md)**

### [Week 13] 음향 특성 — FFT 기반 경도 분석
충격 가진(Impact Excitation) 후 발생하는 공명 주파수를 FFT로 추출하고, 경도 지수($S = f^2 m^{2/3}$)를 산출하여 과실 성숙도별 등급 분류 수행
- **주요 학습 스크립트**:
  - `step1_acoustic_fft.py`: 가상 타격 응답 신호 생성 → FFT 스펙트럼 → `scipy.signal.find_peaks` 피크 검출 → 경도 지수 산점도 + 슬라이더 UI
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week13/13주차_실습_음향특성_경도분석.md)**

### [Week 14] 열적 특성 — 냉각 시뮬레이션과 에너지 공학
1D 구형 좌표계 열전도 편미분 방정식(PDE)을 SciPy `solve_ivp`로 풀어 과실 중심/표면 온도 변화 시뮬레이션 및 반감기 산출
- **주요 학습 스크립트**:
  - `step1_cooling_simulation.py`: 열물성 파라미터 설정 → FDM 공간 이산화 → RK45 시간 적분 → 중심/표면 온도 시계열 + 슬라이더 3개(h, R, T_init)
- ➡️ **[해당 주차 상세 실습 튜토리얼 보기](week14/14주차_실습_열적특성_냉각시뮬레이션.md)**

---

## 👩‍🏫 실습 준비 공통 가이드 (환경 설정 및 코드 실행)
본 실습은 개인 PC에서 파이썬과 외부 라이브러리(OpenCV, Numpy)가 설치된 환경을 전제로 함 학습을 시작하기 전 아래 단계를 수행 필요.

### 1. 베이스코드 및 데이터 다운로드 (Clone)
학생들은 매주 교수진이 배포하는 베이스 코드와 영상 데이터가 포함된 본 저장소를 자신의 로컬 PC로 가져와야 함
- **[방법 1] Git 명령어 (권장)**: 터미널에서 해당 저장소를 통째로 다운로드(Clone)함
   ```bash
   git clone [제공된_실습_레포지토리_주소.git]
   ```
- **[방법 2] AI IDE 프롬프트 활용**: Cursor 또는 Antigravity 같은 AI 기반 IDE를 사용 중인 경우 별도 명령어 없이 채팅 창에 바로 입력을 할 수 있음
  - *예) "이 GitHub 저장소([레포지토리_주소])를 C 드라이브 밑에 biomaterial-handling 폴더로 통째로 복제해서 열어줘."*
- **[방법 3] 다운로드**: GitHub 웹페이지 우상단 `Code` 버튼 > `Download ZIP`으로 압축을 풀어 지정 폴더에 저장함

### 2. IDE (통합 개발 환경) 실행 및 폴더 로드
1. VS Code, Cursor, Antigravity 등 본인에게 익숙한 에디터를 켭니다.
2. 항상 상단 메뉴의 **`File` > `Open Folder...` (폴더 열기)**를 눌러 **본 최상위 디렉터리(`biomaterial-handling/`) 전체**를 열어바람. 
   *(하위 주차 폴더만 개별로 열 경우 파이썬 터미널 실행 시 상대 경로 인식에 오류가 생길 수 있음)*

### 3. 파이썬 필수 환경 설치 및 포트폴리오 갱신
1. IDE 내부 터미널을 엽니다. (예: VS Code의 경우 `` Ctrl + ` ``)
2. 실습에 필요한 OpenCV 및 Numpy 패키지를 설치함
   ```bash
   pip install opencv-python numpy
   ```
3. 각 주차별로 작성된 스크립트 코드명(예: `python step1_preprocess.py`)을 입력하여 터미널에서 구동 성능을 확인해 봄.
4. **결과물 업데이트**: 실습을 끝낸 후에는 반드시 이 `README.md` 문서를 스스로 수정하고(`git add/commit`), 본인의 GitHub 저장소에 `push`하여 과제 해결 이력을 본인의 포트폴리오로 누적 관리 필요.
5. 학습 중 코딩 지식이 필요하거나 이해가 되지 않을 때는 AI 도구(ChatGPT, Antigravity 등)에 자유롭게 문의하여 해결책을 도출해 보시길 권장함

---

## 4. 실습 결과물 버전 관리 및 GitHub 제출 가이드 (주석 기반 폴더 관리)

학생들은 매주 새로운 저장소(Repository)를 만들 필요 없이, **하나의 마스터 저장소(예: `biomaterial-handling`) 내에 주차별(week02, week03...) 폴더를 생성하여 과제를 누적 관리**해야 함

### 4-1. 프로젝트 Git 저장소 초기화 (최초 1회만 수행)
내 컴퓨터의 학습용 최상위 폴더(예: `C:\biomaterial-handling`) 내에서 명령 프롬프트(또는 터미널)를 엽니다.
1. `git init` : 현재 최상위 폴더를 로컬 Git 저장소로 초기화함
2. (GitHub 웹사이트) `biomaterial-handling` 이름으로 새 Repository를 생성함
3. `git remote add origin https://github.com/[본인아이디]/biomaterial-handling.git` : 원격 저장소 주소를 연동함

> 💡 **[AI Prompt 대안] Cursor / Antigravity 등 활용 시**
> 터미널 명령이 어렵다면, 해당 폴더를 IDE에서 연 상태에서 **직접 AI에게 요청**할 수도 있음
> - *"현재 열린 폴더를 로컬 Git 저장소로 초기화해 주고, 방금 내가 만든 GitHub의 `[본인아이디]/biomaterial-handling` 주소로 origin 원격을 연결해 줘."*

### 4-2. 주차별(Week) 과제 폴더 생성 및 소스코드 저장
매주 새로운 실습이 주어질 때마다 최상위 폴더 내에 해당 주차의 폴더를 만들고 그 안에 코드를 저장함
1. 이번 주 과제 폴더 생성: `week02` (다음 주는 `week03`)
2. `week02` 폴더 내에 방금 작성한 파이썬 스크립트(`step1`, `step2`, `step3`), 원본 이미지(`apple_side_A.png`), 그리고 결과 창 캡처 이미지를 모두 복사/저장함

### 4-3. GitHub 원격 저장소로 과제 Push (매주 수행)
폴더 정리가 끝났다면 최상위 경로 터미널에서 아래 명령을 통해 추가된 주차별 코드만 깃허브에 올립니다.
1. `git add .` : 변경되거나 새롭게 추가된 주차별 폴더(week02 등) 전체를 스테이징(Staging)
2. `git commit -m "Add week02 shape analysis python scripts"` : 주차별 스냅샷 저장
3. `git push -u origin main` : (최초 시에만 `-u origin main` 사용, 이후엔 `git push`만 입력)
   - **주의**: 비밀번호 대신 **개인 액세스 토큰 (PAT, Personal Access Token)** 사용을 권장함

> 💡 **[AI Prompt 대안] 매주 간편한 커밋 & 푸시 요령**
> - *"새롭게 만든 `week02` 폴더의 코드 내용들을 모두 스테이징(add) 하고 'Add week02 shape analysis python scripts' 라는 메시지로 커밋해 줘. 그 후에 origin main으로 push까지 한 번에 완료해 줘."*

### 4-4. 메인 README.md 작성 (협업/평가용)
최상위 폴더에 있는 `README.md` 문서를 매주 업데이트하여 학위/과제 포트폴리오를 구성함
- **프로젝트 개요**: 본인의 이름 / 학번 / 생물자원가공공학 과제 레포지토리임을 명시
- **주차별 업데이트 내역**: 
  - `[Week 02]` 사과 윤곽선 인식 및 원형도/구형도 산출 스크립트 개발 완료
  - `[Week 03]` 수치 적분 기반 아보카도 체적/표면적 추정 실습 진행
  - `[Week 04]` 농산물 밀도/공극률 산출 및 3D 가상 패킹 구현
  - `[Week 05]` 사과즙 점도 트레이드오프 및 레이놀즈 유동 최적화 4단계 시뮬레이터 개발
  - `[Week 06]` 전분 풀 및 토마토 페이스트의 파워 로우 피팅 및 항복 응력 분석 시뮬레이션 완성
  - `[Week 07]` 점탄성 모델(Maxwell, KV, Burgers) 크리프·응력 이완 시뮬레이션 개발
  - `[Week 08]` 중간고사 (2~7주차 범위)
  - `[Week 09]` 헤르츠 접촉 응력 계산기, 3D 압력 분포 시각화, 인터랙티브 시뮬레이터 개발
  - `[Week 10]` Tracker 물리 분석 기반 과일 낙하 반발 계수 측정 및 충격 손상 예측 스크립트 구현
  - `[Week 11]` 색 공간 변환 기반 숙도 분할 모델 구현
  - `[Week 12]` NIR 분광 스펙트럼 전처리 및 당도 예측 모델링 실습
  - `[Week 13]` 음향 FFT 기반 공명 주파수 검출 및 경도 지수 산출 시뮬레이터 개발
  - `[Week 14]` 1D 구형 냉각 PDE 시뮬레이션 및 디지털 트윈 기반 예측 제어 조망

---
*과제 제출 완료 후, 본인의 GitHub 저장소 URL(예: `https://github.com/아이디/biomaterial-handling/tree/main/ko/week02`)을 조교/교수에게 제출하여 최종 성적에 반영함*


## 📝 변경 이력 (Changelog)

- **2026-05-03 00:56:51** [[Dongsoo Ryu](mailto:ryudongsoo@gmail.com)] feat(week10): add english translation for Tracker manual and update python script
- **2026-05-03 00:54:13** [[Dongsoo Ryu](mailto:ryudongsoo@gmail.com)] feat(week10): add Tracker video analysis manual and interactive impact simulation
- **2026-05-02 15:51:55** [[Dongsoo Ryu](mailto:ryudongsoo@gmail.com)] Update week 10 materials: impact characteristics and damage prediction
- **2026-04-28 17:04:21** [[ryu-dongsoo](mailto:ryudongsoo@jbnu.ac.kr)] 최근 변경사항 업데이트 (week7)
- **2026-04-28 16:58:13** [[unknown](mailto:41464@staff.jbnu.ac.kr)] Apply writing-style guidelines to README and QUIZ_BANK