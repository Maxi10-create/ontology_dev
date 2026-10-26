import pytest

from mapact.llm import NotLocalError, assert_local, load_config


def test_lokale_endpunkte_erlaubt():
    assert_local("http://localhost:11434/api/generate")
    assert_local("http://127.0.0.1:11434")


@pytest.mark.parametrize("url", ["https://api.anthropic.com/v1/messages", "https://api.openai.com/v1", "http://10.0.0.5:11434"])
def test_cloud_und_fremde_endpunkte_abgelehnt(url):
    with pytest.raises(NotLocalError):
        assert_local(url)


def test_freigegebener_rechner_im_eigenen_netz():
    assert_local("http://10.0.0.5:11434", extra_hosts=["10.0.0.5"])


def test_konfiguration_ist_lokal():
    cfg = load_config()
    assert_local(cfg["endpoint"], cfg.get("allowed_hosts"))
