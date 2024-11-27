import socket
import time
import pygame
import sys
import struct
import json

def calibrer_axe(joystick, axe_index, nom_axe):
    print(f"Initialisation de l'axe {nom_axe}.")
    time.sleep(2)
    valeur_0 = joystick.get_axis(axe_index)
    
    print(f"Mettre le joystick au MAX de l'axe {nom_axe}.")
    time.sleep(2)
    valeur_max = joystick.get_axis(axe_index)
    
    print("Ne touchez pas le joystick.")
    time.sleep(2)
    valeur_max_0 = joystick.get_axis(axe_index)
    
    print(f"Mettre le joystick au MIN de l'axe {nom_axe}.")
    time.sleep(2)
    valeur_min = joystick.get_axis(axe_index)
    
    print("Ne touchez pas le joystick.")
    time.sleep(2)
    valeur_min_0 = joystick.get_axis(axe_index)
    
    return {
        "valeur_initiale": valeur_0,
        "valeur_max": valeur_max,
        "valeur_max_apres": valeur_max_0,
        "valeur_min": valeur_min,
        "valeur_min_apres": valeur_min_0
    }

def mvt():
    
    pygame.init()
    pygame.joystick.init()
    print("Pygame count : ", pygame.joystick.get_count())

    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print("Le EXTREME 3D PRO est prêt.")
        
        for i in range(joystick.get_numaxes()):
            if i == 0:  # Axe X
                axis_x_index = i  
            if i == 1 : # Axe Y
                axis_y_index = i  
            if i == 2 : # Axe Z
                axis_z_index = i
            if i == 3 : # Axe RZ
                axis_rz_index = i  

        # Calibration des axes
        calibration_data = {}
        
        axis_x_index = 0
        axis_y_index = 1
        axis_z_index = 2
        axis_rz_index = 3

        calibration_data['axe_x'] = calibrer_axe(joystick, axis_x_index, "X")
        calibration_data['axe_y'] = calibrer_axe(joystick, axis_y_index, "Y")
        calibration_data['axe_z'] = calibrer_axe(joystick, axis_z_index, "Z")
        calibration_data['axe_rz'] = calibrer_axe(joystick, axis_rz_index, "RZ")

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