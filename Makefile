PYTHON=python

all: help

help: 								## Show this help
	@echo -e "Specify a command. The choices are:\n"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-18s\033[m %s\n", $$1, $$2}'
	@echo ""
.PHONY: help

ci-install:
	make -C papis-html ci-install
.PHONY: ci-install

ci-test:
	make -C papis-html ci-lint
.PHONY: ci-test
