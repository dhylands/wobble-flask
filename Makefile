all: run

run:
	flask --app app.py --debug run

style:
	yapf -i $(wildcard *.py)

lint:
	pylint *.py

make-pylintrc:
	pylint --generate-rcfile > .pylintrc

requirements:
	pip install -r requirements.txt
