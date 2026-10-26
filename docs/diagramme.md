# Diagramme

Automatisch erzeugt mit `python -m mapact.visualize`; nicht von Hand bearbeiten.

## Prozessablauf

Gestrichelte Pfeile führen zurück (Schleifen).

```mermaid
flowchart TD
  subgraph P1_Bedarf["Bedarf und Planung"]
    S01_BedarfKlaeren["Bedarf klären<br/><i>Auftraggeber</i>"]
    S02_Planen["Planen<br/><i>Planer</i>"]
  end
  subgraph P2_Ausschreibung["Ausschreibung"]
    S03_LeistungBeschreiben["Leistung beschreiben<br/><i>Planer</i>"]
    S04_ZurAbgabeAuffordern["Zur Angebotsabgabe auffordern<br/><i>Auftraggeber, Planer</i>"]
  end
  subgraph P3_Angebot["Angebotserstellung"]
    S05_AnfragePruefen{"Anfrage prüfen<br/><i>Bieter</i>"}
    S06_Kalkulieren["Kalkulieren<br/><i>Bieter</i>"]
    S07_AngebotErstellen["Angebot erstellen und einreichen<br/><i>Bieter</i>"]
  end
  subgraph P4_Vergabe["Prüfung und Vergabe"]
    S08_AngebotePruefen["Angebote prüfen<br/><i>Planer</i>"]
    S09_AngeboteVergleichen["Angebote vergleichen<br/><i>Planer</i>"]
    S10_Nachverhandeln{"Nachverhandeln?<br/><i>Auftraggeber</i>"}
    S11_AngebotUeberarbeiten["Angebot überarbeiten<br/><i>Bieter</i>"]
    S12_Vergeben["Vergeben<br/><i>Auftraggeber</i>"]
  end
  S01_BedarfKlaeren --> S02_Planen
  S02_Planen --> S03_LeistungBeschreiben
  S03_LeistungBeschreiben --> S04_ZurAbgabeAuffordern
  S04_ZurAbgabeAuffordern --> S05_AnfragePruefen
  S05_AnfragePruefen -->|"Bieter gibt ein Angebot ab"| S06_Kalkulieren
  S05_AnfragePruefen -.->|"Rückfrage des Bieters wird beantwortet"| S04_ZurAbgabeAuffordern
  S06_Kalkulieren --> S07_AngebotErstellen
  S07_AngebotErstellen --> S08_AngebotePruefen
  S08_AngebotePruefen --> S09_AngeboteVergleichen
  S09_AngeboteVergleichen --> S10_Nachverhandeln
  S10_Nachverhandeln -->|"Auftraggeber verhandelt nach"| S11_AngebotUeberarbeiten
  S11_AngebotUeberarbeiten -.->|"Neue Angebotsversion liegt vor"| S08_AngebotePruefen
  S10_Nachverhandeln -->|"Keine weitere Nachverhandlung"| S12_Vergeben
```

## Wertentstehung

Gestrichelte Kästen beruhen auf Annahmen und warten auf den Experten.

```mermaid
flowchart BT
  AbweichungVomMedian["Abweichung vom Median"]
  Einheitspreis["Einheitspreis"]
  Einheitspreis --> AbweichungVomMedian
  AngebotssummeBrutto["Angebotssumme brutto"]
  AngebotssummeNetto["Angebotssumme netto"]
  AngebotssummeNetto --> AngebotssummeBrutto
  Mehrwertsteuersatz["Mehrwertsteuersatz"]
  Mehrwertsteuersatz --> AngebotssummeBrutto
  Nachlasssatz["Nachlasssatz"]
  Nachlasssatz --> AngebotssummeNetto
  Positionsbetrag["Positionsbetrag"]
  Positionsbetrag --> AngebotssummeNetto
  Geraetekosten["Gerätekosten"]
  Geraetekosten --> Einheitspreis
  Lohnkosten["Lohnkosten"]
  Lohnkosten --> Einheitspreis
  Materialkosten["Materialkosten"]
  Materialkosten --> Einheitspreis
  Zuschlagssatz["Zuschlagssatz"]
  Zuschlagssatz --> Einheitspreis
  Mittellohn["Mittellohn"]
  Mittellohn --> Lohnkosten
  Zeitansatz["Zeitansatz"]
  Zeitansatz --> Lohnkosten
  Einheitspreis --> Positionsbetrag
  Menge["Menge"]
  Menge --> Positionsbetrag
  class Zuschlagssatz annahme
  classDef annahme stroke-dasharray: 5 4
```
