CC = gcc 
OPTFLAGS = -O3 -fno-strict-aliasing -D_GNU_SOURCE
COPTIONS = -DLINUX -D_FILE_OFFSET_BITS=64 -std=c99 -g -Wall\
           -Wno-unused-function -Wno-unused-label -Wno-unused-variable\
           -Wno-parentheses -Wsequence-point -fopenmp

GKINCHOME=/home/sharmamo/dev/coldplay/ppr/trunk
GKLIBHOME=/home/sharmamo/dev/coldplay/ppr/trunk/build/Linux-x86_64/

#Standard Libraries
STDLIBS = -lm -lpthread 

#external libraries
EXT_LIBS = -lGKlib

EXT_LIBS_DIR= -L$(GKLIBHOME)
#CFLAGS = $(COPTIONS)  $(OPTFLAGS) -I$(GKINCHOME) 
CFLAGS = $(COPTIONS)  -I$(GKINCHOME) 
LIBS = $(STDLIBS) $(EXT_LIBS)

SOURCE = topicSensPRank.c
EXE = topicSensPRank 

default:
	$(CC) $(CFLAGS) $(SOURCE) -o $(EXE) $(LIBS) $(EXT_LIBS_DIR)

