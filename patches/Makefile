
# max allowed parallel tasks.
MAXJOBS?=$(shell getconf _NPROCESSORS_ONLN)
# MARGS: extra make arguments to forward
MARGS?=-j$(MAXJOBS)

COMMON_MESEN_DEBUG_FILE=VARIA.msl

all:
	@make $(MARGS) -C common all MESEN_DEBUG_FILE=$(COMMON_MESEN_DEBUG_FILE)
	@make $(MARGS) -C vanilla all MESEN_DEBUG_FILE=VARIA_vanilla.msl MESEN_DEBUG_FILE_BASE=$(COMMON_MESEN_DEBUG_FILE)

clean:
	@make -C common clean
	@make -C vanilla clean
