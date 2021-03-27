from apumetodit import arvosanamuunnin, hae_pisteet
from laskumetodit import aineen_pistelasku, paras_kieli, paras_xxx_aine, kauttaviivatilanne, muu_syotteessa, paras_xxx_ainereaali, aidinkielen_pisteenlasku_normaali
from aineiden_kasittelijat import poista_aine
from aineet import yhteiskuntatieteelliset_aineet


# Testattu, löydetyt bugit korjattu, pitäisi toimia oikein kaikissa tilanteissa, Joonas
def elintarviketiede(syote, laskentatapaID, database, ainelistat):
    pisteet = 0
    mydb = database
    
    #Lasketaan äidinkielen pisteet
    metodi = aidinkielen_pisteenlasku_normaali(laskentatapaID, mydb, syote)
    pisteet += metodi[0]
    poistettava = metodi[1]

    poista_aine(poistettava, syote, ainelistat)
    
    metodi = kauttaviivatilanne("Matematiikka pitkä/Matematiikka lyhyt", syote, laskentatapaID, mydb)
    pisteet += metodi[0]
    poistettava = metodi[1]

    # Poistetaan parempi aine syötteestä.
    if len(poistettava) != 0:
        poista_aine(poistettava, syote, ainelistat)
    
    aineet = []
    pistesailyttaja = []

    for reaali in ainelistat[3]:
        if reaali[0] == "Fysiikka" or reaali[0] == "Kemia" or reaali[0] == "Biologia":
            aineet.append(reaali[0])
            pistesailyttaja.append(reaali)

    if len(aineet) == 0:
        metodi = muu_syotteessa(syote, laskentatapaID, mydb)
        pisteet += metodi[0]
        

    elif len(aineet) == 1:
        if "Fysiikka" in aineet:
            metodi = aineen_pistelasku("Fysiikka", "Matemaattinen aine", syote, laskentatapaID, mydb, ainelistat[0])
            pisteet += metodi[0]
            poistettava = metodi[1]

            poista_aine(poistettava, syote, ainelistat)

            metodi = muu_syotteessa(syote, laskentatapaID, mydb)
            pisteet += metodi[0]
            
        elif "Kemia" in aineet:
            metodi = aineen_pistelasku("Kemia", "Matemaattinen aine", syote, laskentatapaID, mydb, ainelistat[0])
            pisteet += metodi[0]
            poistettava = metodi[1]

            poista_aine(poistettava, syote, ainelistat)

            metodi = muu_syotteessa(syote, laskentatapaID, mydb)
            pisteet += metodi[0]
            

        else:
            metodi = aineen_pistelasku("Biologia", "Biologinen aine", syote, laskentatapaID, mydb, ainelistat[0])
            pisteet += metodi[0]
            poistettava = metodi[1]

            poista_aine(poistettava, syote, ainelistat)

            metodi = muu_syotteessa(syote, laskentatapaID, mydb)
            pisteet += metodi[0]
            
    if len(aineet) == 2:
        if "Fysiikka" in aineet:
            metodi = aineen_pistelasku("Fysiikka", "Matemaattinen aine", syote, laskentatapaID, mydb, ainelistat[0])
            pisteet += metodi[0]
            poistettava = metodi[1]

            poista_aine(poistettava, syote, ainelistat)
            aineet.remove("Fysiikka")

            metodi = aineen_pistelasku(aineet[0], "Biologinen aine", syote, laskentatapaID, mydb, ainelistat[0])
            pisteet += metodi[0]
            poistettava = metodi[1]

            poista_aine(poistettava, syote, ainelistat)
            
            metodi = muu_syotteessa(syote, laskentatapaID, mydb)
            pisteet += metodi[0]
            
        else:
            metodi = aineen_pistelasku("Kemia", "Matemaattinen aine", syote, laskentatapaID, mydb, ainelistat[0])
            pisteet += metodi[0]
            poistettava = metodi[1]
            
            poista_aine(poistettava, syote, ainelistat)

            metodi = aineen_pistelasku("Biologia", "Biologinen aine", syote, laskentatapaID, mydb, ainelistat[0])
            pisteet += metodi[0]
            poistettava = metodi[1]

            poista_aine(poistettava, syote, ainelistat)

            metodi = muu_syotteessa(syote, laskentatapaID, mydb)
            pisteet += metodi[0]
            
    elif len(aineet) == 3:

        for reaali in ainelistat[3]:
            if reaali[0] == "Fysiikka" or reaali[0] == "Kemia" or reaali[0] == "Biologia":
                syote.remove(reaali)
            
        
        metodi = muu_syotteessa(syote, laskentatapaID, mydb)
        valipisteet = metodi[0]
        indeksi_fy = 0
        indeksi_ke = 0
        indeksi_bi = 0

        laskuri = 0
        for aine in pistesailyttaja:
            if aine[0] == "Biologia":
                indeksi_bi = laskuri
            elif aine[0] == "Fysiikka":
                indeksi_fy = laskuri
            else:
                indeksi_ke = laskuri
            laskuri += 1
        kirjoitetut = {
            "fysiikka": arvosanamuunnin(pistesailyttaja[indeksi_fy][1]),
            "kemia": arvosanamuunnin(pistesailyttaja[indeksi_ke][1]),
            "biologia": arvosanamuunnin(pistesailyttaja[indeksi_bi][1])
        }

        sql = "SELECT l, e, m, c, b, a, i FROM aineet WHERE aine = 'Matemaattinen aine' AND laskentatapaid = " + str(laskentatapaID)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        fysiikkataikemia = mycursor.fetchall()[0]

        sql = "SELECT l, e, m, c, b, a, i FROM aineet WHERE aine = 'Biologinen aine' AND laskentatapaid = " + str(laskentatapaID)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        kemiataibiologia = mycursor.fetchall()[0]

        sql = "SELECT l, e, m, c, b, a, i FROM aineet WHERE aine = 'Fysiikka' AND laskentatapaid = " + str(laskentatapaID)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        fysiikka = mycursor.fetchall()[0]

        sql = "SELECT l, e, m, c, b, a, i FROM aineet WHERE aine = 'Kemia' AND laskentatapaid = " + str(laskentatapaID)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        kemia = mycursor.fetchall()[0]

        sql = "SELECT l, e, m, c, b, a, i FROM aineet WHERE aine = 'Biologia' AND laskentatapaid = " + str(laskentatapaID)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        biologia = mycursor.fetchall()[0]

        
        points = {
            "fysiikka": fysiikka[6 - kirjoitetut["fysiikka"]],
            "kemia": kemia[6 - kirjoitetut["kemia"]],
            "biologia": biologia[6 - kirjoitetut["biologia"]]
        }


        yhtfk = fysiikkataikemia[6 - kirjoitetut["fysiikka"]] + kemiataibiologia[6 - kirjoitetut["kemia"]]
        yhtfb = fysiikkataikemia[6 - kirjoitetut["fysiikka"]] + kemiataibiologia[
            6 - kirjoitetut["biologia"]]
        yhtkb = fysiikkataikemia[6 - kirjoitetut["kemia"]] + kemiataibiologia[6 - kirjoitetut["biologia"]]
        # FK + B
        fkb = yhtfk + points["biologia"]
        # FK + M
        fkm = yhtfk + valipisteet
        # FB + K
        fbk = yhtfb + points["kemia"]
        # FB + M
        fbm = yhtfb + valipisteet
        # KB + F
        kbf = yhtkb + points["fysiikka"]
        # KB + M
        kbm = yhtkb + valipisteet
        
        pisteet += max(fkb, fkm, fbk, fbm, kbf, kbm)

    return pisteet

# Testattu, bugeja ei löydetty, havaintojen mukaan pitäisi toimia oikein, Joonas
def yhteiskuntatieteet(syote, laskentatapaID, database, ainelistat):
    #luodaan muuttujat pisteille ja tietokantayhteydelle
    pisteet = 0
    mydb = database
    
    #Lasketaan äidinkielen pisteet ja poistetaan listoista
    metodi = aidinkielen_pisteenlasku_normaali(laskentatapaID, mydb, syote)
    pisteet += metodi[0]
    poistettava = metodi[1]

    poista_aine(poistettava, syote, ainelistat)
    

    #Lasketaan matematiikan pisteet ja poistetaan listoista
    metodi = kauttaviivatilanne("Matematiikka pitkä/Matematiikka lyhyt", syote, laskentatapaID, mydb)
    pisteet += metodi[0]
    poistettava = metodi[1]

    poista_aine(poistettava, syote, ainelistat)
    
    
    #Lasketaan parhaan kielen pisteet ja poistetaan listoista
    metodi = paras_kieli(ainelistat[1], laskentatapaID, "Kieli", mydb)
    pisteet += metodi[0]
    poistettava = metodi[1]
    
    poista_aine(poistettava, syote, ainelistat)
    

    #luodaan bufferit aineille sekä (aine,arvosana) yhdistelmille
    ainelista = []
    pistesailyttaja = []

    #käydään läpi käyttäjän ainereaalit ja täytetään yllä luodut listat ja poistetaan kaikki yhteiskuntatieteelliset aineet ainelistoista
    for reaali in ainelistat[3]:
        if reaali[0] in yhteiskuntatieteelliset_aineet:
            ainelista.append(reaali[0])
            pistesailyttaja.append(reaali)
    
    for i in pistesailyttaja:
        poista_aine(i, syote, ainelistat)


    #määritetään paras reaali ilman yhteiskuntatieteellisiä aineita
    muu_reaali = paras_xxx_ainereaali(ainelistat[3], laskentatapaID, database)[0]

    # ei yhteiskuntatieteellisiä aineita
    if len(ainelista) == 0:
        pisteet += muu_reaali

    # yksi yhteiskuntatieteellinen aine
    elif len(ainelista) == 1:
        
        myresult = hae_pisteet(laskentatapaID, database, "Yhteiskuntatieteellinen aine", pistesailyttaja[0][1])

        if len(myresult) != 0:
            pisteet += myresult[0][0]

        pisteet += muu_reaali

    # kaksi tai enemmän yhteiskuntatieteellistä ainetta
    else:
        
        pistelista = []

        for i in pistesailyttaja:

            myresult = hae_pisteet(laskentatapaID, database, i[0], i[1])
        
            if len(myresult) != 0:
                pistelista.append((myresult[0][0]))


        yhteiskuntatieteelliset_pisteet = []

        for i in range(len(pistesailyttaja)):
            yhteiskuntatieteelliset_pisteet.append(hae_pisteet(laskentatapaID, database, "Yhteiskuntatieteellinen aine", pistesailyttaja[i][1])[0][0])

        yhteiskuntatieteelliset_pisteet_kopio = yhteiskuntatieteelliset_pisteet.copy()

        result_buffer = []
        
        for i in range(len(pistesailyttaja)):
            result_buffer.append(muu_reaali + yhteiskuntatieteelliset_pisteet_kopio[i])

            yhteiskuntatieteelliset_pisteet.remove(yhteiskuntatieteelliset_pisteet_kopio[i])
           
            yhteiskuntatieteelliset_pisteet = sorted(yhteiskuntatieteelliset_pisteet)

            valitulos = pistelista[i] + yhteiskuntatieteelliset_pisteet[len(yhteiskuntatieteelliset_pisteet) - 1]
            result_buffer.append(valitulos)

            yhteiskuntatieteelliset_pisteet = yhteiskuntatieteelliset_pisteet_kopio.copy()

        
        pisteet += sorted(result_buffer)[len(result_buffer) - 1]
        

        #     indeksi = 0
        #     for i in range(len):
        #         if pistelista[i] == pistelista_kopio[len - 2]:
        #             indeksi = i

        #     vaihtoehto_1 = pistelista_kopio[len - 1] 

        #     myresult = hae_pisteet(laskentatapaID, database, "Yhteiskuntatieteellinen aine", pistesailyttaja[indeksi][1])

        #     if len(myresult) != 0:
        #         vaihtoehto_1 += myresult[0][0]

        #     indeksi = 0
        #     for i in range(len):
        #         if pistelista[i] == pistelista_kopio[len - 1]:
        #             indeksi = i

        #     vaihtoehto_2 = muu_reaali

        #     myresult = hae_pisteet(laskentatapaID, database, "Yhteiskuntatieteellinen aine", pistesailyttaja[indeksi][1])

        #     if len(myresult) != 0:
        #         vaihtoehto_2 += myresult[0][0]
            
        #     pisteet += max(vaihtoehto_1, vaihtoehto_2)

        # else:
        #     indeksi = 0
        #     for i in range(len):
        #         if pistelista[i] == pistelista_kopio[len - 2]:
        #             indeksi = i

        #     vaihtoehto_1 = pistelista_kopio[len - 1] 

        #     myresult = hae_pisteet(laskentatapaID, database, "Yhteiskuntatieteellinen aine", pistesailyttaja[indeksi][1])

        #     if len(myresult) != 0:
        #         vaihtoehto_1 += myresult[0][0]

        #     indeksi = 0
        #     for i in range(len):
        #         if pistelista[i] == pistelista_kopio[len - 1]:
        #             indeksi = i

        #     vaihtoehto_2 = pistelista_kopio[len - 2] 

        #     myresult = hae_pisteet(laskentatapaID, database, "Yhteiskuntatieteellinen aine", pistesailyttaja[indeksi][1])

        #     if len(myresult) != 0:
        #         vaihtoehto_2 += myresult[0][0]
            
        #     pisteet += max(vaihtoehto_1, vaihtoehto_2)

    return pisteet

# Tastattu, bugeja ei löydetty, havaintojen mukaan pitäisi toimia oikein, Joonas
def viestintatieteet(syote, laskentatapaID, database, ainelistat):

    #luodaan muuttujat pisteille ja tietokantayhteydelle
    pisteet = 0
    mydb = database

    # lasketaan äidinkielen pisteet
    metodi = aidinkielen_pisteenlasku_normaali(laskentatapaID, mydb, syote)
    pisteet += metodi[0]
    poistettava = metodi[1]

    poista_aine(poistettava, syote, ainelistat)

    # lasketaan matematiikan pisteet
    metodi = kauttaviivatilanne("Matematiikka pitkä/Matematiikka lyhyt", syote, laskentatapaID, mydb)
    matematiikka =  metodi[0]
    poistettava = metodi[1]

    poista_aine(poistettava, syote, ainelistat)


    # lasketaan kielen pisteet
    metodi = paras_kieli(ainelistat[1], laskentatapaID, "Kieli", mydb)
    kieli = metodi[0]
    poistettava = metodi[1]
    
    poista_aine(poistettava, syote, ainelistat)

    # lasketaan parhaan reaalin pisteet
    paras_reaali = paras_xxx_ainereaali(ainelistat[3], laskentatapaID, database)[0]

    #luodaan bufferit aineille ja (aine, arvosana) yhdistelmille
    ainelista = []
    pistesailyttaja = []

    # käydään käyttäjän reaalit läpi ja täytetään bufferit
    for reaali in ainelistat[3]:
        if reaali[0] in yhteiskuntatieteelliset_aineet:
            ainelista.append(reaali[0])
            pistesailyttaja.append(reaali)
    
    for i in pistesailyttaja:
        poista_aine(i, syote, ainelistat)

    # Matematiikan ja kielen pisteet paremmat tai yhtä suuret kuin parhaan reaalin
    if paras_reaali <= matematiikka and paras_reaali <= kieli:
        pisteet += matematiikka
        pisteet += kieli

        paras_arvosana = "I"

        for i in pistesailyttaja:
            if arvosanamuunnin(paras_arvosana) <= arvosanamuunnin(i[1]):
                paras_arvosana = i[1]
        
        myresult = hae_pisteet(laskentatapaID, database, "Yhteiskuntatieteellinen aine", paras_arvosana)

        if len(myresult) != 0:
            pisteet += myresult[0][0]
    
    else:

        #lasketaan reaali ilman yhteiskuntatieteellisiä aineita
        muu_reaali = paras_xxx_ainereaali(ainelistat[3], laskentatapaID, database)[0]

        # muu reaali on sama kuin paras reaali
        if muu_reaali == paras_reaali:
            pisteet += muu_reaali
            pisteet += max(matematiikka, kieli)

            paras_arvosana = "I"

            for i in pistesailyttaja:
                if arvosanamuunnin(paras_arvosana) <= arvosanamuunnin(i[1]):
                    paras_arvosana = i[1]
            
            myresult = hae_pisteet(laskentatapaID, database, "Yhteiskuntatieteellinen aine", paras_arvosana)

            if len(myresult) != 0:
                pisteet += myresult[0][0]
        # muu reaali on huonompi kuin paras kieli
        else:
            #lisätään pisteisiin matematiikan ja kielen pisteistä parempi
            pisteet += max(matematiikka, kieli)
            
            # vain yksi yhteiskuntatieteellinen aine
            if len(ainelista) == 1:
                
                myresult = hae_pisteet(laskentatapaID, database, "Yhteiskuntatieteellinen aine", pistesailyttaja[0][1])

                if len(myresult) != 0:
                    pisteet += myresult[0][0]

                pisteet += max(muu_reaali, min(matematiikka, kieli))
            # kaksi tai useampia yhteiskuntatieteellisiä aineita
            elif muu_reaali >= min(matematiikka, kieli):

                pistelista = []

                for i in pistesailyttaja:

                    myresult = hae_pisteet(laskentatapaID, database, i[0], i[1])
                
                    if len(myresult) != 0:
                        pistelista.append((myresult[0][0]))


                yhteiskuntatieteelliset_pisteet = []
                
                for i in range(len(pistesailyttaja)):
                    myresult = hae_pisteet(laskentatapaID, database, "Yhteiskuntatieteellinen aine", pistesailyttaja[i][1])
                
                    yhteiskuntatieteelliset_pisteet.append(myresult[0][0])

                yhteiskuntatieteelliset_pisteet_kopio = yhteiskuntatieteelliset_pisteet.copy()

                result_buffer = []

                for i in range(len(pistesailyttaja)):
                    result_buffer.append(max(muu_reaali, min(matematiikka, kieli)) + yhteiskuntatieteelliset_pisteet_kopio[i])

                    yhteiskuntatieteelliset_pisteet.remove(yhteiskuntatieteelliset_pisteet_kopio[i])
                    yhteiskuntatieteelliset_pisteet = sorted(yhteiskuntatieteelliset_pisteet)

                    valitulos = max(pistelista[i], min(matematiikka, kieli)) + yhteiskuntatieteelliset_pisteet[len(yhteiskuntatieteelliset_pisteet) - 1]
                    result_buffer.append(valitulos)

                    yhteiskuntatieteelliset_pisteet = yhteiskuntatieteelliset_pisteet_kopio.copy()

                    
                pisteet += sorted(result_buffer)[len(result_buffer) - 1]

                
    return pisteet

# Testattu, löydetyt bugit korjattu, pitäisi toimia oikein kaikissa tilanteissa, Joonas
def saamelainen_kulttuuri(syote, laskentatapaID, database, ainelistat, syote_sailio, kielet_ilman_aidinkielia):
    #luodaan bufferit ja variable
    pisteet = 0
    aidinkielet = ainelistat[2]

    # tutkitaan onko kirjoittanut saamea tai suomea äidinkielien ulkopuolella
    onko_saame = False
    onko_suomi = False

    # poistetaan äidinkielet syote_sailiosta
    for i in aidinkielet:
        syote_sailio.remove(i)

    # tutkitaan onko kirjoittanut saamea tai suomea
    for i in kielet_ilman_aidinkielia:
        if "saame" in i[0]:
            onko_saame = True
        if "Suomi" in i[0]:
            onko_suomi = True

    # haetaan paras lyhyt saame
    paras_saame = ("", "")
    saame_pituus = ""
    if onko_saame:
        for i in kielet_ilman_aidinkielia:
            if "saame" in i[0]:
                if paras_saame == ("", ""):
                    paras_saame = i
                elif arvosanamuunnin(paras_saame[1]) < arvosanamuunnin(i[1]):
                    paras_saame = i

        saame_pituus = paras_saame[0].split(" ")[1]

        # poistetaan paras lyhyt saame syote_sailiosta
        syote_sailio.remove(paras_saame)

    # haetaan paras suomi
    paras_suomi = ("", "")
    suomi_pituus = ""

    if onko_suomi:
        for i in kielet_ilman_aidinkielia:
            if "Suomi" in i[0]:
                if paras_suomi == ("", ""):
                    paras_suomi = i
                elif arvosanamuunnin(paras_suomi[1]) < arvosanamuunnin(i[1]):
                    paras_suomi = i
        
        suomi_pituus = paras_suomi[0].split(" ")[1]

        # poistetaan paras suomi syote_sailiosta
        syote_sailio.remove(paras_suomi)


    # käyttäjällä äidinkieliä 0-1
    if len(aidinkielet) <= 1:
        metodi = aidinkielen_pisteenlasku_normaali(laskentatapaID, database, syote)
        pisteet += metodi[0]
        
        # luodaan kolmea muuta ainetta varten buffer
        muut = []

        # haetaan muut ja lisätään ne bufferiin
        for i in range(3):
            metodi = muu_syotteessa(syote_sailio, laskentatapaID, database)
            if metodi[1] != ("", ""):
                syote_sailio.remove(metodi[1])
            muut.append(metodi[0])
        
        # tehdään pistebufferit suomelle ja saamelle ja lisätään sinne joko nollat tai sekä kohdasta suomi/saame
        # että kohdasta muu saatavat pisteet kyseiselle aineelle
        suomi = []
        saame = []

        if onko_suomi:
            suomi.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", paras_suomi[1])[0][0])
            suomi.append(hae_pisteet(laskentatapaID, database, "Kieli " + str(suomi_pituus), paras_suomi[1])[0][0])
        else:
            suomi.append(0)
            suomi.append(0)
        
        if onko_saame:
            saame.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", paras_saame[1])[0][0])
            saame.append(hae_pisteet(laskentatapaID, database, "Kieli " + str(saame_pituus), paras_saame[1])[0][0])
        else:
            saame.append(0)
            saame.append(0)

        # haetaan huonoin muu muut sisältävästä bufferista
        huonoin_muu = muut[2]

        # luodaan vaihtoehdoille buffer ja lisätään vaihtoehdot bufferiin
        vaihtoehdot = []
        vaihtoehdot.append(suomi[0] + max(saame[1], huonoin_muu))
        vaihtoehdot.append(saame[0] + max(suomi[1], huonoin_muu))
        
        # lisätään muut ja paras vaihtoehto pisteisiin
        pisteet += max(vaihtoehdot)
        pisteet += muut[0]
        pisteet += muut[1]

    # käyttäjällä äidinkieliä kaksi
        
    else:
        # vain kaksi äidinkieltä
        if not onko_saame and not onko_suomi:
            onko_ruotsi = False
            for j in aidinkielet:
                if j[0] == "Ruotsi 2" or j[0] == "Äidinkieli Ruotsi":
                    onko_ruotsi = True
                # kaksi äidinkieltä ja toinen äidinkieli on ruotsi
            if onko_ruotsi:
                arvosana = ""
                for i in aidinkielet:
                    if i[0] == "Ruotsi 2" or i[0] == "Äidinkieli Ruotsi":
                        arvosana = i[1]
                        aidinkielet.remove(i)
                        break
                pisteet += hae_pisteet(laskentatapaID, database, "Äidinkieli", arvosana)[0][0]
                pisteet += hae_pisteet(laskentatapaID, database, "Suomi pitkä", aidinkielet[0][1])[0][0]


                metodi = muu_syotteessa(syote_sailio, laskentatapaID, database)
                pisteet += metodi[0]
                if metodi[1] == ("",""):
                    return pisteet

                syote_sailio.remove(metodi[1])

                metodi = muu_syotteessa(syote_sailio, laskentatapaID, database)
                pisteet += metodi[0]
                if metodi[1] == ("", ""):
                    return pisteet

                syote_sailio.remove(metodi[1])

                metodi = muu_syotteessa(syote_sailio, laskentatapaID, database)
                pisteet += metodi[0]
                if metodi[1] == ("", ""):
                    return pisteet

                syote_sailio.remove(metodi[1])

            
            # kaksi äidinkieltä joista toinen on suomi ja toinen on saame
            else:
                # luodaan variablet pisteille
                vaihtoehto1 = 0
                vaihtoehto2 = 0
                
                # lasketaan vaihtoehdon 1 pisteet
                vaihtoehto1 += hae_pisteet(laskentatapaID, database, "Äidinkieli", aidinkielet[0][1])[0][0]
                vaihtoehto1 += hae_pisteet(laskentatapaID, database, "Suomi pitkä", aidinkielet[1][1])[0][0]

                # lasketaan vaihtoehdon 2 pisteet
                vaihtoehto2 += hae_pisteet(laskentatapaID, database, "Äidinkieli", aidinkielet[1][1])[0][0]
                vaihtoehto2 += hae_pisteet(laskentatapaID, database, "Suomi pitkä", aidinkielet[0][1])[0][0]

                # lisätään paremmat pisteet pisteisiin
                pisteet += max(vaihtoehto1, vaihtoehto2)


                # lasketaan kolmen muun pisteet
                metodi = muu_syotteessa(syote_sailio, laskentatapaID, database)
                pisteet += metodi[0]
                if metodi[1] == ("",""):
                    return pisteet

                syote_sailio.remove(metodi[1])

                metodi = muu_syotteessa(syote_sailio, laskentatapaID, database)
                pisteet += metodi[0]
                if metodi[1] == ("", ""):
                    return pisteet

                syote_sailio.remove(metodi[1])

                metodi = muu_syotteessa(syote_sailio, laskentatapaID, database)
                pisteet += metodi[0]
                if metodi[1] == ("", ""):
                    return pisteet

                syote_sailio.remove(metodi[1])

        # kaksi äidinkieltä ja saame lyhyenä kielenä
        elif not onko_suomi:
            
            # luodaan kolmea muuta ainetta varten buffer
            muut = []

            # haetaan muut ja lisätään ne bufferiin
            for i in range(3):
                metodi = muu_syotteessa(syote_sailio, laskentatapaID, database)
                if metodi[1] != ("", ""):
                    syote_sailio.remove(metodi[1])
                muut.append(metodi[0])
            
            # luodaan bufferit joihin haetaan pisteet järjestyksessä äidinkieli, suomi/saame, muu
            # saamen kohdalla haetaan pisteet vain kohdista suomi/saame ja muu 
            aidinkieli1 = []
            aidinkieli2 = []
            saame = []

            aidinkieli1.append(hae_pisteet(laskentatapaID, database, "Äidinkieli", aidinkielet[0][1])[0][0])
            aidinkieli1.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", aidinkielet[0][1])[0][0])
            aidinkieli1.append(hae_pisteet(laskentatapaID, database, "Kieli pitkä", aidinkielet[0][1])[0][0])
            
            aidinkieli2.append(hae_pisteet(laskentatapaID, database, "Äidinkieli", aidinkielet[1][1])[0][0])
            aidinkieli2.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", aidinkielet[1][1])[0][0])
            aidinkieli2.append(hae_pisteet(laskentatapaID, database, "Kieli pitkä", aidinkielet[1][1])[0][0])

            saame.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", paras_saame[1])[0][0])
            saame.append(hae_pisteet(laskentatapaID, database, "Kieli " + str(saame_pituus), paras_saame[1])[0][0])

            # luodaan buffer kaikille eri kombinaatioille ja täytetään se
            vaihtoehdot = []

            # aidinkieli1 on ruotsi
            if aidinkielet[0][0] == "Ruotsi 2" or aidinkielet[0][0] == "Äidinkieli Ruotsi":
                # A1 + A2 + S/muu
                vaihtoehdot.append(aidinkieli1[0] + aidinkieli2[1] + max(muut[2], saame[1]))
                # A1 + S + A2/muu
                vaihtoehdot.append(aidinkieli1[0] + saame[0] + max(muut[2], aidinkieli2[2]))
                # A2 + S + A1/muu
                vaihtoehdot.append(aidinkieli2[0] + saame[0] + max(muut[2], aidinkieli1[2]))
            # aidinkieli2 on ruotsi
            elif aidinkielet[1][0] == "Ruotsi 2" or aidinkielet[1][0] == "Äidinkieli Ruotsi":
                # A1 + S + A2/muu
                vaihtoehdot.append(aidinkieli1[0] + saame[0] + max(muut[2], aidinkieli2[2]))
                # A2 + A1 + S/muu
                vaihtoehdot.append(aidinkieli2[0] + aidinkieli1[1] + max(muut[2], saame[1]))
                # A2 + S + A1/muu
                vaihtoehdot.append(aidinkieli2[0] + saame[0] + max(muut[2], aidinkieli1[2]))
            # kumpikaan äidinkieli ei ole ruotsi
            else:
                # A1 + A2 + S/muu
                vaihtoehdot.append(aidinkieli1[0] + aidinkieli2[1] + max(muut[2], saame[1]))
                # A1 + S + A2/muu
                vaihtoehdot.append(aidinkieli1[0] + saame[0] + max(muut[2], aidinkieli2[2]))
                # A2 + A1 + S/muu
                vaihtoehdot.append(aidinkieli2[0] + aidinkieli1[1] + max(muut[2], saame[1]))
                # A2 + S + A1/muu
                vaihtoehdot.append(aidinkieli2[0] + saame[0] + max(muut[2], aidinkieli1[2]))

            # lisätään pisteisiin paras vaihtoehdoista sekä kaksi muuta
            pisteet += max(vaihtoehdot)
            pisteet += muut[0]
            pisteet += muut[1]

        # kaksi äidinkieltä ja toinen kotimainen kieli suomi
        elif not onko_saame:

            # luodaan kolmea muuta ainetta varten buffer
            muut = []

            # haetaan muut ja lisätään ne bufferiin
            for i in range(3):
                metodi = muu_syotteessa(syote_sailio, laskentatapaID, database)
                if metodi[1] != ("", ""):
                    syote_sailio.remove(metodi[1])
                muut.append(metodi[0])
            
            # luodaan bufferit joihin haetaan pisteet järjestyksessä äidinkieli, suomi/saame, muu
            # suomen kohdalla haetaan pisteet vain kohdista suomi/saame ja muu 
            aidinkieli1 = []
            aidinkieli2 = []
            suomi = []

            aidinkieli1.append(hae_pisteet(laskentatapaID, database, "Äidinkieli", aidinkielet[0][1])[0][0])
            aidinkieli1.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", aidinkielet[0][1])[0][0])
            aidinkieli1.append(hae_pisteet(laskentatapaID, database, "Kieli pitkä", aidinkielet[0][1])[0][0])
            
            aidinkieli2.append(hae_pisteet(laskentatapaID, database, "Äidinkieli", aidinkielet[1][1])[0][0])
            aidinkieli2.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", aidinkielet[1][1])[0][0])
            aidinkieli2.append(hae_pisteet(laskentatapaID, database, "Kieli pitkä", aidinkielet[1][1])[0][0])

            suomi.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", paras_suomi[1])[0][0])
            suomi.append(hae_pisteet(laskentatapaID, database, "Kieli " + str(suomi_pituus), paras_suomi[1])[0][0])

            # luodaan buffer kaikille eri kombinaatioille ja täytetään se
            vaihtoehdot = []

            # aidinkieli1 on ruotsi
            if aidinkielet[0][0] == "Ruotsi 2" or aidinkielet[0][0] == "Äidinkieli Ruotsi":
                # A1 + A2 + S/muu
                vaihtoehdot.append(aidinkieli1[0] + aidinkieli2[1] + max(muut[2], suomi[1]))
                # A1 + S + A2/muu
                vaihtoehdot.append(aidinkieli1[0] + suomi[0] + max(muut[2], aidinkieli2[2]))
                # A2 + S + A1/muu
                vaihtoehdot.append(aidinkieli2[0] + suomi[0] + max(muut[2], aidinkieli1[2]))
            # aidinkieli2 on ruotsi
            elif aidinkielet[1][0] == "Ruotsi 2" or aidinkielet[1][0] == "Äidinkieli Ruotsi":
                # A1 + S + A2/muu
                vaihtoehdot.append(aidinkieli1[0] + suomi[0] + max(muut[2], aidinkieli2[2]))
                # A2 + A1 + S/muu
                vaihtoehdot.append(aidinkieli2[0] + aidinkieli1[1] + max(muut[2], suomi[1]))
                # A2 + S + A1/muu
                vaihtoehdot.append(aidinkieli2[0] + suomi[0] + max(muut[2], aidinkieli1[2]))
            # kumpikaan äidinkieli ei ole ruotsi
            else:
                # A1 + A2 + S/muu
                vaihtoehdot.append(aidinkieli1[0] + aidinkieli2[1] + max(muut[2], suomi[1]))
                # A1 + S + A2/muu
                vaihtoehdot.append(aidinkieli1[0] + suomi[0] + max(muut[2], aidinkieli2[2]))
                # A2 + A1 + S/muu
                vaihtoehdot.append(aidinkieli2[0] + aidinkieli1[1] + max(muut[2], suomi[1]))
                # A2 + S + A1/muu
                vaihtoehdot.append(aidinkieli2[0] + suomi[0] + max(muut[2], aidinkieli1[2]))

            # lisätään pisteisiin paras vaihtoehdoista sekä kaksi muuta
            pisteet += max(vaihtoehdot)
            pisteet += muut[0]
            pisteet += muut[1]
        # kaksi äidinkieltä ja lyhyt saame sekä toinen kotimainen kieli suomi
        else:
            # luodaan kolmea muuta ainetta varten buffer
            muut = []
            # haetaan muut ja lisätään ne bufferiin
            for i in range(3):
                metodi = muu_syotteessa(syote_sailio, laskentatapaID, database)
                if metodi[1] != ("", ""):
                    syote_sailio.remove(metodi[1])
                muut.append(metodi[0])

            # luodaan säiliö muille jonka avulla buffer muut voidaan palauttaa
            muut_sailio = muut.copy()

            
            # luodaan bufferit joihin haetaan pisteet järjestyksessä äidinkieli, suomi/saame, muu
            # suomen kohdalla haetaan pisteet vain kohdista suomi/saame ja muu 
            aidinkieli1 = []
            aidinkieli2 = []
            suomi = []
            saame = []

            aidinkieli1.append(hae_pisteet(laskentatapaID, database, "Äidinkieli", aidinkielet[0][1])[0][0])
            aidinkieli1.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", aidinkielet[0][1])[0][0])
            aidinkieli1.append(hae_pisteet(laskentatapaID, database, "Kieli pitkä", aidinkielet[0][1])[0][0])
            
            aidinkieli2.append(hae_pisteet(laskentatapaID, database, "Äidinkieli", aidinkielet[1][1])[0][0])
            aidinkieli2.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", aidinkielet[1][1])[0][0])
            aidinkieli2.append(hae_pisteet(laskentatapaID, database, "Kieli pitkä", aidinkielet[1][1])[0][0])

            suomi.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", paras_suomi[1])[0][0])
            suomi.append(hae_pisteet(laskentatapaID, database, "Kieli " + str(suomi_pituus), paras_suomi[1])[0][0])

            saame.append(hae_pisteet(laskentatapaID, database, "Suomi pitkä", paras_saame[1])[0][0])
            saame.append(hae_pisteet(laskentatapaID, database, "Kieli " + str(saame_pituus), paras_saame[1])[0][0])

            # luodaan buffer kaikille eri kombinaatioille ja täytetään se
            vaihtoehdot = []
            # luodaan apumuuttuja vaihtoehtojen luomista varten
            valiaikainen = 0
            
            # aidinkieli1 + suomi + 3 muuta
            valiaikainen += aidinkieli1[0] + suomi[0]

            # päivitetään muut
            muut[2] = max(muut[2], aidinkieli2[2])
            muut.sort(reverse = True)
            muut[2] = max(muut[2], saame[1])

            # lisätään muut apumuuttujaan
            for i in muut:
                valiaikainen += i
            
            # lisätään apumuuttuja vaihtoehtoihin
            vaihtoehdot.append(valiaikainen)


            # nollataan muuttuja valiaikainen
            valiaikainen = 0
            # nollataan buffer muut
            muut = muut_sailio.copy()
            # aidinkieli1 + saame + 3 muuta
            valiaikainen += aidinkieli1[0] + saame[0]

            # päivitetään muut
            muut[2] = max(muut[2], aidinkieli2[2])
            muut.sort(reverse = True)
            muut[2] = max(muut[2], suomi[1])

            # lisätään muut apumuuttujaan
            for i in muut:
                valiaikainen += i
            
            # lisätään apumuuttuja vaihtoehtoihin
            vaihtoehdot.append(valiaikainen)




            # nollataan muuttuja valiaikainen
            valiaikainen = 0
            # nollataan buffer muut
            muut = muut_sailio.copy()
            # aidinkieli2 + suomi + 3 muuta
            valiaikainen += aidinkieli2[0] + suomi[0]

            # päivitetään muut
            muut[2] = max(muut[2], aidinkieli1[2])
            muut.sort(reverse = True)
            muut[2] = max(muut[2], saame[1])

            # lisätään muut apumuuttujaan
            for i in muut:
                valiaikainen += i
            
            # lisätään apumuuttuja vaihtoehtoihin
            vaihtoehdot.append(valiaikainen)




            # nollataan muuttuja valiaikainen
            valiaikainen = 0
            # nollataan buffer muut
            muut = muut_sailio.copy()
            # aidinkieli2 + saame + 3 muuta
            valiaikainen += aidinkieli2[0] + saame[0]

            # päivitetään muut
            muut[2] = max(muut[2], aidinkieli1[2])
            muut.sort(reverse = True)
            muut[2] = max(muut[2], suomi[1])

            # lisätään muut apumuuttujaan
            for i in muut:
                valiaikainen += i
            
            # lisätään apumuuttuja vaihtoehtoihin
            vaihtoehdot.append(valiaikainen)



            # nollataan muuttuja valiaikainen
            valiaikainen = 0
            # nollataan buffer muut
            muut = muut_sailio.copy()
            # aidinkieli1 ei ole ruotsi
            if aidinkielet[0][0] != "Ruotsi 2" and aidinkielet[0][0] != "Äidinkieli Ruotsi":

                # aidinkieli2 + aidinkieli1 + 3 muuta
                valiaikainen += aidinkieli2[0] + aidinkieli1[1]
                # päivitetään muut
                muut[2] = max(muut[2], saame[1])
                muut.sort(reverse = True)
                muut[2] = max(muut[2], suomi[1])
                # lisätään muut apumuuttujaan
                for i in muut:
                    valiaikainen += i
                # lisätään apumuuttuja vaihtoehtoihin
                vaihtoehdot.append(valiaikainen)


            # nollataan muuttuja valiaikainen
            valiaikainen = 0
            # nollataan buffer muut
            muut = muut_sailio.copy()
            # aidinkieli2 ei ole ruotsi
            if aidinkielet[1][0] != "Ruotsi 2" and aidinkielet[1][0] != "Äidinkieli Ruotsi":
                # aidinkieli1 + aidinkieli2 + 3 muuta
                valiaikainen += aidinkieli1[0] + aidinkieli2[1]

                # päivitetään muut
                muut[2] = max(muut[2], saame[1])
                muut.sort(reverse = True)
                muut[2] = max(muut[2], suomi[1])

                # lisätään muut apumuuttujaan
                for i in muut:
                    valiaikainen += i
                # lisätään apumuuttuja vaihtoehtoihin
                vaihtoehdot.append(valiaikainen)
            
            pisteet += max(vaihtoehdot)
    
    return pisteet


def aidinkieli_rajattu(syote, laskentatapaID, database, ainelistat, pisteytettava, muutettu_aidinkieli):
    pisteet = 0.0
    indeksi = 0

    for i in range(len(ainelistat[2])):
        aine = ainelistat[2][i]
        if aine[0] == pisteytettava:
            myresult = hae_pisteet(laskentatapaID, database, pisteytettava, aine[1])

            if len(myresult) != 0 and pisteet < myresult[0][0]:
                pisteet = myresult[0][0]
                indeksi = i
            break
    
    aidinkielien_maara = len(ainelistat[2])
    if aidinkielien_maara == 0:
        poista_aine(("Äidinkieli", "I"), syote, ainelistat)
    elif aidinkielien_maara == 1:
        poista_aine(("Äidinkieli", ainelistat[2][0][1]), syote, ainelistat)
    elif aidinkielien_maara == 2:
        if muutettu_aidinkieli[0] == pisteytettava:
            poista_aine(("Äidinkieli", str(ainelistat[2][indeksi][1])), syote, ainelistat)
            
        else:
            if ainelistat[2][indeksi][0] == "Suomi 2" or ainelistat[2][indeksi][0] == "Ruotsi 2":
                kieli = ainelistat[2][indeksi][0].split(" ")[0]
                aine = kieli + " pitkä"

                for j in syote:
                    if j[0] == aine:
                        poista_aine(j, syote, ainelistat)
                        ainelistat[2].remove((str(ainelistat[2][indeksi][0]), j[1]))
                        break
            else:
                kieli = ainelistat[2][indeksi][0].split(" ")[1]
                aine = kieli + " pitkä"
                for j in syote:
                    if j[0] == aine:
                        poista_aine(j, syote, ainelistat)
                        ainelistat[2].remove(("Äidinkieli " + str(kieli), j[1]))
                        break
            
            if ainelistat[2][0][0] == "Suomi 2" or ainelistat[2][0][0] == "Ruotsi 2":
                aine = ainelistat[2][0][0].split(" ")[0] + " pitkä"
                arvosana = ainelistat[2][0][1]
                syote.append((aine, arvosana))
                ainelistat[0].append(aine)
                ainelistat[1].append((aine, arvosana))
                
            else:
                aine = ainelistat[2][0][0].split(" ")[1] + " pitkä"
                arvosana = ainelistat[2][0][1]
                syote.append((aine, arvosana))
                ainelistat[0].append(aine)
                ainelistat[1].append((aine, arvosana))
            
            poista_aine(("Äidinkieli", ainelistat[2][0][1]), syote, ainelistat)

    return pisteet


