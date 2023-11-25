import itertools  # Für die Erzeugung von Testfällen
from tabulate import tabulate  # Für die Tabellenausgabe

# Funktion zur Generierung aller möglichen Testfälle basierend auf den gegebenen Indizes der Quellen
def test_case_generation(indeces):
    possible_test_cases = list(
        map(list, itertools.product([0, 1], repeat=len(indeces))))
    return possible_test_cases

# Funktion zur Logikgatter-Implementierung, leftRight gibt an, ob das Gatter-Teil, was mit dem aktuellen Gatter verbunden ist, links oder rechts ist
def gate_logic(k, arr, id, leftRight):
    # NAND LOGIC GATE
    if id == "W":
        if leftRight == "r":
            if arr[k] == 0 and arr[k+1] == 0:
                arr[k] = 1
                arr[k+1] = 1
                return arr

            elif arr[k] == 0 and arr[k+1] == 1:
                arr[k] = 1
                arr[k+1] = 1
                return arr

            elif arr[k] == 1 and arr[k+1] == 0:
                arr[k] = 1
                arr[k+1] = 1
                return arr

            elif arr[k] == 1 and arr[k+1] == 1:
                arr[k] = 0
                arr[k+1] = 0
                return arr

        if leftRight == "l":
            if arr[k] == 0 and arr[k-1] == 0:
                arr[k] = 1
                arr[k-1] = 1
                return arr

            elif arr[k] == 0 and arr[k-1] == 1:
                arr[k] = 1
                arr[k-1] = 1
                return arr

            elif arr[k] == 1 and arr[k-1] == 0:
                arr[k] = 1
                arr[k-1] = 1
                return arr

            elif arr[k] == 1 and arr[k-1] == 1:
                arr[k] = 0
                arr[k-1] = 0
                return arr

    # NOT LOGIC GATE
    if id == "R":
        if leftRight == "r":
            if arr[k] == 0:
                arr[k] = 1
                arr[k+1] = 1
                return arr

            elif arr[k] == 1:
                arr[k] = 0
                arr[k+1] = 0
                return arr

        if leftRight == "l":
            if arr[k] == 0:
                arr[k] = 1
                arr[k-1] = 1
                return arr

            elif arr[k] == 1:
                arr[k] = 0
                arr[k-1] = 0
                return arr

    # OR LOGIC GATE
    if id == "B":
        if leftRight == "r":
            if arr[k] == 0 and arr[k+1] == 0:
                arr[k] = 0
                arr[k+1] = 0
                return arr

            elif arr[k] == 0 and arr[k+1] == 1:
                arr[k] = 0
                arr[k+1] = 1
                return arr

            elif arr[k] == 1 and arr[k+1] == 0:
                arr[k] = 1
                arr[k+1] = 0
                return arr

            elif arr[k] == 1 and arr[k+1] == 1:
                arr[k] = 1
                arr[k+1] = 1
                return arr

        if leftRight == "l":
            if arr[k] == 0 and arr[k-1] == 0:
                arr[k] = 0
                arr[k-1] = 0
                return arr

            elif arr[k] == 0 and arr[k-1] == 1:
                arr[k] = 0
                arr[k-1] = 1
                return arr

            elif arr[k] == 1 and arr[k-1] == 0:
                arr[k] = 1
                arr[k-1] = 0
                return arr

            elif arr[k] == 1 and arr[k-1] == 1:
                arr[k] = 1
                arr[k-1] = 1
                return arr

        return arr
 
# Schleife über verschiedene Beispieldateien
for i in range(1, 8):
    print(f"Beispieldatei nmr.: {i}")
    with open(f"nandu{i}.txt", "r", encoding="utf-8") as datei:
        lines = datei.read().splitlines()
        n, m = map(int, lines[0].split(" "))
        # indizes der Quellen und die Quellen selbst einlesen
        quellen = [line for line in lines[1].split(" ") if line != ""]
        indeces = [quellen.index(quelle)
                   for quelle in quellen if quelle.startswith("Q")]

        test_cases = test_case_generation(indeces=indeces)

        # testing für jeden testfall
        output = []
        for case in test_cases:
            # für die Simulation nötige Liste mit 0en initialisieren
            crnt_arr = [0]*n

            # setzen der Werte der Quellen für den aktuellen Testfall
            for index, num in enumerate(indeces):
                crnt_arr[num] = case[index]

            # durchlaufen aller Zeilen mit Gatter, exklusive Quellen und Lampen
            
            for j in range(2, m+1):
                print(crnt_arr, case)
                # zurücksetzen der verwendeten Gatter für jede Zeile
                usedGates = [False for _ in range(n)]

                # aufteilen der Zeile basierend auf den Zeichen
                zeile = [line for line in lines[j].split(" ") if line != ""]
                # vorherige Zeile für die Überprüfung, ob ein "X" über dem Gatter ist
                vorherige_zeile = [_ for _ in lines[j-1].split(" ") if _ != ""]
                # Iteration über die Zeile
                for k in range(0, len(zeile)):
                    # wenn das Zeichen kein X ist und das Gatter noch nicht verwendet wurde
                    if zeile[k] != "X":
                        # bedingung um zu schauen, ob ein "X" über dem Gatter ist, falls ja, vernachlässigen wir diesen Teil des Gatters
                    
                        if usedGates[k] == False:
                            # NAND LOGIC GATE
                            if zeile[k] == "W":
                                # schauen, wo der andere Eingang des Gatters ist
                                if k - 1 >= 0:
                                    if zeile[k-1] == "W" and usedGates[k-1] == False:                                
                                        gate_logic(k=k, arr=crnt_arr,
                                                id="W", leftRight="l")
                                        
                                        usedGates[k] = True
                                        usedGates[k-1] = True


                                if k + 1 <= len(zeile):
                                    if zeile[k+1] == "W" and usedGates[k+1] == False:
                                        gate_logic(k=k, arr=crnt_arr,
                                                   id="W", leftRight="r")
                                        usedGates[k] = True
                                        usedGates[k+1] = True
                                        
                            # OR LOGIC GATE
                            if zeile[k] == "B":
                                if k - 1 >= 0:
                                    if zeile[k-1] == "B" and usedGates[k-1] == False:
                                        gate_logic(k=k, arr=crnt_arr,
                                                   id="B", leftRight="l")   
                                        usedGates[k] = True
                                        usedGates[k-1] = True
                                        

                                if k + 1 <= len(zeile):
                                    if zeile[k+1] == "B" and usedGates[k+1] == False:
                                        gate_logic(k=k, arr=crnt_arr,
                                                   id="B", leftRight="r")
                                        usedGates[k] = True
                                        usedGates[k+1] = True
                                        
                            # NOT LOGIC GATE
                            if zeile[k] == "R":
                                if k - 1 >= 0:
                                    if zeile[k-1] == "r" and usedGates[k-1] == False:
                                        '''
                                        diese Bedingung ist nur für nandu6.txt nötig, 
                                        da dort ein Spezialfall vorliegt (wenn ein "X" über einem Gatter-Eingang liegt),
                                        deswegen ist es hier nur beim Roten Gatter implementiert worden
                                        '''
                                        if vorherige_zeile[k] == "X":
                                            crnt_arr[k] = 0
                                            crnt_arr[k-1] = 0

                                            usedGates[k] = True
                                            usedGates[k-1] = True

                                        else:
                                            gate_logic(k=k, arr=crnt_arr,
                                                    id="R", leftRight="l")
                                            usedGates[k] = True
                                            usedGates[k-1] = True

                                if k + 1 < len(zeile):
                                    if zeile[k+1] == "r" and usedGates[k+1] == False:
                                        if vorherige_zeile[k] == "X":
                                            crnt_arr[k] = 0
                                            crnt_arr[k+1] = 0

                                            usedGates[k] = True
                                            usedGates[k+1] = True
                                            
                                        else:
                                            gate_logic(k=k, arr=crnt_arr,
                                                        id="R", leftRight="r")
                                            usedGates[k] = True
                                            usedGates[k+1] = True
            # Erzeugung der Lampenliste
            lampen = [line for line in lines[-1].split(" ") if line != ""]
            lampen_indeces = [lampen.index(l)
                              for l in lampen if l.startswith("L")]
            
            # Erzeugung der Outputliste
            crnt_arr = [crnt_arr[index] for index in lampen_indeces]
            
            output.append([case, crnt_arr])
            
        '''
        OUTPUT GENERIERUNG
        '''
        # output Liste in eine Liste von Listen umwandeln (nötig für die tabulate Funktion)
        output = [[item for sublist in inner_list for item in sublist] for inner_list in output]
        
        # Erzeugung der Header für die Output-Tabelle
        lamp_headers = [lampen[index] for index in lampen_indeces]
        quellen_headers = [quellen[index] for index in indeces]

        headers = quellen_headers + lamp_headers

        # Ausgabe in eine Datei schreiben und auf der Konsole anzeigen
        with open("OUTPUT.txt", "a", encoding="utf-8") as datei:
            datei.write("\captionsetup{labelformat=empty}")
            datei.write("\n")
            datei.write(f"\caption{{nandu{i}}}\\\\")
            datei.write("\n")
            datei.write(tabulate(output, headers=[*headers], tablefmt="latex_longtable"))
            datei.write("\n")

        print("\n")