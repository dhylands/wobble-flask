all: run

run:
	flask --app app.py --debug run --host=0.0.0.0

style:
	yapf -i $(wildcard *.py)

lint:
	pylint *.py

make-pylintrc:
	pylint --generate-rcfile > .pylintrc

requirements:
	pip3 install -r requirements.txt
