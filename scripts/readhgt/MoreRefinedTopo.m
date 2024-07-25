close all
clear all
clc

a = readhgt('N41E024.hgt');

dem(a.lon,a.lat,a.z)

