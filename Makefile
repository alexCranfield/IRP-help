TARGETS = format test
CMD:=conda run

.PHONY: $(TARGETS)

format:
	$(CMD) isort . --profile=black --lines-after-imports=2
	$(CMD) black . --line-length=132