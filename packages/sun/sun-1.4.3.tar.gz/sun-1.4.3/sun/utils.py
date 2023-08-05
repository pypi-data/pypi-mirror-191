#!/usr/bin/python3
# -*- coding: utf-8 -*-

# utils.py is a part of sun.

# Copyright 2015-2023 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# sun is a tray notification applet for informing about
# package updates in Slackware.

# https://gitlab.com/dslackw/sun

# sun is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import re
import tomli
import getpass
import urllib3
from sun.__metadata__ import data_configs


class Utilities:

    def __init__(self):
        self.data_configs = data_configs

    @staticmethod
    def url_open(mirror):
        """ Read the url and return the changelog.txt file. """
        changelog_txt = ''
        try:
            http = urllib3.PoolManager()
            con = http.request('GET', mirror)
            changelog_txt = con.data.decode()
        except KeyError:
            print('SUN: error: ftp mirror not supported')

        return changelog_txt

    @staticmethod
    def read_file(registry):
        """ Return reading file. """
        with open(registry, 'r', encoding='utf-8', errors='ignore') as file_txt:
            return file_txt.read()

    def slack_ver(self):
        """ Open a file and read the Slackware version. """
        dist = self.read_file('/etc/slackware-version')
        sv = re.findall(r'\d+', dist)

        if len(sv) > 2:
            version = ('.'.join(sv[:2]))
        else:
            version = ('.'.join(sv))

        return dist.split()[0], version

    @staticmethod
    def read_mirrors_file(mirrors):
        """ Read a mirror from the /etc/slackpkg/mirrors file. """
        for mirror in mirrors.splitlines():

            if mirror and not mirror.startswith('#'):
                return mirror.lstrip()

        return ''

    def mirror_url(self):
        """ Return the mirror url. """
        # TOML configurations
        configs = self.configs()
        alter_mirror = configs['mirror']['HTTP_MIRROR']
        changelog_file = configs['library']['CHANGELOG_FILE']

        # Data configurations
        changelog = self.data_configs["changelog_txt"]

        # Read the mirror from /etc/slackpkg/mirrors
        mirror = self.read_mirrors_file(self.read_file(f'{self.data_configs["etc_slackpkg"]}mirrors'))

        if alter_mirror:
            mirror = alter_mirror

        if changelog_file:
            changelog = changelog_file

        if not mirror:
            print('You do not have any http/s mirror selected in /etc/slackpkg/'
                  'mirrors.\nPlease edit that file and uncomment ONE http/s mirror\n '
                  'or edit the /etc/sun/sun.toml configuration file.')
            return ''

        elif mirror.startswith('ftp'):
            print('Please select an http/s mirror not ftp.')
            return ''

        return f'{mirror}{changelog}'

    def fetch(self):
        """ Get the ChangeLog.txt file size and counts
        the upgraded packages.
        """
        mirror = self.mirror_url()
        configs = self.configs()
        r, slackpkg_last_date = '', ''
        upgraded = []

        # Default patterns
        packages = ('z:  Upgraded.', 'z:  Rebuilt.', 'z:  Added.', 'z:  Removed.')
        kernel = ('*:  Upgraded.', '*:  Rebuilt.')

        # TOML Configuration file settings
        packages_pattern = tuple(configs['pattern']['PACKAGES'])
        kernel_pattern = tuple(configs['pattern']['KERNEL'])
        library_path = configs['library']['LIBRARY_PATH']
        changelog_file = configs['library']['CHANGELOG_FILE']

        if packages_pattern:
            packages = packages_pattern

        if kernel_pattern:
            kernel = kernel_pattern

        if mirror:
            changelog_txt = self.url_open(mirror)

            path = f'{self.data_configs["var_lib_slackpkg"]}{self.data_configs["changelog_txt"]}'
            if library_path:
                path = f'{library_path}{changelog_file}'

            if os.path.isfile(path):
                slackpkg_last_date = self.read_file(path).split('\n', 1)[0].strip()

            for line in changelog_txt.splitlines():
                if slackpkg_last_date == line.strip():
                    break

                # This condition checks the packages
                if line.endswith(packages):
                    upgraded.append(line.split('/')[-1])

                # This condition checks the kernel
                if line.endswith(kernel):
                    upgraded.append(line)

        return upgraded

    def configs(self):
        """ SUN configurations. """

        # Default arguments
        configs_args = {
            'time': {
                'INTERVAL': 60,
                'STANDBY': 3
             }
        }

        config_file = f'{self.data_configs["conf_path"]}sun.toml'

        if os.path.isfile(config_file):
            with open(config_file, 'rb') as conf:
                configs_args = tomli.load(conf)

        return configs_args

    def os_info(self):
        """ Get the OS info. """
        stype = 'Stable'
        mir = self.mirror_url()

        if mir and 'current' in mir:
            stype = 'Current'

        info = (
            f'User: {getpass.getuser()}\n'
            f'OS: {self.slack_ver()[0]}\n'
            f'Version: {self.slack_ver()[1]}\n'
            f'Type: {stype}\n'
            f'Arch: {self.data_configs["arch"]}\n'
            f'Packages: {len(os.listdir(self.data_configs["pkg_path"]))}\n'
            f'Kernel: {self.data_configs["kernel"]}\n'
            f'Uptime: {self.data_configs["uptime"]}\n'
            '[Memory]\n'
            f'Free: {self.data_configs["mem"][9]}, Used: {self.data_configs["mem"][8]}, '
            f'Total: {self.data_configs["mem"][7]}\n'
            '[Disk]\n'
            f'Free: {self.data_configs["disk"][2] // (2**30)}Gi, Used: '
            f'{self.data_configs["disk"][1] // (2**30)}Gi, '
            f'Total: {self.data_configs["disk"][0] // (2**30)}Gi\n'
            f'[Processor]\n'
            f'CPU: {self.data_configs["cpu"]}'
            )

        return info
