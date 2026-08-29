# CamProject Raspberry Pi 사용 안내

CamProject의 Raspberry Pi 버전입니다.

기본 버전은 **카메라 1대만 사용**합니다. 다음 두 방식 중 하나를 선택할 수 있습니다.

- 일반 USB 웹캠 1대
- Raspberry Pi Camera Module 1대 (Picamera2)

기존 Windows용 `onecam.py`와 `twocam(turn_videotocctv).py`는 변경하지 않습니다.

## 파일 구성

```text
raspberry/
├── README_RASPBERRY.md
├── camera_sources.py
├── onecam_raspberry.py
└── twocam_raspberry.py
```

- `camera_sources.py`: USB 웹캠과 Pi Camera 입력을 공통 인터페이스로 처리합니다.
- `onecam_raspberry.py`: 카메라 1대로 얼굴을 감지하고 `black.mp4`와 `seoultech.mp4`를 전환합니다. 기본 권장 버전입니다.
- `twocam_raspberry.py`: 필요할 때만 사용하는 2카메라/CCTV 전환 버전입니다.

## 동작 구조

```text
USB 웹캠 또는 Pi Camera 1대
          ↓
      얼굴 검출
          ↓
   ┌──────┴──────┐
 얼굴 없음      얼굴 있음
   ↓              ↓
black.mp4     seoultech.mp4
```

카메라 영상은 얼굴 검출에 사용하고, 화면에는 동영상이 표시됩니다.

`seoultech.mp4`는 얼굴이 사라질 때 현재 재생 위치를 기억하고, 다시 얼굴이 나타나면 그 위치에서 재생을 이어갑니다.

## 권장 환경

- Raspberry Pi 4 또는 Raspberry Pi 5 권장
- Raspberry Pi OS Desktop 권장
- Python 3
- OpenCV
- USB UVC 웹캠 또는 Raspberry Pi Camera Module

OpenCV의 `imshow()`로 화면을 표시하므로 Raspberry Pi OS Lite만 사용하는 헤드리스 환경에서는 별도 디스플레이 구성이 필요합니다.

## 1. 저장소 받기

```bash
git clone https://github.com/AIN108/camproject.git
cd camproject
```

## 2. OpenCV 설치

Raspberry Pi OS에서는 시스템 패키지로 설치하는 방법을 권장합니다.

```bash
sudo apt update
sudo apt install -y python3-opencv
```

설치 확인:

```bash
python3 -c "import cv2; print(cv2.__version__)"
```

## 3. USB 웹캠 1대 사용

USB 웹캠을 연결한 뒤 장치가 잡혔는지 확인합니다.

```bash
ls /dev/video*
```

보통 첫 번째 USB 카메라는 `/dev/video0`이며 OpenCV에서는 인덱스 `0`으로 사용합니다.

실행:

```bash
python3 raspberry/onecam_raspberry.py --camera usb
```

카메라가 다른 번호라면:

```bash
python3 raspberry/onecam_raspberry.py --camera usb --camera-index 1
```

기본 입력 설정은 640×480, 30 FPS입니다.

```bash
python3 raspberry/onecam_raspberry.py --camera usb --width 1280 --height 720 --fps 30
```

## 4. Raspberry Pi Camera Module 사용

현재 Raspberry Pi OS에서는 기존 `Picamera`가 아니라 **Picamera2**를 사용합니다.

최근 Raspberry Pi OS 이미지에는 Picamera2가 기본 포함되어 있을 수 있습니다. 없는 경우:

```bash
sudo apt install -y python3-picamera2
```

카메라 확인:

```bash
rpicam-hello --list-cameras
```

카메라 미리보기 확인:

```bash
rpicam-hello -t 5000
```

CamProject 실행:

```bash
python3 raspberry/onecam_raspberry.py --camera picamera
```

카메라 인덱스를 지정해야 하는 경우:

```bash
python3 raspberry/onecam_raspberry.py --camera picamera --camera-index 0
```

## Python 가상환경을 사용하는 경우

Picamera2는 Raspberry Pi OS의 `apt` 패키지와 libcamera 구성요소에 의존합니다.

가상환경이 필요한 경우 시스템 패키지를 사용할 수 있게 생성하는 것이 안전합니다.

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
```

## 종료

다음 중 하나로 프로그램을 종료합니다.

- `q`
- `Esc`

## 주요 옵션

```text
--camera usb|picamera
--camera-index N
--width N
--height N
--fps N
--detect-interval SECONDS
--idle-video PATH
--active-video PATH
--windowed
```

예시:

```bash
python3 raspberry/onecam_raspberry.py \
  --camera usb \
  --camera-index 0 \
  --width 640 \
  --height 480 \
  --fps 30
```

## 영상 파일

기본적으로 저장소 루트의 다음 파일을 자동으로 사용합니다.

```text
black.mp4
seoultech.mp4
```

따라서 기존 Windows판처럼 `C:\onecam\...` 경로를 만들 필요가 없습니다.

다른 영상을 사용하려면:

```bash
python3 raspberry/onecam_raspberry.py \
  --camera usb \
  --idle-video /home/pi/video/idle.mp4 \
  --active-video /home/pi/video/active.mp4
```

## Haar Cascade

라즈베리판은 Haar XML의 절대경로를 직접 지정하지 않습니다.

```python
cv2.data.haarcascades
```

에서 OpenCV가 제공하는 `haarcascade_frontalface_default.xml`을 자동으로 사용합니다.

## USB 웹캠 오류

카메라가 열리지 않는 경우:

```bash
ls -l /dev/video*
```

으로 장치를 확인한 뒤 `--camera-index` 값을 바꿔 실행합니다.

예:

```bash
python3 raspberry/onecam_raspberry.py --camera usb --camera-index 1
```

다른 프로그램이 카메라를 사용하고 있으면 먼저 종료해야 합니다.

## Pi Camera 오류

먼저 다음 명령으로 카메라 자체가 Raspberry Pi OS에서 인식되는지 확인합니다.

```bash
rpicam-hello --list-cameras
```

목록에 카메라가 없다면 Python 코드보다 케이블 연결, 카메라 커넥터 방향, Raspberry Pi OS 및 카메라 인식 상태를 먼저 확인해야 합니다.

## 2카메라 버전

`twocam_raspberry.py`는 선택사항입니다. 얼굴 검출용 카메라와 평상시 CCTV 화면용 카메라를 별도로 사용할 때만 필요합니다.

USB 웹캠 2대 예시:

```bash
python3 raspberry/twocam_raspberry.py \
  --detector-source usb --detector-index 0 \
  --cctv-source usb --cctv-index 1
```

Pi Camera + USB 웹캠 예시:

```bash
python3 raspberry/twocam_raspberry.py \
  --detector-source picamera --detector-index 0 \
  --cctv-source usb --cctv-index 0
```

카메라 1대만 사용할 경우에는 이 파일을 사용할 필요가 없습니다.
