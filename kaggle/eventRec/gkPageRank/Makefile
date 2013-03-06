CC = gcc 
OPTFLAGS = -O3 -fno-strict-aliasing -D_GNU_SOURCE
COPTIONS = -DLINUX -D_FILE_OFFSET_BITS=64 -std=c99 -Wall\
           -Wno-unused-function -Wno-unused-label -Wno-unused-variable\
           -Wno-parentheses -Wsequence-point

#Standard Libraries
STDLIBS = -lm -lpthread

#external libraries
EXTLIBS = -I ~/Documents/George/trunk/

CFLAGS = $(COPTIONS)  $(OPTFLAGS)
LIBS = $(STDLIBS) $(EXTLIBS)

SOURCE = personPageRank.c
EXE = personPageRank

default:
	$(CC) $(CFLAGS) $(SOURCE) -o $(EXE) $(LIBS)