ifndef IMPERAS_HOME
  IMPERAS_ERROR := $(error "IMPERAS_HOME not defined, please setup Imperas/OVP environment")
endif
IMPERAS_HOME := $(shell getpath.exe "$(IMPERAS_HOME)")
include $(IMPERAS_HOME)/bin/Makefile.include

CROSS?=
OPTIMIZATION?=

-include $(IMPERAS_HOME)/lib/$(IMPERAS_ARCH)/CrossCompiler/$(CROSS).makefile.include
ifeq ($($(CROSS)_CC),)
    IMPERAS_ERROR := $(error "Please install the toolchain to support $(CROSS) ")
endif

PROF_LD?=$(LFLAGS_MAKE)
PROF_CC?=$(CFLAGS_MAKE)

SRC = $(sort $(wildcard *.c))
EXE = $(patsubst %.c,%.$(CROSS).elf,$(SRC))
DUMP = $(patsubst %.elf, %.dump, $(EXE))

all: $(EXE) $(DUMP)

%.dump: %.elf
	$(V)  echo "# Dump $<"
	$(V)  $(IMPERAS_OBJDUMP) -d $< > $@

%.$(CROSS).elf: %.$(CROSS).o
	$(V)  echo "# Linking $@"
	$(V)  $(IMPERAS_LINK) -o $@ $< $(IMPERAS_LDFLAGS) -lm

%.$(CROSS).o: %.c
	$(V)  echo "# Compiling $< "
	$(V)  $(IMPERAS_CC) -c -o $@ $< $(OPTIMIZATION)

clean:
	-rm -f *.elf *.o

realclean: clean
	-rm -f *.log
