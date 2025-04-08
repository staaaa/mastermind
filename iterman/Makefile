.PHONY: all
all: build

# Build - shared object (.so) -> dynamiczna bibilioteka z dekodera
.PHONY: build
build:
	python setup.py build_ext --inplace

# Uruchom grę 
.PHONY: run
run:
	python main.py

# Wyczyść projekt z artefaktów
.PHONY: clean
clean:
	rm -rf build/
	rm -f *.so
	rm -f *.c
	rm -f *.pyd
	rm -f *.pyc
	rm -rf __pycache__/
	rm -rf *.egg-info/