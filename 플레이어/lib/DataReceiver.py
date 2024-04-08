# import threading
# import math
# from lib.SerialCommunicator import SerialCommunicator

# class DataReceiver(threading.Thread):
#     def __init__(self,  f):
#         threading.Thread.__init__(self)
#         self.update_callback = update_callback
#         self.running = True

#         self.communicator = SerialCommunicator()
#         device_ports = self.communicator.find_devices("/dev/ttyACM*")
#         self.communicator.connect(device_ports[0])

#         self.sensor_pos_y = 0
#         self.sensor_pos_x = 0

#         self.count = 0
    
#     def adjust_center_y(self,pos_x,pos_y):
#         self.sensor_pos_y = pos_x
#         self.sensor_pos_x = pos_y


#     def run(self):
#         while self.running:
#             coord = self.communicator.receive_message()
#             if coord is not None:
#                 values = coord.split('/')
#                 if int(values[0]) == 1:
#                     self.count = 0 
#                     target_X, target_Y, target_Z = map(float, values[1:])
#                     target_X = -(target_X + self.sensor_pos_x)
#                     target_Y = target_Y + self.sensor_pos_y
#                     self.update_callback(True, target_X, target_Y, target_Z)
#                 else:
#                     self.count += 1
#                     if self.count > 10:
#                         self.update_callback(False, 0 ,0,0.7)
            
#     def stop(self):
#         self.running = False