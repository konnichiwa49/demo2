import subprocess
import sys

PY = sys.executable


def run(*args):
    r = subprocess.run([PY, "main.py", *args], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def test_hello():
    out = run("hello", "--name", "Kenji")
    assert "Hello, Kenji!" in out


def test_add():
    out = run("add", "2", "3")
    assert out == "5"


def test_echo():
    out = run("echo", "xyz")
    assert out == "xyz"


def test_info():
    out = run("info")
    assert "OK" in out


def test_calc():
    out = run("calc", "3*7+2")
    assert "23" in out


def test_time():
    out = run("time")
    assert out  # 何か文字列が出ればOK
