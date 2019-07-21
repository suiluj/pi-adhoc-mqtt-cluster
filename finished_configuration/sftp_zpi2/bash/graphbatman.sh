#!/bin/bash

sudo batadv-vis > batmanmeshnetwork.dot
dot -T png -o batmanmeshnetwork.png batmanmeshnetwork.dot