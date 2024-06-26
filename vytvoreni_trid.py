"""
Tímhle skriptem se vytvoří třídy.
"""

from website import create_app
from website.models.valtice_trida import Valtice_trida

app = create_app()
with app.app_context():
    # short name = pouze jmeno lektora, pokud letor má dvě třídy, je tam i upřesnění
    # full name = jmeno lektora + detailní název třídy
    Valtice_trida(short_name="Beatriz Lafont", full_name="Beatriz Lafont – Sólový zpěv").update()
    Valtice_trida(short_name="Margot Oitzinger", full_name="Margot Oitzinger – Sólový zpěv").update()
    Valtice_trida(short_name="Peter Kooij", full_name="Peter Kooij – Sólový zpěv").update()
    Valtice_trida(short_name="Jürgen Banholzer | Sólo", full_name="Jürgen Banholzer – Sólový zpěv").update()
    Valtice_trida(short_name="Jürgen Banholzer | Ansámbly", full_name="Jürgen Banholzer – Vokální ansámbly", je_ansamblova = True).update()
    Valtice_trida(short_name="Barbora Kabátková", full_name="Barbora Kabátková – Gregoriánský chorál").update()
    Valtice_trida(short_name="Robert Hugo", full_name="Robert Hugo – Sbor", je_zdarma_jako_vedlejsi=True).update()
    Valtice_trida(short_name="Lukáš Vendl | Varhany", full_name="Lukáš Vendl – Varhany").update()
    Valtice_trida(short_name="Lukáš Vendl | Basso continuo", full_name="Lukáš Vendl – Basso continuo").update()
    Valtice_trida(short_name="Jana Semerádová", full_name="Jana Semerádová – Barokní příčná flétna").update()
    Valtice_trida(short_name="Peter Holtslag | Sólo flétna", full_name="Peter Holtslag – Zobcová flétna").update()
    Valtice_trida(short_name="Peter Holtslag | Komorní hudba", full_name="Peter Holtslag – Komorní hudba", je_ansamblova = True).update()
    Valtice_trida(short_name="Julie Braná", full_name="Julie Braná – Zobcová flétna").update()
    Valtice_trida(short_name="Gábor Prehoffer", full_name="Gábor Prehoffer – Zobcová flétna").update()
    Valtice_trida(short_name="Corina Marti | Sólo flétna", full_name="Corina Marti – Zobcová flétna").update()
    Valtice_trida(short_name="Corina Marti | Ansámbly", full_name="Corina Marti – Středověké ansámbly", je_ansamblova = True).update()
    Valtice_trida(short_name="Marek Špelina", full_name="Marek Špelina – Ansámbly zobcových fléten").update()
    Valtice_trida(short_name="Luise Haugk", full_name="Luise Haugk – Barokní hoboj").update()
    Valtice_trida(short_name="Michael Brüssing", full_name="Michael Brüssing – Viola da gamba").update()
    Valtice_trida(short_name="Magdaléna Malá", full_name="Magdaléna Malá – Barokní housle").update()
    Valtice_trida(short_name="Irmtraud Hubatschek", full_name="Irmtraud Hubatschek – Barokní violoncello a kontrabas").update()
    Valtice_trida(short_name="Brian Wright", full_name="Brian Wright – Loutna, romantická kytara").update()
    Valtice_trida(short_name="Shalev Ad-El", full_name="Shalev Ad-El – Cembalo").update()
    Valtice_trida(short_name="Marek Štryncl", full_name="Marek Štryncl – Barokní orchestr", je_zdarma_jako_vedlejsi = True).update()
    Valtice_trida(short_name="Assunta Fanuli", full_name="Assunta Fanuli – Historický tanec (19. století)").update()
    Valtice_trida(short_name="Bruno Benne", full_name="Bruno Benne – Historický tanec (baroko)").update()
    Valtice_trida(short_name="Kateřina Klementová", full_name="Kateřina Klementová – Historický tanec (renesance)").update()
    Valtice_trida(short_name="Lorenzo Charoy", full_name="Lorenzo Charoy – Herectví a barokní gestika").update()
    Valtice_trida(short_name="Ondřej Tichý", full_name="Ondřej Tichý – Dramatická třída").update()
    Valtice_trida(short_name="Eva Káčerková", full_name="Eva Káčerková – Pohybová výchova dětí, zpěv a hry").update()
    Valtice_trida(short_name="Veronika Jíchová", full_name="Veronika Jíchová – Dětský orchestr").update()
    Valtice_trida(short_name="Ondřej Šmíd", full_name="Ondřej Šmíd – Zpěv při bohoslužbě", je_zdarma_jako_vedlejsi = True).update()
    print("done")