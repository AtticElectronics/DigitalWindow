from lib.FrameReader import FrameReader
from lib.PygameDisplay import PygameDisplay
from lib.FrameCropper import FrameCropper
from lib.MP3Player import MP3Player
from lib.CoordEstimator import CoordEstimator
from lib.TcpSocket import TCPServer

class MainApplication:
    def __init__(self):

        self.player = MP3Player()
        self.player.add_mp3_file("output.mp3")

        self.frame_reader = FrameReader()
        self.frame_reader.add_video_source("output.mkv")
        # self.frame_reader.limit_fps(30)
        
        # https://www.ihee.com/613 16 : 9 비율 해상도 참조
        self.display = PygameDisplay(1920, 1080)
        # self.cropper = FrameCropper(src_w=3840, src_h=2160, window_w=2560, window_h=1440, display_w=1920, display_h=1080)
        # self.cropper = FrameCropper(src_w=3840, src_h=2160q, window_w=1920, window_h=1080, display_w=1920, display_h=1080)
        self.cropper = FrameCropper(src_w=2560, src_h=1440, window_w=1920, window_h=1080, display_w=1920, display_h=1080)
        
        self.coord = CoordEstimator()
        self.coord.set_lock_release_threshold(0,1)
        self.coord.setFocusDistance(-300)

        self.cropper.set_zoom_value(aspect_ratio =9/16, min_z=0.1)
        self.cropper.set_zoom_scale(0.1)
        self.cropper.crop_area = self.cropper.crop_infinite_area
        # self.cropper.crop_area = self.cropper.crop_limited_area


        self.server = TCPServer('0.0.0.0', 62035, 5, self.update_coordinates)
        # self.data_receiver = DataReceiver(self.update_coordinates)
        self.sensor_pos_x = 0
        self.sensor_pos_y = -0.3
        self.count = 0

        self.detected = None
        self.x, self.y, self.z = 0, 0, 0.7

        self.quotes_trans = 0
        self.date_trans = 0
        self.title_trans = 0
        self.dir = 1



    def update_coordinates(self, tcp_msg):
        if tcp_msg is not None:
            values = tcp_msg.split('/')
            if int(values[0]) == 1:
                self.count = 0 
                target_X, target_Y, target_Z = map(float, values[1:])
                target_X = -(target_X + self.sensor_pos_x)
                target_Y = target_Y + self.sensor_pos_y

                self.detected = True
                self.x = target_X
                self.y = target_Y
                self.z = target_Z
            else:
                self.count += 1
                if self.count > 10:
                    self.detected = False
                    self.x = 0
                    self.y = 0
                    self.z = 0.7


    def run(self):
        self.player.play(0) 
        # self.data_receiver.start()
        self.player.start()  # 볼륨 조절을 위한 스레드 시작
        while self.display.running:
            self.display.handle_events()
            frame = self.frame_reader.read_frame_loop()
            x,y,z = self.coord.run(self.detected,self.x, self.y, self.z)
            y=y-300
            cropped_frame = self.cropper.run(frame,x,y,z)

            self.display.draw_image(cropped_frame)

            if self.player.get_button_state():
                if self.quotes_trans == 1000:
                    self.dir = -1
                elif self.quotes_trans == 0:
                    self.dir = 1
                    self.display.quotes_index += 1
                    self.display.set_random_quote()

                self.quotes_trans = self.quotes_trans + (10 * self.dir)
                self.quotes_trans = max(0, self.quotes_trans)
                self.quotes_trans = min(1000, self.quotes_trans)

                self.date_trans = self.date_trans + 10
                self.date_trans = min(1000, self.date_trans)
            else:
                if self.quotes_trans > 255:
                    self.quotes_trans = 255
                if self.date_trans > 255:
                    self.date_trans = 255
                self.quotes_trans = max(0, self.quotes_trans - 3)
                self.date_trans = max(0, self.date_trans - 3)
            
                    
            if not self.detected and not self.player.get_button_state():
                self.title_trans +=5
                self.title_trans = min(255, self.title_trans)
            else:
                self.title_trans -=5
                self.title_trans = max(0, self.title_trans)

            if self.title_trans > 0 :
                self.display.draw_title(min(self.title_trans,255))

            if self.quotes_trans > 0:
                self.display.draw_quote(min(self.quotes_trans,255),x=1100,y=600)

            if self.date_trans > 0:
                self.display.draw_date(min(self.date_trans,255), x=80,y=250)

            

            # self.display.draw_text(None, f"FPS: {self.frame_reader.get_fps()}", (100, 100))
            self.display.flip()

        self.server.stop()
        self.display.quit()

main = MainApplication()
main.run()