# CamProject

Python과 OpenCV를 이용해 **웹캠의 얼굴 감지 결과에 따라 영상 또는 카메라 화면을 전환하는 영상처리 프로젝트**입니다.

Windows용 초기 구현과 Raspberry Pi용 구현을 함께 보존하면서, 현재 기본 실행 코드는 특정 PC의 절대경로 없이 저장소 자체에서 실행할 수 있도록 정리했습니다.

## 주요 구성

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

## 처리 구조

```text
카메라 입력
    ↓
OpenCV Haar Cascade 얼굴 검출
    ↓
얼굴 감지 여부 판단
    ↓
홍보영상 / 검은 화면 / CCTV 카메라 전환
    ↓
OpenCV 전체화면 출력
```

## Windows: `onecam.py`

웹캠 한 대에서 얼굴을 감지하고, 얼굴 감지 여부에 따라 `black.mp4`와 `seoultech.mp4`를 전환합니다.

현재 코드는 다음과 같이 정리되어 있습니다.

- OpenCV 패키지에 포함된 Haar Cascade 자동 사용
- `black.mp4`, `seoultech.mp4`를 저장소 기준 상대경로로 자동 탐색
- 특정 PC의 `C:\\opencv`, `C:\\onecam` 경로 불필요
- 웹캠 프레임 읽기 실패 및 영상 파일 누락 처리
- `q` 또는 `Esc`로 종료

실행:

```bash
pip install -r requirements.txt
python onecam.py
```

## Windows: 듀얼 카메라 / 듀얼 화면

`twocam(turn_videotocctv).py`는 카메라 두 대를 사용합니다.

- 얼굴 감지용 카메라
- 기본 CCTV 화면용 카메라
- 얼굴 감지 시 `seoultech.mp4` 표시
- 얼굴이 사라지면 CCTV 화면으로 복귀
- 하나의 출력 프레임을 좌우로 나누어 두 개의 OpenCV 창에 표시

기본 실행:

```bash
python "twocam(turn_videotocctv).py"
```

카메라 번호와 모니터 크기는 실행 시 바꿀 수 있습니다.

```bash
python "twocam(turn_videotocctv).py" \
  --detect-camera 1 \
  --cctv-camera 0 \
  --monitor-width 1080 \
  --monitor-height 1920 \
  --hold-seconds 1.0
```

종료는 `q` 또는 `Esc`입니다.

## Raspberry Pi

`raspberry/` 폴더에는 Raspberry Pi용으로 경로·카메라 입력을 분리한 코드가 있습니다.

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

자세한 내용은 [`raspberry/README_RASPBERRY.md`](./raspberry/README_RASPBERRY.md)를 참고하세요.

## 미디어 자산

이 프로젝트에는 실행 재현을 위해 `black.mp4`와 `seoultech.mp4`가 남아 있습니다.

- `black.mp4`: 화면 전환용 검은 화면 테스트 영상으로 사용했던 것으로 추정
- `seoultech.mp4`: 서울과학기술대학교 재학 당시 프로젝트에서 사용한 학교 홍보영상으로 추정

후자의 원본 URL과 재배포 조건은 현재 저장소 기록만으로 확인되지 않습니다. 따라서 소스 코드의 MIT License가 해당 영상에 적용되는 것으로 간주하지 않습니다.

자세한 내용은 [`ASSET_NOTICE.md`](./ASSET_NOTICE.md)를 참고하세요.

## 개인정보 및 촬영

웹캠을 실제 환경에서 사용할 때는 촬영 대상자에게 카메라 사용 사실을 알리고, 영상 저장·전송 기능을 추가하는 경우 개인정보와 초상권 관련 기준을 별도로 확인해야 합니다.

현재 기본 실행 코드는 웹캠 영상을 파일로 녹화하는 기능을 포함하지 않습니다.

## 문서

- [`MANUAL_KO.md`](./MANUAL_KO.md): 기존 Windows 사용 매뉴얼
- [`raspberry/README_RASPBERRY.md`](./raspberry/README_RASPBERRY.md): Raspberry Pi 사용 안내
- [`ASSET_NOTICE.md`](./ASSET_NOTICE.md): 포함된 영상 자산의 출처/권리 구분

## License

AIN108이 작성한 소스 코드는 MIT License로 공개합니다. 제3자 미디어 자산은 별도 권리가 적용될 수 있습니다.
