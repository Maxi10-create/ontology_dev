from pyshacl import validate
from rdflib import OWL, RDF

from mapact.graph import load, load_model, model_files, shape_files


def test_alle_module_parsen():
    assert len(model_files()) >= 2
    assert len(load_model(reason=False)) > 0


def test_reasoner_findet_keinen_widerspruch():
    g = load_model()
    assert not list(g.subjects(RDF.type, OWL.Nothing))


def test_shacl_formen_erfuellt():
    conforms, _, text = validate(load_model(reason=False), shacl_graph=load(shape_files()), inference="rdfs")
    assert conforms, text


def test_bestaetigung_ohne_pruefer_wird_abgelehnt():
    from rdflib import Literal, URIRef
    from rdflib.namespace import XSD

    mp = "https://w3id.org/mapact/core#"
    g = load_model(reason=False)
    schritt = URIRef("https://w3id.org/mapact/ausschreibung#S06_Kalkulieren")
    g.add((schritt, URIRef(mp + "reviewStatus"), URIRef(mp + "ExperteBestaetigt")))
    conforms, _, _ = validate(g, shacl_graph=load(shape_files()), inference="rdfs")
    assert not conforms
    g.add((schritt, URIRef(mp + "reviewedBy"), URIRef("https://example.org/experte")))
    g.add((schritt, URIRef(mp + "reviewedOn"), Literal("2026-11-01", datatype=XSD.date)))
    conforms, _, text = validate(g, shacl_graph=load(shape_files()), inference="rdfs")
    assert conforms, text
