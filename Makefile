
# Error Handling
SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c

# Name of this Makefile
MAKEFILE_NAME := $(lastword $(MAKEFILE_LIST))

# Special targets that should not be listed
EXCLUDE_LIST := menu .PHONY

# Function to extract targets from the Makefile
define extract_targets
	$(shell awk -F: '/^[a-zA-Z0-9_-]+:/ {print $$1}' $(MAKEFILE_NAME) | grep -v -E '^($(EXCLUDE_LIST))$$')
endef

TARGETS := $(call extract_targets)

.PHONY: $(TARGETS) menu all help venv install run bundle bundleWithOutModels ci compressBundle downloadModels
menu: ## Makefile Interactive Menu
	@# Check if fzf is installed
	@if command -v fzf >/dev/null 2>&1; then \
		echo "Using fzf for selection..."; \
		echo "$(TARGETS)" | tr ' ' '\n' | fzf > .selected_target; \
		target_choice=$$(cat .selected_target); \
	else \
		echo "fzf not found, using numbered menu:"; \
		echo "$(TARGETS)" | tr ' ' '\n' > .targets; \
		awk '{print NR " - " $$0}' .targets; \
		read -p "Enter choice: " choice; \
		target_choice=$$(awk 'NR == '$$choice' {print}' .targets); \
	fi; \
	if [ -n "$$target_choice" ]; then \
		$(MAKE) $$target_choice; \
	else \
		echo "Invalid choice"; \
	fi

venv:
	@( \
		test -d .venv || \
		python3 -m venv .venv; \
		echo "Virtual environment created"; \
	)

install:
	@( \
       source .venv/bin/activate; \
       pip install -U -r requirements.txt; \
    )

run:
	@( \
       source .venv/bin/activate; \
       python3 superprompter.py; \
    )

bundle:
	@( \
		source .venv/bin/activate; \
		python download_models.py; \
		python3 bundle.py --include-models; \
	)

bundleWithOutModels:
	@( \
		rm -f *.spec; \
		source .venv/bin/activate; \
		python bundle.py; \
	)

downloadModels:
	@( \
		source .venv/bin/activate; \
		python download_models.py; \
	)

compressBundle:
# tar gz the SuperPrompter.app directory and the dist/SuperPrompter linux executable
	@( \
		if [ -f dist/SuperPrompter.app ]; then \
			tar -czvf dist/SuperPrompter.app.tar.gz dist/SuperPrompter.app; \
		fi; \
		if [ -f dist/SuperPrompter ]; then \
				tar -czvf dist/SuperPrompter.linux.tar.gz dist/SuperPrompter; \
		fi; \
	)

help: ## This help function
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

all: venv install run
ci: venv install bundleWithOutModels compressBundle

.DEFAULT_GOAL := menu

