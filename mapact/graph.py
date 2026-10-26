"""Lädt Ontologie-Module und beantwortet Kompetenzfragen."""

from pathlib import Path

import owlrl
from rdflib import Graph

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_DIR = ROOT / "ontology"
CQ_DIR = ROOT / "cq"


def model_files() -> list[Path]:
    return sorted(p for p in ONTOLOGY_DIR.rglob("*.ttl") if not p.name.endswith(".shapes.ttl"))


def shape_files() -> list[Path]:
    return sorted(ONTOLOGY_DIR.rglob("*.shapes.ttl"))


def load(files: list[Path]) -> Graph:
    g = Graph()
    for f in files:
        g.parse(f, format="turtle")
    return g


def load_model(reason: bool = True) -> Graph:
    """Alle Module zusammen; mit reason=True um die OWL-2-RL-Schlüsse erweitert."""
    g = load(model_files())
    if reason:
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    return g


def competency_questions() -> dict[str, str]:
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(CQ_DIR.glob("*.rq"))}


def ask(name: str, g: Graph | None = None) -> list[dict[str, str]]:
    g = g if g is not None else load_model()
    rows = g.query(competency_questions()[name])
    return [{str(k): str(v) for k, v in row.asdict().items()} for row in rows]


if __name__ == "__main__":
    g = load_model()
    for name in competency_questions():
        rows = ask(name, g)
        print(f"\n== {name} ({len(rows)} Zeilen)")
        for row in rows[:12]:
            print("  " + " | ".join(row.values()))
