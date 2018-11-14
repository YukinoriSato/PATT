include ../../config.mk

EXTRA_FLAGS=

fdtd-3d: fdtd-3d.c fdtd-3d.h
	${VERBOSE} ${CC} -o fdtd-3d fdtd-3d.c ${CFLAGS} -I. -I../../utilities ../../utilities/polybench.c ${EXTRA_FLAGS}

clean:
	@ rm -f fdtd-3d

