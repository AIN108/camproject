# CamProject 한국어 사용 매뉴얼

## 1. 프로젝트 개요

CamProject는 Python과 OpenCV를 이용하여 웹캠의 실시간 영상을 입력받고, 얼굴 검출 결과에 따라 카메라 영상과 동영상 파일을 전환해 출력하는 영상처리 프로젝트입니다.

주요 구성 요소는 다음과 같습니다.

- Python에서 웹캠 입력 받기
- OpenCV `VideoCapture` 사용
- 프레임 단위 영상 처리
- Haar Cascade 얼굴 검출
- 얼굴 검출 결과에 따른 상태 전환
- 동영상 파일 재생
- 여러 카메라 동시 사용
- 듀얼 모니터 출력
- 영상 자원 해제

현재 코드는 Windows 환경과 작성 당시의 로컬 경로를 기준으로 작성되어 있으므로, 처음 실행하는 PC에서는 경로와 카메라 번호를 확인해야 합니다.

---

## 2. 프로젝트 구성

```text
camproject/
├── README.md
├── MANUAL_KO.md
├── requirements.txt
├── onecam.py
├── twocam(turn_videotocctv).py
├── black.mp4
└── seoultech.mp4
```

| 파일 | 역할 |
|---|---|
| `onecam.py` | 웹캠 1대로 얼굴을 검출하고 두 동영상을 전환하여 출력 |
| `twocam(turn_videotocctv).py` | 웹캠 2대와 2개 출력 창을 이용한 확장 프로그램 |
| `black.mp4` | `onecam.py`의 기본 상태 출력 영상 |
| `seoultech.mp4` | 얼굴 검출 후 재생되는 예제 영상 |
| `README.md` | 프로젝트 요약 및 빠른 시작 안내 |
| `MANUAL_KO.md` | 상세 설치 및 실행 설명서 |

---

## 3. 권장 실행 환경

- Windows 10 또는 Windows 11
- Python 3.x
- OpenCV (`opencv-python`)
- `onecam.py` 실행 시 웹캠 1대
- `twocam(turn_videotocctv).py` 실행 시 웹캠 2대 권장
- 듀얼 화면 기능 확인 시 모니터 2대 권장

`onecam.py`는 Windows 화면 해상도를 얻기 위해 `ctypes.windll.user32`를 사용합니다.

`twocam(turn_videotocctv).py`는 Windows용 DirectShow 백엔드인 `cv2.CAP_DSHOW`를 사용합니다.

따라서 현재 코드를 수정하지 않고 실행할 때는 Windows 환경이 가장 적합합니다.

---

## 4. 프로젝트 다운로드

### Git 사용

PowerShell 또는 명령 프롬프트에서 다음을 실행합니다.

```bash
git clone https://github.com/AIN108/camproject.git
cd camproject
```

이후 저장소가 갱신되었을 때는:

```bash
git pull
```

을 사용합니다.

### ZIP 사용

GitHub 저장소 페이지에서:

1. `Code` 선택
2. `Download ZIP` 선택
3. 다운로드한 ZIP 압축 해제

---

## 5. Python 설치 확인

다음 명령 중 하나를 실행합니다.

```bash
python --version
```

또는:

```bash
py --version
```

정상 설치된 경우 `Python 3.x.x` 형태의 버전이 표시됩니다.

---

## 6. OpenCV 설치

프로젝트 폴더에서 다음 명령을 실행합니다.

```bash
pip install -r requirements.txt
```

직접 설치하려면:

```bash
pip install opencv-python
```

설치 확인:

```bash
python -c "import cv2; print(cv2.__version__)"
```

OpenCV 버전이 출력되면 정상입니다.

---

## 7. 실행 전 반드시 확인할 경로

현재 소스에는 다음 절대경로가 직접 지정되어 있습니다.

```text
C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml
C:\onecam\black.mp4
C:\onecam\seoultech.mp4
```

따라서 사용하는 PC의 파일 위치가 다르면 소스 코드의 경로를 수정해야 합니다.

### 7.1 Haar Cascade 파일

얼굴 검출에 필요한 파일:

```text
haarcascade_frontalface_default.xml
```

소스의 다음 부분을 실제 파일 위치로 변경합니다.

```python
face_cascade = cv2.CascadeClassifier(
    r'C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml'
)
```

### 7.2 동영상 경로

현재 코드는 다음 위치를 사용합니다.

```text
C:\onecam\black.mp4
C:\onecam\seoultech.mp4
```

가장 단순한 방법은 `C:\onecam` 폴더를 만들고 두 MP4 파일을 복사하는 것입니다.

또는 코드의 경로를 현재 저장소 위치에 맞게 수정할 수 있습니다.

---

## 8. `onecam.py` 동작

`onecam.py`는 웹캠 1대를 얼굴 검출용으로 사용합니다.

기본 흐름:

```text
웹캠 입력
   ↓
얼굴 검출
   ↓
┌────────────────┐
│ 얼굴이 검출되는가 │
└───────┬────────┘
        │
   YES  │  NO
    ↓   │   ↓
seoultech.mp4   black.mp4
```

프로그램이 시작되면 `black.mp4`를 재생합니다.

웹캠에서 얼굴이 검출되면 `seoultech.mp4`로 전환됩니다.

얼굴이 다시 사라지면 `black.mp4`로 돌아갑니다.

---

## 9. `onecam.py` 실행

```bash
python onecam.py
```

또는:

```bash
py onecam.py
```

기본 카메라는 다음 설정을 사용합니다.

```python
cap = cv2.VideoCapture(0)
```

`0`은 일반적으로 첫 번째 카메라입니다.

---

## 10. 카메라 번호 변경

카메라가 열리지 않거나 잘못된 카메라가 선택되면 다음 숫자를 바꾸어 확인합니다.

```python
cv2.VideoCapture(0)
cv2.VideoCapture(1)
cv2.VideoCapture(2)
```

일반적으로:

```text
0 = 첫 번째 카메라
1 = 두 번째 카메라
2 = 세 번째 카메라
```

형태로 사용하지만 실제 장치 번호는 PC와 USB 연결 순서에 따라 달라질 수 있습니다.

---

## 11. `onecam.py`의 얼굴 검출

카메라 프레임을 흑백으로 변환합니다.

```python
gray = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2GRAY)
```

그 후 Haar Cascade로 얼굴을 찾습니다.

```python
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=4
)
```

현재 프로그램은 얼굴 검출을 약 2초 간격으로 수행합니다.

```python
Face_detection_interval = 2
```

이는 매 프레임마다 얼굴 검출을 수행하는 것보다 연산량을 줄이기 위한 방식입니다.

---

## 12. 영상 재생 위치 유지

`onecam.py`는 얼굴이 사라져 `seoultech.mp4` 재생이 중단되었을 때 현재 재생 위치를 저장합니다.

```python
video2_position = video2.get(cv2.CAP_PROP_POS_FRAMES)
```

동작 흐름:

```text
얼굴 등장
→ 영상 재생
→ 얼굴 사라짐
→ 영상 정지 및 위치 저장
→ 다시 얼굴 등장
→ 이전 위치부터 이어서 재생
```

---

## 13. `onecam.py` 종료

현재 `onecam.py`에는 `q`와 같은 특정 종료키가 지정되어 있지 않습니다.

OpenCV 창이 활성화된 상태에서 키 입력이 감지되면 루프를 종료합니다.

종료 시 다음 자원을 해제합니다.

```python
video1.release()
video2.release()
cap.release()
cv2.destroyAllWindows()
```

카메라 프로그램에서는 자원 해제가 중요합니다. 정상적으로 해제하지 않으면 이후 다른 프로그램에서 카메라를 사용하지 못하는 경우가 있습니다.

---

## 14. `twocam(turn_videotocctv).py` 동작

현재 실행부에서는 두 개의 카메라를 사용합니다.

```python
webcam1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
webcam2 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

역할:

| 입력 | 역할 |
|---|---|
| `webcam1` | 얼굴 검출용 카메라 |
| `webcam2` | 기본 CCTV 화면용 카메라 |
| `seoultech.mp4` | 얼굴 검출 시 출력할 영상 |

기본 흐름:

```text
Webcam 1
   ↓
얼굴 검출
   ↓
┌────────────────┐
│ 얼굴이 검출되는가 │
└───────┬────────┘
        │
   YES  │  NO
    ↓   │   ↓
seoultech.mp4   Webcam 2
        ↓
    화면 분할
    ↓       ↓
Monitor1  Monitor2
```

---

## 15. 듀얼 카메라 프로그램 실행

파일 이름에 괄호가 포함되어 있으므로 따옴표로 감싸는 것이 안전합니다.

```bash
python "twocam(turn_videotocctv).py"
```

프로그램 종료는 `q` 키입니다.

---

## 16. 얼굴 검출 영역

`twocam` 프로그램은 전체 프레임이 아니라 화면 중앙 영역을 잘라 얼굴 검출에 사용합니다.

현재 호출:

```python
center_rectangle = get_center_rectangle(
    frame1,
    width=480,
    height=320
)
```

즉 중앙의 약 `480 × 320` 영역만 검사합니다.

이 방식은 검사 영역을 줄이고 연산량을 낮추며 특정 위치에 접근한 사람을 감지하는 구조를 만드는 데 사용할 수 있습니다.

---

## 17. 얼굴 검출 민감도

현재 설정:

```python
faces = face_cascade.detectMultiScale(
    frame_gray,
    scaleFactor=1.2,
    minNeighbors=2
)
```

일반적으로 `minNeighbors` 값을 낮추면 더 많은 후보를 얼굴로 판단할 수 있으나 오검출 가능성도 커집니다.

실제 결과는 카메라 화질, 조명, 얼굴 크기와 각도에 따라 달라집니다.

---

## 18. 얼굴이 사라진 후 화면 전환

얼굴이 한 프레임에서 사라졌다고 즉시 상태를 변경하지 않습니다.

현재 코드에서는 마지막 얼굴 검출 후 약 1초가 지나면 기본 CCTV 화면으로 돌아갑니다.

```python
elif current_time - last_detected_time > 1:
    if video_playing:
        video_playing = False
```

이 지연은 순간적인 미검출 때문에 화면이 빠르게 깜빡이는 현상을 줄이는 역할을 합니다.

---

## 19. 듀얼 모니터 출력

프로그램은 다음 두 개의 OpenCV 창을 만듭니다.

```text
Monitor1
Monitor2
```

현재 모니터 해상도 값은 다음과 같습니다.

```python
MONITOR_WIDTH = 1080
MONITOR_HEIGHT = 1920
```

이는 세로형 또는 특정 설치 환경을 기준으로 작성된 값입니다.

일반적인 1920×1080 가로형 모니터를 사용한다면 예를 들어 다음과 같이 바꿀 수 있습니다.

```python
MONITOR_WIDTH = 1920
MONITOR_HEIGHT = 1080
```

Windows의 디스플레이 배치와 실제 모니터 해상도를 함께 확인해야 합니다.

---

## 20. 영상 분할 원리

`split_frame()` 함수는 출력할 영상을 두 모니터 너비만큼 리사이즈합니다.

```python
resized_frame = cv2.resize(
    frame,
    (monitor_width * 2, monitor_height)
)
```

그 다음 좌우 절반으로 나눕니다.

```text
┌────────────────────────────┐
│       하나의 넓은 영상       │
└────────────────────────────┘
              ↓
┌──────────────┬──────────────┐
│     LEFT     │    RIGHT     │
│  Monitor 1   │  Monitor 2   │
└──────────────┴──────────────┘
```

왼쪽 절반은 `Monitor1`, 오른쪽 절반은 `Monitor2`에 표시됩니다.

---

## 21. 주요 OpenCV 함수

### `cv2.VideoCapture()`

카메라 또는 동영상 파일을 엽니다.

```python
cap = cv2.VideoCapture(0)
```

또는:

```python
video = cv2.VideoCapture("video.mp4")
```

### `read()`

한 프레임을 읽습니다.

```python
ret, frame = cap.read()
```

`ret`은 프레임을 정상적으로 읽었는지 나타내고 `frame`은 실제 영상 데이터입니다.

### `cv2.cvtColor()`

영상의 색 공간을 변경합니다.

```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

### `CascadeClassifier`

Haar Cascade 분류기를 로드합니다.

```python
face_cascade = cv2.CascadeClassifier(path)
```

### `detectMultiScale()`

얼굴 후보를 찾습니다.

```python
faces = face_cascade.detectMultiScale(gray)
```

### `cv2.resize()`

프레임 크기를 변경합니다.

```python
frame = cv2.resize(frame, (1920, 1080))
```

### `cv2.imshow()`

OpenCV 창에 프레임을 표시합니다.

```python
cv2.imshow("Screen", frame)
```

### `cv2.waitKey()`

키 입력을 확인합니다.

```python
key = cv2.waitKey(1)
```

### `release()`

카메라 또는 비디오 파일 자원을 해제합니다.

```python
cap.release()
```

---

## 22. 오류 해결

### 카메라를 열 수 없다는 메시지가 나오는 경우

확인 항목:

- 웹캠 연결 상태
- 다른 프로그램이 웹캠을 사용 중인지 여부
- Windows 카메라 권한
- 카메라 인덱스 `0`, `1`, `2`

### `twocam`에서 카메라2를 열 수 없는 경우

현재 프로그램은 두 카메라 사용을 전제로 합니다.

웹캠이 한 대뿐이라면 현재 코드 그대로는 전체 기능을 사용할 수 없습니다.

### 동영상이 열리지 않는 경우

다음 경로가 실제 파일 위치와 일치하는지 확인합니다.

```text
C:\onecam\black.mp4
C:\onecam\seoultech.mp4
```

### 얼굴을 전혀 찾지 못하는 경우

Haar Cascade XML 파일의 위치와 로딩 여부를 확인합니다.

```text
haarcascade_frontalface_default.xml
```

경로가 틀리면 얼굴 분류기가 정상적으로 초기화되지 않습니다.

### 화면 크기나 위치가 이상한 경우

다음을 확인합니다.

```python
MONITOR_WIDTH
MONITOR_HEIGHT
```

그리고 Windows:

```text
설정 → 시스템 → 디스플레이
```

에서 모니터의 실제 배치 순서를 확인합니다.

---

## 23. 현재 버전의 제한사항

현재 CamProject는 완성형 CCTV 제품이 아니라 개발 예제 소스 코드입니다.

현재 제약:

- Windows 절대경로 사용
- Haar Cascade XML 경로 고정
- 카메라 인덱스 직접 지정
- 모니터 해상도 직접 지정
- 자동 장치 검색 기능 없음
- 설정용 GUI 없음
- Haar Cascade 방식의 검출 정확도 한계

다른 PC에서 실행할 때는 경로, 카메라 번호와 디스플레이 구성을 확인해야 합니다.

---

## 24. README와 실제 코드의 관계

이 매뉴얼과 현재 README는 GitHub의 실제 실행 코드를 기준으로 작성되어 있습니다.

현재 실제 구현의 핵심 기능은:

```text
웹캠 입력
얼굴 검출
얼굴 검출에 따른 영상 전환
2대 카메라 사용
듀얼 화면 영상 분할
전체화면 출력
```

입니다.

스크린샷 저장, 녹화, 타임스탬프, 위치 오버레이 등은 현재 실행 코드에 구현되어 있지 않습니다.

---

## 25. 개인정보 및 촬영 주의

웹캠을 사용하는 경우 촬영 대상자에게 카메라 사용 사실을 알리는 것이 좋습니다.

특히 실제 촬영 데이터를 저장하거나 외부에 공개하는 기능을 추가할 경우 다음을 확인해야 합니다.

- 촬영 대상자 동의
- 개인정보 및 초상권 관련 규정
- 영상의 보관 기간
- 외부 전송 여부
- 불필요한 촬영 데이터 최소화

현재 저장소의 실행 코드에는 웹캠 영상을 파일로 녹화하거나 저장하는 기능은 구현되어 있지 않습니다.

---

## 26. 라이선스 주의

현재 저장소에는 별도의 `LICENSE` 파일이 없습니다.

다음 용도로 사용하려는 경우에는 저장소 소유자에게 이용 조건을 확인하는 것이 좋습니다.

- 외부 재배포
- 수정본 공개
- 다른 프로젝트에 포함
- 상업적 활용

---

## 27. 처리 흐름 요약

```text
카메라 열기
   ↓
프레임 읽기
   ↓
영상 전처리
   ↓
얼굴 검출
   ↓
상태 판단
   ↓
출력 영상 선택
   ↓
영상 출력
   ↓
입력 반복
   ↓
자원 해제
```

`onecam.py`는 기본적인 카메라 입력과 얼굴 검출, 영상 전환 흐름을 담당합니다.

`twocam(turn_videotocctv).py`는 다중 카메라, 영상 상태 전환, 화면 분할과 다중 디스플레이 출력을 담당합니다.
