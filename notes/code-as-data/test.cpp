#include <iostream>
#include <vector>

using namespace std;

int NAND(int a, int b) { return !(a && b); }

int LOOKUP3(vector<int> X, vector<int> i) {
#include "nand-circ.h"
}

int main() {
  vector<int> F = {0, 0, 1, 1, 0, 0, 1, 0};

  for (auto i = 0; i <= 1; i++) {
    for (auto j = 0; j <= 1; j++) {
      for (auto k = 0; k <= 1; k++) {
        cout << "LOOKUP3(" << F[0] << "," << F[1] << "," << F[2] << "," << F[3]
             << "," << F[4] << "," << F[5] << "," << F[6] << "," << F[7] << ","
             << i << "," << j << "," << k << ") = " << LOOKUP3(F, {i, j, k})
             << endl;
      }
    }
  }

  return EXIT_SUCCESS;
}