/* Grade-School Multiplication */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char** argv) {
    int x, y, z = 0;

    if (argc == 3 && (x = atoi(argv[1])) && (y = atoi(argv[2]))) {
        printf("%d * %d", x, y);

        const size_t n = log10(x) + 1;
        const size_t m = log10(y) + 1;
        int* xptr = (int*) malloc(sizeof(int) * n);
        int* yptr = (int*) malloc(sizeof(int) * m);

        int i = 0, j = 0;
        while (x > 0) {
            xptr[i++] = x % 10;
            x /= 10;
        }

        while (y > 0) {
            yptr[j++] = y % 10;
            y /= 10;
        }

        for (i = 0; i < n; ++i) {
            for (j = 0; j < m; ++j) {
                z += pow(10, i+j) * xptr[i] * yptr[j];
            }
        }

        printf(" = %d\n", z);

        free(xptr);
        free(yptr);
    }
}
