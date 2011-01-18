backupdeleter.py
================
`backupdeleter.py` is a python script which can be used for automatically
deleting old backups files. The script reads a configuration file which defines
the paths, patterns, and age of the files which should be deleted.

By triggering this to run as a post-backup script or as a cron job you can ensure
that you only keep the desired amount of backups necessary.


Prerequisites
-------------

1.  Python 2.7.1+ - [http://python.org/](http://python.org)

    The python runtime is required for executing this script. A minimum of
    version 2.7.1 is needed for the pattern matching libraries.


Usage
-----
Executing this script requires passing in the configuration file as the only
parameter. It will then parse the configuration and act accordingly on the
directories contained therein.

By default the script will output a log of any warnings or errors and any files
that are deleted to `backupdeleter.log`. If you wish to see more information
you can edit the script and change the logging level to `DEBUG`. To see only
issues with the configuration change the logging level to `WARN`.

You can see an example configuration file and the syntax that it uses in
`config.txt.sample`.


Developed By
------------
Champion International Moving, Ltd.

* Jake Wharton - <jake@champmove.com>

Git repository located at
[http://github.com/ChampionInternationalMoving/backupdeleter](http://github.com/ChampionInternationalMoving/backupdeleter)


License
-------
    Copyright 2011 Champion International Moving, Ltd.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
