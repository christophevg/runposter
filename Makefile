TODAY=$(shell date "+%Y%m%d")
CANVAS_TODAY=assets/canvas.${TODAY}.svg

all: html/canvas.svg

# today snapshots are rendered square, to minimize whitespace loss in README
today: HEIGHT=841
today: ${CANVAS_TODAY}

%.svg:
	python -m runposter render strava/activities.csv ${YEAR} ${HEIGHT} > $@

html/canvas.svg: .FORCE
${CANVAS_TODAY}: .FORCE
.FORCE:
.PHONY: .FORCE

RUFF_PYTHON_VERSION=py311

lint:
	ruff check --select=E9,F63,F7,F82 --target-version=$(RUFF_PYTHON_VERSION) .
	ruff check --target-version=$(RUFF_PYTHON_VERSION) .
