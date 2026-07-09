NAME 	=	a_maze_ing

PYTHON	=	python3
MAIN	=	${NAME}.py

install:
	@uv sync
# 	${PYTHON} -m venv ${VENV}
# 	source ${VENV}/bin/activate
# 	pip install -r requirements.txt

run:
	@uv run ${PYTHON} ${MAIN}

debug:
	@uv run ${PYTHON} -m pdb ${MAIN}

clean:
	@rm --force --recursive __pycache__ mypy_cache

.PHONY: install run debug clean