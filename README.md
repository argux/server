[![Build Status](https://travis-ci.org/argux/server.svg?branch=master)](https://travis-ci.org/argux/server)
[![Coverage Status](https://coveralls.io/repos/argux/server/badge.svg?branch=master&service=github)](https://coveralls.io/github/argux/server?branch=master)
[![Code Climate](https://codeclimate.com/github/argux/server/badges/gpa.svg)](https://codeclimate.com/github/argux/server)
[![Code Health](https://landscape.io/github/argux/server/master/landscape.svg?style=flat)](https://landscape.io/github/argux/server/master)
[![Documentation Status](https://readthedocs.org/projects/argux-server/badge/?version=latest)](http://argux-server.readthedocs.org/en/latest/?badge=latest)
[![Join the chat at https://gitter.im/argux/server](https://badges.gitter.im/argux/server.svg)](https://gitter.im/argux/server?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Install Argux Server ##

    python setup.py install

## Generate config-file
    $ argux-server_genconfig

    ###########################################
    ###                                     ###
    ### Argux Server configuration wizard.  ###
    ###                                     ###
    ###########################################
     
    Config file location [./argux-server.ini]: ./argux.ini
    Use secure cookies? (Enforce HTTPS) ['y', 'n'] (Default: y)n
    Enable debugging? ['y', 'n'] (Default: n)
    WSGI Server? ['pserve', 'uwsgi'] (Default: pserve)
    Choose Database Engine ['mysql', 'pgsql', 'sqlite'] sqlite
    database path: (/var/lib/argux-server/argux.sqlite)

## Initialize the database

    argux-server_initdb argux-server.ini

# Dependencies
Argux depends the following software

 - pyramid 1.7.0
 - bootstrap 3.3.5 (http://getbootstrap.com)
 - bootstrap-datetimepicker (https://github.com/Eonasdan/bootstrap-datetimepicker)
 - chartjs (http://chartjs.org) 2.1.3
 - bcrypt 2.0.0

## Development

# Installing development tools

    npm install --only=dev

# Compile javascripts
    gulp

# Running test-suites

Testing javascripts

    npm test

Testing python modules

    python setup.py nosetests
