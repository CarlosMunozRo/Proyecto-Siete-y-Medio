
import random
import xml.etree.ElementTree as et
from xml.dom import minidom

flag_menu1=False
flag_ganador=False

mazo=[]
mazo_backup=[]

jugadores={}

orden=[("Oros",1),("Copas",2),("Espadas",3),("Bastos",4)]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

tree=et.parse('Basic_Config_Game.xml')
root=tree.getroot()
count_normas=1
min_players=0
max_players=0
max_rounds=0
initial_points=0
allow_auto=""
for child in root:
    if count_normas==1:
        min_players=child.text
    elif count_normas==2:
        max_players=child.text
    elif count_normas==3:
        max_rounds=child.text
    elif count_normas==4:
        initial_points=child.text
    elif count_normas==5:
        allow_auto=child.text
    count_normas+=1

min_players=int(min_players)
max_players=int(max_players)
max_rounds=int(max_rounds)
initial_points=int(initial_points)

def sacar_mazo():
    global mazo
    global mazo_backup
    tree = et.parse('Cartas.xml')
    root = tree.getroot()
    for child in root:
        if child[4].text == "SI":
            mazo.append((int(child[1].text), child[2].text, float(child[3].text)))

    mazo_backup=mazo

sacar_mazo()

def reset_mazo():
    global mazo
    global mazo_backup
    mazo =[]
    for cartas in mazo_backup:
        mazo.append(cartas)


def sum_mazo():  # Suma los puntos de el mazo de los jugadores
    global jugadores
    for i in jugadores.keys():
        suma_mazo=0
        for h in jugadores[i]['mano']:
            suma_mazo+=h[2]
        jugadores[i]['puntos mano']=suma_mazo

def robar_ia(i):
    global jugadores
    global mazo
    sum_mazo()
    cartas_restantes=len(mazo)
    cartas_pasa_siete=0
    print("\tTe toco", jugadores[i]['mano'][0][2], "de", jugadores[i]['mano'][0][1], "y", jugadores[i]['puntos mano'],"puntos del mazo")
    while True:
        for cartas in mazo:
            if jugadores[i]['puntos mano']+cartas[2]<7.5:
                cartas_pasa_siete+=1
        probabilidad_pasarse=(cartas_pasa_siete/cartas_restantes)*100  # Probabilidad de no pasarse

        if probabilidad_pasarse>65 and jugadores[i]['estado mano']=="jugando":  # Si la probabilidad de no pasarnos es mayor de un 65% pediremos carta con total seguridad.
            carta_robada = random.choice(mazo)
            jugadores[i]['mano'].insert(0, carta_robada)
            mazo.remove(carta_robada)
            sum_mazo()
            print("\tTe toco", jugadores[i]['mano'][0][2], "de", jugadores[i]['mano'][0][1], "y", jugadores[i]['puntos mano'],
                  "puntos del mazo")
            if jugadores[i]['puntos mano'] > 7.5:
                print(f"{bcolors.FAIL}Te has pasado.{bcolors.ENDC}")
                jugadores[i]['estado mano'] = "plantado"
                break

        elif probabilidad_pasarse<65 and probabilidad_pasarse>50:  # Si está entre un 50 y un 65%, esta será la probabilidad con la que pediremos carta.

            random_robar=random.randint(1,100)

            if random_robar<probabilidad_pasarse:
                carta_robada = random.choice(mazo)
                jugadores[i]['mano'].insert(0, carta_robada)
                mazo.remove(carta_robada)
                sum_mazo()
                print("\tTe toco", jugadores[i]['mano'][0][2], "de", jugadores[i]['mano'][0][1], "y",
                      jugadores[i]['puntos mano'],
                      "puntos del mazo")
                if jugadores[i]['puntos mano'] > 7.5:
                    print(f"{bcolors.FAIL}Te has pasado.{bcolors.ENDC}")
                    jugadores[i]['estado mano'] = "plantado"
                    break
            else:
                break

        elif probabilidad_pasarse<50:  # Si es menor de un 50%, dividiremos esta probabilidad entre 3, y como resultado nos dará la probabilidad con la que pediremos carta.

            probabilidad_pasarse=probabilidad_pasarse/3

            random_robar = random.randint(1, 100)

            if random_robar < probabilidad_pasarse:
                carta_robada = random.choice(mazo)
                jugadores[i]['mano'].insert(0, carta_robada)
                mazo.remove(carta_robada)
                sum_mazo()
                print("\tTe toco", jugadores[i]['mano'][0][2], "de", jugadores[i]['mano'][0][1], "y",jugadores[i]['puntos mano'],"puntos del mazo")
                if jugadores[i]['puntos mano'] > 7.5:
                    print(f"{bcolors.FAIL}Te has pasado.{bcolors.ENDC}")
                    jugadores[i]['estado mano'] = "plantado"
                    break
            else:
                break

def apostar_ia(min,max):
    random_apostar=random.randint(min,max)
    jugadores[i]['puntos apostados']=random_apostar
    jugadores[i]['puntos restantes']-=random_apostar
    print(f"{bcolors.UNDERLINE}{i}{bcolors.ENDC} a apostado: {bcolors.OKBLUE}{random_apostar}{bcolors.ENDC}")

while not flag_menu1:
    while True:
        try:
            opt_menu1=int(input("\n1. Juego Manual\n2. Contra La Maquina\n3. Salir\n\nEscoje una opcion: "))
        except:
            print("Tiene que ser un numero")
        else:
            break

    if opt_menu1==1:
        mod_juego="Manual"
        flag_menu1=True
    elif opt_menu1==2:
        mod_juego="Maquina"
        flag_menu1=True
    elif opt_menu1==3:
        mod_juego=""
        flag_menu1=True
    else:
        print("Opcion incorrecta")

if mod_juego=="Manual" or mod_juego=="Maquina":

    if mod_juego=="Manual":
        while True:
            try:
                while True:
                    num_jugadores = int(input("Cuantos Jugadores van a Jugar 2/8: "))
                    if num_jugadores>max_players or num_jugadores<min_players:
                        print("Numero de jugadores incorrecta.")
                    else:
                        break
            except:
                print("Tiene que ser un numero")
            else:
                break
    else:
        while True:
            try:
                while True:
                    num_jugadores = int(input("Cuantos Jugadores van a Jugar 2/8: "))
                    if num_jugadores>max_players or num_jugadores<min_players:
                        print("Numero de jugadores incorrecta.")
                    else:
                        break

                while True:
                    while True:
                        try:
                            num_ia= int(input("Cuantas jugadores son maquinas  (min 1): "))
                        except:
                            print("Tiene que ser un numero.")
                        else:
                            break
                    print(num_jugadores, max_players,num_ia)

                    if num_ia == 0:
                        print("Tiene que haber minimo 1 ia.")
                    else:
                        break

            except:
                print("Tiene que ser un numero")
            else:
                break

    if num_jugadores >= min_players and num_jugadores <= max_players and mod_juego=="Manual": # Modo Manual

        for i in range(num_jugadores):  # Crea el diccionario de jugadores
            while True:
                while True:
                    try:
                        nombre = input("Nombre del jugador " + str(i + 1) + ": ")
                    except:
                        print("Entrada invalida")
                    else:
                        break
                if not nombre.isalnum() or not nombre[0].isalpha() or ' ' in nombre:  # Comprueba si el nombre es aceptable
                    print("Nombre no permitido")
                else:
                    jugadores[nombre] = {}
                    jugadores[nombre]['mano'] = []
                    jugadores[nombre]['estado mano'] = "jugando"
                    jugadores[nombre]['estado partida'] = "jugando"
                    jugadores[nombre]['prioridad del jugador'] = 0
                    jugadores[nombre]['puntos mano'] = 0
                    jugadores[nombre]['puntos apostados'] = 0
                    jugadores[nombre]['puntos restantes'] = initial_points
                    jugadores[nombre]['ia']=0  # Si 0 es jugador, 1 si es ia
                    break

    if num_jugadores >= min_players and num_jugadores <= max_players and mod_juego=="Maquina": # Modo Maquina

        for i in range(num_jugadores-num_ia):  # Crea el diccionario de jugadores
            while True:
                while True:
                    try:
                        nombre = input("Nombre del jugador " + str(i + 1) + ": ")
                    except:
                        print("Entrada invalida")
                    else:
                        break
                if not nombre.isalnum() or not nombre[0].isalpha() or ' ' in nombre:  # Comprueba si el nombre es aceptable
                    print("Nombre no permitido")
                else:
                    jugadores[nombre] = {}
                    jugadores[nombre]['mano'] = []
                    jugadores[nombre]['estado mano'] = "jugando"
                    jugadores[nombre]['estado partida'] = "jugando"
                    jugadores[nombre]['prioridad del jugador'] = 0
                    jugadores[nombre]['puntos mano'] = 0
                    jugadores[nombre]['puntos apostados'] = 0
                    jugadores[nombre]['puntos restantes'] = initial_points
                    jugadores[nombre]['ia']=0  # Si 0 es jugador, 1 si es ia
                    break

        for i in range(num_ia):  # Crea el diccionario de jugadores
            while True:
                while True:
                    try:
                        nombre = input("Nombre de la maquina " + str(i + 1) + ": ")
                    except:
                        print("Entrada invalida")
                    else:
                        break
                if not nombre.isalnum() or not nombre[0].isalpha() or ' ' in nombre:  # Comprueba si el nombre es aceptable
                    print("Nombre no permitido")
                else:
                    jugadores[nombre] = {}
                    jugadores[nombre]['mano'] = []
                    jugadores[nombre]['estado mano'] = "jugando"
                    jugadores[nombre]['estado partida'] = "jugando"
                    jugadores[nombre]['prioridad del jugador'] = 0
                    jugadores[nombre]['puntos mano'] = 0
                    jugadores[nombre]['puntos apostados'] = 0
                    jugadores[nombre]['puntos restantes'] = initial_points
                    jugadores[nombre]['ia']=1  # Si 0 es jugador, 1 si es ia
                    break

    else:
        print("Demasiados jugadores.")

    for i in jugadores.keys():
        carta_robada = random.choice(mazo)
        jugadores[i]['mano'].append(carta_robada)  # Primera repartida de Cartas
        mazo.remove(carta_robada)

    sum_mazo()

    jugadores_ord = []  # Se crea una lista para almazenar los jugadores ordenados por puntos

    for i, j in jugadores.items():
        jugadores_ord.append((i, j['puntos mano']))  # Añado a los jugadores y sus puntos a la lista

    count = 0
    for i in range(len(jugadores_ord) - 1):  # Ordeno los jugadores por puntos
        for j in range(len(jugadores_ord) - i - 1):
            if jugadores_ord[j][1] > jugadores_ord[j + 1][1]:
                a = jugadores_ord[j]
                b = jugadores_ord[j + 1]
                jugadores_ord[j] = b
                jugadores_ord[j + 1] = a


    count=1
    for i in range(len(jugadores_ord)):

        if count>1:
            print(jugadores[jugadores_ord[i - 1][0]]['mano'][0][1],jugadores[jugadores_ord[i][0]]['mano'][0][1])
            if jugadores[jugadores_ord[i][0]]['mano'][0][1]==jugadores[jugadores_ord[i-1][0]]['mano'][0][1]:
                print("")

        count+=1

    jugadores_ord = jugadores_ord[::-1]  # Le doy la vuelta a la lista para que quede en orden descendente de puntos
    banca = jugadores_ord[0][0]  # Escoje el jugador con mas puntos como la banca
    print("La banca es:", banca)
    jugadores[banca]['prioridad del jugador'] = 0
    print("")

    count = 1
    for h in range(1, len(jugadores_ord)):  # Cuenta la prioridad de los jugadores exceptuando la banca
        jugadores[jugadores_ord[h][0]]['prioridad del jugador'] = count
        count += 1

    aux=jugadores_ord[0]
    jugadores_ord.pop(0)
    jugadores_ord.append(aux)


    contador_mano=1
    while contador_mano<=max_rounds and flag_ganador==False:
        reset_mazo()
        for i in jugadores.keys():
            jugadores[i]['mano']=[]
            jugadores[i]['puntos mano'] = 0
            jugadores[i]['estado mano'] = "jugando"

        for i in jugadores.keys():
            carta_robada = random.choice(mazo)
            jugadores[i]['mano'].append(carta_robada)  # Primera repartida de Cartas
            mazo.remove(carta_robada)

        contador_mano+=1
        for i in jugadores_ord:
            print("")
            if contador_mano < 30 * 1 / 4:  # Se determina el min y max de puntos a apostar
                min = 2
                max = 5
            elif contador_mano < 30 * 1 / 2:
                min = 3
                max = 7
            elif contador_mano < 30 * 3 / 4:
                min = 4
                max = 9
            else:
                min = 6
                max = 12

            i=i[0]
            print(f"El turno es de: {bcolors.UNDERLINE}{bcolors.BOLD}{i}{bcolors.ENDC}")

            if jugadores[i]['prioridad del jugador']!=0: #  Si no es la vanca
                if jugadores[i]['ia']==0:
                    #Turno de jugador
                    sum_mazo()

                    print("\tTe toco",jugadores[i]['mano'][0][2],"de",jugadores[i]['mano'][0][1],"y",jugadores[i]['puntos mano'],"puntos del mazo")

                    print("Apuesta entre", min,"/", max)

                    while True:
                        while True:
                            try:
                                apuesta=int(input("Apuesta: "))
                            except:
                                print("Tiene que ser un numero")
                            else:
                                break

                        if apuesta<min or apuesta>max:
                            print("Apuesta incorrecta.")
                        else:
                            jugadores[i]['puntos apostados']=apuesta
                            jugadores[i]['puntos restantes']-=apuesta
                            break

                    while True:

                        while True:
                            try:
                                opt_plantarse=int(input("\n1) Seguir\n2) Pararse\nEscoje la opcion: "))
                            except:
                                print("Tiene que ser un numero.")
                            else:
                                break

                        if opt_plantarse==1:

                            carta_robada = random.choice(mazo)
                            jugadores[i]['mano'].insert(0,carta_robada)
                            mazo.remove(carta_robada)
                            sum_mazo()
                            print("\tTe toco",jugadores[i]['mano'][0][2],"de",jugadores[i]['mano'][0][1],"y",jugadores[i]['puntos mano'],"puntos del mazo")
                            if jugadores[i]['puntos mano'] > 7.5:
                                print(f"{bcolors.FAIL}Te has pasado.{bcolors.ENDC}")
                                break


                        elif opt_plantarse==2:

                            jugadores[i]['estado mano']="plantado"
                            print()
                            break
                        else:
                            print("Opcion incorrecta.")

                else:
                    # Turno Jugador IA
                    apostar_ia(min,max)
                    robar_ia(i)

            else:
                if jugadores[i]['ia']==0:
                    # Turno de la Banca Humano
                    print("Turno Banca")
                    contador_no_se_paso=0
                    for j in jugadores_ord:
                        j=j[0]
                        if jugadores[j]['puntos mano']<=7.5:
                            contador_no_se_paso+=1
                    if contador_no_se_paso>0:
                        # Si queda alguien que no se haya pasado
                        print("\tTe toco", jugadores[i]['mano'][0][2], "de", jugadores[i]['mano'][0][1], "y",jugadores[i]['puntos mano'], "puntos del mazo")
                        while True:
                            print()
                            while True:
                                try:
                                    opt_plantarse = int(input("\n1) Seguir\n2) Pararse\nEscoje la opcion: "))
                                except:
                                    print("Tiene que ser un numero.")
                                else:
                                    break
                            if opt_plantarse == 1:
                                carta_robada = random.choice(mazo)
                                jugadores[i]['mano'].insert(0, carta_robada)
                                mazo.remove(carta_robada)
                                sum_mazo()
                                print("\tTe toco", jugadores[i]['mano'][0][2], "de", jugadores[i]['mano'][0][1], "y",jugadores[i]['puntos mano'], "puntos del mazo")
                                if jugadores[i]['puntos mano']>7.5:
                                    print(f"{bcolors.FAIL}Te has pasado.{bcolors.ENDC}")
                                    break
                            elif opt_plantarse == 2:
                                jugadores[i]['estado mano'] = "plantado"
                                print()
                                break
                            else:
                                print("Opcion incorrecta.")
                else:
                    robar_ia(i)


        print("")
        print(f"{bcolors.WARNING}Resultados ronda:{bcolors.ENDC}", contador_mano-1)
        print("")
        for i in jugadores_ord:  # Condiciones de ser eliminado
            i=i[0]
            if jugadores[i]['puntos restantes']<=0:
                jugadores[i]['estado partida']="eliminado"
                for j in jugadores_ord:
                    if i in j:
                        jugadores_ord.remove(j)
                print(f"{bcolors.FAIL}{bcolors.BOLD}{bcolors.UNDERLINE}{i}{bcolors.ENDC}{bcolors.FAIL}{bcolors.BOLD} queda eliminado por falta de puntos.{bcolors.ENDC}{bcolors.ENDC}")
            else:
                if jugadores[i]['puntos mano']>7.5:
                    jugadores[i]['estado mano']="eliminado"
                    jugadores[i]['puntos mano']=0


        if jugadores[jugadores_ord[-1][0]]['puntos mano']>7.5:  # Si se pasa, paga a todos los plantados
            for i in jugadores_ord[:-1]:
                i=i[0]
                jugadores[i]['puntos restantes']  # Duda. Sin acabar
                print()

        sieteymedio=False
        for i in jugadores_ord:
            i=i[0]
            if jugadores[i]['puntos mano']==7.5:  # Alguien a sacado 7.5
                sieteymedio=True
                jugadores[i]['puntos restantes']+=jugadores[i]['puntos apostados']*3
                if jugadores[jugadores_ord[-1]]['puntos restantes']<jugadores[i]['puntos apostados']*2:
                    jugadores[i]['puntos restantes']+=jugadores[jugadores_ord[-1]]['puntos restantes']
                else:
                    jugadores[jugadores_ord[-1]]['puntos restantes']-=jugadores[i]['puntos apostados']*2
                print(i,"a ganado:",jugadores[i]['puntos apostados']*3,"puntos, ahora tiene:",jugadores[i]['puntos restantes'])

        if not sieteymedio and num_jugadores>2:  # Nadie a sacado 7.5
            suma=0
            flag_mas_cercano=False
            for i in jugadores_ord[:-1]:
                i=i[0]
                sum_mazo()
                if jugadores[i]['puntos mano']>suma:
                    mas_cercano_siete_y_medio=i
                    suma=jugadores[i]['puntos mano']
                    flag_mas_cercano=True

            jugadores[mas_cercano_siete_y_medio]['puntos restantes']+=1

            print(mas_cercano_siete_y_medio, "a ganado:", 1, "punto, ahora tiene:",jugadores[mas_cercano_siete_y_medio]['puntos restantes'])

            print("El resto pierte sus puntos apostados.")

            for i in jugadores_ord[:-1]:
                i=i[0]
                if i!=mas_cercano_siete_y_medio:
                    jugadores[i]['puntos restantes']-=jugadores[i]['puntos apostados']
                    print(i,"pierde:",jugadores[i]['puntos apostados'],"puntos, ahora tiene:",jugadores[i]['puntos restantes'])

            # Si jugador saca 7.5 y la banca no, el jugador se convierte en la banca

        sieteymedio_comprobacion=False
        for i in jugadores_ord[:-1]:
            aux=i
            i=i[0]
            if jugadores[i]['puntos mano']==7.5:
                sieteymedio_comprobacion=True
                jugador_a_banca=aux

        for i in jugadores_ord[:-1]:  # Quien a perdido contra la Banca
            i = i[0]
            if jugadores[jugadores_ord[-1][0]]['puntos mano']<jugadores[i]['puntos mano'] and jugadores[i]['estado mano']=="plantado":  # Si la banca pierde

                if jugadores[i]['puntos mano']==7.5:  # Si saca 7.5

                    jugadores[jugadores_ord[-1][0]]['puntos restantes']-=jugadores[i]['puntos apostados']*2
                    jugadores[i]['puntos restantes']+=jugadores[i]['puntos apostados']*3
                    print("la banca (",jugadores_ord[-1][0],") pierde",jugadores[i]['puntos apostados']*2,"y",i,"gana",jugadores[i]['puntos apostados']*3)
                else:  # Si no saca 7.5

                    jugadores[jugadores_ord[-1][0]]['puntos restantes']-=jugadores[i]['puntos apostados']
                    jugadores[i]['puntos restantes']+=jugadores[i]['puntos apostados']*2
                    print("la banca (",jugadores_ord[-1][0],") pierde",jugadores[i]['puntos apostados'],"y",i,"gana",jugadores[i]['puntos apostados']*2)

            else:
                jugadores[jugadores_ord[-1][0]]['puntos restantes']+=jugadores[i]['puntos apostados']
                print(i,"a pagado",jugadores[i]['puntos apostados'],"a la banca (",jugadores_ord[-1][0],")")

        if jugadores[jugadores_ord[-1][0]]['puntos mano']!=7.5 and sieteymedio_comprobacion:
            # [(carlos,4),(nil,7.5),(marti,6),(aida,7)]
            jugadores_ord.remove(jugador_a_banca)
            jugadores_ord.append(jugador_a_banca)

        count_elim=0
        for i in jugadores.keys():
            if jugadores[i]['estado partida']=="eliminado":
                count_elim+=1

        if count_elim==num_jugadores-1:
            for j in jugadores.keys():
                if jugadores[j]['estado partida']!="eliminado":
                    print("El Ganador es",j)
                    flag_ganador=True
                    contador_mano==31

    if contador_mano==31 and not flag_ganador:
        suma=0
        for i in jugadores_ord:
            i=i[0]

            if jugadores[i]['puntos restantes']>suma:
                suma=jugadores[i]['puntos restantes']
                ganador=i

        print("El Ganador es",i)

'''
for i in jugadores.keys():
    print(jugadores[i]['puntos restantes'])
'''