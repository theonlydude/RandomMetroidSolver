# config:
VANILLA?=$(ROOT_DIR)/vanilla.sfc
ASAR?=asar
ASAR_OPTS?=--fix-checksum=off
MAKE_IPS?=$(ROOT_DIR)/tools/make_ips.sh
DEP_TOOL?=$(ROOT_DIR)/tools/gen_asm_dep.sh
MSL_TOOL?=$(ROOT_DIR)/tools/gen_msl.py
SYM_TOOL?=$(ROOT_DIR)/tools/gen_syms.py
IPS_CHECK_TOOL?=$(ROOT_DIR)/tools/ips_check.py

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

export VANILLA
export INCLUDE_DIRS
export SYM_ASM_FILES
export ASAR

# rules
all:	$(IPS_FILES) $(SYM_ASM_FILES) $(SYM_JSON_FILES) $(MESEN_DEBUG_FILE)

check:	all
	@$(IPS_CHECK_TOOL) $(VANILLA) $(IPS_FILES)

# FIXME Doing make clean twice will actually rebuild patches on which other patches depend :
#       .d files are considered part of the Makefile, and depends on the source to be generated.
#       They add a dependency on the source, to depend from symbol files not yet generated (since we cleaned them).
#       So the Makefile itself ends up depending on symbol files, therefore on IPS generation, whether we just want to clean or not.
#       This is the drawback of generating the "header files" for the ASM source, when compiling it.
#       It's analogous to C source files depending on object files directly instead of headers.
clean:
	@echo "Cleaning ..."
	@rm -rf $(BUILD_DIR)
	@rm -f $(IPS_FILES) $(SYM_ASM_FILES) $(MESEN_DEBUG_FILE)

help:
	@echo "- all (default) : builds IPS patches, symbols and debug files"
	@echo "- clean : removes everything 'all' builds"
	@echo "- check : all, then check IPS patches overlap"

.PHONY:	all check clean help

-include $(DEP_FILES)

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
