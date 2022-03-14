#include <iostream>

/*
    C++ version of
    https://nbviewer.org/github/boazbk/tcscode/blob/master/Chap_04_Syntactic_Sugar.ipynb#Even-more-sugar
*/

using namespace std;

string NAND(string a, string b) {
  static auto counter = 1;
  auto v = "temp_" + to_string(counter++);
  cout << "auto " << v << " = NAND(" << a << "," << b << ");" << endl;
  return v;
}

string NOT(string a) { return NAND(a, a); }

string AND(string a, string b) {
  auto temp = NAND(a, b);
  return NOT(temp);
}

string OR(string a, string b) {
  auto temp1 = NOT(a);
  auto temp2 = NOT(b);
  return NAND(temp1, temp2);
}

string MAJ(string a, string b, string c) {
  auto and1 = AND(a, b);
  auto and2 = AND(a, c);
  auto and3 = AND(b, c);
  auto or1 = OR(and1, and2);
  return OR(or1, and3);
}

string IF(string cond, string a, string b) {
  auto notcond = NAND(cond, cond);
  auto temp = NAND(b, notcond);
  auto temp1 = NAND(a, cond);
  return NAND(temp, temp1);
}

string LOOKUP1(string X0, string X1, string X2) { return IF(X2, X1, X0); }

string LOOKUP2(string X0, string X1, string X2, string X3, string i0,
               string i1) {
  auto a = LOOKUP1(X2, X3, i1);
  auto b = LOOKUP1(X0, X1, i1);
  return IF(i0, a, b);
}

string LOOKUP3(string X0, string X1, string X2, string X3, string X4, string X5,
               string X6, string X7, string i0, string i1, string i2) {
  auto a = LOOKUP2(X4, X5, X6, X7, i1, i2);
  auto b = LOOKUP2(X0, X1, X2, X3, i1, i2);
  return IF(i0, a, b);
}

int main() {
  auto output = LOOKUP3("X[0]", "X[1]", "X[2]", "X[3]", "X[4]", "X[5]", "X[6]",
                        "X[7]", "i[0]", "i[1]", "i[2]");
  cout << "return " << output << ";" << endl;

  return EXIT_SUCCESS;
}