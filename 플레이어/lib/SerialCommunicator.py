import serial
import glob
import time

class SerialCommunicator:
    def __init__(self):
        self.connected_port = None
        self.serial_connection = None

    def find_devices(self, pattern):
        ports = glob.glob(pattern)
        device_ports = []
        for port in ports:
            print("try on ", port)
            try:
                with serial.Serial(port, 115200, timeout=2) as ser:
                    ser.write(b'C\n')
                    time.sleep(1)  # 장치가 응답하는 데 시간을 줍니다.
                    response = ser.readline().decode().strip()
                    if response == "COMP":
                        device_ports.append(port)
                        break
            except serial.SerialException as e:
                print(f"Error on {port}: {e}")
        return device_ports

    def setReceiverMac(self, port, mac_add="FFFFFFFFFFFF"):
        try:
            with serial.Serial(port, 115200, timeout=2) as ser:
                command = f'F{mac_add}\n'.encode()  # 'S'와 MAC 주소를 결합하여 명령 생성
                ser.write(command)
                time.sleep(1)  # 장치가 응답하는 데 시간을 줍니다.
                response = ser.readline().decode().strip()
                if response == "MAC Address Updated":
                    print("Success")
                else:
                    print("Failed")

        except serial.SerialException as e:
            print(f"Error on {port}: {e}")

    def getMacAddress(self,port):
        try:
            with serial.Serial(port, 115200, timeout=5) as ser:
                ser.write(b'M\n')
                time.sleep(1)  # 장치가 응답하는 데 시간을 줍니다.
                response = ser.readline().decode().strip()
                print(response)

        except serial.SerialException as e:
            print(f"Error on {port}: {e}")



    def connect(self, port):
        try:
            self.serial_connection = serial.Serial(port, 115200, timeout=2)
            self.connected_port = port
            time.sleep(1)
            return True
        except serial.SerialException as e:
            print(f"Error connecting to {port}: {e}")
            return False

    def disconnect(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.connected_port = None

    def send_message(self, message):
        if not self.serial_connection or not self.serial_connection.is_open:
            print("Device not connected")
            return False
        try:
            self.serial_connection.write(b'D'+message.encode() + b'\n')
            response = self.serial_connection.readline().decode().strip()
            if response == '0':
                return True
            else:
                return False

        except serial.SerialException as e:
            print(f"Error: {e}")
            return False

    def receive_message(self):
        if not self.serial_connection or not self.serial_connection.is_open:
            print("Device not connected")
            return None
        try:
            response = self.serial_connection.readline().decode().strip()
            if response == "":  # 읽은 데이터가 없을 때
                return None
            return response
        except serial.SerialException as e:
            print(f"Error: {e}")
            return None
        
if __name__ == "__main__":
    # communicator = SerialCommunicator()
    # device_ports = communicator.find_devices()
    # print(f"Found devices: {device_ports}")
    # if device_ports:
    communicator = SerialCommunicator()
    device_ports = communicator.find_devices("/dev/ttyACM*")
    successful_connection = communicator.connect(device_ports[0])
    if successful_connection:
        try:
            while True:
                msg = communicator.receive_message()
                print(msg)
        except:
            pass
        communicator.disconnect()
        print("Disconnected")
