

# Apufunktio kynnysehtojen tarkistamiseen
# käy parametrin 'ehdot' läpi ja jos yksikin ehdoista toteutuu palautetaan True
# Testattu, toimii, Joonas
def lauseen_tarkistus(ehdot, ainepuskuri, kayttajan_arvosanat, kynnys):
    # käydään ehdot läpi for loopilla
    for j in ehdot:
        # löytyykö aine käyttäjän kirjoittamista aineista
        if j in ainepuskuri:
            # luodaan muuttujat käyttäjän arvosanaa ja kynnysehtona olevaa arvosanaa varten
            kayttajan_arvosana = 0
            vaadittu_arvosana = 0

            # haetaan käyttäjän arvosana käymällä käyttäjän aineita läpi kunnes oikea aine löytyy
            for k in kayttajan_arvosanat:
                if k[0] == j:
                    kayttajan_arvosana = k[1]
                    break
            # haetaan vaadittu arvosana käymällä läpi kynnysehtoja kunnes oikea aine löytyy
            for k in kynnys:
                if k[0] == j:
                    vaadittu_arvosana = k[1]
                    break
            # jos käyttäjän arvosana on suurempi tai yhtäsuuri kuin vaadittu arvosana palautetaan True
            if kayttajan_arvosana >= vaadittu_arvosana:
                return True
    # mikään ehto ei toteutunut joten palautetaan False
    return False
    

# Tutkii, täyttyykö hakukohteen kynnysehto.
# 'Kynnys' kertoo kynnysehdon aineen ja arvosanan numerona. 'Käyttäjän_arvosanat' sisältää käyttäjän aineet ja arvosanat
# muunnettuna numeromuotoon.
# Testattu, toimii, Joonas
def tayttyyko_kynnysehto(kynnysehto_lause, kynnys, kayttajan_arvosanat, laskentatapaID):

    ainepuskuri = []
    # Aluksi katsotaan käyttäjän kirjoittamat aineet.
    for i in kayttajan_arvosanat:
        ainepuskuri.append(i[0])
    
    # DIA valinnassa pitkä matematiikka tulee olla suoritettu hyväksytysti
    # saattaa puuttua joitain laskentatapoja
    if laskentatapaID == 1:
            if "Matematiikka pitkä" in ainepuskuri:
                indeksi = 0
                for i in kayttajan_arvosanat:
                    if i[0] == "Matematiikka pitkä":
                        break
                    indeksi += 1
                if kayttajan_arvosanat[indeksi][1] <= 0:
                    return False
            else:
                return False

    # Jos kynnysehtojen määrä on 0, palautetaan True.
    if str(kynnysehto_lause) == "None" or str(kynnysehto_lause) == "":
        return True
    # vähintään yksi kynnysehto
    else:
        # tehdään muuttuja kynnysehtoja varten
        kynnysehdot = kynnysehto_lause

        # pilkotaan kynnysehdot pilkkujen kohdalta
        # Kaikki muuttujan sisältämät lauseet on täten toteuduttava
        kynnysehdot = kynnysehdot.split(",")
            
        # käydään jokainen lause erikseen läpi
        for i in kynnysehdot:
            # pilkotaan lause '/' merkkien kohdalta osiin joista vähintään yhden on täytyttävä
            ehdot = i.split("/")
            # tarkistetaan toteutuuko joku ehdoista
            boolean = lauseen_tarkistus(ehdot, ainepuskuri, kayttajan_arvosanat, kynnys)
            # jos ei toteudu palautetaan False
            if not boolean:
                return False
        
        # kaikki ehdot toteutuivat joten palautetaan True
        return True



# # testejä
# kynnysehto = "Suomi 2,Kemia/Fysiikka"
# arvosanat = [("Suomi 2", 6), ("Kemia", 4), ("Fysiikka", 6)]
# syote = [('Matematiikka lyhyt', 6), ('Äidinkieli Suomi', 3), ('Suomi 2', 6), ('Kemia',4), ('Fysiikka', 3), ('Ruotsi keskipitkä', 6), ('Englanti pitkä', 4), ('Yhteiskuntaoppi', 5), ('Biologia', 6), ('Äidinkieli', 5)]
# hakukohdeID = 5
# print(tayttyyko_kynnysehto(kynnysehto, arvosanat, syote, hakukohdeID))