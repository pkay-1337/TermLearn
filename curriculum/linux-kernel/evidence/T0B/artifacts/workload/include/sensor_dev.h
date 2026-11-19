#ifndef SENSOR_DEV_H
#define SENSOR_DEV_H

struct sensor_device {
    int id;
    const char *name;
    int status;
    int (*read_sample)(void *buf);
};

/* Function declarations */
int sensor_init(struct sensor_device *dev, int id);
int sensor_poll(struct sensor_device *dev);

/* Kernel-style declarative registration macro */
#define REGISTER_SENSOR(name_sym, id_val) \
    static struct sensor_device sensor_##name_sym = { \
        .id = (id_val), \
        .name = #name_sym, \
        .status = 0, \
        .read_sample = 0 \
    }

#endif /* SENSOR_DEV_H */
