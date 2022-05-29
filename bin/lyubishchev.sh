#!/bin/bash

if [[ ! $@ ]]; then
    python3 -m lyubishchev -h
else
    python3 -m lyubishchev $@
fi