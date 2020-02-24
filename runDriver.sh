#!/bin/bash

python3 driver.py owls 1200 100 100 4 6 0.1
rm -r Output/*
rm Ordered/*
rm Grid/*

python3 driver.py owls 1200 100 100 4 6 0.2
rm -r Output/*
rm Ordered/*
rm Grid/*

python3 driver.py owls 1200 100 100 4 6 0.3
rm -r Output/*
rm Ordered/*
rm Grid/*

python3 driver.py rats 1200 100 100 4 6 0.1
rm -r Output/*
rm Ordered/*
rm Grid/*

python3 driver.py rats 1200 100 100 4 6 0.2
rm -r Output/*
rm Ordered/*
rm Grid/*

python3 driver.py rats 1200 100 100 4 6 0.3
rm -r Output/*
rm Ordered/*
rm Grid/*