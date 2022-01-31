/* Grade-School Multiplication */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char** argv) {
	if (argc == 3) {
        int x = atoi(argv[1]), y = atoi(argv[2]), i, j, z;
        const size_t n = log10(x) + 1, m = log10(y) + 1;
        int *xptr = new int[n], *yptr = new int[m];

        i = j = z = 0;
        int xt = x, yt = y;

        while (xt > 0) {
            xptr[i++] = xt % 10;
            xt /= 10;
        }

        while (yt > 0) {
            yptr[j++] = yt % 10;
            yt /= 10;
        }

		for (i = 0; i < n; ++i) {
            for (j = 0; j < m; ++j) {
                z += pow(10, i+j) * xptr[i] * yptr[j];
            }
        }

		printf("%d * %d = %d\n", x, y, z);
	}
}
