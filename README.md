# CamProject

Python과 OpenCV를 이용해 **웹캠의 얼굴 감지 결과에 따라 영상 또는 카메라 화면을 전환하고 출력하는 영상처리 실습 프로젝트**입니다.

대학 수업이나 OpenCV 입문 실습에서 카메라 입력, 프레임 처리, Haar Cascade 얼굴 검출, 영상 전환, 다중 카메라 및 듀얼 모니터 출력을 살펴보는 예제로 사용할 수 있습니다.

> 현재 코드는 Windows 환경과 특정 로컬 경로를 기준으로 작성되어 있습니다. 처음 사용하는 경우 반드시 [한국어 사용 매뉴얼](./MANUAL_KO.md)의 환경 설정 부분을 먼저 확인하세요.

## 주요 기능

### `onecam.py`

- 웹캠 1대 입력
- Haar Cascade 기반 얼굴 검출
- 얼굴 검출 여부에 따라 `black.mp4` / `seoultech.mp4` 전환
- `seoultech.mp4`의 재생 위치 보존
- 현재 화면 해상도에 맞춘 전체화면 출력

### `twocam(turn_videotocctv).py`

- 웹캠 2대 사용
- 첫 번째 카메라를 얼굴 검출용으로 사용
- 두 번째 카메라를 기본 CCTV 화면으로 사용
- 얼굴 검출 시 `seoultech.mp4` 재생
- 출력 영상을 좌우로 분할해 2개 OpenCV 창에 표시
- `q` 키로 종료

## 프로젝트 구조

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

## 권장 환경

- Windows 10 / 11
- Python 3.x
- OpenCV (`opencv-python`)
- `onecam.py`: 웹캠 1대
- `twocam(turn_videotocctv).py`: 웹캠 2대 권장
- 듀얼 카메라 예제의 전체 기능 확인 시 모니터 2대 권장

## 다운로드

```bash
git clone https://github.com/AIN108/camproject.git
cd camproject
```

Git을 사용하지 않는 경우 GitHub의 **Code → Download ZIP**으로 받을 수 있습니다.

## 설치

```bash
pip install -r requirements.txt
```

또는 직접 설치하려면:

```bash
pip install opencv-python
```

## 실행 전 확인

현재 소스에는 작성 당시 사용한 Windows 절대경로가 포함되어 있습니다.

```text
C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml
C:\onecam\black.mp4
C:\onecam\seoultech.mp4
```

사용하는 PC의 파일 위치가 다르면 Python 소스의 해당 경로를 수정해야 합니다.

카메라 번호 역시 PC마다 달라질 수 있습니다.

```python
cv2.VideoCapture(0)
cv2.VideoCapture(1)
```

자세한 설치 방법과 문제 해결은 [MANUAL_KO.md](./MANUAL_KO.md)를 참고하세요.

## 실행

### 단일 카메라

```bash
python onecam.py
```

`onecam.py`는 현재 특정 종료키를 지정하지 않았으며 OpenCV 창이 활성화된 상태에서 키 입력이 발생하면 종료됩니다.

### 듀얼 카메라 / 듀얼 화면

```bash
python "twocam(turn_videotocctv).py"
```

종료:

```text
q
```

## 기본 처리 흐름

```text
카메라 입력
    ↓
프레임 획득
    ↓
흑백 변환
    ↓
Haar Cascade 얼굴 검출
    ↓
얼굴 검출 여부 판단
    ↓
영상 / 카메라 화면 선택
    ↓
OpenCV 화면 출력
```

## 개인정보 및 촬영 주의

웹캠을 사용하는 교육 실습에서는 촬영 대상자에게 카메라 사용 사실을 알리고, 실제 촬영 자료를 저장하거나 외부에 공개할 경우 개인정보 및 초상권 관련 기준을 확인하세요.

현재 실행 코드에는 웹캠 영상을 파일로 녹화·저장하는 기능이 구현되어 있지 않습니다.

## 라이선스

현재 저장소에는 별도의 `LICENSE` 파일이 없습니다. 외부 재배포, 수정본 공개 또는 다른 프로젝트에 포함하여 배포하려는 경우 저장소 소유자에게 이용 조건을 확인하세요.

## 상세 매뉴얼

설치, 코드 구조, 실행 과정, 오류 해결 및 수업용 실습 항목은 다음 문서를 참고하세요.

- [한국어 사용 매뉴얼](./MANUAL_KO.md)

## 개발자

- GitHub: [@AIN108](https://github.com/AIN108)
