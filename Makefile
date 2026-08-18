.PHONY: all session-1 session-2 session-3 session-4 session-5 test clean

all: session-1 session-2 session-3 session-4 session-5

test:
	python3 -m pytest shared/tests/ -v

session-1:
	python3 session-1-blind-verification/run_demo.py

session-2:
	python3 session-2-supply-chain-drift/run_demo.py

session-3:
	python3 session-3-evaluation-design/run_demo.py

session-4:
	python3 session-4-prompt-injection/run_demo.py

session-5:
	python3 session-5-release-assurance/run_demo.py

clean:
	rm -rf shared/__pycache__ shared/assurance/__pycache__ shared/benchmark/__pycache__
	rm -rf session-*/artifacts/ session-*/__pycache__
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
