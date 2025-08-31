import runpy

def test_main_runs(capsys):
    runpy.run_path("main.py")
    out = capsys.readouterr().out
    assert "Hello from new project!" in out
