#!/bin/bash

#Guardem el la nostra matricula en una variable
matricula=$(cat /root/log/accLog.txt | sed -n '3p')

#Executem l'script dels recursos
/root/systemInfo.sh

#Enviem un txt amb els recursos al servidor
scp /root/log/$matricula.txt root@10.10.6.1:/root/matriculasComprovar

#Creem el directori pels arxius de computació en cas de que no existeixi
mkdir -p /root/comp

while :
do
	#Recorrem tots els fitxers a computar
	for x in `ls /root/comp/`; do

		#Li donem permissos d'execució al fitxer
		chmod +x /root/comp/$x

		arxiuResultant="${x::-3}"
		#L'executem i guardem el resultat en un txt
		python3 /root/comp/$x > $matricula--$arxiuResultant.txt

		#Enviem el resultat al servidor
		scp $matricula--$arxiuResultant.txt root@10.10.6.1:/root/executed

		#Esborrem el fitxer i el .txt generat per no tornar-lo a computar
		rm /root/comp/$x $matricula--$arxiuResultant.txt
	done
	sleep 5

done
