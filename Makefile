all: run

run:
	flask --debug run --host=0.0.0.0

RPI_PYTHON_FILES = ./stats.py
ALL_PYTHON_FILES = $(shell find . -name '*.py' -not -path  './.direnv/*')

ifeq ($(shell uname -p),x86_64)
PYTHON_FILES = $(filter-out $(RPI_PYTHON_FILES), $(ALL_PYTHON_FILES))
$(info x86 PYTHON_FILES = $(PYTHON_FILES))
else
PYTHON_FILES = $(ALL_PYTHON_FILES)
$(info rPi PYTHON_FILES = $(PYTHON_FILES))
endif

style:
	yapf -i $(PYTHON_FILES)

lint:
	pylint $(PYTHON_FILES)

make-pylintrc:
	pylint --generate-rcfile > .pylintrc

requirements:
	pip3 install -r requirements.txt
