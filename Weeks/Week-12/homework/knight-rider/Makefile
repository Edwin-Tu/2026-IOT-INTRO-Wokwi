THIS_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ROOT     := $(abspath $(THIS_DIR)/../../../../..)

PORT   ?= 4000
SCRIPT := main.py

.PHONY: run
run:
	@echo ">>> 請確認 VS Code 中 Wokwi 模擬器已啟動"
	python $(ROOT)/tools/wokwi_run.py --port $(PORT) $(SCRIPT)
