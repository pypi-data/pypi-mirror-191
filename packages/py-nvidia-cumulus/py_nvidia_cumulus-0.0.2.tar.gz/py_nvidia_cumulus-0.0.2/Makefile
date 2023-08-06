
.PHONY: help
help: ## show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## run tests
	@python3 -m unittest discover tests

.PHONY: package
package: ## package the module
	@python3 -m build

.PHONY: upload
upload: ## upload the package to PyPi
	@python3 -m twine upload dist/*

.PHONY: all
all: test package upload ## test, build, and upload the package to PyPi
