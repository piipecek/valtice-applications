"""
Tímhle skriptem se vytvoří třídy.
"""

from website import create_app
from website.models.valtice_trida import Valtice_trida

app = create_app()
with app.app_context():
    Valtice_trida(short_name="Beatriz Lafont", full_name="Beatriz Lafont (ES) – Sólový zpěv/Solo singing").update()
    Valtice_trida(short_name="Margot Oitzinger", full_name="Margot Oitzinger (A) – Sólový zpěv/Solo singing").update()
    Valtice_trida(short_name="Peter Kooij", full_name="Peter Kooij (NL) – Sólový zpěv/Solo singing").update()
    Valtice_trida(short_name="Jürgen Banholzer | Sólo", full_name="Jürgen Banholzer (DE) – Sólový zpěv/Solo singing").update()
    Valtice_trida(short_name="Jürgen Banholzer | Ansámbly", full_name="Jürgen Banholzer (DE) – Vokální ansámbly/Vocal ensembles").update()
    Valtice_trida(short_name="Barbora Kabátková", full_name="Barbora Kabátková (CZ) – Gregoriánský chorál a raný vícehlas/Gregorian chant").update()
    Valtice_trida(short_name="Robert Hugo", full_name="Robert Hugo (CZ) – Sbor (duchovní hudba i opera)/Choir (sacred music & opera)").update()
    Valtice_trida(short_name="Lukáš Vendl | Varhany", full_name="Lukáš Vendl (CZ) – Varhany/Organ").update()
    Valtice_trida(short_name="Lukáš Vendl | Basso continuo", full_name="Lukáš Vendl (CZ) – Basso continuo").update()
    Valtice_trida(short_name="Jana Semerádová", full_name="Jana Semerádová (CZ) – Barokní příčná flétna/Baroque traverso").update()
    Valtice_trida(short_name="Peter Holtslag | Sólo flétna", full_name="Peter Holtslag (NL) – Zobcová flétna/Recorder").update()
    Valtice_trida(short_name="Peter Holtslag | Komorní hudba", full_name="Peter Holtslag (NL) – Komorní hudba/Ensemble music").update()
    Valtice_trida(short_name="Julie Braná", full_name="Julie Braná (CZ) – Zobcová flétna/Recorder").update()
    Valtice_trida(short_name="Gábor Prehoffer", full_name="Gábor Prehoffer (HU) – Zobcová flétna/Recorder").update()
    Valtice_trida(short_name="Corina Marti | Sólo flétna", full_name="Corina Marti (CH) – Zobcová flétna/Recorder").update()
    Valtice_trida(short_name="Corina Marti | Ansámbly", full_name="Corina Marti (CH) – Středověké ansámbly/Medieval & renaissance ensemble music").update()
    Valtice_trida(short_name="Marek Špelina", full_name="Marek Špelina (CZ) – Ansámbly zobcových fléten/Recorder ensembles").update()
    Valtice_trida(short_name="Luise Haugk", full_name="Luise Haugk (DE) – Barokní hoboj/Baroque oboe").update()
    Valtice_trida(short_name="Michael Brüssing", full_name="Michael Brüssing (A) – Viola da gamba").update()
    Valtice_trida(short_name="Magdaléna Malá", full_name="Magdaléna Malá (CZ) – Barokní housle/Baroque violin").update()
    Valtice_trida(short_name="Irmtraud Hubatschek", full_name="Irmtraud Hubatschek (A) – Barokní violoncello a kontrabas/Baroque violoncello & Double bass").update()
    Valtice_trida(short_name="Brian Wright", full_name="Brian Wright (GB) – Loutna, romantická kytara/Lute & Romantic guitar").update()
    Valtice_trida(short_name="Shalev Ad-El", full_name="Shalev Ad-El (IL) – Cembalo/Harpsichord").update()
    Valtice_trida(short_name="Marek Štryncl", full_name="Marek Štryncl (CZ) – Barokní orchestr/Baroque orchestra").update()
    Valtice_trida(short_name="Assunta Fanuli", full_name="Assunta Fanuli (IT) – Historický tanec (19. století)/Historical dance (19th century)").update()
    Valtice_trida(short_name="Bruno Benne", full_name="Bruno Benne (FR) – Historický tanec (baroko)/Historical dance (baroque)").update()
    Valtice_trida(short_name="Kateřina Klementová", full_name="Kateřina Klementová (CZ) – Historický tanec (renesance)/Historical dance (renaissance)").update()
    Valtice_trida(short_name="Lorenzo Charoy", full_name="Lorenzo Charoy (FR) – Herectví a barokní gestika/Baroque gesture & acting").update()
    Valtice_trida(short_name="Ondřej Tichý", full_name="Ondřej Tichý (CZ) – Dramatická třída/Musical-dramatic workshop for teenagers").update()
    Valtice_trida(short_name="Eva Káčerková", full_name="Eva Káčerková (CZ) – Pohybová výchova dětí, zpěv a hry/Creative movement, Singing & Games").update()
    Valtice_trida(short_name="Veronika Jíchová", full_name="Veronika Jíchová (CZ) – Dětský orchestr/Children orchestra").update()
    Valtice_trida(short_name="Ondřej Šmíd", full_name="Ondřej Šmíd (CZ) – Zpěv při bohoslužbě/Singing at a church service").update()
    print("done")