from mapact.visualize import DOCS, render


def test_diagramme_sind_aktuell():
    assert DOCS.read_text(encoding="utf-8") == render(), "Bitte `python -m mapact.visualize` ausführen"


def test_prozessdiagramm_enthaelt_entscheidungen_und_schleifen():
    text = render()
    assert 'S10_Nachverhandeln{"' in text
    assert "S11_AngebotUeberarbeiten -.->" in text
