# cron2db

Store cron results in a database. 

This is a pair of scripts:

* __cron2db__ - a bash script runs the command with arguments and passes the return code, stdout, stderr, start & end time to c2db

* __c2db__ - a python 3 script which stores the job run in the configured database

__Work in progress - ALPHA.__

## Installation

    python setup.py install

(Into a virtualenv or wherever)

Or you can use [pipsi](https://github.com/mitsuhiko/pipsi#readme) &

	pipsi install .

SQLAlchemy is used for the DB layer so if you intend to use a DB other than the default sqlite you should install the appropriate drivers.

## Configuration

You may want to configure cron such that cron2db & c2db are in cron's path _([more info](https://stackoverflow.com/questions/2388087/how-to-get-cron-to-call-in-the-correct-paths))_. You can do this by _carefully_ adding a PATH line to the systemwide crontab (/etc/crontab) or to your user crontab, eg:

    $ crontab -e

    SHELL=/bin/sh
    PATH=/path/to/cron2db:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

	10 * * * 1-5	cron2db 'myscript.sh arg1 arg2'

You can initialize a default config file & sqlite DB by just running

    c2db init

This creates ~/.config/cron2db.conf & ~/.config/cron2db.sqlite

## Usage

Old cron entry:

	10 * * * 1-5	myscript.sh arg1 arg2

New cron2db cron entry with results stored in DB

	10 * * * 1-5	/pathto/cron2db 'myscript.sh arg1 arg2'

Also see Configuration for setting cron path above.

A manual test run of your scripts through cron2db is advised before trusting your cron jobs with it.

## Other

Inspiration & some code taken from [cronic](https://habilis.net/cronic/).

License: _Public Domain CC0: http://creativecommons.org/publicdomain/zero/1.0/_