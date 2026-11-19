#include "../include/sensor_dev.h"

struct bus_packet {
    int id;
    char payload[32];
};

int bus_dispatch_poll(struct sensor_device *dev)
{
    /* True caller of sensor_poll */
    return sensor_poll(dev);
}
