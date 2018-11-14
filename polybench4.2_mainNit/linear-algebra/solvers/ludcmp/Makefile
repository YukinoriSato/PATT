include ../../../config.mk

EXTRA_FLAGS=

ludcmp: ludcmp.c ludcmp.h
	${VERBOSE} ${CC} -o ludcmp ludcmp.c ${CFLAGS} -I. -I../../../utilities ../../../utilities/polybench.c ${EXTRA_FLAGS}

clean:
	@ rm -f ludcmp

