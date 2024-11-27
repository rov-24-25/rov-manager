import socket
import time
import pygame
import sys
import struct
import json

def mvt():
    
    pygame.init()
    pygame.joystick.init()
    print("Pygame count : ", pygame.joystick.get_count())

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

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.JOYBUTTONDOWN and event.button == 0): #Bouton d'arret du code sur la gachette du joy
                    running = False
            
            pygame.event.pump()

            axis_z_value = joystick.get_axis(axis_z_index)
            axis_x_value = joystick.get_axis(axis_x_index)
            axis_y_value = joystick.get_axis(axis_y_index)
            axis_rz_value = joystick.get_axis(axis_rz_index)
            

            print("Ne touchez pas le joy.")
            time.sleep(2)

            print("Initialisation de l'axe Z.")
            time.sleep(2)
            axis_z_0 = axis_z_value
            print("Metre le joy au MAX de l'axe Z.")
            time.sleep(2)
            axis_z_max = axis_z_value
            print("Ne touchez pas le joy.")
            time.sleep(2)
            axis_z_max0 = axis_z_value
            print("Metre le joy au MIN de l'axe Z.")
            time.sleep(2)
            axis_z_min = axis_z_value
            print("Ne touchez pas le joy.")
            time.sleep(2)
            axis_z_min0 = axis_z_value

            print("Initialisation de l'axe X.")
            time.sleep(2)
            axis_x_0 = axis_x_value
            print("Metre le joy au MAX de l'axe X.")
            time.sleep(2)
            axis_x_max = axis_x_value
            print("Ne touchez pas le joy.")
            time.sleep(2)
            axis_x_max0 = axis_x_value
            print("Metre le joy au MIN de l'axe X.")
            time.sleep(2)
            axis_x_min = axis_x_value
            print("Ne touchez pas le joy.")
            time.sleep(2)
            axis_x_min0 = axis_x_value
            
            
            print("Initialisation de l'axe Y.")
            time.sleep(2)
            axis_y_0 = axis_y_value
            print("Metre le joy au MAX de l'axe Y.")
            time.sleep(2)
            axis_y_max = axis_y_value
            print("Ne touchez pas le joy.")
            time.sleep(2)
            axis_y_max0 = axis_y_value
            print("Metre le joy au MIN de l'axe Y.")
            time.sleep(2)
            axis_y_min = axis_y_value
            print("Ne touchez pas le joy.")
            time.sleep(2)
            axis_y_min0 = axis_y_value
            
            
            print("Initialisation de l'axe RZ.")
            time.sleep(2)
            axis_rz_0 = axis_rz_value
            print("Metre le joy au MAX de l'axe RZ.")
            time.sleep(2)
            axis_rz_max = axis_rz_value
            print("Ne touchez pas le joy.")
            time.sleep(2)
            axis_rz_max0 = axis_rz_value
            print("Metre le joy au MIN de l'axe RZ.")
            time.sleep(2)
            axis_rz_min = axis_rz_value
            print("Ne touchez pas le joy.")
            time.sleep(2)
            axis_rz_min0 = axis_rz_value


        calibration_data = {}
        
        axis_x_index = 0
        axis_y_index = 1
        axis_z_index = 2
        axis_rz_index = 3

        calibration_data['axe_x'] = {
            "valeur_0": axis_x_0,
            "valeur_max": axis_x_max,
            "valeur_max_0": axis_x_max0,
            "valeur_min": axis_x_min,
            "valeur_min_0": axis_x_min0
        }
        calibration_data['axe_y'] = {
            "valeur_0": axis_y_0,
            "valeur_max": axis_y_max,
            "valeur_max_0": axis_y_max0,
            "valeur_min": axis_y_min,
            "valeur_min_0": axis_y_min0
        }
        calibration_data['axe_z'] = {
            "valeur_0": axis_z_0,
            "valeur_max": axis_z_max,
            "valeur_max_0": axis_z_max0,
            "valeur_min": axis_z_min,
            "valeur_min_0": axis_z_min0
        }
        calibration_data['axe_RZ'] = {
            "valeur_0": axis_rz_0,
            "valeur_max": axis_rz_max,
            "valeur_max_0": axis_rz_max0,
            "valeur_min": axis_rz_min,
            "valeur_min_0": axis_rz_min0
        }



        # Créer des données sous forme de dictionnaire
        donnees = {
            "calibration": calibration_data
        }

        # Ouvrir un fichier en mode écriture et écrire les données JSON
        with open('donnees.json', 'w') as fichier:
            json.dump(donnees, fichier, indent=4)

        print("Les données ont été enregistrées dans 'donnees.json'.")

        pygame.quit()
        sys.exit()
mvt()
# Faire test avec RaspBerry et Led