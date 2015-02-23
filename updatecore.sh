#!/bin/bash
source ~/Snakepit/bin/activate
yes | pip uninstall willie
python setup.py install

version_check="from willie.__init__ import __version__;print __version__"
version=$(echo $version_check | python -)
version=${version/-/_}

rm -rf ~/Snakepit/local/lib/python2.7/site-packages/willie-$version-py2.7.egg/willie/modules
mkdir ~/Snakepit/local/lib/python2.7/site-packages/willie-$version-py2.7.egg/willie/modules
echo "Removed auto-installed modules"
