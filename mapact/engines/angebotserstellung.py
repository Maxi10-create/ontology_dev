"""Engine Angebotserstellung: Rechenregeln aus ausschreibung.ttl (R_Lohnkosten bis R_SummeBrutto)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Kalkulationsansatz:
    """Ansatz für eine LV-Position. Alle Beträge je Einheit, Sätze als Anteil (0,15 = 15 %)."""

    zeitansatz_h: float
    mittellohn: float
    materialkosten: float = 0.0
    geraetekosten: float = 0.0
    zuschlagssatz: float = 0.0


def lohnkosten(a: Kalkulationsansatz) -> float:
    """R_Lohnkosten: Lohnkosten = Zeitansatz × Mittellohn."""
    return a.zeitansatz_h * a.mittellohn


def einheitspreis(a: Kalkulationsansatz) -> float:
    """R_Einheitspreis: (Lohnkosten + Materialkosten + Gerätekosten) × (1 + Zuschlagssatz)."""
    return (lohnkosten(a) + a.materialkosten + a.geraetekosten) * (1 + a.zuschlagssatz)


def positionsbetrag(menge: float, ep: float) -> float:
    """R_Positionsbetrag: Menge × Einheitspreis."""
    return menge * ep


def angebotssumme(positionsbetraege: list[float], nachlasssatz: float = 0.0, mwst_satz: float = 0.0) -> dict[str, float]:
    """R_SummeNetto und R_SummeBrutto."""
    vor_nachlass = sum(positionsbetraege)
    netto = vor_nachlass * (1 - nachlasssatz)
    return {"vor_nachlass": vor_nachlass, "netto": netto, "brutto": netto * (1 + mwst_satz)}
