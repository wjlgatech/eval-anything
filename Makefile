.PHONY: help check validate drift ainative test build

help: ## show every target
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "};{printf "%-12s %s\n", $$1, $$2}'

check: validate drift ainative test ## THE finish line — everything below, in order
	@echo '✅ check green'

validate: ## schema gate over the source of truth
	python3 scripts/validate.py

build: ## regenerate README.md from data/*.yml
	python3 scripts/build.py

drift: ## fail if committed README ≠ generated
	python3 scripts/build.py --check

sync: ## meta-repo heartbeat — refresh registry (open GitHub API) + rebuild
	python3 scripts/sync.py

ainative: ## AI-native self-audit (gate 85)
	python3 scripts/ainative.py --gate 85

test: ## stdlib unittest suite
	python3 -m unittest discover -s tests -q
