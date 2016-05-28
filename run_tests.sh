export ARGUX_CONFIG=./tests/test.ini

argux-server_initdb $ARGUX_CONFIG

python setup.py nosetests
