#!/usr/bin/env python

'''
Simple script to automatically delete old backups.
'''

__version__    = '1.0.0'
__copyright__  = 'Copyright 2011 Champion International Moving, Ltd.'
__author__     = 'Jake Wharton'
__maintainer__ = 'Jake Wharton'
__email__      = 'jake@champmove.com'
__status__     = 'Production'
__license__ = '''
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
'''

import sys
import logging


#Configure logging
#change level to DEBUG for more info, WARN for less
logging.basicConfig(filename='backupdeleter.log', format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.INFO)
log = logging.getLogger('backupdeleter.py')
log.debug('Version %s', __version__)


#Python version check
if sys.version_info < (2, 7, 1):
    log.error('Python version must be 2.7.1 or newer.')
    sys.exit(1)


from datetime import datetime
import fnmatch
import os


#Parse configuration file
log.debug('sys.argv == %s', repr(sys.argv))
if len(sys.argv) != 2:
    log.error('You must specify a configuration file path as the only argument.')
    sys.exit(1)

configs = []
try:
    with open(sys.argv[1], 'r') as cfgfile:
        for cfgline in cfgfile:
            #Skip blank lines and comments
            if cfgline and (cfgline.startswith('#') or cfgline.strip() == ''):
                log.debug('Found comment or blank line.')
                log.debug('> %s', cfgline.rstrip('\n'))
                continue

            #Split into parts
            cfgargs = map(str.strip, cfgline.split(','))

            #Error-check parts
            if len(cfgargs) != 3:
                log.warn('Line does not contain three values. Should be "Path, Pattern, Length (in days)".')
                log.warn('> %s', cfgline)
                continue
            elif not os.path.exists(cfgargs[0]):
                log.warn('Path is invalid or does not exist.')
                log.warn('> %s', cfgargs[0])
                continue
            elif '*' not in cfgargs[1] and '?' not in cfgargs[1]:
                log.warn('No wildcard character in pattern will result in one or zero matches.')
                log.warn('> %s', cfgargs[1])
                continue

            try:
                a = int(cfgargs[2])
                if a <= 1:
                    raise ValueError
            except ValueError:
                log.warn('Specified length is not a valid integer.')
                log.warn('> %s', cfgargs[2])
                continue

            #Add to valid configs
            configs.append({
                'path': cfgargs[0],
                'pattern': cfgargs[1],
                'length': int(cfgargs[2])
            })
            log.debug('Added new configuration.')
            log.debug('> path = %s', cfgargs[0])
            log.debug('> pattern = %s', cfgargs[1])
            log.debug('> length = %s', cfgargs[2])
except IOError:
    log.error('Could not open configuration file.')
    log.error('> %s', sys.argv[1])
    sys.exit(1)


#Run jobs
for config in configs:
    for dirfile in os.listdir(config['path']):
        if fnmatch.fnmatch(dirfile, config['pattern']):
            match = os.path.join(config['path'], dirfile)
            if (datetime.now() - datetime.fromtimestamp(os.stat(match).st_mtime)).days >= config['length']:
                log.info('Removing "%s".', dirfile)
                try:
                    os.remove(match)
                except IOError:
                    log.error('Could not remove file "%s".', dirfile)
