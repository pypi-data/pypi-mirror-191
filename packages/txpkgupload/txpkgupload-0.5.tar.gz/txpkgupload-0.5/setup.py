#!/usr/bin/env python3

# Copyright 2009-2015 Canonical Ltd.  All rights reserved.
#
# This file is part of txpkgupload.
#
# txpkgupload is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# txpkgupload is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with txpkgupload.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages


# generic helpers primarily for the long_description
def generate(*docname_or_string):
    res = []
    for value in docname_or_string:
        if value.endswith('.txt'):
            with open(value) as f:
                value = f.read()
        res.append(value)
        if not value.endswith('\n'):
            res.append('')
    return '\n'.join(res)
# end generic helpers


with open("src/txpkgupload/version.txt") as f:
    __version__ = f.read().strip()
with open("README.txt") as f:
    description = f.readline().strip()

setup(
    name='txpkgupload',
    version=__version__,
    packages=find_packages('src') + ['twisted.plugins'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    maintainer='LAZR Developers',
    maintainer_email='lazr-developers@lists.launchpad.net',
    description=description,
    long_description=generate('src/txpkgupload/NEWS.txt'),
    license='AGPL v3',
    python_requires=">=3.5",
    install_requires=[
        'FormEncode',
        'importlib-metadata; python_version < "3.8"',
        'lazr.sshserver>=0.1.7',
        'oops-datedir-repo>=0.0.21',
        'oops-twisted>=0.0.7',
        'PyYAML',
        'setuptools',
        'six>=1.12.0',
        'Twisted[conch_nacl]',
        'zope.interface>=3.6.0',
        ],
    url='https://launchpad.net/txpkgupload',
    download_url='https://launchpad.net/txpkgupload/+download',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        ],
    extras_require=dict(
        test=['fixtures',
              'testtools'],
    ),
    # This does not play nicely with buildout because it downloads but does
    # not cache the package.
    # setup_requires=['eggtestinfo', 'setuptools_bzr'],
    test_suite='txpkgupload.tests',
    )
