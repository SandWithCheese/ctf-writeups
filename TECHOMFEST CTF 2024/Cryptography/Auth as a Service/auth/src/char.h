#ifndef _CHAR_H
#define _CHAR_H

#include <linux/cdev.h>
#include <linux/kernel.h>
#include "aes.h"

#define DEVICE_NAME "auth"
#define SET_KEY 0xAE5CBC1
#define SET_IV  0xAE5CBC2

struct chrdev_info {
    unsigned int major;
    struct cdev cdev;
    struct class *class;
};

#endif