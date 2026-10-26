# ontology_dev

Prozess-Ontologie, Wissensgraph und Engines für **Mapact**: Abläufe kleiner und mittlerer Betriebe von außen verstehen und sichtbar machen. Erster Prozess: **Ausschreibung und Angebot** im Bau.

## Grundsätze

- **Neutrale Außensicht.** Der Prozess wird nie aus Sicht einer Partei modelliert. Auftraggeber, Planer und Bieter sind Rollen im selben Modell.
- **Abstrakt zuerst.** Das Modell enthält keine Firmen, Projekte oder Beträge. Konkrete Fälle eines Betriebs kommen später über die Fallebene (`mp:Case`, `mp:StepExecution`).
- **Nur lokale LLMs für Daten.** `mapact.llm` lehnt jeden nicht lokalen Endpunkt ab. Echte Dokumente liegen nur in `data/` und werden nie eingecheckt.
- **Werte haben eine Herkunft.** Jede Wertgröße zeigt, aus welchen anderen Werten und nach welcher Regel sie entsteht.
- **Expertenwissen kommt später.** Alles ist Entwurf, bis ein Experte es mit `mp:reviewStatus mp:ExperteBestaetigt`, Prüfer und Datum bestätigt; Annahmen ohne Beleg tragen `mp:knowledgeSource mp:Annahme`.
- **Engines sind deterministisch.** Vergleichen, Prüfen und Rechnen sind feste Programme, die im Modell verankert sind; ein LLM schlägt höchstens vor.

## Aufbau

| Pfad | Inhalt |
| --- | --- |
| `ontology/core/mapact-core.ttl` | Domänenneutraler Kern: Prozessmodell, Phase, Schritt, Entscheidung, Übergang, Rolle, Informationsobjekt, Wertgröße, Rechenregel, Bedingung, Engine; Fallebene als Haken |
| `ontology/core/mapact-core.shapes.ttl` | SHACL-Prüfungen, die für jedes Domänenmodul gelten |
| `ontology/domains/ausschreibung/` | Modul Ausschreibung und Angebot: 5 Phasen, 3 Rollen, 12 Schritte, 13 Übergänge, 15 Wertgrößen, 6 Rechenregeln, 3 Bedingungen, 2 Engines |
| `cq/` | Kompetenzfragen als SPARQL |
| `mapact/engines/` | Engine Angebotserstellung (Kalkulation, Summen) und Engine Angebotsvergleich (Vollständigkeit, LV-Abweichungen, Preisspiegel) |
| `mapact/llm.py`, `config/llm.toml` | Zugang zum lokalen Modell (Ollama) mit Sperre gegen Cloud-Endpunkte |
| `mapact/visualize.py`, `docs/diagramme.md` | Prozessablauf und Wertentstehung als Mermaid, direkt aus der Ontologie erzeugt |
| `tests/` | Syntax, Reasoner, SHACL, Kompetenzfragen, Engines, LLM-Sperre, aktuelle Diagramme |

Wiederverwendet werden [P-Plan](http://purl.org/net/p-plan) für Pläne und Schritte, [PROV-O](https://www.w3.org/TR/prov-o/) für Fälle und Herkunft und SKOS für Begriffe und Synonyme. Ausdrucksstärke: OWL 2 RL.

## Kompetenzfragen

| Nr. | Frage | Datei |
| --- | --- | --- |
| 1 | Welche Phasen und Schritte hat der Prozess, und in welcher Reihenfolge? | `cq01_phasen_und_schritte.rq` |
| 2 | Welche Rolle führt welchen Schritt aus, und wer entscheidet? | `cq02_rollen.rq` |
| 3 | Welche Informationen gehen in einen Schritt ein, und welche entstehen dort? | `cq03_ein_und_ausgaben.rq` |
| 4 | Wie entsteht ein Wert, und aus welchen Bestandteilen und Rechenregeln setzt er sich zusammen? | `cq04_wertentstehung.rq` |
| 5 | Welche Bedingungen müssen erfüllt sein, damit ein Schritt abgeschlossen ist? | `cq05_abschlussbedingungen.rq` |
| 6 | Welche Varianten und Schleifen gibt es? | `cq06_varianten_und_schleifen.rq` |
| 7 | Welche Engine unterstützt welchen Schritt, mit welchen Ein- und Ausgaben? | `cq07_engines.rq` |
| 8 | Welche Modellelemente sind noch nicht vom Experten bestätigt, und welche beruhen nur auf Annahmen? | `cq08_offene_expertenpruefung.rq` |

## Benutzen

```bash
pip install -e ".[dev]"
pytest -q                 # alle Prüfungen
python -m mapact.graph    # Kompetenzfragen beantworten
python -m mapact.visualize  # Diagramme in docs/ neu erzeugen
```

Für die spätere Arbeit mit echten Daten: [Ollama](https://ollama.com) installieren, das Modell aus `config/llm.toml` laden (`ollama pull qwen3:14b`).

## Nächste Schritte

1. Experten-Review: Prozessmodell und Kalkulationsschema mit einem Fachexperten durchgehen und den Review-Status setzen.
2. Fallebene ausbauen und einen anonymisierten Fall lokal einlesen.
3. Phase 5 (Ausführung, Nachträge, Abrechnung) modellieren.
4. Zweiten Prozess eines Handwerksbetriebs modellieren und prüfen, ob der Kern trägt.
