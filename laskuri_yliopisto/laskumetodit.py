from apumetodit import hae_pisteet
from aineiden_kasittelijat import poista_aine, on_kieli
import psycopg2



# Laskee käyttäjän syötteen alkupään sidotuille aineille pisteet.
# Sidotulla aineella tarkoitetaan esimerkiksi ainetta äidinkieli tilanteessa,
# jossa pisteenlaskutapa on muotoa ("Äidinkieli, Fysiikka, paras kieli, paras ainereaali).
# Toimii, tarkastanut Jere
def aineen_pistelasku(aine, hakusana, syote, laskentatapaID, database, kayttajan_aineet):
    pisteet = 0
    # Tarkastelu kohdistuu nimenomaan ensimmäiseen alkioon. Alkio poistetaan main-funktiossa
    # käsittelyn jälkeen.
    if aine in kayttajan_aineet:

        indeksi = 0
        for i in range(len(syote)):
            if aine == syote[i][0]:
                indeksi = i
                break

        myresult = hae_pisteet(laskentatapaID, database, hakusana, syote[indeksi][1])

        if len(myresult) != 0:
            pisteet = myresult[0][0]
            return pisteet, syote[indeksi]
    # Palauttaa syotteen ensimmäisen alkion pistemäärän.
    return (0, "")

    
# def aineen_pistelasku_testimetodi():
#     syote = [("Äidinkieli", "L"), ("Matematiikka pitkä", "E"), ("Kemia", "A")]
#     aine = "Kemia"
#     hakusana = aine
#     aineet = ["Äidinkieli", "Matematiikka pitkä", "Kemia"]
#     database = psycopg2.connect(
#         host="localhost",
#         database="testeri1",
#         user="postgres",
#         password="GDCube201"
#     )
#     testipuskuri = [3.7, 3.7, 4.5, 5.7, 4.5, 5.7]
#     pisteet = []
#     post = []
#     for i in range(6):
#         pisteet.append(aineen_pistelasku(aine, hakusana, syote, 36 + i, database, aineet)[0])
#         print(pisteet)
#         post.append(aineen_pistelasku(aine, hakusana, syote, 36 + i, database, aineet)[1])
#     for i in range(6):
#         print(pisteet[i] == testipuskuri[i])
#         # print(testipuskuri[i])
#         # print(pisteet[i])


# Tässä tarkastellaan tilannetta pistelaskutavassa, jossa kahdesta aineesta valitaan parempi.
# Toimii, testannut Jere
def kauttaviivatilanne(alkio, syote, laskentatapaID, database):
    ainetarkastelulista = alkio.split("/")
    # Muuttujaan 'valitse_parempi' tallennetaan toistaiseksi paremmat pisteet tuottava aine.
    pisteet = 0
    poistettava = ("", "")
    # Seuraavaksi käydään läpi ainetarkastelulistaa, jossa on tallennettuna kaksi kauttaviivalla
    # eroteltua ainetta. Kummankin kohdalla niitä verrataan syötteeseen. Jos syötteessä on alkio, sille haetaan
    # SQL-tietokannasta ainetta vastaava pistemäärä.
    for i in ainetarkastelulista:
        for j in syote:
            if j[0] == i:

                myresult = hae_pisteet(laskentatapaID, database, j[0], j[1])

                # Jos nyt saatu pistemäärä on parempi kuin muuttujaan 'valitse_parempi' on tallennettu, arvo
                # päivitetään vastaamaan parempaa arvoa.
                if len(myresult) != 0 and myresult[0][0] > pisteet:
                    pisteet = myresult[0][0]
                    # Paremman arvosanan tuottama aine poistetaan käyttäjän syötteestä main-funktiossa.
                    poistettava = j
                    break
    # Funktio palauttaa paremman pistemäärän ja syötteestä poistettavan alkion
    return pisteet, poistettava


# def kauttaviivatilanne_testeri():
#     syote = [("Matematiikka lyhyt", "L"), ("Matematiikka pitkä", "M"), ("Espanja lyhyt", "L"), ("Espanja keskipitkä", "E")]
#     aine = "Kemia"
#     database = psycopg2.connect(
#         host="localhost",
#         database="testeri1",
#         user="postgres",
#         password="GDCube201"
#     )
#     test = kauttaviivatilanne("Matematiikka pitkä/Matematiikka lyhyt", syote, 29, database)
#     print(test)
#
#
# kauttaviivatilanne_testeri()


# Jos pistelaskutavassa halutaan esimerkiksi kolme muuta parhaiten pisteitä tuottavaa ainetta,
# tämä skripti laskee lopuista aineista parhaat.
# Testattu, toimii
def muu_syotteessa(syote, laskentatapaID, database):
    pisteet = 0.0
    poistettava = ("", "")
    for i in syote:
        hakusana = i[0]
        if on_kieli(i):
            hakusana = "Kieli " + str(i[0].split(" ")[1])

        myresult = hae_pisteet(laskentatapaID, database, hakusana, i[1])
        if len(myresult) != 0 and myresult[0][0] > pisteet:
            pisteet = myresult[0][0]
            poistettava = i
    return (pisteet, poistettava)

# database = psycopg2.connect(
#      host="localhost",
#      database="testeri1",
#      user="postgres",
#      password="GDCube201"
#      )
# for i in range(52):
#     print(muu_syotteessa([("Matematiikka lyhyt", "L"), ("Matematiikka pitkä", "M"), ("Espanja lyhyt", "L"), ("Espanja keskipitkä", "E")], i + 1, database))
#     print(i + 1)



# Hakee pisteet parhaalle pitkälle kielelle
# metodia käytetään vain hakukohteen 3 kohdalla
# Testattu, toimii, Joonas
def paras_kieli_pitka(kayttajan_kielet, laskentatapaID, database):
    pisteet = 0.0
    poistettava = ("", "")

    for i in kayttajan_kielet:
        pilkkoja = i[0].split(" ")

        if pilkkoja[1] == "pitkä":

            myresult = hae_pisteet(laskentatapaID, database, "Kieli1 pitkä", i[1])

            if len(myresult) != 0 and myresult[0][0] > pisteet:
                pisteet = myresult[0][0]
                poistettava = i

    return (pisteet, poistettava)




# database = psycopg2.connect(
# host="localhost",
# database="laskurin_data",
# user="postgres",
# password="kkouluun"
# )

# print(paras_kieli_pitka([("Espanja pitkä", "C"), ("Englanti pitkä", "L"), ("Saksa pitkä", "L")], 3, database))
# print(3)
# print()




# Laskee käyttäjän kirjoittamista kielistä parhaat pisteet tuottavan kielen.
# Testattu, toimii, Joonas
def paras_kieli(kayttajan_kielet, laskentatapaID, hakusana, database):
    pisteet = 0.0
    poistettava = ("", "")
    # Käy läpi käyttäjän kielet ja laskee jokaiselle pisteet, jotka tallennetaan vertailua varten ylläolevaan
    # listaan 'pisteet[]'.
    for i in kayttajan_kielet:
        pilkkoja = i[0].split(" ")
        
        myresult = hae_pisteet(laskentatapaID, database, str(hakusana) + " " + str(pilkkoja[1]), i[1])

        if len(myresult) != 0 and myresult[0][0] > pisteet:
            pisteet = myresult[0][0]
            poistettava = i
   
    return (pisteet, poistettava)
    # Palauttaa listan viimeisen alkion, eli alkion, joka antaa käyttäjälle suurimmat pisteet.


# database = psycopg2.connect(
# host="localhost",
# database="laskurin_data",
# user="postgres",
# password="kkouluun"
# )

# for i in range(52):
#     print(paras_kieli([("Espanja pitkä", "C"), ("Englanti lyhyt", "E"), ("Saksa keskipitkä", "L")], i + 1, "Kieli", database))
#     print(i + 1)
#     print()




# Sama toimintaperiaate kuin funktiolla 'paras_kieli'. Laskee käyttäjälle parhaat pisteet tuottavan ainereaalin.
# def paras_ainereaali(ainelistat[3], laskentatapaID, database):
#     pisteet = 0.0
#     poistettava = ("", "")

#     # Käy läpi käyttäjän kirjoittamat ainereaalit
#     for i in ainelistat[3]:

#         myresult = hae_pisteet(laskentatapaID, database, i[0], i[1])

#         if len(myresult) != 0 and myresult[0][0] > pisteet:
#             pisteet = myresult[0][0]
#             poistettava = i
   
#     return (pisteet, poistettava)
#     # Palauttaa listan viimeisen alkion, eli alkion, joka antaa käyttäjälle suurimmat pisteet.

# tilanteisiin joissa haetaan tieto tietokannasta syötteessä olevalla aineella
# paras ainereaali, paras_matemaattinen ainereaali
# Testattu, toimii, Joonas
def paras_xxx_ainereaali(kayttajan_xxx_ainereaalit, laskentatapaID, database):
    pisteet = 0.0
    poistettava = ("", "")
    # Käy läpi käyttäjän kirjoittamat matemaattiset ainereaalit
    for i in kayttajan_xxx_ainereaalit:

        myresult = hae_pisteet(laskentatapaID, database, i[0], i[1])

        if len(myresult) != 0 and myresult[0][0] > pisteet:
            pisteet = myresult[0][0]
            poistettava = i
            
    return (pisteet, poistettava)


# database = psycopg2.connect(
# host="localhost",
# database="laskurin_data",
# user="postgres",
# password="kkouluun"
# )

# for i in range(52):
#     print(paras_xxx_ainereaali([("Fysiikka", "E"), ("Kemia", "E")], i + 1, database))
#     print(i + 1)
#     print()





#TOIMII. tarkastanut Joonas
#
# Selvittää käyttäjän parhaan matemaattisen ainereaalin.
# def paras_matemaattinen_ainereaali(ainelistat[4], laskentatapaID, database):
#     pisteet = 0.0
#     poistettava = ("", "")
#     # Käy läpi käyttäjän kirjoittamat matemaattiset ainereaalit
#     for i in ainelistat[4]:

#         myresult = hae_pisteet(laskentatapaID, database, i[0], i[1])

#         if len(myresult) != 0 and myresult[0][0] > pisteet:
#             pisteet = myresult[0][0]
#             poistettava = i
            
#     # Asettaa pisteet kasvavaan suuruusjärjestykseen
    
#     # Palauttaa listan viimeisen alkion, eli alkion, joka antaa käyttäjälle suurimmat pisteet.
#     return (pisteet, poistettava)




# Tilanteisiin joissa käytetään erillistä hakusanaa pisteiden laskuun
# (Yhteiskuntatieteellinen aine,) Uskonnollinen aine
# Testattu, toimii, Joonas
def paras_xxx_aine(kayttajan_xxx_aineet, laskentatapaID, hakusana, database):
    pisteet = 0.0
    poistettava = ("", "")
    # Käy läpi käyttäjän kirjoittamat yhteiskuntatieteelliset ainereaalit
    for i in kayttajan_xxx_aineet:

        myresult = hae_pisteet(laskentatapaID, database, hakusana, i[1])

        if len(myresult) != 0 and myresult[0][0] > pisteet:
            pisteet = myresult[0][0]
            poistettava = i

    return (pisteet, poistettava)



# database = psycopg2.connect(
# host="localhost",
# database="laskurin_data",
# user="postgres",
# password="kkouluun"
# )

# for i in range(52):
#     print(paras_xxx_aine([("Yhteiskuntaoppi", "E"), ("Historia", "M"), ("Psykologia", "L")], i + 1, "Yhteiskuntatieteellinen aine", database))
#     print(i + 1)
#     print()




# TOIMII, tarkistanut Joonas
# 
# Selvittää käyttäjän parhaan yhteiskuntatieteellisen ainereaalin.
# def paras_yhteiskuntatieteellinen_ainereaali(ainelistat[6], laskentatapaID, database):
#     pisteet = 0
#     poistettava = ("", "")
#     # Käy läpi käyttäjän kirjoittamat yhteiskuntatieteelliset ainereaalit
#     for i in ainelistat[6]:

#         myresult = hae_pisteet(laskentatapaID, database, "Yhteiskuntatieteellinen aine", i[1])

#         if len(myresult) != 0 and myresult[0][0] > pisteet:
#             pisteet = myresult[0][0]
#             poistettava = i
#     # Asettaa pisteet kasvavaan suuruusjärjestykseen
#     # Palauttaa listan viimeisen alkion, eli alkion, joka antaa käyttäjälle suurimmat pisteet.

#     return (pisteet, poistettava)

# Laskee pisteet tilanteesta, jossa halutaan tietää kaksi parhaiten tuottavaa ainetta kolmesta.
# Esimerkiksi pistelaskutapana saattaa olla tilanne (Fysiikka, paras kieli, paras ainereaali).
# Testattu, Toimii, Joonas
def kaksi_kolmesta(ainelistat, laskentatapaID, syote, b, database):
    syotteen_pilkkominen = b.split(": ")
    # Sisältää esimerkiksi listan (Fysiikka, paras kieli, paras ainereaali)
    ainelista = syotteen_pilkkominen[1].split("\\")
    pisteet = []
    # Tarkastaa, onko pistelaskutavassa ilmoitettua ainetta syötteessä.
    for i in ainelista:
        if "/" in i:
            metodi = kauttaviivatilanne(i, syote, laskentatapaID, database)
            pisteet.append(metodi[0])
            poistettavat = i.split('/')

            for j in poistettavat:
                if j in ainelistat[0]:
                    for k in syote:
                        if k[0] == j:
                            poista_aine(k, syote, ainelistat)

        elif i == "Kieli":
            pisteet.append(paras_kieli(ainelistat[1], laskentatapaID, i, database)[0])

            lista_kopio = ainelistat[1].copy()

            for x in lista_kopio:
                poista_aine(x, syote, ainelistat)

        elif i == "Reaali":
            pisteet.append(paras_xxx_ainereaali(ainelistat[3], laskentatapaID, database)[0])

            lista_kopio = ainelistat[3].copy()

            for x in lista_kopio:
                poista_aine(x, syote, ainelistat)

        elif i == "Matemaattinen aine":
            pisteet.append(paras_xxx_ainereaali(ainelistat[4], laskentatapaID, database)[0])
            
            lista_kopio = ainelistat[4].copy()

            for x in lista_kopio:
                poista_aine(x, syote, ainelistat)

        # Kommentoituna on kaksi if lauseketta jotka saattavat olla hyödyllisiä joskus, mutta
        # tämänhetkisillä laskentatavoilla kyseisiä metodeita ei tarvita

        # elif i == "Yhteiskuntatieteellinen aine":
        #     pisteet.append(paras_xxx_aine(ainelistat[6], laskentatapaID, i, database)[0])
           
        #     lista_kopio = ainelistat[6].copy()

        #     for x in lista_kopio:
        #         poista_aine(x, syote, ainelistat)

        # elif i == "Uskonnollinen aine":
        #     pisteet.append(paras_xxx_aine(ainelistat[5], laskentatapaID, i, database)[0])
           
        #     lista_kopio = ainelistat[5].copy()

        #     for x in lista_kopio:
        #         poista_aine(x, syote, ainelistat)

        # elif i == "Äidinkieli":
        #     pisteet.append(paras_xxx_aine(ainelistat[2], laskentatapaID, i, database)[0])

        #     lista_kopio = ainelistat[2].copy()

        #     for x in lista_kopio:
        #         poista_aine(x, syote, ainelistat)

        else:
            aine_loytyi = False
            for aine in syote:
                if aine[0] == i:
                    aine_loytyi = True
                    poistettava = aine

                    myresult = hae_pisteet(laskentatapaID, database, aine[0], aine[1])

                    if len(myresult) != 0:
                        pisteet.append(myresult[0][0])
                    else:
                        pisteet.append(0)
                    poista_aine(poistettava, syote, ainelistat) 
            if not aine_loytyi:
                pisteet.append(0)
        
        

    pisteet = sorted(pisteet)
    palautusarvo = 0
    palautusarvo += pisteet[len(pisteet) - 1]
    palautusarvo += pisteet[len(pisteet) - 2]

    
    return palautusarvo




    
# Normaalitilanteessa äidinkielen pisteenlaskuun
# syöte sisältää vain yhden ("Äidinkieli", "arvosana") parin joten tehtävänä on vain etsiä se ja palauttaa
# arvosanaa vastaavat pisteet
# Testattu, toimii, Joonas
def aidinkielen_pisteenlasku_normaali(laskentatapaID, database, syote):
    pisteet = 0.0
    poistettava = ("", "")
    # Tarkastelu kohdistuu nimenomaan ensimmäiseen alkioon. Alkio poistetaan main-funktiossa
    # käsittelyn jälkeen.
    for aine in syote:
        if aine[0] == "Äidinkieli":
            myresult = hae_pisteet(laskentatapaID, database, "Äidinkieli", aine[1])

            if len(myresult) != 0 and pisteet < myresult[0][0]:
                pisteet = myresult[0][0]
                poistettava = aine
            
            break

    # Palauttaa syotteen ensimmäisen alkion pistemäärän.
    return (pisteet, poistettava)

# database = psycopg2.connect(
# host="localhost",
# database="laskurin_data",
# user="postgres",
# password="kkouluun"
# )

# for i in range(52):
#     print(aidinkielen_pisteenlasku_normaali(i + 1, database, [("Yhteiskuntaoppi", "E"),("Äidinkieli Suomi", "E"),("Äidinkieli Ruotsi", "E"), ("Historia", "M"), ("Psykologia", "L")]))
#     print(i + 1)
#     print()
        

# def paras_uskonnollinen_ainereaali(ainelistat[5], laskentatapaID, database):
#     pisteet = 0.0
#     poistettava = ("", "")
#     # Käy läpi käyttäjän kirjoittamat yhteiskuntatieteelliset ainereaalit
#     for i in ainelistat[5]:

#         myresult = hae_pisteet(laskentatapaID, database, "Uskonnollinen aine", i[1])

#         if len(myresult) != 0 and myresult[0][0] > pisteet:
#             pisteet = myresult[0][0]
#             poistettava = i
#     # Asettaa pisteet kasvavaan suuruusjärjestykseen
#     # Palauttaa listan viimeisen alkion, eli alkion, joka antaa käyttäjälle suurimmat pisteet.

#     return (pisteet, poistettava)
        
    

