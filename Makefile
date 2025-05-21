
CXXFLAGS=-O3 -std=c++11 -Wall 
RM=rm -f
EXEC=mandelbrot

all: $(EXEC)

$(EXEC):
	mpic++ $(CXXFLAGS) $(EXEC).cpp -c -o $(EXEC).o
	mpic++ $(CXXFLAGS) $(EXEC).o -o $(EXEC) –fopenmp

clean:
	$(RM) $(EXEC).o $(EXEC)
