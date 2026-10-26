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
