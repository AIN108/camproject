# CamProject 한국어 사용 매뉴얼

## 1. 개요

CamProject는 Python과 OpenCV를 사용해 웹캠 영상을 읽고, Haar Cascade 얼굴 검출 결과에 따라 동영상 또는 카메라 화면을 전환하는 프로젝트입니다.

Windows용 단일/듀얼 카메라 코드와 Raspberry Pi용 코드가 함께 있습니다.

현재 Windows 코드도 저장소 상대경로와 OpenCV 내장 Haar Cascade를 사용하므로, 과거처럼 `C:\opencv` 또는 `C:\onecam` 폴더를 따로 만들 필요가 없습니다.

## 2. 프로젝트 구성

```text
camproject/
├── README.md
├── MANUAL_KO.md
├── ASSET_NOTICE.md
├── LICENSE
├── requirements.txt
├── onecam.py
├── twocam(turn_videotocctv).py
├── black.mp4
├── seoultech.mp4
└── raspberry/
    ├── README_RASPBERRY.md
    ├── camera_sources.py
    ├── onecam_raspberry.py
    └── twocam_raspberry.py
```

## 3. Windows 권장 환경

- Windows 10/11
- Python 3.x
- OpenCV 4.x
- `onecam.py`: 웹캠 1대
- `twocam(turn_videotocctv).py`: 웹캠 2대
- 듀얼 출력 전체 확인 시 모니터 2대 권장

`onecam.py`는 화면 크기 확인에 Windows `ctypes.windll.user32`를 사용하고, 듀얼 카메라 코드는 DirectShow(`cv2.CAP_DSHOW`)를 사용합니다.

## 4. 설치

```bash
git clone https://github.com/AIN108/camproject.git
cd camproject
python -m venv .venv
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

OpenCV 확인:

```bash
python -c "import cv2; print(cv2.__version__)"
```

## 5. 미디어 파일

Windows 기본 코드에서는 루트의 다음 파일을 자동으로 찾습니다.

```text
black.mp4
seoultech.mp4
```

`black.mp4`는 화면 전환용 검은 화면 테스트 영상으로 사용했던 것으로 추정됩니다.

`seoultech.mp4`는 서울과학기술대학교 재학 당시 프로젝트에서 사용했던 학교 홍보영상으로 추정되지만, 현재 저장소에는 원본 URL과 재배포 조건을 입증할 기록이 없습니다.

따라서 코드의 MIT License가 `seoultech.mp4`에 적용되는 것으로 간주하지 않습니다. 자세한 내용은 `ASSET_NOTICE.md`를 확인하세요.

## 6. `onecam.py`

### 동작

```text
웹캠
  ↓
회색조 변환
  ↓
얼굴 검출
  ↓
얼굴 있음 ─→ seoultech.mp4
얼굴 없음 ─→ black.mp4
```

OpenCV 설치 경로에서 Haar Cascade를 자동으로 찾습니다.

```python
Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
```

동영상 역시 `onecam.py`가 있는 저장소 루트를 기준으로 찾기 때문에 별도의 절대경로 수정이 필요하지 않습니다.

### 실행

```bash
python onecam.py
```

### 종료

```text
q 또는 Esc
```

### 얼굴 검출 주기

현재 얼굴 검출은 약 2초 간격으로 수행합니다. 매 프레임 얼굴 검출을 수행하지 않아 연산 부하를 줄이는 구조입니다.

### 영상 재생 위치

얼굴이 사라져 홍보영상 재생이 중단되면 현재 프레임 위치를 저장하고, 얼굴이 다시 감지되면 해당 위치에서 재생을 이어가도록 구성되어 있습니다.

## 7. 웹캠이 열리지 않을 때

기본 단일 카메라는 카메라 번호 `0`을 사용합니다.

다른 카메라를 사용해야 한다면 `onecam.py`의 다음 값을 변경할 수 있습니다.

```python
cv2.VideoCapture(0)
```

예:

```python
cv2.VideoCapture(1)
```

카메라 번호는 PC와 USB 연결 순서에 따라 달라질 수 있습니다.

## 8. `twocam(turn_videotocctv).py`

이 프로그램은 두 개의 카메라를 사용합니다.

```text
얼굴 감지용 카메라
        ↓
   얼굴 검출
   ↙       ↘
있음       없음
 ↓           ↓
seoultech   CCTV 카메라
      \      /
       출력 영상
          ↓
      좌/우 분할
       ↓     ↓
 Monitor1  Monitor2
```

### 기본 실행

```bash
python "twocam(turn_videotocctv).py"
```

기본값:

```text
얼굴 감지 카메라: 1
CCTV 카메라: 0
모니터 폭: 1080
모니터 높이: 1920
얼굴 미검출 후 유지 시간: 1초
```

## 9. 듀얼 카메라 옵션

현재 버전은 소스 파일을 수정하지 않고 실행 옵션으로 설정을 바꿀 수 있습니다.

```bash
python "twocam(turn_videotocctv).py" \
  --detect-camera 1 \
  --cctv-camera 0 \
  --monitor-width 1080 \
  --monitor-height 1920 \
  --hold-seconds 1.0
```

### 일반적인 가로형 1920×1080 모니터

```bash
python "twocam(turn_videotocctv).py" --monitor-width 1920 --monitor-height 1080
```

### 카메라 번호를 반대로 바꾸기

```bash
python "twocam(turn_videotocctv).py" --detect-camera 0 --cctv-camera 1
```

## 10. 얼굴 검출 영역

듀얼 카메라 코드는 전체 영상이 아니라 중앙 영역을 잘라 얼굴 검출에 사용합니다.

기본 영역은 약 `480 × 320`입니다.

이는 특정 위치에 접근한 사람을 감지하는 구조를 만들면서 연산량을 줄이기 위한 방식입니다.

## 11. 얼굴 검출 민감도

현재 주요 값:

```python
scaleFactor=1.2
minNeighbors=2
```

`minNeighbors`를 낮추면 더 많은 후보를 얼굴로 판단할 가능성이 있지만 오검출도 늘어날 수 있습니다.

결과는 조명, 얼굴 크기, 카메라 화질, 각도에 영향을 받습니다.

## 12. 화면 전환 지연

얼굴이 한 프레임에서 사라졌다고 바로 CCTV로 돌아가지 않습니다.

기본 `--hold-seconds 1.0`으로 마지막 얼굴 검출 후 1초 동안 홍보영상을 유지합니다.

필요하면 값을 늘릴 수 있습니다.

```bash
python "twocam(turn_videotocctv).py" --hold-seconds 2.5
```

## 13. 듀얼 모니터 출력

프로그램은 `Monitor1`, `Monitor2` 두 창을 만들고 하나의 넓은 영상을 좌우로 나눠 각각 표시합니다.

```text
원본 출력 영상
      ↓
두 모니터 너비만큼 리사이즈
      ↓
┌──────────────┬──────────────┐
│    LEFT      │    RIGHT     │
│  Monitor1    │  Monitor2    │
└──────────────┴──────────────┘
```

실제 Windows 디스플레이 설정에서 두 모니터의 배치 방향과 해상도를 확인해야 합니다.

## 14. Raspberry Pi

Raspberry Pi 버전은 `raspberry/` 폴더에 있습니다.

### USB 웹캠

```bash
sudo apt update
sudo apt install -y python3-opencv
python3 raspberry/onecam_raspberry.py --camera usb
```

### Raspberry Pi Camera Module

```bash
sudo apt update
sudo apt install -y python3-opencv python3-picamera2
python3 raspberry/onecam_raspberry.py --camera picamera
```

자세한 카메라 설정은 `raspberry/README_RASPBERRY.md`를 참고하세요.

## 15. 문제 해결

### `영상 파일을 열 수 없습니다`

루트에 다음 파일이 있는지 확인합니다.

```text
black.mp4
seoultech.mp4
```

### `기본 웹캠(0)을 열 수 없습니다`

다른 프로그램이 카메라를 사용 중인지 확인하고 카메라 번호를 점검합니다.

### 듀얼 카메라 중 한 대가 열리지 않음

다음처럼 번호를 바꿔 실행합니다.

```bash
python "twocam(turn_videotocctv).py" --detect-camera 0 --cctv-camera 2
```

### 화면 배치가 맞지 않음

`--monitor-width`, `--monitor-height` 값을 실제 디스플레이 해상도에 맞춥니다.

### Raspberry Pi에서 OpenCV 창이 뜨지 않음

SSH만 연결된 headless 환경이라면 GUI 창을 표시할 디스플레이 세션이 없을 수 있습니다. 데스크톱 세션 또는 적절한 디스플레이 전달 환경에서 실행해야 합니다.

## 16. 개인정보와 촬영

웹캠 사용 사실을 촬영 대상자에게 알리고, 영상 저장·전송 기능을 추가하는 경우 개인정보 및 초상권 관련 기준을 별도로 확인해야 합니다.

현재 기본 코드에는 웹캠 영상을 파일로 녹화하는 기능이 없습니다.

## 17. 라이선스

AIN108이 작성한 소스 코드는 MIT License로 공개합니다.

제3자 권리가 적용될 수 있는 영상 자산은 MIT License 대상에 포함되지 않습니다. `ASSET_NOTICE.md`를 참고하세요.
