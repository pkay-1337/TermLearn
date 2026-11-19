#include <stdio.h>

int add(int a, int b)
{
    return a + b;
}

int main(void)
{
    int x = 2;
    int y = 3;

    printf("%d\n", add(x, y));
    return 0;
}
