import subprocess


def test_main_runs():
    r = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    assert "Hello from new project!" in r.stdout
