"""Erzeugt Mermaid-Diagramme direkt aus der Ontologie: Prozessablauf mit Rollen und Wertentstehung."""

import re
from pathlib import Path

from rdflib import Graph, URIRef

from mapact.graph import ROOT, load_model

PREFIXES = """
PREFIX mp:    <https://w3id.org/mapact/core#>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
PREFIX pplan: <http://purl.org/net/p-plan#>
"""


def _id(uri) -> str:
    return re.sub(r"\W", "_", str(uri).rsplit("#", 1)[-1])


def _label(g: Graph, uri) -> str:
    for lbl in g.objects(URIRef(uri), URIRef("http://www.w3.org/2000/01/rdf-schema#label")):
        if getattr(lbl, "language", None) in ("de", None):
            return str(lbl).replace('"', "'")
    return _id(uri)


def process_diagram(g: Graph) -> str:
    """Ablauf je Prozessmodell; Schritte nach Phase gruppiert, Rollen im Kasten, Entscheidungen als Raute."""
    lines = ["flowchart TD"]
    phases = g.query(PREFIXES + "SELECT ?ph ?o WHERE { ?ph a mp:Phase ; mp:phaseOrder ?o } ORDER BY ?o")
    for ph, _ in phases:
        steps = list(g.query(PREFIXES + "SELECT ?s WHERE { ?s mp:inPhase ?ph } ORDER BY ?s", initBindings={"ph": ph}))
        if not steps:
            continue
        lines.append(f'  subgraph {_id(ph)}["{_label(g, ph)}"]')
        for (s,) in steps:
            rows = g.query(PREFIXES + "SELECT ?r WHERE { ?s mp:performedBy|mp:decidedBy ?r } ORDER BY ?r", initBindings={"s": s})
            roles = sorted({_label(g, r) for (r,) in rows})
            text = f"{_label(g, s)}<br/><i>{', '.join(roles)}</i>"
            decision = (s, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                        URIRef("https://w3id.org/mapact/core#Decision")) in g
            lines.append(f'    {_id(s)}{{"{text}"}}' if decision else f'    {_id(s)}["{text}"]')
        lines.append("  end")
    for f, t, guard, loop in g.query(PREFIXES + """
        SELECT ?f ?t ?guard ?loop WHERE {
          ?tr a mp:Transition ; mp:fromStep ?f ; mp:toStep ?t .
          OPTIONAL { ?tr mp:guard ?guard } OPTIONAL { ?tr mp:isLoopBack ?loop }
        } ORDER BY ?tr"""):
        arrow = "-.->" if loop is not None and loop.toPython() else "-->"
        label = f'|"{guard}"|' if guard else ""
        lines.append(f"  {_id(f)} {arrow}{label} {_id(t)}")
    return "\n".join(lines)


def value_diagram(g: Graph) -> str:
    """Welche Wertgröße entsteht aus welchen anderen; Annahmen sind markiert."""
    lines = ["flowchart BT"]
    seen = set()
    for v, r, o in g.query(PREFIXES + "SELECT ?v ?r ?o WHERE { ?v mp:derivedBy ?r . ?r mp:operand ?o } ORDER BY ?v ?o"):
        for node in (v, o):
            if node not in seen:
                seen.add(node)
                lines.append(f'  {_id(node)}["{_label(g, node)}"]')
        lines.append(f"  {_id(o)} --> {_id(v)}")
    for (a,) in g.query(PREFIXES + "SELECT ?a WHERE { ?a mp:knowledgeSource mp:Annahme ; a mp:ValueType } ORDER BY ?a"):
        lines.append(f"  class {_id(a)} annahme")
    lines.append("  classDef annahme stroke-dasharray: 5 4")
    return "\n".join(lines)


DOCS = ROOT / "docs" / "diagramme.md"


def render() -> str:
    g = load_model()
    return (
        "# Diagramme\n\nAutomatisch erzeugt mit `python -m mapact.visualize`; nicht von Hand bearbeiten.\n\n"
        "## Prozessablauf\n\nGestrichelte Pfeile führen zurück (Schleifen).\n\n"
        f"```mermaid\n{process_diagram(g)}\n```\n\n"
        "## Wertentstehung\n\nGestrichelte Kästen beruhen auf Annahmen und warten auf den Experten.\n\n"
        f"```mermaid\n{value_diagram(g)}\n```\n"
    )


def write_docs(out: Path = DOCS) -> Path:
    out.parent.mkdir(exist_ok=True)
    out.write_text(render(), encoding="utf-8")
    return out


if __name__ == "__main__":
    print(write_docs())
