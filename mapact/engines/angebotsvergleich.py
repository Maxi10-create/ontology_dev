"""Engine Angebotsvergleich: prüft C_AngebotVollstaendig und C_LVUnveraendert, erstellt den Preisspiegel."""

from dataclasses import dataclass, field
from statistics import median

from mapact.engines.angebotserstellung import angebotssumme, positionsbetrag


@dataclass(frozen=True)
class LVPosition:
    oz: str
    kurztext: str
    menge: float
    einheit: str


@dataclass(frozen=True)
class Angebotsposition:
    oz: str
    ep: float | None
    kurztext: str | None = None
    menge: float | None = None
    einheit: str | None = None


@dataclass
class Angebot:
    bieter: str
    positionen: dict[str, Angebotsposition]
    nachlasssatz: float = 0.0
    version: str = "1"


@dataclass
class Preisspiegel:
    summen: dict[str, dict[str, float]] = field(default_factory=dict)
    guenstigster_je_position: dict[str, str] = field(default_factory=dict)
    abweichung_vom_median: dict[str, dict[str, float]] = field(default_factory=dict)
    fehlende_preise: dict[str, list[str]] = field(default_factory=dict)
    lv_abweichungen: dict[str, list[str]] = field(default_factory=dict)


def fehlende_preise(lv: list[LVPosition], angebot: Angebot) -> list[str]:
    """C_AngebotVollstaendig: LV-Positionen ohne Einheitspreis."""
    return [p.oz for p in lv if (ap := angebot.positionen.get(p.oz)) is None or ap.ep is None]


def lv_abweichungen(lv: list[LVPosition], angebot: Angebot) -> list[str]:
    """C_LVUnveraendert: Positionen, bei denen der Bieter Kurztext, Menge oder Einheit geändert hat."""
    abweichend = []
    for p in lv:
        ap = angebot.positionen.get(p.oz)
        if ap is None:
            continue
        if (ap.kurztext is not None and ap.kurztext != p.kurztext) or \
           (ap.menge is not None and ap.menge != p.menge) or \
           (ap.einheit is not None and ap.einheit != p.einheit):
            abweichend.append(p.oz)
    return abweichend


def vergleichen(lv: list[LVPosition], angebote: list[Angebot], mwst_satz: float = 0.0) -> Preisspiegel:
    ps = Preisspiegel()
    for a in angebote:
        betraege = [positionsbetrag(p.menge, a.positionen[p.oz].ep)
                    for p in lv if p.oz in a.positionen and a.positionen[p.oz].ep is not None]
        ps.summen[a.bieter] = angebotssumme(betraege, a.nachlasssatz, mwst_satz)
        ps.fehlende_preise[a.bieter] = fehlende_preise(lv, a)
        ps.lv_abweichungen[a.bieter] = lv_abweichungen(lv, a)
    for p in lv:
        preise = {a.bieter: a.positionen[p.oz].ep for a in angebote
                  if p.oz in a.positionen and a.positionen[p.oz].ep is not None}
        if not preise:
            continue
        ps.guenstigster_je_position[p.oz] = min(preise, key=preise.get)
        m = median(preise.values())
        if m:
            ps.abweichung_vom_median[p.oz] = {b: (ep - m) / m for b, ep in preise.items()}
    return ps
