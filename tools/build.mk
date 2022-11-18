# config:
ASAR?=asar
ASAR_OPTS?=--fix-checksum=off
MAKE_IPS?=$(ROOT_DIR)/tools/make_ips.sh
DEP_TOOL?=$(ROOT_DIR)/tools/gen_asm_dep.sh
MSL_TOOL?=$(ROOT_DIR)/tools/gen_msl.py
SYM_TOOL?=$(ROOT_DIR)/tools/gen_syms.py

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
MESEN_DEBUG_FILE=$(DEBUG_DIR)/VARIA$(FLAVOR).msl

# env
ASAR_OPTS+=$(patsubst %,-I%,$(INCLUDE_DIRS))
ASAR_OPTS+=--symbols=wla

export INCLUDE_DIRS
export ASAR

# rules
all:	$(IPS_FILES) $(SYM_ASM_FILES) $(SYM_JSON_FILES) $(MESEN_DEBUG_FILE)

clean:
	@echo "Cleaning ..."
	@rm -rf $(BUILD_DIR)
	@rm -f $(IPS_FILES) $(SYM_ASM_FILES) $(MESEN_DEBUG_FILE)

include $(DEP_FILES)

$(DEP_DIR)/.%.d:       $(SRC_DIR)/%.asm
	@$(DEP_TOOL) $< > $@

$(IPS_DIR)/%.ips:	$(SRC_DIR)/%.asm
	@echo "Building $@ ..."
	@ASAR_OPTS="$(ASAR_OPTS) --symbols-path=$(patsubst $(SRC_DIR)/%.asm,$(BUILD_DIR)/%.sym,$<)" $(MAKE_IPS) $< > $(BUILD_DIR)/$$(basename $<).log

# already generated along with ips, just add this rule to enforce dependency order
$(BUILD_DIR)/%.sym:	$(IPS_DIR)/%.ips
	@true

$(SRC_SYM_DIR)/%.asm:	$(BUILD_DIR)/%.sym
	@echo "Exporting ASM and JSON symbols from $< ..."
	@$(SYM_TOOL) $(patsubst $(BUILD_DIR)/%.sym,$(SYM_DIR)/%.json,$<) $@ $<

# same as above, JSON are generated at the same time as asm
$(SYM_DIR)/%.json:	$(SRC_SYM_DIR)/%.asm	
	@true

$(MESEN_DEBUG_FILE):	$(SYM_WLA_FILES)
	@echo "Updating debug file $@ ..."
	@cp $(DEBUG_DIR)/vanilla.msl $@
	@$(MSL_TOOL) $@ $^