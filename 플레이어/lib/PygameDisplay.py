import pygame
from datetime import datetime
import calendar
import random
import textwrap
# 16:9 비율 해상도 정보 https://www.ihee.com/613
class PygameDisplay:

    def __init__(self, width, height):
        pygame.init()
        self.running = True
        # 화면 설정 (전체 화면 + 하드웨어 가속)  더블 버퍼링은 보류
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.HWSURFACE )

        self.ExtraBoldItalic_200 = pygame.font.Font("./font/ExtraBoldItalic.ttf", 200) # time
        self.ExtraBoldItalic_90 = pygame.font.Font("./font/ExtraBoldItalic.ttf", 90) # # sec
        self.BoldItalic_64 = pygame.font.Font("./font/BoldItalic.ttf", 64) #PM AM / date

        self.title = pygame.font.Font("./font/ExtraBoldItalic.ttf", 180).render("Digital Window", True, (255,255,255)).convert_alpha()
        self.subtitle = pygame.font.Font("./font/Bold.ttf", 36).render("Powered by Raspberry Pi5", True, (255,255,255)).convert_alpha()
        
        self.clock_title = pygame.font.Font("./font/ExtraBoldItalic.ttf", 90).render("Digital Window", True, (255,255,255)).convert_alpha()
        self.clock_subtitle = pygame.font.Font("./font/Bold.ttf", 30).render("Powered by Raspberry Pi5", True, (255,255,255)).convert_alpha()
        self.tag = pygame.font.Font("./font/BoldItalic.ttf", 32).render("@AtticElectronics", True, (255,255,255)).convert_alpha()
        self.colon = self.ExtraBoldItalic_90.render(":", True, (255,255,255)).convert_alpha()

        # now = datetime.now()
        # date_str = now.strftime("%Y/%m/%d")
        # time_str = now.strftime("%I:%M")
        # sec_str = now.strftime("%S")
        # meridiem_str = now.strftime("%p")
        # self.date = self.BoldItalic_64.render(date_str, True, (255,255,255)).convert_alpha()
        # self.time = self.ExtraBoldItalic_200.render(time_str, True, (255,255,255)).convert_alpha()
        # self.sec = self.ExtraBoldItalic_90.render(sec_str, True, (255,255,255)).convert_alpha()
        # self.meridiem = self.BoldItalic_64.render(meridiem_str, True, (255,255,255)).convert_alpha()

        self.quotes_list = [
                        ("Albert Einstein", "Imagination is more important than knowledge. For knowledge is limited, whereas imagination embraces the entire world, stimulating progress, giving birth to evolution."),
                        ("Marie Curie", "Nothing in life is to be feared, it is only to be understood. Now is the time to understand more, so that we may fear less."),
                        ("Niels Bohr", "An expert is a person who has made all the mistakes that can be made in a very narrow field."),
                        ("Carl Sagan", "The nitrogen in our DNA, the calcium in our teeth, the iron in our blood, the carbon in our apple pies were made in the interiors of collapsing stars. We are made of starstuff."),
                        ("Richard Feynman", "If you can't explain it to a six year old, you don't understand it yourself."),
                        ("Charles Darwin", "It is not the strongest of the species that survive, nor the most intelligent, but the one most responsive to change."),
                        ("Steve Jobs", "Innovation distinguishes between a leader and a follower."),
                        ("Elon Musk", "When something is important enough, you do it even if the odds are not in your favor."),
                        ("Sundar Pichai", "Keep pushing your limits.")
                    ]

        self.quotes_index = 0

        # 폰트 설정
        self.name_font = pygame.font.Font("./font/ExtraBoldItalic.ttf", 46)
        self.quotes_font = pygame.font.Font("./font/ExtraBoldItalic.ttf", 32)
    
    def set_random_quote(self):
        self.quotes_index = random.randint(0,len(self.quotes_list)-1)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False

    def draw_title(self,transparent):
        self.title.set_alpha(transparent)
        self.subtitle.set_alpha(transparent)
        self.screen.blit(self.title, (300, 411))
        self.screen.blit(self.subtitle, (1150, 585))

    def draw_clock_and_calendar(self,transparent):
        self.draw_date(transparent, x=80,y=250)
        self.draw_comment(transparent,x=1100,y=400)

    def draw_date(self, transparent, x=80,y=300):
        now = datetime.now()
        date_str = now.strftime("%Y/%m/%d")
        time_str = now.strftime("%I:%M")
        # time_str = "00:00"
        sec_str = now.strftime("%S")
        meridiem_str = now.strftime("%p")
        date = self.BoldItalic_64.render(date_str, True, (255,255,255)).convert_alpha()
        time = self.ExtraBoldItalic_200.render(time_str, True, (255,255,255)).convert_alpha()
        sec = self.ExtraBoldItalic_90.render(sec_str, True, (255,255,255)).convert_alpha()
        meridiem = self.BoldItalic_64.render(meridiem_str, True, (255,255,255)).convert_alpha()
        
        self.clock_title.set_alpha(transparent)
        self.clock_subtitle.set_alpha(transparent)
        
        self.colon.set_alpha(transparent)
        
        time.set_alpha(transparent)
        sec.set_alpha(transparent)
        meridiem.set_alpha(transparent)


        # 요소 blit
        self.screen.blit(self.clock_title, (x+40, y))
        self.screen.blit(self.clock_subtitle, (x+290, y+90))
        self.screen.blit(self.colon,(x+590,y+185))
        self.screen.blit(time, (x, y+82))  # time 위치 변동 없음
        self.screen.blit(sec, (x+620, y+185))
        self.screen.blit(meridiem, (x+600, y+130))


        date.set_alpha(transparent)
        self.tag.set_alpha(transparent)

        self.screen.blit(self.tag, (x+30, y+345))
        self.screen.blit(date, (x+350, y+315))

        y = y + 400
        now = datetime.now()
        today = now.day
        month = now.month
        year = now.year
        cal = calendar.monthcalendar(year, month)
        day_font = pygame.font.Font("./font/ExtraBoldItalic.ttf", 32)
        date_font = pygame.font.Font("./font/ExtraBoldItalic.ttf", 28)

        # 요일 이름 표시 및 요일별 중앙 정렬을 위한 준비
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        total_width = 740
        day_gap = total_width // len(days)  # 전체 너비를 요일 수로 나누어 각 요일 간격 계산
        day_widths = [day_font.size(day)[0] for day in days]
        
        # 요일 표시
        for i, day in enumerate(days):
            day_surface = day_font.render(day, True, (255, 255, 255))
            day_surface.set_alpha(transparent)
            day_x = x + i * day_gap + (day_gap - day_widths[i]) // 2  # 중앙 정렬 위치 계산
            self.screen.blit(day_surface, (day_x, y))

        # 달력의 날짜 표시
        y_offset = 32 + 20  # 날짜 시작 위치 조정
        for week in cal:
            for i, day in enumerate(week):
                if day != 0:
                    day_str = str(day)
                    day_surface = date_font.render(day_str, True, (255, 255, 255) if day != today else (255, 100, 100))
                    day_surface.set_alpha(transparent)
                    day_text_width = day_surface.get_width()
                    # 날짜 중앙 정렬
                    day_x = x + i * day_gap + (day_gap - day_text_width) // 2
                    self.screen.blit(day_surface, (day_x, y + y_offset))
            y_offset += 28 + 10  # 다음 주로 이동


        

    def draw_quote(self, transparent, x=80, y=30):
        # 현재 인덱스에 해당하는 인물의 이름과 명언 가져오기
        current_name, current_quote = self.quotes_list[self.quotes_index]

        # 명언 렌더링 (48자 넘어가면 자동 줄바꿈)
        wrapped_quote = textwrap.wrap(current_quote, width=48)
        y_offset = y
        for line in wrapped_quote:
            quote_surface = self.quotes_font.render(line, True, (255, 255, 255))
            quote_surface.set_alpha(transparent)
            self.screen.blit(quote_surface, (x, y_offset))
            y_offset += quote_surface.get_height() + 10  # 다음 줄 위치 조정
        
        # 인물 이름 렌더링 (오른쪽 아래에 배치)
        name_surface = self.name_font.render(current_name, True, (255, 255, 255))
        name_surface.set_alpha(transparent)
        name_width = name_surface.get_width()
        self.screen.blit(name_surface, (x+ 750 - name_width , y_offset))  # 오른쪽 정렬을 위해 x 위치 조정


    # 이미지 그리기 메서드
    def draw_preload_image(self, position):
        # image = pygame.image.load(image_path).convert_alpha()  # 이미지 로드 및 알파 채널 처리
        self.screen.blit(self.ready_image, position)  # 이미지를 지정된 위치에 그림

    # 투명한 상자 그리기 메서드
    def draw_transparent_box(self, position, size):
        # 알파 채널이 포함된 서피스 생성
        box_surface = pygame.Surface(size, pygame.SRCALPHA)
        # 알파값이 125인 검정색 상자를 서피스에 그림
        box_surface.fill((0, 0, 0, 125))
        self.screen.blit(box_surface, position)  # 상자를 지정된 위치에 그림

    def draw_image(self, image_surface):
        self.screen.blit(image_surface, (0, 0))  # 이미지 그리기

    def flip(self):
        pygame.display.flip()  # 화면 업데이트

    def quit(self):
        pygame.quit()
        exit()
        
