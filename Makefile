TODAY=$(shell date "+%Y%m%d")
CANVAS_TODAY=assets/canvas.${TODAY}.svg

LAYOUT ?= spiral 21
SHAPE  ?= segments 19.5
SRC    ?= strava/activities.csv

RUNPOSTER = uv run python -m runposter using_layout ${LAYOUT} using_shape ${SHAPE}

all: html/canvas.svg
	qlmanage -p $<

# today snapshots are rendered square, to minimize whitespace loss in README
today: HEIGHT=841
today: ${CANVAS_TODAY}

%.svg:
	${RUNPOSTER} render ${SRC} ${YEAR} ${HEIGHT} > $@

html/canvas.svg: .FORCE
${CANVAS_TODAY}: .FORCE
.FORCE:
.PHONY: .FORCE

RUFF_PYTHON_VERSION=py311

lint:
	uv run ruff check .

format:
	uv run ruff check --fix .
