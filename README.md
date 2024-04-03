# DigitalWindow
## 개요
- 본프로젝트는 두가지 소규모 프로젝트로 구성된다. [스테레오 비전 카메라],[착시창문 플레이어]
- 학생들이 저렴한 가격에 착시창문을 제작하며 컴퓨터 비전과 라즈베리파이에 대한 가벼운 경험을 시켜주기 위해 제작되었다.
- 필자가 커피마실 때, 분위기 내기 하기위해 제작되었다.

# 스태레오 비전 카메라
## 하드웨어 
1. OV5693 USB 카메라 모듈 x2
2. raspberry pi 5 (4GB ram)

- 라즈베이파이os의 펌웨어설정을 수정을 아래처럼 한다.(스로틀링 방지)
```bash
$ sudo nano /boot/firmware/config.txt 
```
```bash
dtparam=fan_temp0_speed=150
dtparam=fan_temp1_speed=180
dtparam=fan_temp2_speed=225
dtparam=fan_temp3_speed=250
dtoverlay=w1-gpio
```



### 개발환경
1. debian (ubuntu / raspberry pi os)
2. python 3.10

### 의존 패치지
- pip install -r /sensor/requirements.txt
- pip install opencv-python numpy dlib pyserial opencv-contrib-python



# 착시창문 플레이어
## 하드웨어
1. raspberry pi 5 (4GB ram)
2. PCle M.2 2230 2280 NVMe [X1001]
3. 삼성전자 PM991 M2 SSD 128GB

### ssd 가속
1. sudo nano /boot/firmware/config.txt
2. 아래 내용을 추가
```
[all]
dtparam=pciex1
dtparam=pciex1_gen=3
```

### 개발환경
1. debian (ubuntu / raspberry pi os)
2. python 3.10

### 권한관련
- sudo usermod -a -G gpio username
- python -m venv --system-site-packages Player
- sudo pip install gpiozero
- 이후 Player 가상환경을 사용한다.

### 의존 패치지
- pip install -r /player/requirements.txt
