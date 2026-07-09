NAME 	=	a_maze_ing

PYTHON	=	python3
MAIN	=	${NAME}.py

SRC		=	${MAIN} ./maze

# RUN THIS BEFORE FINISHING THE PROJECT
.build:
	@uv build --wheel
	@mv dist/*.whl .
	@rm --recursive --force dist

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
	@find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +

lint:
	@-uv run flake8 ${SRC}
	@uv run mypy ${SRC} \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	@-uv run flake8 ${SRC}
	@uv run mypy ${SRC} --strict

.PHONY: install run debug clean lint lint-strict .build