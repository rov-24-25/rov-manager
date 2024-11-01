import socket
import time
import pygame
import sys
import struct
#import RPi.GPIO as GPIO

def mvt():
    pygame.init()
    pygame.joystick.init()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    axis_indices = [0, 1, 2, 4]  # indices for X, Y, Z, RZ axes

    running = True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.1.24', 12345))
        
        try:
            while running:
                pygame.event.pump()
                data = bytearray()
                for index in axis_indices:
                    axis_value = joystick.get_axis(index)
                    #if abs(axis_value) < 0.1:
                     #   axis_value = 0.0
                    print(index, axis_value)
                    data.extend(struct.pack('f', axis_value))
                
                # Send a fifth dummy value to make it 5 floats (20 bytes)
                #data.extend(struct.pack('f', 0.0))
                print("tout vas bien")

                s.sendall(data)
                #print("ça a pas planter")
                
                time.sleep(0.1)

        except Exception as e:
                print(f"Error sending data: {e}")
                

    pygame.quit()
    sys.exit()
mvt()

# Faire test avec RaspBerry et Led
    
    
    
    
    
    
    
    