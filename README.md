# 📹 Video to CCTV Converter

영상 파일을 CCTV 스타일로 변환하고 실시간 카메라 처리를 수행하는 Python 프로젝트입니다.

## 📋 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 목적 | 영상/카메라 실시간 처리 및 CCTV 스타일 변환 |
| 언어 | Python |
| 핵심 기술 | OpenCV |

## 📂 프로젝트 구조

```
camproject/
├── onecam.py                    # 단일 카메라 처리
├── twocam(turn_videotocctv).py  # 듀얼 카메라 + CCTV 변환
├── black.mp4                    # 테스트 영상 1
└── seoultech.mp4                # 테스트 영상 2 (서울과기대)
```

## 🛠️ 기술 스택

- **언어**: Python 3.x
- **영상 처리**: OpenCV
- **GUI**: OpenCV Window

## 🚀 실행 방법

### 1. 필수 라이브러리 설치

```bash
pip install opencv-python
```

### 2. 단일 카메라 실행

```bash
python onecam.py
```

### 3. 듀얼 카메라 + CCTV 변환 실행

```bash
python "twocam(turn_videotocctv).py"
```

## 🎯 주요 기능

### 단일 카메라 (onecam.py)
- 웹캠 실시간 영상 캡처
- 기본 영상 처리

### 듀얼 카메라 + CCTV 변환 (twocam)
- 두 개의 카메라 동시 처리
- 영상 파일 → CCTV 스타일 변환
- 타임스탬프 오버레이
- 흑백/컬러 전환

## 📸 CCTV 스타일 효과

- 🕐 실시간 타임스탬프 표시
- 📍 위치 정보 오버레이
- 🎬 프레임 레이트 조절
- 🖼️ 화면 분할 (듀얼 카메라)

## 💡 활용 예시

```python
import cv2

# 카메라 열기
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    # CCTV 스타일 처리
    cv2.imshow('CCTV', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## ⌨️ 단축키

| 키 | 기능 |
|----|------|
| `q` | 종료 |
| `s` | 스크린샷 저장 |
| `r` | 녹화 시작/중지 |

## 👨‍💻 개발자

- GitHub: [@AIN108](https://github.com/AIN108)

