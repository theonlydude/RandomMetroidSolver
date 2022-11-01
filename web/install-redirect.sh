#!/bin/bash

for webapp in web2py-redirect web2py-backend; do
    # first remove brocken symlinks
    find ~/${webapp}/applications/solver/static -xtype l -exec rm -f {} \;

    # create app dirs
    mkdir -p ~/${webapp}/applications/solver/views/solver_web
    cd ~/${webapp}/applications/solver/
    mkdir -p cache  controllers  cron  databases  errors  languages  models  modules  private  sessions  static  uploads  views

    # create all the required symlinks if they don't already exist
    [ -L ~/${webapp}/applications/solver/static/favicon.ico ] || ln -s ~/RandomMetroidSolver/web/static/favicon.ico ~/${webapp}/applications/solver/static/favicon.ico
    [ -L ~/${webapp}/applications/solver/static/favicon.png ] || ln -s ~/RandomMetroidSolver/web/static/favicon.png ~/${webapp}/applications/solver/static/favicon.png

    [ -L ~/${webapp}/applications/solver/controllers/solver_web.py ] || ln -s ~/RandomMetroidSolver/web/controllers/solver_web.py ~/${webapp}/applications/solver/controllers/solver_web.py
    [ -L ~/${webapp}/standard_presets ] || ln -s ~/RandomMetroidSolver/standard_presets ~/${webapp}/standard_presets
    [ -L ~/${webapp}/community_presets -o -d ~/${webapp}/community_presets ] || ln -s ~/community_presets ~/${webapp}/community_presets
    [ -L ~/${webapp}/rando_presets ] || ln -s ~/RandomMetroidSolver/rando_presets ~/${webapp}/rando_presets
    [ -L ~/${webapp}/routes.py ] || ln -s ~/RandomMetroidSolver/web/static/routes-redirect.py ~/${webapp}/routes.py
    [ -L ~/${webapp}/varia_repository ] || ln -s ~/varia_repository ~/${webapp}/varia_repository
done
