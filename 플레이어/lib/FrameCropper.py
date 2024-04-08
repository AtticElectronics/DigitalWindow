
import cv2
import numpy as np
import pygame
class FrameCropper:
    def __init__(self, src_w, src_h, window_w, window_h, display_w, display_h):
        self.src_w = src_w
        self.src_h = src_h
        self.window_w = window_w
        self.window_h = window_h
        self.display_w = display_w
        self.display_h = display_h



        self.crop_area = self.crop_infinite_area

        # 현재 X, Y 좌표 초기화
        self.current_X = 0
        self.current_Y = 0
        self.current_Z = 0.7

        self.movement_lock = 2  # 움직임이 이 임계값 이하일 때는 움직이지 않음
        self.movement_release = 4  # 움직임이 이 임계값 이하일 때는 움직이지 않음
        self.active_movement = False  # 현재 움직임 상태를 추적

        self.first_movement = True
        
        self.reduce_K = 0.12
        self.ASPECT_RATIO = 9/16
        self.min_z = 0.1
        
    def set_zoom_scale(self, K):
        self.reduce_K = K

    def set_zoom_value(self, aspect_ratio = 0.0577,min_z=0.1):
        self.ASPECT_RATIO = aspect_ratio  # 16:9 비율을 상수로 정의
        self.min_z = min_z

    def calculate_resolution(self, z):
        scale_factor = (self.min_z / z) ** self.reduce_K
        new_width = int(self.window_w * scale_factor)
        new_height = int(new_width * self.ASPECT_RATIO)
        return new_width, new_height

    
    def run(self, frame, center_x, center_y, z):
        cropped_frame = self.crop_area(frame, center_x, center_y, z)
        image = pygame.transform.scale(cropped_frame, (self.display_w, self.display_h))
        return image


    def crop_infinite_area(self, frame, cx, cy, z):
        # 프레임 중심을 기준으로 cx, cy 계산
        cx = int((self.src_w / 2) + cx)
        cy = int((self.src_h / 2) + cy)

        # 크롭 영역 계산
        ori_w, ori_h = self.calculate_resolution(z)

        startX = cx - ori_w // 2
        startY = cy - ori_h // 2
        endX = startX + ori_w
        endY = startY + ori_h

        # 크롭 및 패딩 처리된 이미지 생성
        cropped_and_padded_image = np.zeros((ori_h, ori_w, 3), dtype=np.uint8)

        # 프레임 내에서 실제로 크롭할 수 있는 영역의 시작과 끝 좌표 계산
        startX_clamped = max(startX, 0)
        startY_clamped = max(startY, 0)
        endX_clamped = min(endX, self.src_w)
        endY_clamped = min(endY, self.src_h)


        # 이미지 경계를 넘어가는 경우에 대한 패딩 처리를 명확히 함
        # 이전 코드에서 이미지 크기와 패딩 필요 여부를 계산
        need_padding = startX < 0 or startY < 0 or endX > self.src_w or endY > self.src_h

        if need_padding:
            # 패딩이 필요한 경우, 전체 영역을 초기화
            cropped_and_padded_image = np.zeros((ori_h, ori_w, 3), dtype=np.uint8)
            # 패딩 영역 계산
            pad_top = max(0, -startY)
            pad_left = max(0, -startX)
            pad_bottom = max(0, endY - self.src_h)
            pad_right = max(0, endX - self.src_w)
            try:
                # 실제 크롭할 수 있는 영역을 이미지에 복사
                crop_area = frame[startY_clamped:endY_clamped, startX_clamped:endX_clamped]
                cropped_and_padded_image[pad_top:ori_h-pad_bottom, pad_left:ori_w-pad_right] = crop_area
            except:
                cropped_and_padded_image = np.zeros((ori_h, ori_w, 3), dtype=np.uint8)
        else:
            # 패딩이 필요 없는 경우, 직접 크롭된 이미지 사용
            cropped_and_padded_image = frame[startY_clamped:endY_clamped, startX_clamped:endX_clamped].copy()

        # OpenCV 이미지(BGR)를 Pygame 포맷(RGB)으로 변환
        frame_rgb = cv2.cvtColor(cropped_and_padded_image, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
        return frame_surface

    def crop_limited_area(self, frame, cx, cy, z):
        cx = int((self.src_w / 2) + cx)
        cy = int((self.src_h / 2) + cy)

        # 크롭 영역 계산
        ori_w, ori_h = self.calculate_resolution(z)

        # 크롭 영역 계산 및 경계 조정
        startX = max(cx - ori_w // 2, 0)
        startY = max(cy - ori_h // 2, 0)
        endX = min(startX + ori_w, self.src_w)
        endY = min(startY + ori_h, self.src_h)
        startX = min(startX, self.src_w - ori_w)
        startY = min(startY, self.src_h - ori_h)

        cropped_and_padded_image = frame[startY:endY, startX:endX]
        frame_rgb = cv2.cvtColor(cropped_and_padded_image, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
        return frame_surface
