# config:
VANILLA?=$(ROOT_DIR)/vanilla.sfc
ASAR?=asar
ASAR_OPTS?=--fix-checksum=off -wnofeature_deprecated --no-title-check
DEP_TOOL?=$(ROOT_DIR)/tools/gen_asm_dep.sh
MSL_TOOL?=$(ROOT_DIR)/tools/gen_msl.py
SYM_TOOL?=$(ROOT_DIR)/tools/gen_syms.py
MESEN_DEBUG_FILE_BASE?=vanilla.msl
MESEN_DEBUG_FILE?=VARIA.msl

# dirs
SRC_DIR=src
INCLUDE_DIR=$(SRC_DIR)/include
IPS_DIR=ips
BUILD_DIR=build
SYM_DIR=sym
SRC_SYM_DIR=$(INCLUDE_DIR)/sym
DEBUG_DIR=$(ROOT_DIR)/patches/debug
DEP_DIR=$(BUILD_DIR)

DUMMY:=$(shell mkdir -p $(BUILD_DIR) $(SRC_SYM_DIR) $(SYM_DIR))

INCLUDE_DIRS+=$(INCLUDE_DIR)

# files
SRC_FILES:=$(wildcard $(SRC_DIR)/*.asm)
IPS_FILES:=$(patsubst $(SRC_DIR)/%.asm,$(IPS_DIR)/%.ips,$(SRC_FILES))
SYM_WLA_FILES:=$(patsubst $(SRC_DIR)/%.asm,$(BUILD_DIR)/%.sym,$(SRC_FILES))
SYM_JSON_FILES:=$(patsubst $(SRC_DIR)/%.asm,$(SYM_DIR)/%.json,$(SRC_FILES))
SYM_ASM_FILES:=$(patsubst $(SRC_DIR)/%.asm,$(SRC_SYM_DIR)/%.asm,$(SRC_FILES))
DEP_FILES:=$(patsubst $(SRC_DIR)/%.asm,$(DEP_DIR)/.%.d,$(SRC_FILES))
MESEN_DEBUG_FILE_TARGET=$(DEBUG_DIR)/$(MESEN_DEBUG_FILE)

# env
ASAR_OPTS+=$(patsubst %,-I%,$(INCLUDE_DIRS))
ASAR_OPTS+=--symbols=wla

export VANILLA
export INCLUDE_DIRS
export SYM_ASM_FILES
export ASAR

# rules
all:	$(IPS_FILES) $(SYM_ASM_FILES) $(SYM_JSON_FILES) $(MESEN_DEBUG_FILE_TARGET)

clean:
	@echo "Cleaning ..."
	@rm -rf $(BUILD_DIR)
	@rm -f $(IPS_FILES) $(SYM_ASM_FILES) $(MESEN_DEBUG_FILE)

help:
	@echo "- all (default) : builds IPS patches, symbols and debug files"
	@echo "- clean : removes everything 'all' builds"

.PHONY:	all clean help

-include $(DEP_FILES)

$(DEP_DIR)/.%.d:       $(SRC_DIR)/%.asm
	@$(DEP_TOOL) $< $(patsubst $(SRC_DIR)/%.asm,$(IPS_DIR)/%.ips,$<) > $@

$(IPS_DIR)/%.ips:	$(SRC_DIR)/%.asm
	@echo "Building $@ ..."
	@$(ASAR) $(ASAR_OPTS) --ips $@ --symbols-path=$(patsubst $(SRC_DIR)/%.asm,$(BUILD_DIR)/%.sym,$<) $< > $(BUILD_DIR)/$$(basename $<).log
	@-rm -f $(patsubst $(SRC_DIR)/%.asm,$(SRC_DIR)/%.sfc,$<)

# already generated along with ips, just add this rule to enforce dependency order
$(BUILD_DIR)/%.sym:	$(IPS_DIR)/%.ips
	@true

$(SRC_SYM_DIR)/%.asm:	$(BUILD_DIR)/%.sym
	@echo "Exporting ASM and JSON symbols from $< ..."
	@$(SYM_TOOL) $(patsubst $(BUILD_DIR)/%.sym,$(SYM_DIR)/%.json,$<) $@ $<

# same as above, JSON are generated at the same time as asm
$(SYM_DIR)/%.json:	$(SRC_SYM_DIR)/%.asm
	@true

$(MESEN_DEBUG_FILE_TARGET):	$(SYM_WLA_FILES)
	@echo "Updating debug file $@ ..."
	@cp $(DEBUG_DIR)/$(MESEN_DEBUG_FILE_BASE) $@
	@$(MSL_TOOL) $@ $^
