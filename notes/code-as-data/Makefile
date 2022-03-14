CXXFLAGS = -g -std=c++17 -Wall -Wextra -Wpedantic -Werror

.PHONY: clean

run: test
	./test

test: test.cpp nand-circ.h
	$(CXX) $(CXXFLAGS) $< -o $@

nand-circ.h: desugar
	./desugar > nand-circ.h

clean:
	rm -f *.o *.gch nand-circ.h desugar test