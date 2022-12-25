# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

TOPLEVEL_LANG ?= verilog
SIM ?= icarus

PWD=$(shell pwd)

# Matrix parameters
DATA_WIDTH ?= 128
ADDR_WIDTH ?= 11

ifeq ($(TOPLEVEL_LANG),verilog)
    # VERILOG_SOURCES = $(PWD)/../../rtl/matmul-main/hardware/src/mm_acc_.sv
    VERILOG_SOURCES = $(PWD)/dut.sv
    # Set module parameters
    # ifeq ($(SIM),icarus)
    #     COMPILE_ARGS += -Pm_acc.DATA_WIDTH=$(DATA_WIDTH) -Pmm_acc.ADDR_WIDTH=$(ADDR_WIDTH) 
    # else ifneq ($(filter $(SIM),questa modelsim riviera activehdl),)
    #     SIM_ARGS += -gDATA_WIDTH=$(DATA_WIDTH) -gADDR_WIDTH=$(ADDR_WIDTH)
    # else ifeq ($(SIM),vcs)
    #     COMPILE_ARGS += -pvalue+mm_acc/DATA_WIDTH=$(DATA_WIDTH) -pvalue+mm_acc/ADDR_WIDTH=$(ADDR_WIDTH)
    # else ifeq ($(SIM),verilator)
    #     COMPILE_ARGS += -GDATA_WIDTH=$(DATA_WIDTH) -GADDR_WIDTH=$(ADDR_WIDTH)
    # else ifneq ($(filter $(SIM),ius xcelium),)
    #     EXTRA_ARGS += -defparam "mm_acc.DATA_WIDTH=$(DATA_WIDTH)" -defparam "mm_acc.ADDR_WIDTH=$(ADDR_WIDTH)"
    # endif

    ifneq ($(filter $(SIM),riviera activehdl),)
        COMPILE_ARGS += -sv2k12
    endif
else
    $(error "A valid value (verilog) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

# Fix the seed to ensure deterministic tests
export RANDOM_SEED := 123456789

TOPLEVEL    := mm_acc
MODULE      := tb_mm_acc
PLUSARGS    += +UVM_TESTNAME=test
COCOTB_RESULTS_FILE = results.xml

include $(shell cocotb-config --makefiles)/Makefile.sim


# Profiling

DOT_BINARY ?= dot

test_profile.pstat: sim

callgraph.svg: test_profile.pstat
	$(shell cocotb-config --python-bin) -m gprof2dot -f pstats ./$< | $(DOT_BINARY) -Tsvg -o $@

.PHONY: profile
profile:
	COCOTB_ENABLE_PROFILING=1 $(MAKE) callgraph.svg
