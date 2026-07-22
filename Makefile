# =========================================
# ANSI Escape Sequences
# =========================================

# Basic
ESC			:=	\033
RESET		:=	$(ESC)[0m

# Colors
BLACK		:=	$(ESC)[0;30m
RED			:=	$(ESC)[0;31m
GREEN		:=	$(ESC)[0;32m
YELLOW		:=	$(ESC)[0;33m
BLUE		:=	$(ESC)[0;34m
MAGENTA		:=	$(ESC)[0;35m
CYAN		:=	$(ESC)[0;36m
WHITE		:=	$(ESC)[0;37m
DEFAULT		:=	$(ESC)[0;39m

# Text Styles
BOLD		:=	$(ESC)[1m
DIM			:=	$(ESC)[2m
ITALIC		:=	$(ESC)[3m
UNDERLINE	:=	$(ESC)[4m
INVERSE		:=	$(ESC)[7m
HIDDEN		:=	$(ESC)[8m
STRIKE		:=	$(ESC)[9m

# =========================================
# Compilation Targets
# =========================================

NAME 	=	a_maze_ing

PYTHON	=	python3
MAIN	=	${NAME}.py
CONFIG	=	config.txt

SRC		=	${MAIN} ./mazegen

# RUN THIS BEFORE FINISHING THE PROJECT
.build:
	@printf "${BOLD}${MAGENTA}Building the package${RESET}\n"
	@uv build --wheel
	@mv dist/*.whl .
	@rm --recursive --force dist

install:
	@printf "${BOLD}${BLUE}Synchronizing packages${RESET}\n"
	@uv sync
# 	${PYTHON} -m venv ${VENV}
# 	source ${VENV}/bin/activate
# 	pip install -r requirements.txt

run:
	@uv run ${PYTHON} ${MAIN} ${CONFIG}

debug:
	@printf "${INVERSE}${YELLOW}Running in DEBUG mode${RESET}\n"
	@uv run ${PYTHON} -m pdb ${MAIN} ${CONFIG}

clean:
	@printf "${YELLOW}Cleaning artifacts${RESET}\n"
	@find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +

lint:
	@printf "${GREEN}${BOLD}Linting${RESET}\n"
	@printf "${GREEN}Syntax ${CYAN}(flake8)${RESET}\n"
	@uv run flake8 ${SRC} || true
	@printf "${GREEN}Typing ${CYAN}(mypy)${RESET}\n"
	@uv run mypy ${SRC} \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs \
	|| true

lint-strict:
	@printf "${GREEN}${BOLD}Linting${RESET}\n"
	@printf "${GREEN}Syntax ${CYAN}(flake8)${RESET}\n"
	@uv run flake8 ${SRC} || true
	@printf "${GREEN}Typing ${CYAN}(mypy ${RED}--strict${CYAN})${RESET}\n"
	@uv run mypy ${SRC} --strict || true

.PHONY: install run debug clean lint lint-strict .build