.PHONY: run run-venv deps

run:
	python3 main.py

run-venv:
	./venv/bin/python main.py

deps:
	python3 -m pip install -r requirements.txt
