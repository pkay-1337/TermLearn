#include "../include/sensor_dev.h"

static int sanitize_sensor_id(int id)
{
    if (id < 0 || id > 1024) {
        return -1;
    }
    return id;
}

int sensor_init(struct sensor_device *dev, int id)
{
    if (!dev) {
        return -1;
    }
    int valid = sanitize_sensor_id(id);
    if (valid < 0) {
        return -1;
    }
    dev->id = valid;
    dev->status = 1;
    return 0;
}

int sensor_poll(struct sensor_device *dev)
{
    if (!dev || dev->status == 0) {
        return -1;
    }
    return dev->status;
}
