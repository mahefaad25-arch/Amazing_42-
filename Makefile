# Makefile for A-Maze-ing common tasks

VENV=env
PY=python3
PIP=$(VENV)/bin/pip
PYTHON=$(VENV)/bin/python

.PHONY: help venv activate install upgrade-pip reinstall-mlx run clean

help:
	@echo "Available targets:"
	@echo "  make venv          -> create virtualenv (env/)"
	@echo "  make activate      -> show activation command for your shell"
	@echo "  make install       -> install mlx wheel into the venv"
	@echo "  make upgrade-pip   -> upgrade pip inside the venv"
	@echo "  make reinstall-mlx -> force reinstall mlx wheel"
	@echo "  make run           -> run a_maze_ing.py with config.txt using venv python"
	@echo "  make clean         -> remove the virtualenv"

venv:
	@test -d $(VENV) || $(PY) -m venv $(VENV)
	@$(PIP) install --upgrade pip setuptools wheel

activate:
	@echo "For bash/zsh: source $(VENV)/bin/activate"
	@echo "For fish:    source $(VENV)/bin/activate.fish"
	@echo "Then run: make install  (or make run)"

install: venv
	@echo "Installing mlx wheel into virtualenv..."
	@$(PIP) install ./mlx-2.2-py3-none-any.whl

upgrade-pip: venv
	@echo "Upgrading pip in virtualenv..."
	@$(PIP) install --upgrade pip

reinstall-mlx: venv
	@echo "Forcing reinstall of mlx wheel..."
	@$(PIP) install --force-reinstall ./mlx-2.2-py3-none-any.whl

run: venv
	@echo "Running a_maze_ing.py with $(PYTHON)..."
	@$(PYTHON) a_maze_ing.py config.txt

clean:
	@echo "Removing virtualenv '$(VENV)'..."
	rm -rf $(VENV)
