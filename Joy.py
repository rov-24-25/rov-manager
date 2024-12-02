import socket
import time
import pygame
import sys
import struct
#import RPi.GPIO as GPIO

"""
led = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
"""

def send_data(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('169.254.85.12', 12345))
        s.sendall(data)

def mvt():
    
    pygame.init()
    pygame.joystick.init()
    #print(pygame.joystick.get_count())
    
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print("Le flightstick PXN 2113 est prêt.")
        axis_z_index = -1
        axis_x_index = -1
        axis_y_index = -1
        axis_rz_index = -1
        
        #s.sendall(data)
        for i in range(joystick.get_numaxes()):
            if i == 0:  # Axe X
                axis_x_index = i  
            if i == 1 : # Axe Y
                axis_y_index = i  
            if i == 2 : # Axe Z
                axis_z_index = i  
            if i == 4 : # Axe RZ
                axis_rz_index = i  

        running = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('169.254.85.12', 12345))
            
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.JOYBUTTONDOWN and event.joy == 0:
                        print("Bouton", event.button, "appuyé.")
                   # GPIO.output(led, GPIO.HIGH)
                #else:
                   # GPIO.output(led, GPIO.LOW) 
                
                pygame.event.pump() 

                axis_z_value = joystick.get_axis(axis_z_index)
                axis_x_value = joystick.get_axis(axis_x_index)
                axis_y_value = joystick.get_axis(axis_y_index)
                axis_rz_value = joystick.get_axis(axis_rz_index)
                
                if abs(axis_z_value) < 0.1:
                    axis_z_value=0.0
                else:
                    print("Mouvement de l'axe Z détecté. Valeur:", axis_z_value)
                data=struct.pack('f',axis_z_value)
                s.sendall(data)
                    
                if abs(axis_x_value) < 0.1:
                    axis_x_value=0.0
                else:
                    print("Mouvement de l'axe X détecté. Valeur:", axis_x_value)
                data=struct.pack('f',axis_x_value)
                s.sendall(data)  

                if abs(axis_y_value) < 0.1:
                    axis_y_value=0.0
                else:
                    print("Mouvement de l'axe Y détecté. Valeur:", axis_y_value)
                data=struct.pack('f',axis_y_value)
                s.sendall(data)  
                
                if abs(axis_rz_value) < 0.5:
                    axis_rz_value=0.0
                else:
                    print("Mouvement de l'axe RZ détecté. Valeur:", axis_rz_value)
                data=struct.pack('f',axis_rz_value)
                s.sendall(data)
                
                time.sleep(0.01)
            

        pygame.quit()
        #GPIO.cleanup()
        sys.exit()
mvt()

# Faire test avec RaspBerry et Led
    
    
    
    
    
    
    
    