import subprocess

def test_main_runs():
    result = subprocess.run(
        ["python", "main.py"], capture_output=True, text=True
    )
    assert "Hello from new project!" in result.stdout
