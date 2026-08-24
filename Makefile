.PHONY: test lint clean coverage

test:
	python3 -m pytest tests/ -v

lint:
	python3 -m py_compile src/utils/string_helpers.py
	python3 -m py_compile src/utils/date_helpers.py
	python3 -m py_compile src/config/settings.py
	python3 -m py_compile src/models/task.py

coverage:
	python3 -m pytest tests/ --cov=src --cov-report=term-missing

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info
