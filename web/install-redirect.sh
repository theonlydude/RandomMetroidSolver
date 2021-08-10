#!/bin/bash

# first remove brocken symlinks
find ~/web2py-redirect/applications/solver/static -xtype l -exec rm -f {} \;

# create app dirs
mkdir -p ~/web2py-redirect/applications/solver/views/solver_web
cd ~/web2py-redirect/applications/solver/
mkdir -p cache  controllers  cron  databases  errors  languages  models  modules  private  sessions  static  uploads  views


# create all the required symlinks if they don't already exist
[ -L ~/web2py-redirect/applications/solver/static/favicon.ico ] || ln -s ~/RandomMetroidSolver/web/static/favicon.ico ~/web2py-redirect/applications/solver/static/favicon.ico

[ -L ~/web2py-redirect/applications/solver/controllers/solver_web.py ] || ln -s ~/RandomMetroidSolver/web/controllers/solver_web.py ~/web2py-redirect/applications/solver/controllers/solver_web.py
[ -L ~/web2py-redirect/standard_presets ] || ln -s ~/RandomMetroidSolver/standard_presets ~/web2py-redirect/standard_presets
[ -L ~/web2py-redirect/community_presets -o -d ~/web2py-redirect/community_presets ] || ln -s ~/RandomMetroidSolver/community_presets ~/web2py-redirect/community_presets
[ -L ~/web2py-redirect/rando_presets ] || ln -s ~/RandomMetroidSolver/rando_presets ~/web2py-redirect/rando_presets
[ -L ~/web2py-redirect/routes.py ] || ln -s ~/RandomMetroidSolver/web/static/routes-redirect.py ~/web2py-redirect/routes.py
