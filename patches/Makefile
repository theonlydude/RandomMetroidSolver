
ROOT_DIR=..

# config
IPS_CHECK_TOOL?=$(ROOT_DIR)/tools/ips_check.py
# IPS basename filter to remove them from overlap check
IPS_CHECK_FILTER?=remove_|bank_|area_ids|Blinking\[|Indicator\[|Disable_Clear_Save_Boot|Removes_Gravity_Suit_heat_protection
# max allowed parallel tasks.
MAXJOBS?=$(shell getconf _NPROCESSORS_ONLN)
# MARGS: extra make arguments to forward
MARGS?=-j$(MAXJOBS)

COMMON_MESEN_DEBUG_FILE=VARIA.msl

all:
	@make $(MARGS) -C common all MESEN_DEBUG_FILE=$(COMMON_MESEN_DEBUG_FILE)
	@make $(MARGS) -C vanilla all MESEN_DEBUG_FILE=VARIA_vanilla.msl MESEN_DEBUG_FILE_BASE=$(COMMON_MESEN_DEBUG_FILE)
	@make $(MARGS) -C mirror all MESEN_DEBUG_FILE=VARIA_mirror.msl MESEN_DEBUG_FILE_BASE=$(COMMON_MESEN_DEBUG_FILE)

clean:
	@make -C common clean
	@make -C vanilla clean
	@make -C mirror clean

export IPS_CHECK_FILTER

check:	all
	@echo "* Check IPS conflicts for vanilla flavor :"
	@$(IPS_CHECK_TOOL) vanilla vanilla/patches.py common/ips/*.ips vanilla/ips/*.ips
	@echo "* Check IPS conflicts for mirror flavor :"
	@$(IPS_CHECK_TOOL) mirror mirror/patches.py common/ips/*.ips mirror/ips/*.ips

help:
	@echo "- all (default) : builds IPS patches, symbols and debug files"
	@echo "- clean : removes everything 'all' builds"
	@echo "- check : all, then check IPS patches overlap for all flavors"

.PHONY:	all clean check help
