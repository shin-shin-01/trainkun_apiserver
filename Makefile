autopep:
	find . -type d -name env -prune -o -type f -name '*.py' -print | xargs autopep8 --in-place --aggressive --aggressive

