setup_venv:
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip3 install -r requirements.txt

build_library:
	. venv/bin/activate && \
	python setup.py build_ext --inplace && \
	deactivate
run:
	. venv/bin/activate && \
	python main.py