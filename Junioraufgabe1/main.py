from mobil_ave.tables import create_matrix_table
for i in range(0, 9):
    with open(f"wundertuete{i}.txt", "r", encoding="utf-8") as datei:
        anzahl_wundertueten = int(datei.readline())

        spiele_sorten_anzahl = int(datei.readline())

        spiele_pro_sorte = [int(datei.readline()) for _ in range(spiele_sorten_anzahl)]

        #verteilen der spiele auf die wundertueten
        output = [[spiel // anzahl_wundertueten for spiel in spiele_pro_sorte] for _ in range(anzahl_wundertueten)]

        #herausfinden, wie viele spiele pro sorte noch übrig sind
        uebrig_spiele_pro_sorte = [spiel % anzahl_wundertueten for spiel in spiele_pro_sorte]

        #übrige spiele auf die wundertueten verteilen
        ind = 0
        for index, value in enumerate(uebrig_spiele_pro_sorte):
            for j in range(value):
                output[ind][index] += 1

                ind += 1
                ind %= anzahl_wundertueten
        with open("OUTPUT.txt", "a", encoding="utf-8") as datei:
            datei.write(f"wundertuete{i}\n")
            datei.write(create_matrix_table("Spiel", "Wundertüte", output))
            datei.write("\n\n")
