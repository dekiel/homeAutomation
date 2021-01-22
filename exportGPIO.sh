#!/usr/bin/env sh

for i in 79 80 81 82 83 84 86 87
  do echo ${i} > /sys/class/gpio/export; echo out > /sys/class/gpio/gpio${i}/direction; echo 1 > /sys/class/gpio/gpio${i}/active_low; echo 0 > /sys/class/gpio/gpio${i}/value
done