# DigitalWindow
착시 전자창문



# 스태레오 비전 카메라
## 하드웨어 
1. OV5693 USB 카메라 모듈 x2
2. raspberry pi 5 (4GB ram)
   
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


### 의존 패치지
- pip install -r /player/requirements.txt

3. 
## 함수 설명: find_xy_on_line_at_fz

### 목적
- 주어진 입력 좌표 \((x, y, z)\)와 원점을 지나는 직선을 구하고, 이 직선이 특정 \(z\) 값 (\(f_z\))에서의 \(x, y\) 좌표를 계산하여 반환합니다.

### 입력
- `x`: 직선을 정의하는 점의 \(x\) 좌표입니다.
- `y`: 직선을 정의하는 점의 \(y\) 좌표입니다.
- `z`: 직선을 정의하는 점의 \(z\) 좌표입니다. \(z\)의 값은 반드시 양수여야 합니다 (\(z > 0\)).
- `f_z`: 직선 위에서 찾고자 하는 \(z\) 값입니다.

### 출력
- 함수는 계산된 \(x, y\) 좌표를 튜플 형태로 반환합니다. 이 좌표는 원점과 입력 좌표를 지나는 직선이 \(f_z\)에서의 \(x, y\) 위치입니다.

### 작동 원리
- 함수는 먼저 주어진 입력 좌표 \((x, y, z)\)와 원점을 지나는 직선의 방정식을 사용하여, \(f_z\)에서의 \(x, y\) 좌표를 계산합니다.
- 이 과정은 다음 공식을 사용하여 수행됩니다:
  \[
  X = x \left(\frac{f_z}{z}\right),\quad Y = y \left(\frac{f_z}{z}\right)
  \]
  여기서 \(X, Y\)는 계산된 좌표이며, \(x, y, z\)는 입력 좌표입니다.
- 함수는 주어진 \(f_z\) 값에 대해 직선 위의 새로운 \(x, y\) 좌표를 성공적으로 계산합니다.
