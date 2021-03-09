#!/bin/bash

python3 -m twine upload dist/* -u ${USERNAME} -p ${PASSWORD}