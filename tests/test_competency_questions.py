import pytest

from mapact.graph import ask, competency_questions, load_model


@pytest.fixture(scope="module")
def g():
    return load_model()


@pytest.mark.parametrize("name", sorted(competency_questions()))
def test_jede_kompetenzfrage_hat_antworten(g, name):
    assert ask(name, g), f"{name} liefert keine Zeilen"


def test_kf1_phasen_in_reihenfolge(g):
    reihenfolge = [int(r["reihenfolge"]) for r in ask("cq01_phasen_und_schritte", g)]
    assert reihenfolge == sorted(reihenfolge)


def test_kf2_bieter_entscheidet_ueber_anfrage(g):
    rows = ask("cq02_rollen", g)
    assert {"schritt": "Anfrage prüfen", "rolle": "Bieter", "entscheidet": "true"} in rows


def test_kf4_einheitspreis_haengt_an_lohn_material_geraet_zuschlag(g):
    rows = ask("cq04_wertentstehung", g)
    teile = {r["bestandteil"] for r in rows if r["wert"] == "Einheitspreis"}
    assert teile == {"Lohnkosten", "Materialkosten", "Gerätekosten", "Zuschlagssatz"}
    assert {r["wert"] for r in rows} >= {"Angebotssumme brutto", "Positionsbetrag", "Lohnkosten"}


def test_kf6_nachverhandlung_fuehrt_zurueck_zur_pruefung(g):
    rows = ask("cq06_varianten_und_schleifen", g)
    assert any(r["von"] == "Angebot überarbeiten" and r["nach"] == "Angebote prüfen" and r["zurueck"] == "true"
               for r in rows)


def test_kf7_beide_engines_verankert(g):
    engines = {r["engine"] for r in ask("cq07_engines", g)}
    assert engines == {"Engine Angebotserstellung", "Engine Angebotsvergleich"}
