from gpiozero import Button
import pygame
import threading
import time

class MP3Player(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True  # 프로그램 종료시 스레드도 함께 종료되도록 설정
        self.mp3_files = []
        self.current_index = -1
        self.is_playing = False
        self.volume = 0.5  # 볼륨 초기값 (0.0: 무음, 1.0: 최대 볼륨)
        pygame.mixer.init()
        self.button_state = True
        self.button = Button(27)

    def add_mp3_file(self, file_path):
        self.mp3_files.append(file_path)
    
    def play(self, index):
        if index < 0 or index >= len(self.mp3_files):
            return  # 잘못된 인덱스 처리
        self.current_index = index
        if self.is_playing:
            pass
            pygame.mixer.music.stop()  # 현재 재생 중인 음악 정지
        pygame.mixer.music.load(self.mp3_files[index])
        pygame.mixer.music.play(-1)  # 무한 반복 재생
        self.is_playing = True

    def set_volume(self, volume):
        if 0 <= volume <= 1:
            self.volume = volume
            pygame.mixer.music.set_volume(volume)

    def get_button_state(self):
        return self.button_state

    def run(self):
        while True:
            if self.button.is_pressed:
                self.button_state = True
                self.set_volume(0.1)  # 볼륨 0
            else:
                self.button_state = False
                self.set_volume(1.0)  # 볼륨 최대
            time.sleep(0.2)  # 핀 상태 체크 주기
