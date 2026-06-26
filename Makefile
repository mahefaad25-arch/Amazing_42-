NAME=a_maze_ing.py
VENV=.venv
BIN_PATH=./$(VENV)/bin
PIP=./$(BIN_PATH)/pip
PYTHON=./$(BIN_PATH)/python
FLAKE=./$(BIN_PATH)/flake8
MYPY=./$(BIN_PATH)/mypy

install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

$(VENV):
	python3 -m venv $(VENV)

run:
	$(PYTHON) $(NAME) config.txt

debug:
	$(PYTHON) -m pdb $(NAME)

flake:
	$(FLAKE) --exclude=$(VENV) .

lint: flake
	$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --explicit-package-bases .

clean:
	find . -name "*.pyc" -exec rm -rf {} +
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)

re: fclean install

.PHONY: clean re fclean install run lint lint-strict flake debug
