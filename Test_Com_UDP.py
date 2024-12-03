import socket
import struct
import time

# Créer un socket UDP pour IPv6
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Adresse du serveur (IPv6 loopback)
server_address = ("192.168.137.245", 8080)

# Données à envoyer
data = struct.pack('f', 123.45)  # Exemple : un float

try:
    for i in range(1233):  # Envoie plusieurs messages pour tester
        s.sendto(data, server_address)
        print(f"Message envoyé à {server_address}")
        time.sleep(1)
except Exception as e:
    print(f"Erreur lors de l'envoi des données : {e}")
finally:
    s.close()
