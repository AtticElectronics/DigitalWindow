import cv2
import time

class FrameReader:
    def __init__(self):
        self.video_sources = []  # 비디오 소스 경로를 저장할 리스트
        self.current_video_index = -1  # 현재 비디오 소스의 인덱스
        self.cap = None  # cv2.VideoCapture 객체
        
        self.last_frame = None
        self.last_frame_time = 0
        self.last_time = time.time()

        self.call_count = 0
        self.new_frame_count = 0
        
        self.total_fps = 0
        self.new_frame_fps = 0
        
        self.max_fps_inhibit = -1
        self.min_interval = 1.0 / self.max_fps_inhibit

        self.ram_frame = []
        self.frame_index = 0

    def add_video_source(self, path):
        self.video_sources.append(path)
        if self.current_video_index == -1:  # 첫 비디오 소스가 추가되면 바로 로드
            self.next_video()

    def next_video(self):
        if not self.video_sources:
            return  # 비디오 소스가 없는 경우 처리하지 않음

        self.current_video_index = (self.current_video_index + 1) % len(self.video_sources)
        video_path = self.video_sources[self.current_video_index]
        if self.cap:
            self.cap.release()  # 기존에 열린 비디오가 있다면 해제
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Unable to open video source {video_path}")
        self.ram_frame = []
        self.frame_index = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:  # 프레임을 읽지 못했을 경우
                break
            self.ram_frame.append(frame)
        self.last_frame = None
        self.last_frame_time = 0
        self.reset_fps_counters()

    def read_frame_loop(self):

        now = time.time()
        
        # max_fps_inhibit가 -1이 아니고, FPS 제한을 초과하지 않는 경우에만 마지막 프레임을 반환
        if self.max_fps_inhibit != -1 and now - self.last_frame_time < self.min_interval:
            self.call_count += 1  # 호출 횟수는 여전히 증가
            return self.last_frame  # 설정한 FPS를 초과할 경우, 마지막 프레임 반환
        frame = self.ram_frame[self.frame_index%len(self.ram_frame)]
        self.frame_index = self.frame_index +1
        # 새 프레임 처리
        self.last_frame = frame
        self.last_frame_time = now
        self.new_frame_count += 1
        self.call_count += 1
        self.update_fps(now)
        
        return frame
    
    
    def update_fps(self, current_time):
        elapsed = current_time - self.last_time
        if elapsed >= 1.0:
            self.total_fps = self.call_count / elapsed
            self.new_frame_fps = self.new_frame_count / elapsed
            self.reset_fps_counters()
            self.last_time = current_time

    def reset_fps_counters(self):
        self.call_count = 0
        self.new_frame_count = 0

    def get_fps(self):
        return self.total_fps, self.new_frame_fps

    def limit_fps(self, max_fps):
        self.max_fps_inhibit = max_fps
        self.min_interval = 1.0 / self.max_fps_inhibit

    def release(self):
        if self.cap:
            self.cap.release()

