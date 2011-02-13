#!/bin/bash
PYTHONPATH=$PWD:$PWD/..${PYTHONPATH:+:$PYTHONPATH}
export PYTHONPATH

echo "** Core **"
django-admin.py test valentunes --settings=settings
