.SUFFIXES : .cpp

INCDIR = -Isrc/kaitai
LIBDIR =

VPATH = bin:./bin src:./src/kaitai 

CC = g++
CXXFLAGS = -g -std=c++11 -DKS_STR_ENCODING_NONE
LIBS =  

OBJS = main.o animal.o kaitaistream.o

TARGET = kaitaiAnimalExample

$(TARGET): $(OBJS)
		$(CC) -o $@ $(OBJS) $(LIBDIR) $(LIBS) 

.cpp.o:
		$(CC) -c $(CXXFLAGS) $(INCDIR) $^

clean:
		rm -f $(OBJS) bin/$(TARGET) core
