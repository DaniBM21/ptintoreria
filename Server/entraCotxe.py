# -*- coding: utf-8 -*-
#!/usr/bin/python3


import socket
import sys
import requests
import json
import os
import shutil

hostname = socket.gethostname()
hostname = hostname.strip()


try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_address = ('0.0.0.0', 140)
	sock.bind(server_address)
except Exception as e:
	print ("No s'ha pogut establir la conexió amb la barrera")
	res = "1,9"
	sent = sock.sendto(bytes(res.encode("utf-8")), ('10.90.0.18',120))

while True:
	print ('\nwaiting to receive message')

	try:
		mat, address = sock.recvfrom(100)
		mat = bytes(mat).decode("utf-8")
		print(mat)
	except Exception as e:
		print ("No s'ha pogut llegir la matrícula")
		res = "1,9"
		sent = sock.sendto(bytes(res.encode("utf-8")), ('10.90.0.18',120))

	#Rebem la matricula
	if mat:

		try:
			body = {"matricula": mat, "parkingID": hostname[-1]}
			request = requests.get('https://10.100.0.1:3002/api/comprovar-reserva-cotxe', data= body, verify = False)
			reserva = request.json()
			print(reserva)
			print(reserva['status'])
		except Exception as e:
			print ("No s'ha pogut comprovar la reserva de la matricula")
			res = "1,No s'ha pogut comprovar la reserva de la matricula"
			sent = sock.sendto(bytes(res.encode("utf-8")), ('10.90.0.18',120))


		#Comprovem status de la reserva
		if(reserva['status'] == 0):
			sPath = "/root/matriculasComprovar/"
			end = ".txt"
			dPath = "/root/matriculasValidas/"
			sPath = sPath + str(mat) + end
			dPath = dPath + str(mat) + end
			os.system('touch {}'.format(sPath))
			os.rename(sPath, dPath)

			# Preguntem la plaça disponible
			try:
				request2 =  requests.post('https://10.100.0.1:3002/api/introduir-cotxe-parking', data = body, verify = False)
				plaza = request2.json()
				print(request2.status_code)
				print(plaza)
			#Enviem OK a l'entrada del cotxe amb la plaça

				res = "0,"+str(plaza['plazaID'])
				print(plaza['plazaID'])
				sent = sock.sendto(bytes(res.encode("utf-8")), ('10.90.0.18',120))
			except Exception as e:
			#else:
				print ("Error al enviar OK a la barrera")
				res = "1,PlazaID no disponible"
				sent = sock.sendto(bytes(res.encode("utf-8")), ('10.90.0.18',120))


		else:
			#Informem que no pot passar a la barrera
			try:
				res = "1,El cotxe no té reserva. No pot entrar"
				sent = sock.sendto(bytes(res.encode("utf-8")), ('10.90.0.18',120))
				print("El cotxe no té reserva. No pot entrar")
			except Exception as e:
				sys.exit("Error al enviar codi de negació de matrícula a la barrera: " +str(e))
	break
