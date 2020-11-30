mazo=[(1,"oros",1),(2,"oros",2),(3,"oros",3),(4,"oros",4)]
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
        for h in jugadores[i]['valor']:
            suma_mazo+=h[2]
        jugadores[i]['mano']=suma_mazo



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

    for i in range(num_jugadores):
        nombre=input("Nombre del jugador "+str(i+1)+": ")

        jugadores[nombre]={}
        jugadores[nombre]['valor']=[]
        jugadores[nombre]['estado mano']=40
        jugadores[nombre]['estado partida']=""
        jugadores[nombre]['prioridad del jugador']=""
        jugadores[nombre]['puntos mano']=0
        jugadores[nombre]['puntos apostados']=0
        jugadores[nombre]['puntos restantes']=0
        jugadores[nombre]['mano']=0



    print("Repartiendo las Cartas",end="")
    for i in range(5):
        time.sleep(0.5)
        print(".",end="")
    print()


    # Primera repartida de Cartas
    for i in jugadores.keys():
        jugadores[i]['valor'].append(random.choice(mazo))

    sum_mazo() # Suma los puntos de el mazo de los jugadores

    jugadores_ord=[]

    for i,j in jugadores.items():
        jugadores_ord.append((i,j['mano']))


    count = 0
    for i in range(len(jugadores_ord) - 1):
        for j in range(len(jugadores_ord) - i - 1):
            if jugadores_ord[j][1] > jugadores_ord[j + 1][1]:
                a = jugadores_ord[j]
                b = jugadores_ord[j + 1]
                jugadores_ord[j] = b
                jugadores_ord[j + 1] = a


    jugadores_ord=jugadores_ord[::-1]
    banca=jugadores_ord[0][0]  # Escoje el jugador con mas puntos como la banca
    print("La banca es:",banca)
    jugadores[banca]['estado mano'] = 0
    count=1
    for h in range(1,len(jugadores_ord)):   # Cuenta la prioridad de los jugadores exceptuando la banca
        jugadores[jugadores_ord[h][0]]['estado mano']=count
        count+=1



#elif mod_juego=="Maquina":


