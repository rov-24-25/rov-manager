import socket
import time
import pygame
import sys
import struct

def mvt():
    pygame.init()
    pygame.joystick.init()
    print("Pygame count : ", pygame.joystick.get_count())
    axis_indices = [0, 1, 2, 4]

    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print("Le EXTREME 3D PRO est prêt.")
        axis_z_index = -1
        axis_x_index = -1
        axis_y_index = -1
        axis_rz_index = -1
        
        print("Get_numaxes : ", joystick.get_numaxes())
        for i in range(joystick.get_numaxes()):
            if i == 0:  # Axe X
                axis_x_index = i  
            if i == 1 : # Axe Y
                axis_y_index = i  
            if i == 2 : # Axe Z
                axis_z_index = i
            if i == 3 : # Axe RZ
                axis_rz_index = i  

        running = True
        # Créer un socket UDP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            server_address = socket.getaddrinfo("raspberrypi.local", 8080, socket.AF_INET6)[0][4]

        
            try:
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.JOYBUTTONDOWN and event.button == 0): #Bouton d'arret du code sur la gachette du joy
                            running = False
                        elif event.type == pygame.JOYBUTTONDOWN and event.joy == 0:
                            print(" Bouton", event.button, "appuyé.")
                    
                    pygame.event.pump()
                    data = bytearray() 

                    factor = 100 #nombre par lequelle va etre multiplier les valeur des axe dans  ce cas 100

                    axis_z_value = joystick.get_axis(axis_z_index)
                    axis_x_value = joystick.get_axis(axis_x_index)
                    axis_y_value = joystick.get_axis(axis_y_index)
                    axis_rz_value = joystick.get_axis(axis_rz_index)

                    axis_rz_value = round(axis_rz_value*factor, 0) #Permet d'avoir les valeur en 53.0 au lieu de 0.867875877848748
                    axis_z_value = round(axis_z_value*factor, 0)
                    axis_x_value = round(axis_x_value*factor, 0)
                    axis_y_value = round(axis_y_value*factor, 0)

                    if abs(axis_z_value) < 10:
                        axis_z_value = 0.0
                    if abs(axis_x_value) < 10:
                        axis_x_value = 0.0
                    if abs(axis_y_value) < 10:
                        axis_y_value = 0.0
                    if abs(axis_rz_value) < 10:
                        axis_rz_value = 0.0

                    print(f"\rX: {axis_x_value} Y: {axis_y_value} Z: {axis_z_value} RZ: {axis_rz_value}", end=" ", flush=True)

                    data.extend(struct.pack('f', axis_x_value))
                    s.sendto(data, server_address)

                    data.extend(struct.pack('f', axis_y_value))
                    s.sendto(data, server_address)

                    data.extend(struct.pack('f', axis_z_value))
                    s.sendto(data, server_address)

                    data.extend(struct.pack('f', axis_rz_value))
                    s.sendto(data, server_address)
                    
                    time.sleep(1)
            except Exception as e:
                print(f"Error sending data: {e}")

    pygame.quit()
    sys.exit()

mvt()

#pygame.event.pump()
#data = bytearray()
#    
#axis_value = joystick.get_axis(0)
#
#print("axe value")
#
#print(0, axis_value)
#
#data.extend(struct.pack('f', axis_value))
#
# Envoyer les données au serveur via UDP
#s.sendto(data, server_address)