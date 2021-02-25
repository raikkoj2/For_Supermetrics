# Sivustolla korkeakouluun.fi toimivan laskurin lähdekoodi.
# Koodin dokumentaatio on erillisessä tiedostossa 'documentation.txt', mutta
# koodia on kommentoitu siten, että koodia voi ymmärtää lukematta dokumentaatiota.
# Viimeisin muokkausajankohta: 25.11.2020
# Tekijät: Jere Niemi & Joonas Räikkönen

# VIIMEISIMMÄT MUUTOKSET
# 25.11.2020 00.30
# Koodiin on implementoitu tarvittavat metodit äidinkielen käsittelyä varten
# 25.11.2020 01.05
# Koodiin on implementoitu tarvittavat metodit uskonnolisten aineiden käsittelyä varten
#


# Työkalut ohjelman ulkopuolelta.
import psycopg2
import time
import json
import os



# metodit ja muuttujat toisista tiedostoista

from .aineiden_kasittelijat import aineet_syotteesta, kielet_syotteesta, paras_aidinkielen_arvosana_syotteesta, poista_aine, xxx_syotteesta, aidinkielet_syotteesta
from .kynnysehtojen_tarkistin import tayttyyko_kynnysehto
from .laskumetodit import aidinkielen_pisteenlasku_normaali, aineen_pistelasku, kauttaviivatilanne, paras_kieli_pitka, paras_kieli
from .laskumetodit import paras_xxx_ainereaali, paras_xxx_aine, kaksi_kolmesta, muu_syotteessa
from .apumetodit import convert
from .erikoislaskutavat import elintarviketiede, viestintatieteet, yhteiskuntatieteet, saamelainen_kulttuuri, aidinkieli_rajattu
from .aineet import ainereaalit, matemaattiset_aineet, yhteiskuntatieteelliset_aineet, aidinkielet, uskonnolliset_aineet


# Alustaa laskutoimituksen ohjelman suorituksen kestolle.
start_time = time.time()

# Alustaa tarvittavat listat.

# Tämä osio koodista on musta aukko. Singulariteetti. Paikka, josta ei pakene valo eikä varsinkaan teekkari.
# Aamuja lukijalle.

# Pääfunktio, joka suorittaa itse laskutoimituksen hyödyntäen ylläolevia funktioita.
def laskuri_yliopisto(parametri):
    if len(parametri) == 0:
        return None

    # syote = Tulee käyttäjältä, yhdistetään myöhemmin.
    syote = parametri.copy()
    # ajettava ennen äidinkieliä koska aidinkielet_syotteesta lisää kielien määrää, Huom ajetaan uudelleen alempana
    kielet_ilman_aidinkielia = kielet_syotteesta(syote)
    metodi = aidinkielet_syotteesta(syote, aidinkielet, kielet_ilman_aidinkielia)
    kayttajan_aidinkielet_sailio = metodi[0]
    muutettu_aidinkieli = metodi[1]
    kayttajan_aineet_sailio = aineet_syotteesta(syote)
    kayttajan_kielet_sailio = kielet_syotteesta(syote)
    kayttajan_ainereaalit_sailio = xxx_syotteesta(syote, ainereaalit)
    kayttajan_matemaattiset_ainereaalit_sailio = xxx_syotteesta(syote, matemaattiset_aineet)
    kayttajan_uskonnolliset_ainereaalit_sailio = xxx_syotteesta(syote, uskonnolliset_aineet)
    kayttajan_yhteiskuntatieteeliset_ainereaalit_sailio = xxx_syotteesta(syote, yhteiskuntatieteelliset_aineet)
    

    syote_sailio = syote.copy()

    # Luodaan lista kirjoitetuista aineista ja numeroiduista arvosanoista 
    kayttajan_arvosanat = convert(parametri)
    # lisätään listaan parhaan äidinkielen arvosana
    paras_aidinkieli = paras_aidinkielen_arvosana_syotteesta(kayttajan_aidinkielet_sailio)
    kayttajan_arvosanat.append(("Äidinkieli", paras_aidinkieli))
    
    
    mydb = psycopg2.connect(
        host=os.environ['KK_DB_HOST'],
        database=os.environ['KK_DB_NAME'],
        user=os.environ['KK_DB_USER'],
        password=os.environ['KK_DB_PASSWORD']
    )


    # määritetään hakukohteiden määrä tietokannasta
    mycursor = mydb.cursor()
    sql = "SELECT COUNT(hakukohdeid) FROM hakukohde"
    mycursor.execute(sql)
    hakukohteiden_maara = mycursor.fetchall()[0][0]


    #Alustetaan buffer hakukohteita varten (hakukohdeID, pisteraja, saadut pisteet, kynnysehto läpäisty, pääseekö sisään, marginaali)
    final_buffer = []
    # alustetaan testibufferi hakukohteita varten (hakukohdeID, yliopisto, nimi, pisteraja, saadut pisteet, kynnysehto läpäisty, pääseekö sisään, marginaali)
    final_test_buffer = []

    #Luodaan tyhjät bufferit buffereihin
    for i in range(hakukohteiden_maara):
        final_test_buffer.append([0, "", "", 0.0, 0.0, False, False, 0.0])
        final_buffer.append([0, 0.0, 0.0, False, False, 0.0])
    

    # määritetään laskentatapojen määrä
    mycursor = mydb.cursor()
    sql = "SELECT COUNT(laskentatapaid) FROM laskentatapa"
    mycursor.execute(sql)
    laskentatapojen_maara = mycursor.fetchall()[0][0]

    # Suorittaa varsinaisen pistelaskun käyttämällä yllä olevia erillismetodeja. 'Tulos' sisältää hakukohteiden
    # lukumäärän.
    for i in range(laskentatapojen_maara):
        laskentatapaID = i + 1
        pisteet = 0

        sql = "SELECT laskutapa FROM laskentatapa WHERE laskentatapaid = " + str(laskentatapaID)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        # laskentatapa sisältää laskutavan hakukohteelle.
        laskentatapa = mycursor.fetchall()

        aineet_joista_pisteita = laskentatapa[0][0].split(",")
        
        kayttajan_aineet = kayttajan_aineet_sailio.copy()
        kayttajan_kielet = kayttajan_kielet_sailio.copy()
        kayttajan_aidinkielet = kayttajan_aidinkielet_sailio.copy()
        kayttajan_ainereaalit = kayttajan_ainereaalit_sailio.copy()
        kayttajan_matemaattiset_ainereaalit = kayttajan_matemaattiset_ainereaalit_sailio.copy()
        kayttajan_uskonnolliset_ainereaalit = kayttajan_uskonnolliset_ainereaalit_sailio.copy()
        kayttajan_yhteiskuntatieteeliset_ainereaalit = kayttajan_yhteiskuntatieteeliset_ainereaalit_sailio.copy()
        

        ainelistat = [kayttajan_aineet, kayttajan_kielet, kayttajan_aidinkielet, kayttajan_ainereaalit, kayttajan_matemaattiset_ainereaalit, kayttajan_uskonnolliset_ainereaalit, kayttajan_yhteiskuntatieteeliset_ainereaalit]

        # Tutkii laskutapaa alkio kerrallaan.
        for b in aineet_joista_pisteita:

            if laskentatapaID == 12:
                pisteet = yhteiskuntatieteet(syote, laskentatapaID, mydb, ainelistat)
                break
            #if laskentatapaID == 15:
            #    pisteet = elintarviketiede(syote, laskentatapaID, mydb, ainelistat)
            #    break
            if laskentatapaID == 44:
                pisteet = viestintatieteet(syote, laskentatapaID, mydb, ainelistat)
                break
            if laskentatapaID == 48:
                pisteet = saamelainen_kulttuuri(syote, laskentatapaID, mydb, ainelistat, parametri.copy(), kielet_ilman_aidinkielia.copy())
                break
            elif "Äidinkieli" == b:
                metodi = aidinkielen_pisteenlasku_normaali(laskentatapaID, mydb, syote)
                pisteet += metodi[0]
                poistettava = metodi[1]
                poista_aine(poistettava, syote, ainelistat)
            # elif laskentatapaID == 54 and "Suomi 2" == b:
            #     metodi = aidinkieli_rajattu(syote, laskentatapaID, mydb, ainelistat, b, muutettu_aidinkieli)
            #     pisteet += metodi
            elif "Äidinkieli" in b or (laskentatapaID == 54 and "Suomi 2" == b):
                metodi = aidinkieli_rajattu(syote, laskentatapaID, mydb, ainelistat, b, muutettu_aidinkieli)
                pisteet += metodi
            # Jos kahta tilanteena on "kahdesta paras", suoritetaan alla oleva koodinpätkä.
            elif "Kaksi parasta kolmesta" in b:
                pisteet += kaksi_kolmesta(ainelistat, laskentatapaID, syote, b, mydb)
                break
            elif "/" in b:
                metodi = kauttaviivatilanne(b, syote, laskentatapaID, mydb)
                pisteet += metodi[0]
                poistettava = metodi[1]
                # Poistetaan parempi aine syötteestä.
                if len(poistettava) != 0:
                    poista_aine(poistettava, syote, ainelistat)
            # Jos laskutavassa valitaan jokin syötteessä jäljellä olevista aineista, suoritetaan alla oleva koodinpätkä.
            elif "Muu" == b:
                metodi = muu_syotteessa(syote, laskentatapaID, mydb)
                pisteet += metodi[0]
                poistettava = metodi[1]
                poista_aine(poistettava, syote, ainelistat)

            # Jos laskutavassa esiintyy sana 'Kieli', tutkitaan käyttäjän kirjoittamia kieliä ja valitaan
            # parhaat pisteet tuottava.
            elif "Kieli1 pitkä" == b:
                metodi = paras_kieli_pitka(kayttajan_kielet, laskentatapaID, mydb)
                pisteet += metodi[0]
                poistettava = metodi[1]
                poista_aine(poistettava, syote, ainelistat)
            elif "Kieli1" == b:
                metodi = paras_kieli(kayttajan_kielet, laskentatapaID, "Kieli1", mydb)
                pisteet += metodi[0]
                poistettava = metodi[1]
                poista_aine(poistettava, syote, ainelistat)
            elif "Kieli" in b:
                metodi = paras_kieli(kayttajan_kielet, laskentatapaID, "Kieli", mydb)
                pisteet += metodi[0]
                poistettava = metodi[1]
                poista_aine(poistettava, syote, ainelistat)
            # Jos laskutavassa esiintyvät sanat 'paras ainereaali', tutkitaan käyttäjän kirjoittamia ainereaaleja
            # ja valitaan parhaiten pisteitä tuottava.
            elif "Reaali" == b:
                metodi = paras_xxx_ainereaali(kayttajan_ainereaalit, laskentatapaID, mydb)
                pisteet += metodi[0]
                poistettava = metodi[1]
                poista_aine(poistettava, syote, ainelistat)
            elif "Matemaattinen aine" == b:
                metodi = paras_xxx_ainereaali(kayttajan_matemaattiset_ainereaalit, laskentatapaID, mydb)
                pisteet += metodi[0]
                poistettava = metodi[1]
                poista_aine(poistettava, syote, ainelistat)
            elif "Yhteiskuntatieteellinen aine" == b:
                metodi = paras_xxx_aine(kayttajan_yhteiskuntatieteeliset_ainereaalit, laskentatapaID, b, mydb)
                pisteet += metodi[0]
                poistettava = metodi[1]
                poista_aine(poistettava, syote, ainelistat)
            elif "Uskonnollinen aine" == b:
                metodi = paras_xxx_aine(kayttajan_uskonnolliset_ainereaalit, laskentatapaID, b, mydb)
                pisteet += metodi[0]
                poistettava = metodi[1]
                poista_aine(poistettava, syote, ainelistat)
            # Jos pistelaskutapana on valita 'kaksi parhaiten pisteitä tuottavaa ainetta kolmesta eri vaihtoehdosta',
            # suoritetaan alla oleva osa. Senkin suorittaminen psäyttää for-loopin.
            else:
                # Laskee pisteet laskutavan alkuosan "yksittäisaineille". Lisätietoja rivillä 28.
                metodi = aineen_pistelasku(b, b, syote, laskentatapaID, mydb, kayttajan_aineet)
                pisteet += metodi[0]
                poistettava = metodi[1]
                poista_aine(poistettava, syote, ainelistat)

        # Palauttaa alkuperäisen syötteen, sillä syötteestä poistetaan aineita käsittelyn aikana.
        syote = syote_sailio.copy()

            
        # haetaan hakukohdeID:t jotka käyttävät kyseistä laskentatapaa
        sql = "SELECT hakukohde.hakukohdeid, nimi, yliopisto, pistemaara, kynnysehdot FROM kuuluu, hakukohde WHERE hakukohde.hakukohdeid = kuuluu.hakukohdeid AND laskentatapaid = " + str(laskentatapaID)
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        # laskentatapa sisältää laskutavan hakukohteelle.
        hakukohteet = mycursor.fetchall()
        
        
        for hakukohde in hakukohteet:
            #määritetään hakukohteen indeksi final bufferissa
            indeksi = hakukohde[0] - 1

            #haetaan kynnysehdot tietokannasta
            sql = "SELECT aine, arvosana FROM kynnysehto WHERE hakukohdeid = " + str(hakukohde[0])
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            aine_ja_arvosana = mycursor.fetchall()
            
            #tarkistetaan kynnysehdot
            kynnysehto_tayttyy = tayttyyko_kynnysehto(hakukohde[4], convert(aine_ja_arvosana), kayttajan_arvosanat, str(hakukohde[0]))

            #lisätään hakukohdeID final bufferiin
            final_buffer[indeksi][0] = indeksi + 1
            #lisäään pisteraja final bufferiin
            final_buffer[indeksi][1] = hakukohde[3]
            #lisätään saadyt pisteet final bufferiin

            final_buffer[indeksi][2] = round(pisteet, 1)
            #lisätään tieto kynnysehdosta final bufferiin
            final_buffer[indeksi][3] = kynnysehto_tayttyy


             #Tarkistetaan riittävätkö arvosanat sisäänpääsyyn ja lisätään tieto final_bufferiin
            if final_buffer[indeksi][1] <= pisteet and final_buffer[indeksi][3]:
                final_buffer[indeksi][4] = True
            else:
                final_buffer[indeksi][4] = False

            #lisätään marginaali final bufferiin
            final_buffer[indeksi][5] = round(((pisteet / hakukohde[3]) - 1) * 100, 1)



    #         #TESTI BUFFERIN TÄYDENNYS

    #         #lisätään hakukohdeID final bufferiin
    #         final_test_buffer[indeksi][0] = indeksi + 1
    #         #lisätään yliopisto final bufferiin
    #         final_test_buffer[indeksi][1] = hakukohde[2]
    #         # lisätään hakukohteen nimi final bufferiin
    #         final_test_buffer[indeksi][2] = hakukohde[1]
    #         #lisäään pisteraja final bufferiin
    #         final_test_buffer[indeksi][3] = hakukohde[3]
    #         #lisätään saadyt pisteet final bufferiin
    #         final_test_buffer[indeksi][4] = round(pisteet, 1)
    #         #lisätään tieto kynnysehdosta final bufferiin
    #         final_test_buffer[indeksi][5] = kynnysehto_tayttyy     
    #         #lisätään tieto ssäänpääsystä final bufferiin
    #         final_test_buffer[indeksi][6] = final_buffer[indeksi][4]
    #         #lisätään marginaali final bufferiin
    #         final_test_buffer[indeksi][7] = round(((pisteet / hakukohde[3]) - 1) * 100, 1)
            
           
        


    # # # # Seuraavat kohdat testaamista varten

    # # # Tulostaa lopputuloksen jokaiselle mahdolliselle hakukohteelle Suomen yliopistoissa.
    # # for i in final_buffer:
    # #     print(i)


    # # Bufferi tarkasteltavia hakukohteita varten
    # test_buffer = [1, 3, 10, 7, 11 ,12, 20, 21, 22, 23, 24, 25, 27, 29, 31, 33, 35, 36, 40, 41, 42, 43, 51, 52, 53, 54, 55, 57, 58, 60, 61, 62, 63, 64, 69, 73, 74, 75, 79, 89, 99, 104, 45, 115, 121, 124, 135, 176, 177, 240, 246, 291, 294]
    
    # # Tulostaa tarkastelussa olevien hakukohteiden hakukohdeid:n, laskentatapaid:n, nimen, saadut pisteet, läpäisikö kynnysehdon, pääseekö opiskelemaan ja marginaalin
    # for i in test_buffer:
    #     index = i - 1
    #     laskentatapaid = test_buffer.index(i) + 1
    #     print("hakukohdeID = " + str(i) + "\nlaskentatapaID = " + str(laskentatapaid))
    #     print("nimi: " + final_test_buffer[index][2])
    #     print("pisteraja: " + str(final_test_buffer[index][3]))
    #     print("pisteet = " + str(final_test_buffer[index][4]) + "\nkynnysehto läpäisty = " + str(final_test_buffer[index][5]))
    #     print("Pääsee opiskelemaan: " + str(final_test_buffer[index][6]))
    #     print("Marginaali = " + str(final_test_buffer[index][7]))
    #     print()

    # palauta final buffer
    return json.dumps(final_buffer)


# # Suorittaa itse koodin.
# laskuri_yliopisto([("Äidinkieli Ruotsi", "E")])

# # Tulostaa ohjelman suorituksen keston.
# print()
# print("Laskuri toimi ajassa:", round((1000 * (time.time() - start_time)), 2), "ms.")

# tulostaa sql kutsuihin kuluneen ajan ja niiden määrän
# print()
# print("SQL kutsuja tehtiin: " + str(kpl))
# print("Kutsut veivät aikaa:", round((1000 * aika), 2), "ms.")
