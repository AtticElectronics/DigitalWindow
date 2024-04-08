import math

class CoordEstimator:
    def __init__(self):

        # 현재 X, Y 좌표 초기화
        self.current_X = 0
        self.current_Y = 0
        self.current_Z = 0.7

        self.movement_lock = 2  # 움직임이 이 임계값 이하일 때는 움직이지 않음
        self.movement_release = 4  # 움직임이 이 임계값 이하일 때는 움직이지 않음
        self.active_movement = False  # 현재 움직임 상태를 추적

        self.slow_movement = True

        self.focus_z = 0

        self.scale_factor = (6 - (-6)) / 16
        self.offset = 8

        self.slow_scale_factor = (6 - (-6)) / 50
        self.slow_offset = 25

    def setFocusDistance(self, z):
        self.focus_z = z

    # 원점과 x,y,z 가 이루는 직선의 방정식상의 focus_z의 x,y값
    def find_xy_on_line_at_fz(self, x, y, z):
        X = x * (self.focus_z / z)
        Y = y * (self.focus_z / z)
        return X, Y
    
    def set_lock_release_threshold(self,lock,release):
        self.movement_lock = lock # 움직임이 이 임계값 이하일 때는 움직이지 않음
        self.movement_release = release # 움직임이 이 임계값 이하일 때는 움직이지 않음
    
    # def calculate_interpolation_factor(self, distance):
    #     # Sigmoid 함수를 사용한 interpolation_factor 계산
    #     # Sigmoid 함수 적용
    #     sigmoid_input = self.scale_factor * (distance - self.offset)
    #     interpolation_factor = 1 / (1 + math.exp(-sigmoid_input))
    #     return interpolation_factor

    def calculate_slow_interpolation_factor(self, distance):
        scaleFactor = 2.4  # 입력 범위를 넓히기 위해 조정
        offset = 5  # 중간값에 해당하는 distance에서 0이 되도록 설정
        sigmoid_input = scaleFactor * (distance - offset)
        interpolation_factor = 1 / (1 + math.exp(-sigmoid_input))
        return interpolation_factor
    
    def calculate_interpolation_factor(self, distance, min_distance= 0, max_distance=100, steepness=1):


        # distance의 범위를 정규화하여 [0, 1] 범위로 변환
        normalized_distance = (distance - min_distance) / (max_distance - min_distance)

        # 시그모이드 함수의 중간 지점을 0.5로 맞추기 위해 입력 조정
        sigmoid_input = (normalized_distance - 0.5) * steepness
        
        # 시그모이드 함수 적용
        interpolation_factor = 1 / (1 + math.exp(-sigmoid_input))
        
        return interpolation_factor

    
    def run(self, detected, x, y, z):
        target_X, target_Y = self.find_xy_on_line_at_fz(x, y, z)
        target_Z = z

        diff_X = abs(target_X - self.current_X)
        diff_Y = abs(target_Y - self.current_Y)
        diff_Z = abs(target_Z - self.current_Z)

        # 목표 좌표와 현재 좌표 사이의 차이 계산

        if not detected:
            self.slow_movement = True
        else:
            if diff_X <= 10 and diff_Y <= 10 and diff_Z <= 10:
                self.slow_movement = False

        if self.slow_movement:
            interpolation_factor_X = 0.05
            interpolation_factor_Y = 0.05
            interpolation_factor_Z = 0.05
        else:
            if diff_X != 0 :
                interpolation_factor_X = self.calculate_interpolation_factor(diff_X)
            else:
                interpolation_factor_X = 0
            if diff_Y != 0 :
                interpolation_factor_Y = self.calculate_interpolation_factor(diff_Y)
            else:
                interpolation_factor_Y = 0
            if diff_Z != 0 :
                interpolation_factor_Z = self.calculate_interpolation_factor(diff_Z)
            else:
                interpolation_factor_Z = 0
        
        self.current_X += (target_X - self.current_X) * interpolation_factor_X
        self.current_Y += (target_Y - self.current_Y) * interpolation_factor_Y
        self.current_Z += (target_Z - self.current_Z) * interpolation_factor_Z

        # # 활성화 상태에서 목표와 현재 위치 차이가 매우 작을 때 (1 이하) 활성화 상태 해제
        # if self.active_movement and diff_X <= self.movement_lock and diff_Y <= self.movement_lock:
        #     self.active_movement = False
        #     self.first_movement = False
        # if self.active_movement or diff_X > self.movement_release or diff_Y > self.movement_release:
        #     # 활성화 상태이거나, 큰 움직임이 감지되면 위치 업데이트
        #     self.current_X += (target_X - self.current_X) * interpolation_factor_X
        #     self.current_Y += (target_Y - self.current_Y) * interpolation_factor_Y
        #     self.active_movement = True
        
        return self.current_X, self.current_Y, self.current_Z