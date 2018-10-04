.SUFFIXES : .cpp

INCDIR =
LIBDIR =

VPATH = src:./src/kaitai bin:./bin

CC = g++
CXXFLAGS = -g -std=c++11
LIBS = # -lm	the -lm flag links to linux math library but it isn't needed in this context

OBJS = main.o animal.o kaitaistream.o

TARGET = kaitaiAnimalExample

$(TARGET): $(OBJS)
		$(CC) -o $@ $(OBJS) $(LIBDIR) $(LIBS)

.cpp.o:
		$(CC) -c $(CXXFLAGS) $(INCDIR) $<

clean:
		rm -f $(OBJS) bin/$(TARGET) core