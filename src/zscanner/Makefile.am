ACLOCAL_AMFLAGS = -I $(top_srcdir)/m4
AM_CPPFLAGS = \
	-include $(top_builddir)/src/config.h \
	-I$(top_srcdir)/src

lib_LTLIBRARIES = libzscanner.la

EXTRA_DIST =				\
	scanner.rl			\
	scanner_body.rl			\
	scanner.c.g2			\
	scanner.c.t0

BUILT_SOURCES = scanner.c
CLEANFILES = scanner.c

if FAST_PARSER
scanner.c: scanner.c.g2
	cp $(srcdir)/$@.g2 $@
	@echo "NOTE: Compilation of scanner.c can take several minutes!"
else
scanner.c: scanner.c.t0
	cp $(srcdir)/$@.t0 $@
endif

libzscanner_la_SOURCES =		\
	error.h				\
	error.c				\
	functions.h			\
	functions.c			\
	scanner.h

nodist_libzscanner_la_SOURCES =		\
	scanner.c

libzscanner_la_CFLAGS = $(CODE_COVERAGE_CFLAGS)
libzscanner_la_LDFLAGS =		\
	$(CODE_COVERAGE_LDFLAGS)	\
	-version-info 0:1:0

include $(srcdir)/tests/Makefile.inc
