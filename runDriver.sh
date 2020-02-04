#!/bin/bash

python3 driver.py coral 1200 100 100 4 4 0.1
rm -r Output/*
rm Ordered/*
rm Grid/*

python3 driver.py coral 1200 100 100 4 4 0.2
rm -r Output/*
rm Ordered/*
rm Grid/*

python3 driver.py coral 1200 100 100 4 4 0.3
rm -r Output/*
rm Ordered/*
rm Grid/*

python3 driver.py squirrels 1200 100 100 4 4 0.1
rm -r Output/*
rm Ordered/*
rm Grid/*

python3 driver.py squirrels 1200 100 100 4 4 0.2
rm -r Output/*
rm Ordered/*
rm Grid/*

python3 driver.py squirrels 1200 100 100 4 4 0.3
rm -r Output/*
rm Ordered/*
rm Grid/*