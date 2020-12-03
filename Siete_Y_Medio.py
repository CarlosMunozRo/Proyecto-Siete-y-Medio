mazo=[(1,"oros",1),(2,"oros",2),(3,"oros",3),(4,"oros",4),(5,"oros",5),(6,"oros",6),(7,"oros",7),(10,"oros",0.5),(11,"oros",0.5),(12,"oros",0.5),
      (1,"bastos",1),(2,"bastos",2),(3,"bastos",3),(4,"bastos",4),(5,"bastos",5),(6,"bastos",6),(7,"bastos",7),(10,"bastos",0.5),(11,"bastos",0.5),(12,"bastos",0.5),
      (1,"espadas",1),(2,"espadas",2),(3,"espadas",3),(4,"espadas",4),(5,"espadas",5),(6,"espadas",6),(7,"espadas",7),(10,"espadas",0.5),(11,"espadas",0.5),(12,"espadas",0.5),
      (1,"copas",1),(2,"copas",2),(3,"copas",3),(4,"copas",4),(5,"copas",5),(6,"copas",6),(7,"copas",7),(10,"copas",0.5),(11,"copas",0.5),(12,"copas",0.5)]
# Sota, Caballo, Rey son medio punto cada una
jugadores={}

import time
import random


flag_menu0=False
flag_menu1=False
flag_manual=False
mod_juego=""

def sum_mazo():
    global jugadores
    for i in jugadores.keys():
        suma_mazo=0
        for h in jugadores[i]['mano']:
            suma_mazo+=h[2]
        jugadores[i]['puntos mano']=suma_mazo  # Suma los puntos de el mazo de los jugadores



while not flag_menu1:
    opt_menu1=int(input("\n1. Juego Manual\n2. Contra La Maquina\n3. Salir\n\nEscoje una opcion: "))

    if opt_menu1==1:
        mod_juego="Manual"
        flag_menu1=True
    elif opt_menu1==2:
        mod_juego="Maquina"
    elif opt_menu1==3:
        flag_menu1=True
    else:
        print("Opcion incorrecta")

if mod_juego=="Manual":

    num_jugadores=int(input("Cuantos Jugadores van a Jugar: "))

    if num_jugadores>=2 and num_jugadores<=8:

        for i in range(num_jugadores):
            nombre=input("Nombre del jugador "+str(i+1)+": ")

            jugadores[nombre]={}
            jugadores[nombre]['mano']=[]
            jugadores[nombre]['estado mano']="jugando"
            jugadores[nombre]['estado partida']="jugando"
            jugadores[nombre]['prioridad del jugador']=0
            jugadores[nombre]['puntos mano']=0
            jugadores[nombre]['puntos apostados']=0
            jugadores[nombre]['puntos restantes']=20

        print("")
        print("Repartiendo las Cartas",end="")
        for i in range(3):
            time.sleep(0.5)
            print(".",end="")
        print("")


        for i in jugadores.keys():
            carta_robada=random.choice(mazo)
            jugadores[i]['mano'].append(carta_robada)   # Primera repartida de Cartas
            mazo.remove(carta_robada)

        sum_mazo()

        jugadores_ord=[] # Se crea una lista para almazenar los jugadores ordenados por puntos

        for i,j in jugadores.items():
            jugadores_ord.append((i,j['puntos mano']))  # Añado a los jugadores y sus puntos a la lista


        count = 0
        for i in range(len(jugadores_ord) - 1):
            for j in range(len(jugadores_ord) - i - 1):
                if jugadores_ord[j][1] > jugadores_ord[j + 1][1]:  # Los ordeno por puntos
                    a = jugadores_ord[j]
                    b = jugadores_ord[j + 1]
                    jugadores_ord[j] = b
                    jugadores_ord[j + 1] = a


        jugadores_ord=jugadores_ord[::-1]  # Le doy la vuelta a la lista para que quede en orden descendente de puntos
        print(jugadores_ord)
        banca=jugadores_ord[0][0]  # Escoje el jugador con mas puntos como la banca
        print("La banca es:",banca)
        jugadores[banca]['prioridad del jugador'] = 0

        count=1
        for h in range(1,len(jugadores_ord)):
            jugadores[jugadores_ord[h][0]]['prioridad del jugador']=count  # Cuenta la prioridad de los jugadores exceptuando la banca
            count+=1

        print("")

        '''
        for i in jugadores.keys():
            carta_robada=random.choice(mazo)
            jugadores[i]['mano'].insert(0,carta_robada) # Se les da otra carta a todos
            mazo.remove(carta_robada)
            sum_mazo()
        '''

        for i in jugadores_ord[1:]:
            i = i[0]
            print("")
            print("Turno del Jugador:",i)
            print("")
            if jugadores[i]['prioridad del jugador']!=0:
                if jugadores[i]['estado mano']=="jugando" and jugadores[i]['estado partida']=="jugando":
                    for h,l in jugadores.items():
                        print("Cartas de", h, ":",end="")
                        for g in jugadores[h]['mano']:
                            print(g[0],"de",g[1], end=" ")
                        print()
                        print("Puntos de",h,":",jugadores[h]['puntos restantes'])

                while True:
                    opt_apuesta=input("Realiza una apuesta o plantarse? a / p   ")

                    if opt_apuesta=="a":
                        apuesta = float(input("Cuanto quieres apostar: "))
                        jugadores[i]['puntos apostados'] = apuesta
                        jugadores[i]['puntos restantes'] = jugadores[i]['puntos restantes'] - apuesta
                        if jugadores[i]['puntos restantes'] <= 0:
                            jugadores[i]['estado partida'] = "eliminado"
                        carta_robada = random.choice(mazo)
                        jugadores[i]['mano'].append(carta_robada)
                        mazo.remove(carta_robada)
                        sum_mazo()
                        if jugadores[i]['puntos mano'] > 7.5 and banca != jugadores[i]:
                            jugadores[i]['estado mano'] = "eliminado"
                            jugadores[banca]['puntos restantes'] += jugadores[i]['puntos apostados']
                        if jugadores[i]['puntos restantes'] <= 0:
                            jugadores[i]['estado partida'] = "eliminado"
                            print(i,"esta eliminado de la partida")
                            for r in jugadores_ord:
                                if i in r:
                                    jugadores_ord.remove(r)
                                    print(jugadores_ord)
                        break
                    elif opt_apuesta=="p":
                        jugadores[i]['estado partida'] = "plantado"
                        break
                    else:
                        print("Opcion incorrecra")

        else:
            i=banca
            print("")
            print("Turno del Jugador:",i)
            print("")


            if jugadores[i]['estado mano']=="jugando" and jugadores[i]['estado partida']=="jugando":
                for h,l in jugadores.items():
                    print("Cartas de", h, ":",end="")
                    for g in jugadores[h]['mano']:
                        print(g, end=" ")
                    print()
                    print("Puntos de",h,":",jugadores[h]['puntos restantes'])

            while True:
                opt_apuesta=input("Realiza una apuesta o plantarse? a / p   ")

                if opt_apuesta=="a":
                    apuesta = float(input("Cuanto quieres apostar: "))
                    jugadores[i]['puntos apostados'] = apuesta
                    jugadores[i]['puntos restantes'] = jugadores[i]['puntos restantes'] - apuesta
                    if jugadores[i]['puntos restantes'] <= 0:
                        jugadores[i]['estado partida'] = "eliminado"
                    carta_robada = random.choice(mazo)
                    jugadores[i]['mano'].append(carta_robada)
                    mazo.remove(carta_robada)
                    sum_mazo()
                    if jugadores[i]['puntos mano'] > 7.5 and banca != jugadores[i]:
                        jugadores[i]['estado mano'] = "eliminado"
                        jugadores[banca]['puntos restantes'] += jugadores[i]['puntos apostados']
                    if jugadores[i]['puntos restantes'] >= 0:
                        jugadores[i]['estado partida'] = "eliminado"
                        print(i, "esta eliminado de la partida")
                        for r in jugadores_ord:
                            if jugadores[i] in r:
                                jugadores_ord.remove(r)
                                print(jugadores_ord)
                    break
                elif opt_apuesta=="p":
                    jugadores[i]['estado partida'] = "plantado"
                    break
                else:
                    print("Opcion incorrecra")

    else:
        print("Esoje entre 2-8 jugadores.")



#elif mod_juego=="Maquina":


