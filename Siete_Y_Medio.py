mazo=[(1,"oros",1),(2,"oros",2),(3,"oros",3),(4,"oros",4),(5,"oros",5),(6,"oros",6),(7,"oros",7),(10,"oros",0.5),(11,"oros",0.5),(12,"oros",0.5),
      (1,"bastos",1),(2,"bastos",2),(3,"bastos",3),(4,"bastos",4),(5,"bastos",5),(6,"bastos",6),(7,"bastos",7),(10,"bastos",0.5),(11,"bastos",0.5),(12,"bastos",0.5),
      (1,"espadas",1),(2,"espadas",2),(3,"espadas",3),(4,"espadas",4),(5,"espadas",5),(6,"espadas",6),(7,"espadas",7),(10,"espadas",0.5),(11,"espadas",0.5),(12,"espadas",0.5),
      (1,"copas",1),(2,"copas",2),(3,"copas",3),(4,"copas",4),(5,"copas",5),(6,"copas",6),(7,"copas",7),(10,"copas",0.5),(11,"copas",0.5),(12,"copas",0.5)]

jugadores={}

import time
import random

flag_menu0=False
flag_menu1=False
flag_manual=False
mod_juego=""

def sum_mazo():  # Suma los puntos de el mazo de los jugadores
    global jugadores
    for i in jugadores.keys():
        suma_mazo=0
        for h in jugadores[i]['mano']:
            suma_mazo+=h[2]
        jugadores[i]['puntos mano']=suma_mazo

def robar_carta(i):
    opt_robar = input("Quieres robar una carta: s / n   ")
    if opt_robar == "s":  # Si decide Robar
        carta_robada = random.choice(mazo)
        jugadores[i]['mano'].append(carta_robada)
        mazo.remove(carta_robada)
        print("La carta que has robado es: ", carta_robada[0], "de", carta_robada[1])
        sum_mazo()

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

        for i in range(num_jugadores):  # Crea el diccionario de jugadores
            while True:
                nombre=input("Nombre del jugador "+str(i+1)+": ")
                if not nombre.isalnum() or not nombre[0].isalpha() or ' ' in nombre:  # Comprueba si el nombre es aceptable
                    print("Nombre no permitido")
                else:
                    jugadores[nombre]={}
                    jugadores[nombre]['mano']=[]
                    jugadores[nombre]['estado mano']="jugando"
                    jugadores[nombre]['estado partida']="jugando"
                    jugadores[nombre]['prioridad del jugador']=0
                    jugadores[nombre]['puntos mano']=0
                    jugadores[nombre]['puntos apostados']=0
                    jugadores[nombre]['puntos restantes']=20
                    break

        print("")
        print("Repartiendo las Cartas",end="")
        for i in range(3):  # Estetica de repartir cartas (Opcional)
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
        for i in range(len(jugadores_ord) - 1):  # Ordeno los jugadores por puntos
            for j in range(len(jugadores_ord) - i - 1):
                if jugadores_ord[j][1] > jugadores_ord[j + 1][1]:
                    a = jugadores_ord[j]
                    b = jugadores_ord[j + 1]
                    jugadores_ord[j] = b
                    jugadores_ord[j + 1] = a

        jugadores_ord=jugadores_ord[::-1]  # Le doy la vuelta a la lista para que quede en orden descendente de puntos
        banca=jugadores_ord[0][0]  # Escoje el jugador con mas puntos como la banca
        print("La banca es:",banca)
        jugadores[banca]['prioridad del jugador'] = 0

        count=1
        for h in range(1,len(jugadores_ord)):  # Cuenta la prioridad de los jugadores exceptuando la banca
            jugadores[jugadores_ord[h][0]]['prioridad del jugador']=count
            count+=1

        print("")

    # Mueve el primer jugador (la banca) al ultimo puesto para los turnos
    aux=jugadores_ord[0]
    jugadores_ord.pop(0)
    jugadores_ord.append(aux)

    while True:  # Empieza la partida /// Falta Cambiar la condicion para que acabe cuando gane alguien

            for i in jugadores_ord:
                i = i[0]
                print("")
                print("Turno del Jugador:",i)  # Indica el turno del jugador
                print("")

                if jugadores[i]['prioridad del jugador']!=0:
                    # Turno Jugador normal (No banca)
                    #if jugadores[i]['estado mano']=="jugando" and jugadores[i]['estado partida']=="jugando":
                    for h,l in jugadores.items():  # Printa las cartas y los puntos de cada uno de los jugadores
                        print("Cartas de", h, ":",end="")
                        for g in jugadores[h]['mano']:  # Printa las cartas de la mano del jugador
                            print(g[0],"de",g[1], end=" ")
                        print("")
                        print("Puntos de",h,":",jugadores[h]['puntos restantes'])
                        print("")

                    while True: # Hasta que no ponga a o b se repatira el bucle
                        opt_apuesta=input("Realiza una apuesta o plantarse? a / p   ")  # Pregunta si apostar o plantarse

                        if opt_apuesta=="a":  # Si decide apostar
                            apuesta = float(input("Cuanto quieres apostar: "))
                            jugadores[i]['puntos apostados'] = apuesta
                            jugadores[i]['puntos restantes'] = jugadores[i]['puntos restantes'] - apuesta

                            if jugadores[i]['puntos mano'] > 7.5 and banca != jugadores[i]:  # Si el jugador tiene mas de 7.5 puntos, el estado de la mano pasa a eliminado
                                jugadores[i]['estado mano'] = "eliminado"
                                jugadores[banca]['puntos restantes'] += jugadores[i]['puntos apostados']
                            robar_carta(i)
                            break
                        elif opt_apuesta=="p":  # Si decide plantarse
                            jugadores[i]['estado partida'] = "plantado"
                            robar_carta(i)
                            break

                        else:
                            print("Opcion incorrecra")

                        if jugadores[i]['puntos restantes'] <= 0:  # Si el jugador tiene menos o 0 puntos, su estado de partida pasa a eliminado
                            jugadores[i]['estado partida'] = "eliminado"
                            print(i, "esta eliminado de la partida")
                            for r in jugadores_ord:  # Elimina el jugador de la lista para que no tenga turno
                                if i in r:
                                    jugadores_ord.remove(r)
                                    print(jugadores_ord)


                else:
                    # Turno de la Banca
                    for h,l in jugadores.items():  # Printa las cartas y los puntos de cada uno de los jugadores
                        print("Cartas de", h, ":",end="")
                        for g in jugadores[h]['mano']:
                            print(g[0],"de",g[1], end=" ")
                        print()
                        print("Puntos de",h,":",jugadores[h]['puntos restantes'])
                        print()

                    while True: # Hasta que no ponga p o r se repatira el bucle
                        opt_apuesta=input("Plantarse o Robar? p / r   ")

                        if opt_apuesta=="p":  # Si decide plantarse
                            jugadores[i]['estado partida'] = "plantado"
                            break
                        elif opt_apuesta=="r":  # Si decide robar
                            carta_robada = random.choice(mazo)
                            jugadores[i]['mano'].append(carta_robada)
                            mazo.remove(carta_robada)
                            print("La carta que has robado es: ",carta_robada[0],"de",carta_robada[1])
                            sum_mazo()
                        else:
                            print("Opcion incorrecra")

            if jugadores[i]['puntos restantes']==20*len(jugadores.keys()):  # Condicion de ganada no acabada
                print("Ganador", jugadores[i])
    else:
        print("Esoje entre 2-8 jugadores.")

#elif mod_juego=="Maquina":


