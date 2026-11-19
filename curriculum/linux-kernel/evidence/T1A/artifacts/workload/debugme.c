#include <stdio.h>

static int socket_probe(int fd)
{
    int doubled = fd * 2;
    printf("probe fd=%d doubled=%d\n", fd, doubled);
    return doubled;
}

int main(void)
{
    int fd = 7;
    int result = socket_probe(fd);
    printf("result=%d\n", result);
    return 0;
}
