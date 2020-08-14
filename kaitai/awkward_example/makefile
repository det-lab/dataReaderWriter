.SUFFIXES : .cpp

INCDIR = -I/opt/awkward-1.0/include -Isrc/kaitai
LIBDIR = -L/opt/awkward-1.0/build/lib.linux-x86_64-3.7/awkward1

VPATH = bin:./bin src:./src/kaitai 

CC = g++
CXXFLAGS = -g -std=c++11 -DKS_STR_ENCODING_NONE
LIBS = -lawkward -lawkward-cpu-kernels

OBJS = main.o animal.o kaitaistream.o

TARGET = kaitaiAnimalExample

$(TARGET): $(OBJS)
		$(CC) -o $@ $(OBJS) $(LIBDIR) $(LIBS) 

.cpp.o:
		$(CC) -c $(CXXFLAGS) $(INCDIR) $^

clean:
		rm -f $(OBJS) bin/$(TARGET) core
