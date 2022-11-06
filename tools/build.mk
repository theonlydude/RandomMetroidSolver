# config:
ASAR?=asar
ASAR_OPTS?=--fix-checksum=off
MAKE_IPS?=$(ROOT_DIR)/tools/make_ips.sh
DEP_TOOL?=$(ROOT_DIR)/tools/gen_asm_dep.sh

# dirs
SRC_DIR=src
IPS_DIR=ips
SYM_DIR=sym

DUMMY:=$(shell mkdir -p $(SYM_DIR))

DEBUG_DIR=$(ROOT_DIR)/patches/debug
INCLUDE_DIR=$(SRC_DIR)/include
SRC_SYM_DIR=$(INCLUDE_DIR)
DEP_DIR=$(SYM_DIR)

INCLUDE_DIRS+=$(INCLUDE_DIRS)
export INCLUDE_DIRS

# files
SRC_FILES:=$(wildcard $(SRC_DIR)/*.asm)
IPS_FILES:=$(patsubst $(SRC_DIR)/%.asm,$(IPS_DIR)/%.ips)
SYM_WLA_FILES:=$(patsubst $(SRC_DIR)/%.asm,$(SYM_DIR)/%.sym)
SYM_ASM_FILES:=$(patsubst $(SRC_DIR)/%.asm,$(SRC_SYM_DIR)/%.asm)
DEP_FILES:=$(patsubst $(SRC_DIR)/%.asm,$(DEP_DIR)/.%.d)
MESEN_DEBUG_FILE=$(DEBUG_DIR)/VARIA$(FLAVOR).msl

# rules
all:	$(IPS_FILES) $(MESEN_DEBUG_FILE)

-include $(DEP_FILES)

$(DEP_DIR)/.%.d:	$(SRC_DIR)/%.asm
	@$(DEP_TOOL) $< > $@

$(IPS_DIR)/%.ips:	$(SRC_DIR)/%.asm

