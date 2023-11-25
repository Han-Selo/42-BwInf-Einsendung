from PIL import Image

for i in range(1, 8):
    im = Image.open(f"bild0{i}.png")
    width, height = im.size

    crnt_loc = (0, 0)
    crnt = im.getpixel(crnt_loc)[:3]

    chiffre = []
    chiffre.append(chr(crnt[0]))

    run = True
    while run:
        if crnt[1] == 0 and crnt[2] == 0:
            run = False

        else:
            crnt_loc = ((crnt_loc[0]+crnt[1])%width, (crnt_loc[1]+crnt[2])%height)
            crnt = im.getpixel(crnt_loc)

            chiffre.append(chr(crnt[0]))

            
   

    with open(f"Output.txt", "a", encoding="utf-8") as f:
        if i != 5 and i != 6:
            f.write(f"bild0{i}.png \n")
            f.write("".join(chiffre))
            f.write("\n\n")
            
        else:
            f.write(f"bild0{i}.png \n")
            f.write("".join(chiffre))
            f.write("\n\n")
        