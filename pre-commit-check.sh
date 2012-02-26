#!/bin/bash

echo 'Running tests'
bin/py setup.py test

echo '====== Running ZPTLint ======'
for pt in `find src/multitrac/ -name "*.pt"` ; do bin/zptlint $pt; done

echo '====== Running PyFlakes ======'
bin/pyflakes src/multitrac
bin/pyflakes setup.py

echo '====== Running pep8 =========='
bin/pep8 src/multitrac
bin/pep8 setup.py

