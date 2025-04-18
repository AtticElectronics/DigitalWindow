import subprocess
import re
import sys
import platform
import cv2

class ConnectedCameras:
    def __init__(self):
        if not self._check_v4l2_ctl():
            self._print_install_help()
            sys.exit(1)  # v4l2-ctl이 없으면 프로그램 종료
        self.camera_keywords = []
        self.cameras = []

    def _check_v4l2_ctl(self):
        """v4l2-ctl이 시스템에 설치되어 있는지 확인"""
        try:
            subprocess.run(['v4l2-ctl', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False

    def _print_install_help(self):
        """v4l2-ctl 설치 도움말 출력"""
        os_name = platform.system().lower()
        if 'linux' in os_name:
            print("v4l2-ctl이 시스템에 설치되어 있지 않습니다. Linux debian 에서는 다음 명령어로 설치할 수 있습니다:")
            print("sudo apt-get update && sudo apt-get install v4l-utils")
        else:
            print("이 스크립트는 Linux debian 시스템에서만 사용할 수 있습니다.")

    def add_camera_keyword(self, keyword):
        """카메라 식별을 위한 키워드 추가"""
        if keyword.lower() not in self.camera_keywords:
            self.camera_keywords.append(keyword.lower())
        self.cameras = self._detect_cameras()

    def _detect_cameras(self):
        """시스템에서 카메라 장치 탐색 및 정보 수집"""
        if not self.camera_keywords:
            return []

        result = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True)
        devices_output = result.stdout

        cameras = []
        device_sections = devices_output.strip().split("\n\n")
        for section in device_sections:
            if any(keyword in section.lower() for keyword in self.camera_keywords):
                lines = section.strip().split("\n")
                name = lines[0].strip()
                device_files = [line.strip() for line in lines[1:] if line.strip().startswith("/dev/video")]
                indices = [int(re.search(r'(\d+)$', file).group()) for file in device_files]
                indices.sort()

                cameras.append({
                    'name': name,
                    'device_files': device_files,
                    'indices': indices
                })

        return cameras

    def get_cameras_count(self):
        """찾은 카메라 개수 반환"""
        return len(self.cameras)

    def get_camera_names(self):
        """찾은 카메라 이름들 반환"""
        return [camera['name'] for camera in self.cameras]

    def get_camera_indices(self):
        """각 카메라별 인덱스 리스트 반환"""
        return [camera['indices'] for camera in self.cameras]

    def get_camera_paths(self):
        """각 카메라별 경로 리스트 반환"""
        return [camera['device_files'] for camera in self.cameras]

    def print_grouped_camera_info(self):
        """그룹화된 카메라 정보 출력"""
        if not self.cameras:
            print("No cameras found. Make sure to add keywords and detect cameras.")
            return

        for camera in self.cameras:
            print(f"Name: {camera['name']}")
            print(f"Indices: {camera['indices']}")
            print(f"Device Paths: {camera['device_files']}")
            print("-----")
    

    def _initialize_camera(self,camera_index,width,height):
        """주어진 인덱스로 카메라를 초기화하고 성공 여부를 반환합니다."""
        cap = cv2.VideoCapture(camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if cap.isOpened():
            return cap
        else:
            cap.release()
            return None

    def try_initialize_cameras(self, width = 640 ,height = 480):
        """두 카메라를 초기화 시도하고 성공 여부에 따라 반환합니다."""
        assert self.get_cameras_count() == 2, "Number of devices found is not 2"

        self.print_grouped_camera_info()
        left_camera_indices = self.get_camera_indices()[0]
        right_camera_indices = self.get_camera_indices()[1]
    
        left_cap = None
        right_cap = None

        for index in left_camera_indices:
            left_cap = self._initialize_camera(index,width,height)
            if left_cap:
                break

        for index in right_camera_indices:
            right_cap = self._initialize_camera(index,width,height)
            if right_cap:
                break

        # 두 카메라 모두 초기화에 성공했는지 확인합니다.
        assert left_cap and right_cap, "Failed to initialize both cameras"

        return left_cap, right_cap



if __name__ == "__main__":
    # 사용 예
    cameras = ConnectedCameras()
    cameras.add_camera_keyword("WN 5M Camera")  # 예시 키워드 추가

    print("Number of cameras found:", cameras.get_cameras_count())
    print("Camera names:", cameras.get_camera_names())
    print("Camera indices:", cameras.get_camera_indices())
    print("Camera paths:", cameras.get_camera_paths())
#     # 출력
#     # Number of cameras found: 2
#     # Camera names: ['WN 5M Camera: WN 5M Camera (usb-xhci-hcd.0-1):', 'WN 5M Camera: WN 5M Camera (usb-xhci-hcd.0-2):']
#     # Camera indices: [[0, 1], [2, 3]]
#     # Camera paths: [['/dev/video0', '/dev/video1'], ['/dev/video2', '/dev/video3']]



#     # 스테래오 비전 프로젝트를 위한 함수
#     # 두개의 카메라의 opencv VideoCapture()된 객체 두개를 반환
#     # cap1, cap2 = cameras.try_initialize_cameras(width,height)
