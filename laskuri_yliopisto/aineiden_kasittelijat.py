from aineet import ainereaalit, kielet, matemaattiset_aineet, yhteiskuntatieteelliset_aineet, aidinkielet, uskonnolliset_aineet
from apumetodit import arvosanamuunnin

# Ottaa syötteestä aineet erilleen arvosanoista ja listaa ne yhteen bufferiin
# toimii, Joonas
def aineet_syotteesta(syote):
    lista = []
    for i in syote:
        lista.append(i[0])
    return lista

# Poimii tiettyyn aineryhmään kuuluvat aineet ja arvosanat syötteestä omaan listaan
# syöte säilyy ennallaan
# toimii, Joonas
def xxx_syotteesta(syote, lista):
    ainelista = []
    for i in syote:
        if i[0] in lista:
            ainelista.append(i)
    return ainelista

# tarkastaa kuuluuko aine kyseiseen listaan
# toimii, Joonas
def on_xxx(alkio, lista):
    if alkio[0] in lista:
        return True
    else:
        return False

# Tutkii onko alkio kieli vai ei. Jos on, palauttaa Truen.
# Toimii, Joonas
def on_kieli(alkio):
    kieli = alkio[0].split(" ")
    if kieli[0] in kielet and kieli[1] != "2":
        return True
    else:
        return False

# Tutkii käyttäjän kirjottamia aineita ja palauttaa listan, jossa kielet ja niitä vastaavat arvosanat.
# toimii, Joonas
def kielet_syotteesta(syote):
    kielilista = []
    for i in syote:
        kieli = i[0].split(" ")
        if kieli[0] in kielet and kieli[1] != "2":
            kielilista.append(i)
    return kielilista

# Jättää syötteeseen yhden äidinkielen muodossa ("Äidinkieli", "arvosana")
# muuttaa muut äidinkielet pikiksi kieliksi syötteessä
# toimii, Joonas
def aidinkielet_syotteesta(syote, aidinkielet, kielet):
    # Luodaan tyhjä buffer aineille
    ainelista = []

    # poimitaan äidinkielet ja niiden arvosanat ainelistaan
    for i in syote:
        if i[0] in aidinkielet:
            ainelista.append(i)
    
    # poistetaan ainelistan aineet syötteestä
    for i in ainelista:
        syote.remove(i)

    # luodaan muuttujat parhaan äidinkielet etsintää varten
    paras_arvosana = "I"
    paras_aine = ""
    paras_arvosana_converted = 0

    # käydään ainelista läpi ja jos arvosana on parempi kuin edellinen paras, tallennetaan arvosana ja sitä vastaava aine
    for i in ainelista:
        arvosana = arvosanamuunnin(i[1])
        if arvosana >= paras_arvosana_converted:
            paras_arvosana_converted = arvosana
            paras_aine = i[0]
            paras_arvosana = i[1]
    
    # palautetaan paras arvosana syötteeseen Äidinkielenä
    syote.append(("Äidinkieli", paras_arvosana))
    muutettu_aidinkieli = (paras_aine, paras_arvosana)
    # tehdään kopio ainelistasta
    ainelista_kopio = ainelista.copy()
    
    # poistetaan ainelistasta syötteeseen lisättyä arvosanaa vastaava aine
    if paras_aine != "":
        ainelista_kopio.remove((paras_aine, paras_arvosana))
    
    # muunnetaan ainelistan aineet pitkiksi kieliksi ja palautetaan ne syötteeseen
    for i in ainelista_kopio:
        if i[0] == "Suomi 2" or i[0] == "Ruotsi 2":
            aine = i[0].split(" ")[0] + " pitkä"
            loytyi = False
            for j in syote.copy():
                if j[0] == aine:
                    loytyi = True
                    if arvosanamuunnin(i[1]) > arvosanamuunnin(j[1]):
                        syote.remove(j)
                        syote.append((aine, i[1]))
                    break
            if not loytyi:
                syote.append((aine, i[1]))
        else:
            aine = i[0].split(" ")[1] + " pitkä"
            loytyi = False
            for j in syote.copy():
                if j[0] == aine:
                    loytyi = True
                    if arvosanamuunnin(i[1]) > arvosanamuunnin(j[1]):
                        syote.remove(j)
                        syote.append((aine, i[1]))
                    break
            if not loytyi:
                syote.append((aine, i[1]))
        
    # palautetaan ainelista
    return (ainelista, muutettu_aidinkieli)

# Hakee parhaan äidinkielen arvosanan ja palauttaa sen numeroarvona
# Toimii, Joonas
def paras_aidinkielen_arvosana_syotteesta(kayttajan_aidinkielet):
    paras_arvosana = 0

    for i in kayttajan_aidinkielet:
        arvosana = arvosanamuunnin(i[1])
        if arvosana > paras_arvosana:
            paras_arvosana = arvosana
    
    return paras_arvosana


# poistaa aineen kaikista listoista
# tarkastaa ensin että aine on syötteessä ja käyttäjän aineissa, muutoin tarkistetaan vain kuuluuko aine kyseiseen aineryhmään
# sisältyvyyttä kieliin, jne. ei tarkisteta tarkemmin jotta debuggaaminen on helpompaa sillä jos aine on syötteessä tulee sen olla
# myös muissa aineryhmissä ja toisinpäin. Täten tästä aiheutuvat virheet kertovat koodatessa tapahtuneesta virheestä
# Toimii, Joonas
def poista_aine(poistettava, syote, poistokohteet):
    
    if poistettava in syote and poistettava[0] in poistokohteet[0]:
        syote.remove(poistettava)
        poistokohteet[0].remove(poistettava[0])

        if on_kieli(poistettava):
            # Poistetaan aine kielistä (jos on kieli alun perin).
            poistokohteet[1].remove(poistettava)

        if on_xxx(poistettava, aidinkielet):
            poistokohteet[2].remove(poistettava)

        if on_xxx(poistettava, ainereaalit):
            poistokohteet[3].remove(poistettava)

        if on_xxx(poistettava, matemaattiset_aineet):
            poistokohteet[4].remove(poistettava)

        if on_xxx(poistettava, uskonnolliset_aineet):
            poistokohteet[5].remove(poistettava)

        if on_xxx(poistettava, yhteiskuntatieteelliset_aineet):
            poistokohteet[6].remove(poistettava)
    
    else:
        Exception("poistettava väärin")




# # Tutkii onko alkio ainereaali vai ei. Jos on, palauttaa Truen.
# def on_ainereaali(alkio):
#     if alkio[0] in aineet.ainereaalit:
#         return True


# # Toimintaperiaate sama kuin funktiolla 'kielet_syotteesta'. Palauttaa käyttäjän kirjoittamat ainereaalit.
# def ainereaalit_syotteesta(syote):
#     ainereaalilista = []
#     for i in syote:
#         if i[0] in aineet.ainereaalit:
#             ainereaalilista.append(i)
#     return ainereaalilista



# # Selvittää onko aine matemaattinen ainereaali. Jos on, palauttaa True.
# def on_matemaattinen_ainereaali(alkio):
#     if alkio[0] in aineet.matemaattiset_aineet:
#         return True

# # Selvittää syötteestä käyttäjän kirjoittamat matemaattiset ainereaalit.
# def matemaattiset_ainereaalit_syotteesta(syote):
#     ainelista = []
#     for alkio in syote:
#         if on_matemaattinen_ainereaali(alkio):
#             ainelista.append(alkio)
#     return ainelista

# # Selvittää onko aine matemaattinen ainereaali. Jos on, palauttaa True.
# def on_yhteiskuntatieteellinen_ainereaali(alkio):
#     if alkio[0] in aineet.yhteiskuntatieteelliset_aineet:
#         return True

# # Selvittää syötteestä yhteiskuntatieteelliset ainereaalit.
# def yhteiskuntatieteelliset_ainereaalit_syotteesta(syote):
#     ainelista = []
#     for alkio in syote:
#         if on_yhteiskuntatieteellinen_ainereaali(alkio):
#             ainelista.append(alkio)
#     return ainelista

# # Selvittää onko aine äidinkieli
# def on_aidinkieli(alkio):
#     if alkio[0] in aineet.aidinkielet:
#         return True

# # Kerää syötteestä kaikki Äidinkielet ja siihen rinnastettavat aineet ja jättää parhaan arvosanan syötteeseen Äidinkielenä
# def aidinkielet_syotteesta(syote):
#     ainelista = []
#     for alkio in syote:
#         if on_aidinkieli(alkio):
#             ainelista.append(alkio)    
#     return ainelista
    

# def on_uskonnollinen_ainereaali(alkio):
#     if alkio[0] in aineet.uskonnolliset_aineet:
#         return True


# def uskonnolliset_ainereaalit_syotteesta(syote):
#     ainelista = []
#     for alkio in syote:
#         if on_uskonnollinen_ainereaali(alkio):
#             ainelista.append(alkio)    
#     return ainelista


