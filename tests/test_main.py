import runpy

def test_main_runs(capsys):
    runpy.run_module("main", run_name="__main__")
    captured = capsys.readouterr()
    assert "Hello from new project!" in captured.out
