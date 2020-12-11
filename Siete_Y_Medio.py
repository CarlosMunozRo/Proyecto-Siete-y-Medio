mazo=[(1,"oros",1),(2,"oros",2),(3,"oros",3),(4,"oros",4),(5,"oros",5),(6,"oros",6),(7,"oros",7),(10,"oros",0.5),(11,"oros",0.5),(12,"oros",0.5),
      (1,"bastos",1),(2,"bastos",2),(3,"bastos",3),(4,"bastos",4),(5,"bastos",5),(6,"bastos",6),(7,"bastos",7),(10,"bastos",0.5),(11,"bastos",0.5),(12,"bastos",0.5),
      (1,"espadas",1),(2,"espadas",2),(3,"espadas",3),(4,"espadas",4),(5,"espadas",5),(6,"espadas",6),(7,"espadas",7),(10,"espadas",0.5),(11,"espadas",0.5),(12,"espadas",0.5),
      (1,"copas",1),(2,"copas",2),(3,"copas",3),(4,"copas",4),(5,"copas",5),(6,"copas",6),(7,"copas",7),(10,"copas",0.5),(11,"copas",0.5),(12,"copas",0.5)]


import random

flag_menu1=False

jugadores={}

def sum_mazo():  # Suma los puntos de el mazo de los jugadores
    global jugadores
    for i in jugadores.keys():
        suma_mazo=0
        for h in jugadores[i]['mano']:
            suma_mazo+=h[2]
        jugadores[i]['puntos mano']=suma_mazo


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
    elif opt_menu1==3:
        flag_menu1=True
    else:
        print("Opcion incorrecta")

if mod_juego=="Manual":
    while True:
        try:
            num_jugadores = int(input("Cuantos Jugadores van a Jugar: "))
        except:
            print("Tiene que ser un numero")
        else:
            break


    if num_jugadores >= 2 and num_jugadores <= 8:

        for i in range(num_jugadores):  # Crea el diccionario de jugadores
            while True:
                while True:
                    try:
                        nombre = input("Nombre del jugador " + str(i + 1) + ": ")
                    except:
                        print("Entrada invalida")
                    else:
                        break
                if not nombre.isalnum() or not nombre[
                    0].isalpha() or ' ' in nombre:  # Comprueba si el nombre es aceptable
                    print("Nombre no permitido")
                else:
                    jugadores[nombre] = {}
                    jugadores[nombre]['mano'] = []
                    jugadores[nombre]['estado mano'] = "jugando"
                    jugadores[nombre]['estado partida'] = "jugando"
                    jugadores[nombre]['prioridad del jugador'] = 0
                    jugadores[nombre]['puntos mano'] = 0
                    jugadores[nombre]['puntos apostados'] = 0
                    jugadores[nombre]['puntos restantes'] = 20
                    break


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


    contador_mano=0
    while contador_mano<=30:
        mazo = [(1, "oros", 1), (2, "oros", 2), (3, "oros", 3), (4, "oros", 4), (5, "oros", 5), (6, "oros", 6),
                (7, "oros", 7), (10, "oros", 0.5), (11, "oros", 0.5), (12, "oros", 0.5),
                (1, "bastos", 1), (2, "bastos", 2), (3, "bastos", 3), (4, "bastos", 4), (5, "bastos", 5),
                (6, "bastos", 6), (7, "bastos", 7), (10, "bastos", 0.5), (11, "bastos", 0.5), (12, "bastos", 0.5),
                (1, "espadas", 1), (2, "espadas", 2), (3, "espadas", 3), (4, "espadas", 4), (5, "espadas", 5),
                (6, "espadas", 6), (7, "espadas", 7), (10, "espadas", 0.5), (11, "espadas", 0.5), (12, "espadas", 0.5),
                (1, "copas", 1), (2, "copas", 2), (3, "copas", 3), (4, "copas", 4), (5, "copas", 5), (6, "copas", 6),
                (7, "copas", 7), (10, "copas", 0.5), (11, "copas", 0.5), (12, "copas", 0.5)]

        for i in jugadores_ord:
            i=i[0]
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
            print("El turno es de:",i)

            if jugadores[i]['prioridad del jugador']!=0: #  Si no es la vanca
                #Turno de jugador
                sum_mazo()

                print("Tienes",jugadores[i]['mano'][0][2],"de",jugadores[i]['mano'][0][1],"y",jugadores[i]['puntos mano'],"puntos del mazo")

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
                            opt_plantarse=int(input("\n1) Segir\n2) Pararse\nEscoje la opcion: "))
                        except:
                            print("Tiene que ser un numero.")
                        else:
                            break

                    if opt_plantarse==1:

                        carta_robada = random.choice(mazo)
                        jugadores[i]['mano'].insert(0,carta_robada)
                        mazo.remove(carta_robada)
                        sum_mazo()
                        print("Tienes",jugadores[i]['mano'][0][2],"de",jugadores[i]['mano'][0][1],"y",jugadores[i]['puntos mano'],"puntos del mazo")

                    elif opt_plantarse==2:

                        jugadores[i]['estado mano']="plantado"
                        print()
                        break
                    else:
                        print("Opcion incorrecta.")
            else:
                # Turno de la Banca
                print("Turno Banca")

                contador_no_se_paso=0
                for j in jugadores_ord:
                    j=j[0]
                    if jugadores[j]['puntos mano']<=7.5:
                        contador_no_se_paso+=1

                if contador_no_se_paso>0:
                    # Si queda alguien que no se haya pasado
                    print("Tienes", jugadores[i]['mano'][0][2], "de", jugadores[i]['mano'][0][1], "y",jugadores[i]['puntos mano'], "puntos del mazo")
                    while True:

                        print()
                        while True:
                            try:
                                opt_plantarse = int(input("\n1) Segir\n2) Pararse\nEscoje la opcion: "))
                            except:
                                print("Tiene que ser un numero.")
                            else:


                        if opt_plantarse == 1:

                            carta_robada = random.choice(mazo)
                            jugadores[i]['mano'].insert(0, carta_robada)
                            mazo.remove(carta_robada)
                            sum_mazo()
                            print("Tienes", jugadores[i]['mano'][0][2], "de", jugadores[i]['mano'][0][1], "y",jugadores[i]['puntos mano'], "puntos del mazo")


                        elif opt_plantarse == 2:

                            jugadores[i]['estado mano'] = "plantado"
                            print()
                            break
                        else:
                            print("Opcion incorrecta.")

        for i in jugadores_ord:  # Condiciones de ser eliminado
            i=i[0]
            if jugadores[i]['puntos restantes']<=0:
                jugadores[i]['estado partida']="eliminado"
                for j in jugadores_ord:
                    if i in j:
                        jugadores_ord.remove(j)
                print(i,"queda eliminado por falta de puntos.")
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
                jugadores[i]['puntos restantes']+=jugadores[i]['puntos apostados']*2
                print(i,"a ganado:",jugadores[i]['puntos apostados']*2,"puntos, ahora tiene:",jugadores[i]['puntos restantes'])

        if not sieteymedio:  # Nadie a sacado 7.5
            suma=0
            flag_mas_cercano=False
            sum_mazo()
            for i in jugadores_ord[:-1]:
                i=i[0]

                if jugadores[i]['puntos mano']>suma and jugadores[i]['estado mano']=="plantado":
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

        if jugadores[jugadores_ord[-1][0]]['estado mano']=="plantado":
            for i in jugadores_ord[:-1]:  # Quien a perdido contra la Banca
                i = i[0]
                if jugadores[jugadores_ord[-1][0]]['puntos mano']<jugadores[i]['puntos mano']:  # Si la banca pierde

                    if jugadores[i]['puntos mano']==7.5:  # Si saca 7.5
                        jugadores[jugadores_ord[-1][0]]['puntos restantes']-=jugadores[i]['puntos apostados']
                        jugadores[i]['puntos restantes']+=jugadores[i]['puntos apostados']*2
                        print("la banca (",jugadores_ord[-1][0],") pierde",jugadores[i]['puntos apostados'],"y",i,"gana",jugadores[i]['puntos apostados']*2)
                    else:  # Si no saca 7.5

                        jugadores[jugadores_ord[-1][0]]['puntos restantes']-=jugadores[i]['puntos apostados']*2
                        jugadores[i]['puntos restantes']+=jugadores[i]['puntos apostados']*3
                        print("la banca (",jugadores_ord[-1][0],") pierde",jugadores[i]['puntos apostados']*2,"y",i,"gana",jugadores[i]['puntos apostados']*3)

                else:
                    jugadores[jugadores_ord[-1][0]]['puntos restantes']+=jugadores[i]['puntos apostados']
                    print(i,"a pagado",jugadores[i]['puntos apostados'],"a la banca (",jugadores_ord[-1][0],")")


        if jugadores[jugadores_ord[-1][0]]['puntos mano']!=7.5 and sieteymedio_comprobacion:
            # [(carlos,4),(nil,7.5),(marti,6),(aida,7)]
            jugadores_ord.remove(jugador_a_banca)
            jugadores_ord.append(jugador_a_banca)

        count_elim=0
        jugadores_elim=[]
        for i in jugadores_ord:
            i=i[0]
            if jugadores[i]['estado partida']=="eliminado":
                count_elim+=1
                jugadores_elim.append(i)



        if count_elim==num_jugadores-1:
            for i in jugadores_elim:
                for j in jugadores.keys():
                    if i==j:
                        print("El Ganador es",j)






    if contador_mano==30:
        suma=0
        for i in jugadores_ord:
            i=i[0]

            if jugadores[i]['puntos restantes']>suma:
                suma=jugadores[i]['puntos restantes']
                ganador=i

        print("El Ganador es",i)

        '''
        if jugadores[i]['puntos mano'] > 7.5:
            jugadores[i]['estado mano'] == "eliminado"
        if jugadores[i]['estado mano'] == "jugando":
        '''