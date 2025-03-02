help:
	@awk -F ':|##' '/^[^\t].+:.*##/ { printf "\033[36mmake %-28s\033[0m -%s\n", $$1, $$NF }' $(MAKEFILE_LIST) | sort

.PHONY: install-requirements
install-requirements: .install-requirements ## install packages

#---------------------------------------------------------

.install-requirements:
	pip install -r requirements.txt