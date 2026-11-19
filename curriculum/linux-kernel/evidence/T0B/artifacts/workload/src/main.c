#include <stdio.h>
#include "../include/sensor_dev.h"

int bus_dispatch_poll(struct sensor_device *dev);

REGISTER_SENSOR(temp_primary, 101);

int main(void)
{
    struct sensor_device dev;
    int rc = sensor_init(&dev, 42);
    if (rc != 0) {
        printf("init failed\n");
        return 1;
    }
    int val = bus_dispatch_poll(&dev);
    printf("sensor_poll returned %d (registered: %s)\n", val, sensor_temp_primary.name);
    return 0;
}
