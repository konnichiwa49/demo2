import subprocess, sys, os, tempfile, shutil

PY = sys.executable


def run(tmp, *args):
    env = dict(os.environ)
    env["DEMO2_HOME"] = tmp
    r = subprocess.run([PY, "main.py", *args], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def test_cli_basic():
    tmp = tempfile.mkdtemp()
    try:
        assert "Hello, Kenji!" in run(tmp, "hello", "--name", "Kenji")
        assert run(tmp, "add", "2", "3") == "5"
        assert run(tmp, "echo", "xyz") == "xyz"
        assert "OK" in run(tmp, "info")
        assert "23" in run(tmp, "calc", "3*7+2")
        assert run(tmp, "time")  # 非空
    finally:
        shutil.rmtree(tmp)


def test_todo_and_log():
    tmp = tempfile.mkdtemp()
    try:
        run(tmp, "todo", "clear")
        run(tmp, "todo", "add", "aaa")
        out = run(tmp, "todo", "list")
        assert "0. [ ] aaa" in out

        run(tmp, "todo", "done", "0")
        out = run(tmp, "todo", "list")
        assert "0. [x] aaa" in out

        # log は hello 実行ログが入る
        run(tmp, "hello", "--name", "X")
        out = run(tmp, "log", "--tail", "5")
        assert "hello --name X" in out
    finally:
        shutil.rmtree(tmp)
