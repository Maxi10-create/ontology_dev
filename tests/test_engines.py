import importlib

import pytest

from mapact.engines.angebotserstellung import Kalkulationsansatz, angebotssumme, einheitspreis, positionsbetrag
from mapact.engines.angebotsvergleich import Angebot, Angebotsposition, LVPosition, vergleichen
from mapact.graph import ask, load_model

# Nur synthetische Zahlen; echte Daten gehören nicht ins Repository.
LV = [LVPosition("01", "Mauerwerk", 10, "m²"), LVPosition("02", "Putz", 20, "m²")]


def test_einheitspreis_nach_zuschlagsschema():
    a = Kalkulationsansatz(zeitansatz_h=0.5, mittellohn=40, materialkosten=10, geraetekosten=2, zuschlagssatz=0.25)
    assert einheitspreis(a) == pytest.approx((20 + 10 + 2) * 1.25)


def test_summen_mit_nachlass_und_mwst():
    s = angebotssumme([positionsbetrag(10, 5), positionsbetrag(2, 25)], nachlasssatz=0.1, mwst_satz=0.1)
    assert s == pytest.approx({"vor_nachlass": 100, "netto": 90, "brutto": 99})


def test_vergleich_findet_luecken_abweichungen_und_guenstigsten():
    a = Angebot("A", {"01": Angebotsposition("01", 50), "02": Angebotsposition("02", None)})
    b = Angebot("B", {"01": Angebotsposition("01", 60), "02": Angebotsposition("02", 12, menge=18)}, nachlasssatz=0.05)
    c = Angebot("C", {"01": Angebotsposition("01", 70), "02": Angebotsposition("02", 10)})
    ps = vergleichen(LV, [a, b, c], mwst_satz=0.1)
    assert ps.fehlende_preise == {"A": ["02"], "B": [], "C": []}
    assert ps.lv_abweichungen["B"] == ["02"]
    assert ps.guenstigster_je_position == {"01": "A", "02": "C"}
    assert ps.abweichung_vom_median["01"]["C"] == pytest.approx(10 / 60)
    assert ps.summen["B"]["netto"] == pytest.approx((600 + 240) * 0.95)


def test_jede_engine_im_modell_ist_implementiert():
    for row in ask("cq07_engines", load_model()):
        importlib.import_module(row["modul"])
