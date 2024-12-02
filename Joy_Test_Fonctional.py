import socket
import time
import pygame
import sys
import struct
import json

# Fonction pour lire les données JSON à partir du fichier
def lire_donnees_calibration():
    try:
        with open('donnees.json', 'r') as fichier:
            donnees = json.load(fichier)
            return donnees
    except FileNotFoundError:
        print("Le fichier 'donnees.json' n'a pas été trouvé.")
    except json.JSONDecodeError:
        print("Erreur lors de la lecture des données JSON.")
    
    return None


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
                axis_rz_index = i
            if i == 3 : # Axe RZ
                axis_z_index = i  

        
        # Exemple d'utilisation
        donnees_calibration = lire_donnees_calibration()

        if donnees_calibration:
            
            valeur_initiale_x = donnees_calibration['calibration']['axe_x']['valeur_initiale']
            valeur_max_x = donnees_calibration['calibration']['axe_x']['valeur_max']
            valeur_max_apres_x = donnees_calibration['calibration']['axe_x']['valeur_max_apres']
            valeur_min_x = donnees_calibration['calibration']['axe_x']['valeur_min']
            valeur_min_apres_x = donnees_calibration['calibration']['axe_x']['valeur_min_apres']

            valeur_initiale_y = donnees_calibration['calibration']['axe_y']['valeur_initiale']
            valeur_max_y = donnees_calibration['calibration']['axe_y']['valeur_max']
            valeur_max_apres_y = donnees_calibration['calibration']['axe_y']['valeur_max_apres']
            valeur_min_y = donnees_calibration['calibration']['axe_y']['valeur_min']
            valeur_min_apres_y = donnees_calibration['calibration']['axe_y']['valeur_min_apres']

            valeur_initiale_z = donnees_calibration['calibration']['axe_z']['valeur_initiale']
            valeur_max_z = donnees_calibration['calibration']['axe_z']['valeur_max']
            valeur_max_apres_z = donnees_calibration['calibration']['axe_z']['valeur_max_apres']
            valeur_min_z = donnees_calibration['calibration']['axe_z']['valeur_min']
            valeur_min_apres_z = donnees_calibration['calibration']['axe_z']['valeur_min_apres']

            valeur_initiale_rz = donnees_calibration['calibration']['axe_rz']['valeur_initiale']
            valeur_max_rz = donnees_calibration['calibration']['axe_rz']['valeur_max']
            valeur_max_apres_rz = donnees_calibration['calibration']['axe_rz']['valeur_max_apres']
            valeur_min_rz = donnees_calibration['calibration']['axe_rz']['valeur_min']
            valeur_min_apres_rz = donnees_calibration['calibration']['axe_rz']['valeur_min_apres']



        running = True
    
        axis_z_value = 0.0
        axis_x_value = 0.0
        axis_y_value = 0.0
        axis_rz_value = 0.0


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.JOYBUTTONDOWN and event.button == 0): #Bouton d'arret du code sur la gachette du joy
                    running = False
                elif event.type == pygame.JOYBUTTONDOWN and event.joy == 0:
                    print(" Bouton", event.button, "appuyé.")
            
            pygame.event.pump()

            #Recuperation des donnes
            axis_z_value = joystick.get_axis(axis_z_index)
            axis_x_value = joystick.get_axis(axis_x_index)
            axis_y_value = joystick.get_axis(axis_y_index)
            axis_rz_value = joystick.get_axis(axis_rz_index)

            #Calibration des donnes
            factor = 100 #echelle des valeur (Permet d'avoir les valeur en 53.0 au lieu de 0.867875877848748

            #Axe X
            valeur_max_0_x = max(valeur_min_apres_x, valeur_initiale_x, valeur_max_apres_x)
            valeur_min_0_x = min(valeur_min_apres_x, valeur_initiale_x, valeur_max_apres_x)
            if axis_x_value <= valeur_max_0_x and axis_x_value >= valeur_min_0_x:
                axis_x_value = 0.0
            else:
                if(axis_x_value < 0):
                    a = (-factor/(valeur_min_x-valeur_min_0_x))
                    b = a*valeur_min_0_x
                    axis_x_value = (a*axis_x_value) + b  #fonction affine f(x) = ax +b
                else:
                    a = (factor/(valeur_max_x-valeur_max_0_x))
                    b = a*valeur_max_0_x
                    axis_x_value = (a*axis_x_value) + b

            #Axe Y
            valeur_max_0_y = max(valeur_min_apres_y, valeur_initiale_y, valeur_max_apres_y)
            valeur_min_0_y = min(valeur_min_apres_y, valeur_initiale_y, valeur_max_apres_y)
            if axis_y_value <= valeur_max_0_y and axis_y_value >= valeur_min_0_y:
                axis_y_value = 0.0
            else:
                if(axis_y_value < 0):
                    a = (-factor/(valeur_min_y-valeur_min_0_y))
                    b = a*valeur_min_0_y
                    axis_y_value = (a*axis_y_value) + b  #fonction affine f(x) = ax +b
                else:
                    a = (factor/(valeur_max_y-valeur_max_0_y))
                    b = a*valeur_max_0_y
                    axis_y_value = (a*axis_y_value) + b

            #Axe Z
            valeur_max_0_z = max(valeur_min_apres_z, valeur_initiale_z, valeur_max_apres_z)
            valeur_min_0_z = min(valeur_min_apres_z, valeur_initiale_z, valeur_max_apres_z)
            if axis_z_value <= valeur_max_0_z and axis_z_value >= valeur_min_0_z:
                axis_z_value = 0.0
            else:
                if(axis_z_value < 0):
                    a = (-factor/(valeur_min_z-valeur_min_0_z))
                    b = a*valeur_min_0_z
                    axis_z_value = (a*axis_z_value) + b  #fonction affine f(x) = ax +b
                else:
                    a = (factor/(valeur_max_z-valeur_max_0_z))
                    b = a*valeur_max_0_z
                    axis_z_value = (a*axis_z_value) + b
            
            #Axe RZ
            valeur_max_0_rz = max(valeur_min_apres_rz, valeur_initiale_rz, valeur_max_apres_rz)
            valeur_min_0_rz = min(valeur_min_apres_rz, valeur_initiale_rz, valeur_max_apres_rz)
            if axis_rz_value <= valeur_max_0_rz and axis_rz_value >= valeur_min_0_rz:
                axis_rz_value = 0.0
            else:
                if(axis_rz_value < 0):
                    a = (-factor/(valeur_min_rz-valeur_min_0_rz))
                    b = a*valeur_min_0_rz
                    axis_rz_value = (a*axis_rz_value) + b  #fonction affine f(x) = ax +b
                else:
                    a = (factor/(valeur_max_rz-valeur_max_0_rz))
                    b = a*valeur_max_0_rz
                    axis_rz_value = (a*axis_rz_value) + b

            axis_rz_value = round(axis_rz_value, 0) #Permet d'avoir les valeur en 53.0 au lieu de 53.867875877848748
            axis_z_value = round(axis_z_value, 0)
            axis_x_value = round(axis_x_value, 0)
            axis_y_value = round(axis_y_value, 0)

            #Definition de la zone morte utile
            if abs(axis_z_value) < 10:
                axis_z_value = 0.0
            if abs(axis_x_value) < 10:
                axis_x_value = 0.0
            if abs(axis_y_value) < 10:
                axis_y_value = 0.0
            if abs(axis_rz_value) < 25:
                axis_rz_value = 0.0

            print(f"\rX: {axis_x_value} Y: {axis_y_value} Z: {axis_z_value} RZ: {axis_rz_value}", end=" ", flush=True)

            time.sleep(0.1)

        pygame.quit()
        sys.exit()
mvt()

# Faire test avec RaspBerry et Led