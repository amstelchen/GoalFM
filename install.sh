#!/bin/bash

sudo cp -v assets/GoalFM.png /usr/share/pixmaps/GoalFM.png
sudo cp -v assets/GoalFM.desktop /usr/share/applications/
cp -v assets/GoalFM.desktop ~/Desktop/GoalFM.desktop

xgettext -d base -o locales/base.pot GoalFM/*.py
poedit 2>/dev/null

#python setup.py sdist
python -m build --wheel --no-isolation
#updpkgsums
#makepkg -fci

xdg-open ~/Desktop/GoalFM.desktop
#GoalFM.py