from io import BytesIO
from openpyxl import Workbook
from website.models.valtice_ucastnik import Valtice_ucastnik
from website.models.valtice_trida import Valtice_trida

def export() -> BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.append(["cas prihlasky", "cas_registrace", "prijmeni", "jmeno", "vek", "email", "telefon", "finance_dne", "finance_dar", "finance_mena", "finance_kategorie", "finance_korekce_kurzovne", "finance_korekce_kurzovne_duvod", "finance_korekce_strava", "finance_korekce_strava_duvod", "finance_korekce_ubytko", "finance_korekce_ubytko_duvod", "finance_snidane", "finance_obedy", "finance_vecere", "finance_hlavni_trida", "finance_vedlejsi_trida", "finance_ubytovani", "finance_celkem", "ssh_clen", "ucast", "hlavni_trida_1", "hlavni_trida_2", "vedlejsi_trida_placena", "vedlejsi_trida_zdarma", "ubytovani", "ubytovani_pocet", "vzdelani", "nastroj", "repertoir", "student_zus_valtice_mikulov", "strava", "strava_snidane_vinarska", "strava_snidane_zs", "strava_obed_vinarska_maso", "strava_obed_vinarska_vege", "strava_obed_zs_maso", "strava_obed_zs_vege", "strava_vecere_vinarska_maso", "strava_vecere_vinarska_vege", "strava_vecere_zs_maso", "strava_vecere_zs_vege", "uzivatelska_poznamka", "admin_poznamka"])
    for u in Valtice_ucastnik.query.all():
        kalkulace = u.kalkulace()
        trida_1 = u.hlavni_trida_1.full_name if u.hlavni_trida_1 else ""
        trida_2 = u.hlavni_trida_2.full_name if u.hlavni_trida_2 else ""
        trida_vedlejsi_placena = u.vedlejsi_trida_placena.full_name if u.vedlejsi_trida_placena else ""
        trida_vedlejsi_zdarma = u.vedlejsi_trida_zdarma.full_name if u.vedlejsi_trida_zdarma else ""
        ws.append([u.cas, u.cas_registrace, u.prijmeni, u.jmeno, u.vek, u.email, u.telefon, u.finance_dne, u.finance_dar, u.finance_mena, u.finance_kategorie, u.finance_korekce_kurzovne, u.finance_korekce_kurzovne_duvod, u.finance_korekce_strava, u.finance_korekce_strava_duvod, u.finance_korekce_ubytko, u.finance_korekce_ubytko_duvod, kalkulace["snidane"], kalkulace["obedy"], kalkulace["vecere"], kalkulace["prvni_trida"], kalkulace["vedlejsi_trida"], kalkulace["ubytovani"], kalkulace["celkem"], u.ssh_clen, u.ucast, trida_1, trida_2, trida_vedlejsi_placena, trida_vedlejsi_zdarma, u.ubytovani, u.ubytovani_pocet, u.vzdelani, u.nastroj, u.repertoir, u.student_zus_valtice_mikulov, u.strava, u.strava_snidane_vinarska, u.strava_snidane_zs, u.strava_obed_vinarska_maso, u.strava_obed_vinarska_vege, u.strava_obed_zs_maso, u.strava_obed_zs_vege, u.strava_vecere_vinarska_maso, u.strava_vecere_vinarska_vege, u.strava_vecere_zs_maso, u.strava_vecere_zs_vege, u.uzivatelska_poznamka, u.admin_poznamka])
    ws = wb.create_sheet("Tridy")
    ws.append(["id", "short_name", "full_name", "je_zdarma_jako_vedlejsi", "je_ansamblova"])
    for t in Valtice_trida.query.all():
        ws.append([t.id, t.short_name, t.full_name, t.je_zdarma_jako_vedlejsi, t.je_ansamblova])
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output