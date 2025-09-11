VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip
UVICORN=$(VENV_DIR)/bin/uvicorn
LINTER=$(VENV_DIR)/bin/flake8

.PHONY: all
all: env activate lint format clean test
#all: env activate lint format clean test run

env:
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

activate:
	@echo "Run: source $(VENV_DIR)/bin/activate"

lint:
	$(PYTHON) -m flake8 --exit-zero app/

format:
	$(PYTHON) -m black app/

clean:
	rm -rf $(VENV) .pytest_cache __pycache__ *.pyc *.pyo

test:
	$(PYTHON) -m unittest discover -s tests

run:
	@fuser -k 8000/tcp || true
	$(UVICORN) app.main:app --reload

server: env lint test run