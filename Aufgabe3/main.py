import heapq as hq
# noch zu implementieren: output mit pfeilen, die den weg anzeigen, und Sekunden
for i in range(0, 10):
    with open(f"zauberschule{i}.txt", "r", encoding="utf-8") as datei:
        with open("output.txt", "a", encoding="utf-8") as output_datei:
            output_datei.write(f"zauberschule{i}.txt" + "\n")
        # einlesen der ersten zeile mit den werten n und m
        n, m = map(int, datei.readline().split())

        # einlesen der ebenen
        ebene0 = [list(datei.readline().strip()) for _ in range(int(n))]
        ebene1 = [list(datei.readline().strip()) for _ in range(int(n)+1)][1:]

        # np.array aus den ebenen erstellen, wobei es nicht notwendig ist, nur fürs output
        bugwarts = [ebene0, ebene1]
        # print(bugwarts)

        # finden der start und endpunkte in den ebenen und deren Positionen in den Zeilen und Spalten mit einer funktion
        def punkte_finden(labyrinth):
            # findet start und Ziel (A und B) in den ebenen und gibt deren Positionen in den Zeilen und Spalten zurück
            punktA, punktB = (), ()
            for ebene in range(len(labyrinth)):
                for zeile in range(len(labyrinth[ebene])):
                    for spalte in range(len(labyrinth[ebene][zeile])):
                        if labyrinth[ebene][zeile][spalte] == "A":
                            punktA = (ebene, zeile, spalte)
                        elif labyrinth[ebene][zeile][spalte] == "B":
                            punktB = (ebene, zeile, spalte)

            return (punktA, punktB)

        punkte = punkte_finden(bugwarts)

        # erstellen einer liste, die die Positionen der Punkte enthält
        punkte_liste = [punkte[0], punkte[1]]

        # funktion, die die Nachbarn eines Eckpunktes zurückgibt
        def nachbarn_finden(array, eckpunkt):
            nachbarn = []
            # mögliche Richtungen, in die sich ein Eckpunkt "bewegen" kann
            richtungen = [(1, 0, 0), (-1, 0, 0), (0, 1, 0),
                        (0, -1, 0), (0, 0, 1), (0, 0, -1)]

            for dx, dy, dz in richtungen:
                neu_x, neu_y, neu_z = eckpunkt[0] + dx, eckpunkt[1] + dy, eckpunkt[2] + dz


                # überprüft, ob die Nachbarn innerhalb des Arrays liegen und ob sie nicht "#" sind, wenn nicht, werden sie der Liste "nachbarn" hinzugefügt
                if (
                    0 <= neu_x < len(array) and
                    0 <= neu_y < len(array[0]) and
                    0 <= neu_z < len(array[0][0])
                ):
                    if array[neu_x][neu_y][neu_z] != "#":
                        if neu_x == eckpunkt[0]:
                            gewichtung = 1
                            nachbarn.append(((neu_x, neu_y, neu_z), gewichtung))

                        elif neu_x != eckpunkt[0]:
                            gewichtung = 3
                            nachbarn.append(((neu_x, neu_y, neu_z), gewichtung))

            return nachbarn

        def dijkstra(array, start, end):
            distanzen = {} 
            vorgänger = {} # speichert den Vorgänger eines Knotens
            queue = [(0, start)]

            distanzen[start] = 0

            while queue:
                derzeitige_distanz, eckpunkt = hq.heappop(queue)

                if eckpunkt == end:

                    pfad = []
                    while eckpunkt in vorgänger:
                        pfad.insert(0, eckpunkt)
                        eckpunkt = vorgänger[eckpunkt]

                    pfad.insert(0, start)

                    sekunden = distanzen[end]
                    return pfad, sekunden

                if derzeitige_distanz > distanzen[eckpunkt]:
                    continue

                for nachbar, gewichtung in nachbarn_finden(array, eckpunkt):
                    distanz = derzeitige_distanz + gewichtung

                    if nachbar not in distanzen or distanz < distanzen[nachbar]:
                        distanzen[nachbar] = distanz
                        vorgänger[nachbar] = eckpunkt
                        hq.heappush(queue, (distanz, nachbar))

        kürzester_pfad = dijkstra(bugwarts, punkte[0], punkte[1])

        if kürzester_pfad:
            print("Kürzester Pfad:", kürzester_pfad)

        else:
            print("Kein Pfad gefunden")
        

        # implementation der Richtungsanzeige
        pfad = kürzester_pfad[0]
        for x in range(len(pfad)-1):
            x1, y1, z1 = pfad[x]

            x2, y2, z2 = pfad[x + 1]
            
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            
            #ebenen Wechsel
            if dx == 1:
                if bugwarts[x1+1][y1][z1] not in punkte_liste:
                    bugwarts[x1+1][y1][z1] = "!"

            elif dx == -1:
                if bugwarts[x1][y1][z1] not in punkte_liste:
                    bugwarts[x1][y1][z1] = "!"

            #zeilen Wechsel
            if dy == 1:
                if bugwarts[x1][y1+1][z1] not in punkte_liste:
                    bugwarts[x1][y1+1][z1] = "v"

            elif dy == -1:
                if bugwarts[x1][y1][z1] not in punkte_liste:
                    bugwarts[x1][y1][z1] = "^"
            
            #spalten Wechsel
            if dz == 1:
                if bugwarts[x1][y1][z1+1] not in punkte_liste:
                    bugwarts[x1][y1][z1+1] = ">"

            elif dz == -1:
                if bugwarts[x1][y1][z1] not in punkte_liste:
                    bugwarts[x1][y1][z1] = "<"

        for layer in bugwarts:
            for row in layer:
                with open("output.txt", "a", encoding="utf-8") as output_datei:
                    output_datei.write("".join(row) + "\n")
                    
                    #output_datei.write("\n")

        # in der Dokumentation werden die Gesamtkosten direkt nach der Benennung der Beispieldatei angegegeben
        with open("output.txt", "a", encoding="utf-8") as output_datei:
            output_datei.write(f"Gesamtkosten (in Sekunden): {kürzester_pfad[1]}" + "\n" + "\n")