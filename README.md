# DigitalWindow
# 유튜브 영상제작을 위해 "매우 짧은 시간에 작성된 코드"이기 때문에, 문서화 주석이 없어 알아보려면 상당한 시간이 필요할듯합니다.
# 코드관련해서 정말 설명이 필요하신분은 자세한 질문내용을 메일주시면 최대한 도와드리려고 노력하겠습니다.
---

# 1. 스태레오 비전 카메라
### 하드웨어 
1. OV5693 USB 카메라 모듈 x2 (가변초점 사용금지)
2. raspberry pi 5 (4GB ram)

### 라즈베이파이os의 펌웨어설정을 수정을 아래처럼 한다.(스로틀링 방지)
```bash
$ sudo nano /boot/firmware/config.txt 
dtparam=fan_temp0_speed=150
dtparam=fan_temp1_speed=180
dtparam=fan_temp2_speed=225
dtparam=fan_temp3_speed=250
dtoverlay=w1-gpio
```

### 개발환경
1. debian (raspberry pi os)
2. python 3.11
### 의존성 패키지를 설치 후, 해당폴더의 main.py 실행

---

# 2. 착시창문 플레이어
## 하드웨어
1. raspberry pi 5 (8GB ram) (느립니다. 성능좋은 컴퓨터를 사용해야합니다.)
3. PCle M.2 2230 2280 NVMe [X1001]
4. 삼성전자 PM991 M2 SSD 128GB

### ssd 가속
1. sudo nano /boot/firmware/config.txt
2. 아래 내용을 추가
```bash
[all]
dtparam=pciex1
dtparam=pciex1_gen=3
```
### 개발환경
1. debian (raspberry pi os)
2. python 3.11

### 권한관련
- sudo usermod -a -G gpio username
- python -m venv --system-site-packages Player
- sudo pip install gpiozero
- 이후 Player 가상환경을 사용한다.

### 의존성 패키지를 설치 후, 해당폴더의 main.py 실행
---
