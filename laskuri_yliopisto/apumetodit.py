
# Metodi jolla saadaan haettua tietyn aineen pisteet tietylle arvosanalle tietystä laskentatavasta
# Testattu, toimii, Joonas
def hae_pisteet(laskentatapaID, database, aine, arvosana):
    mydb = database

    sql = "SELECT " + str(
            arvosana) + " FROM aineet WHERE aineet.laskentatapaid = " + str(
            laskentatapaID) + " AND aine = " + "'" + str(aine) + "'"

    mycursor = mydb.cursor()
    mycursor.execute(sql)

    return mycursor.fetchall()


# Muuttaa arvosanan numeroksi
# Testattu, toimii, Joonas
def arvosanamuunnin(arvosana):
    if arvosana == "L":
        return 6
    if arvosana == "E":
        return 5
    if arvosana == "M":
        return 4
    if arvosana == "C":
        return 3
    if arvosana == "B":
        return 2
    if arvosana == "A":
        return 1
    else:
        return 0

# Muuttaa käyttäjän arvosanat numeroiksi: L -> 6, E -> 5, M -> 4, C -> 3, B -> 2, A -> 1, I -> 0. Vertailu on helpompaa
# kynnysehtojen täyttymisen tutkimiseksi.
# Testattu, toimii, Joonas
def convert(syote):
    values = []
    for i in syote:
        values.append((i[0], arvosanamuunnin(i[1])))
    return values

# print(convert([("Yhteiskuntaoppi", "E"),("Äidinkieli Suomi", "E"),("Äidinkieli Ruotsi", "E"), ("Historia", "M"), ("Psykologia", "L")]))



