from .aineiden_kasittelijat import aineet_syotteesta, kielet_syotteesta, poista_aine, xxx_syotteesta, aidinkielet_syotteesta, paras_aidinkielen_arvosana_syotteesta
from .kynnysehtojen_tarkistin import tayttyyko_kynnysehto
from .laskumetodit import aidinkielen_pisteenlasku_normaali, aineen_pistelasku, kauttaviivatilanne, paras_kieli_pitka, paras_kieli
from .laskumetodit import paras_xxx_ainereaali, paras_xxx_aine, kaksi_kolmesta, muu_syotteessa
from .apumetodit import convert
from .erikoislaskutavat import elintarviketiede, viestintatieteet, yhteiskuntatieteet, saamelainen_kulttuuri
from .aineet import ainereaalit, matemaattiset_aineet, yhteiskuntatieteelliset_aineet, aidinkielet, uskonnolliset_aineet

import psycopg2

# testaa seuraavana kaksi äidinkieltä ja saame
parametri = [("Suomi 2", "M"), ("Ruotsi 2", "L"), ("Suomi pitkä", "B"), ("Saksa pitkä", "I")]
kauttaviivatilanteen_laskutapa = "kaksi parasta kolmesta: Kieli\Fysiikka\Reaali"

mydb = psycopg2.connect(
        host="localhost",
        database="laskurin_data",
        user="postgres",
        password=""
    )


syote = parametri.copy()
# ajettava ennen äidinkieliä koska aidinkielet_syotteesta lisää kielien määrää, Huom ajetaan uudelleen alempana
kielet_ilman_aidinkielia = kielet_syotteesta(syote)
kayttajan_aidinkielet_sailio = aidinkielet_syotteesta(syote, aidinkielet, kielet_ilman_aidinkielia)
kayttajan_aineet_sailio = aineet_syotteesta(syote)
kayttajan_kielet_sailio = kielet_syotteesta(syote)
kayttajan_ainereaalit_sailio = xxx_syotteesta(syote, ainereaalit)
kayttajan_matemaattiset_ainereaalit_sailio = xxx_syotteesta(syote, matemaattiset_aineet)
kayttajan_uskonnolliset_ainereaalit_sailio = xxx_syotteesta(syote, uskonnolliset_aineet)
kayttajan_yhteiskuntatieteeliset_ainereaalit_sailio = xxx_syotteesta(syote, yhteiskuntatieteelliset_aineet)

kayttajan_aineet = kayttajan_aineet_sailio.copy()
kayttajan_kielet = kayttajan_kielet_sailio.copy()
kayttajan_aidinkielet = kayttajan_aidinkielet_sailio.copy()
kayttajan_ainereaalit = kayttajan_ainereaalit_sailio.copy()
kayttajan_matemaattiset_ainereaalit = kayttajan_matemaattiset_ainereaalit_sailio.copy()
kayttajan_uskonnolliset_ainereaalit = kayttajan_uskonnolliset_ainereaalit_sailio.copy()
kayttajan_yhteiskuntatieteeliset_ainereaalit = kayttajan_yhteiskuntatieteeliset_ainereaalit_sailio.copy()


ainelistat = [kayttajan_aineet.copy(), kayttajan_kielet.copy(), kayttajan_aidinkielet.copy(), kayttajan_ainereaalit.copy(), kayttajan_matemaattiset_ainereaalit.copy(), kayttajan_uskonnolliset_ainereaalit.copy(), kayttajan_yhteiskuntatieteeliset_ainereaalit.copy()]
pisteet = 0


# syote_sailio = syote.copy()
# print(ainelistat)
# laskentatapaID = 12
# print()
# print(laskentatapaID)
# print(syote)
# pisteet = yhteiskuntatieteet(syote.copy(), laskentatapaID, mydb, ainelistat.copy())
# print(pisteet)
# print(ainelistat)

# laskentatapaID = 15
# print()
# print(laskentatapaID)
# print(syote)
# pisteet = elintarviketiede(syote.copy(), laskentatapaID, mydb, ainelistat.copy())
# print(pisteet)

# laskentatapaID = 44
# print()
# print(laskentatapaID)
# print(syote)
# pisteet = viestintatieteet(syote.copy(), laskentatapaID, mydb, ainelistat.copy())
# print(pisteet)

laskentatapaID = 48
# print()
# print(laskentatapaID)
print(syote)
print(parametri)
pisteet = saamelainen_kulttuuri(syote.copy(), laskentatapaID, mydb, ainelistat.copy(), parametri.copy(), kielet_ilman_aidinkielia.copy())
# print(pisteet)

# laskentatapaID = 12
# print()
# print(laskentatapaID)
# print(syote)
# pisteet = kaksi_kolmesta(ainelistat.copy(), laskentatapaID, syote.copy(), kauttaviivatilanteen_laskutapa, mydb)
# print(pisteet)
