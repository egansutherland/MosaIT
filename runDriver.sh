#!/usr/bin/bash


for i in {0..30}
	let temp=i/10 
	python3 /home/egan/Mosait/driver.py coral 1200 100 100 4 4 $temp
	rm -r /home/egan/Mosait/Output/*
	rm Ordered/*
	rm /home/egan/Mosait/Grid/*

	python3 /home/egan/Mosait/driver.py birds 1200 100 100 4 4 $temp
	rm -r /home/egan/Mosait/Output/*
	rm Ordered/*
	rm /home/egan/Mosait/Grid/*