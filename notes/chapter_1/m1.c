/* simple multipliciation via repeated additions */

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
    int x, y, z = 0;

    if (argc == 3 && (x = atoi(argv[1])) && (y = atoi(argv[2]))) {
        for (int i = 0; i < y; ++i)
            z += x;
        printf("%d * %d = %d\n", x, y, z);
    }
}
