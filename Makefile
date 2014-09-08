.PHONY: all test coverage clean clean-test clean-src clean-doc doc

all: test coverage doc

test:
	cd test/ && python test_pypdevs.py True

test-norealtime:
	cd test/ && python test_pypdevs.py False

coverage:
	cd test/ && coverage run test_pypdevs.py && coverage report -m
	
clean: clean-test clean-src clean-doc

clean-test:
	rm -f test/*.pyc 2>/dev/null
	rm -f test/*.pyo 2>/dev/null
	rm -f test/output/* 2>/dev/null
	touch test/output/.keep

clean-src:
	rm -f src/*.pyc 2>/dev/null
	rm -f src/*.pyo 2>/dev/null

clean-doc:
	rm -rf docs/generated 2>/dev/null
	rm -f docs/*.pyc 2>/dev/null
	rm -f docs/*.pyo 2>/dev/null

doc:
	cd docs/ && make html
