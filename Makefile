run:
	. .venv/bin/activate && python main.py
fmt:
	. .venv/bin/activate && black .
lint:
	. .venv/bin/activate && flake8 .
repl:

cli:
	. .venv/bin/activate && python main.py hello --name You
	. .venv/bin/activate && ipython

test:
	. .venv/bin/activate && PYTHONPATH=. pytest -v
