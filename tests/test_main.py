import importlib


def test_main_runs(capsys):
    m = importlib.import_module("main")
    m.main()
    out = capsys.readouterr().out
    assert "Hello from new project!" in out
