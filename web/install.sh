#!/bin/bash

if [ $# -eq 1 -a "$1" == "--clean" ]; then
    find ~/web2py/applications/solver/static/images -type l -exec rm -f {} \;
fi

mkdir -p ~/web2py/roms/

# first remove brocken symlinks
find ~/web2py/applications/solver/static -xtype l -exec rm -f {} \;

# create all the required symlinks if they don't already exist

# directories
[ -L ~/web2py/standard_presets ] || ln -s ~/RandomMetroidSolver/standard_presets ~/web2py/standard_presets
[ -L ~/web2py/community_presets -o -d ~/web2py/community_presets ] || ln -s ~/RandomMetroidSolver/community_presets ~/web2py/community_presets
[ -L ~/web2py/rando_presets ] || ln -s ~/RandomMetroidSolver/rando_presets ~/web2py/rando_presets
[ -L ~/web2py/music ] || ln -s ~/RandomMetroidSolver/varia_custom_sprites/music ~/web2py/music
[ -L ~/web2py/patches ] || ln -s ~/RandomMetroidSolver/patches ~/web2py/patches

# views
[ -L ~/web2py/applications/solver/views/solver_web/home.html ] || ln -s ~/RandomMetroidSolver/web/views/home.html ~/web2py/applications/solver/views/solver_web/home.html
[ -L ~/web2py/applications/solver/views/solver_web/presets.html ] || ln -s ~/RandomMetroidSolver/web/views/presets.html ~/web2py/applications/solver/views/solver_web/presets.html
[ -L ~/web2py/applications/solver/views/solver_web/solver.html ] || ln -s ~/RandomMetroidSolver/web/views/solver.html ~/web2py/applications/solver/views/solver_web/solver.html
[ -L ~/web2py/applications/solver/views/solver_web/randomizer.html ] || ln -s ~/RandomMetroidSolver/web/views/randomizer.html ~/web2py/applications/solver/views/solver_web/randomizer.html
[ -L ~/web2py/applications/solver/views/solver_web/infos.html ] || ln -s ~/RandomMetroidSolver/web/views/infos.html ~/web2py/applications/solver/views/solver_web/infos.html
[ -L ~/web2py/applications/solver/views/solver_web/stats.html ] || ln -s ~/RandomMetroidSolver/web/views/stats.html ~/web2py/applications/solver/views/solver_web/stats.html
[ -L ~/web2py/applications/solver/views/solver_web/tracker.html ] || ln -s ~/RandomMetroidSolver/web/views/tracker.html ~/web2py/applications/solver/views/solver_web/tracker.html
[ -L ~/web2py/applications/solver/views/solver_web/_autotracker.js ] || ln -s ~/RandomMetroidSolver/web/views/_autotracker.js ~/web2py/applications/solver/views/solver_web/_autotracker.js
[ -L ~/web2py/applications/solver/views/solver_web/t_includes.html ] || ln -s ~/RandomMetroidSolver/web/views/t_includes.html ~/web2py/applications/solver/views/solver_web/t_includes.html
[ -L ~/web2py/applications/solver/views/solver_web/t_js.html ] || ln -s ~/RandomMetroidSolver/web/views/t_js.html ~/web2py/applications/solver/views/solver_web/t_js.html
[ -L ~/web2py/applications/solver/views/solver_web/t_main.html ] || ln -s ~/RandomMetroidSolver/web/views/t_main.html ~/web2py/applications/solver/views/solver_web/t_main.html
[ -L ~/web2py/applications/solver/views/solver_web/t_style.html ] || ln -s ~/RandomMetroidSolver/web/views/t_style.html ~/web2py/applications/solver/views/solver_web/t_style.html
[ -L ~/web2py/applications/solver/views/solver_web/plando.html ] || ln -s ~/RandomMetroidSolver/web/views/plando.html ~/web2py/applications/solver/views/solver_web/plando.html
[ -L ~/web2py/applications/solver/views/solver_web/customizer.html ] || ln -s ~/RandomMetroidSolver/web/views/customizer.html ~/web2py/applications/solver/views/solver_web/customizer.html
[ -L ~/web2py/applications/solver/views/solver_web/extStats.html ] || ln -s ~/RandomMetroidSolver/web/views/extStats.html ~/web2py/applications/solver/views/solver_web/extStats.html
[ -L ~/web2py/applications/solver/views/solver_web/progSpeedStats.html ] || ln -s ~/RandomMetroidSolver/web/views/progSpeedStats.html ~/web2py/applications/solver/views/solver_web/progSpeedStats.html
[ -L ~/web2py/applications/solver/views/solver_web/plandorepo.html ] || ln -s ~/RandomMetroidSolver/web/views/plandorepo.html ~/web2py/applications/solver/views/solver_web/plandorepo.html

[ -L ~/web2py/applications/solver/views/layout.html ] || ln -s ~/RandomMetroidSolver/web/web2py/views/layout.html ~/web2py/applications/solver/views/layout.html
[ -L ~/web2py/applications/solver/views/web2py_ajax.html ] || ln -s ~/RandomMetroidSolver/web/web2py/views/web2py_ajax.html ~/web2py/applications/solver/views/web2py_ajax.html

[ -L ~/web2py/applications/solver/views/solver_web/varia.css ] || ln -s ~/RandomMetroidSolver/web/views/varia.css ~/web2py/applications/solver/views/solver_web/varia.css

# controler
[ -L ~/web2py/applications/solver/controllers/solver_web.py ] || ln -s ~/RandomMetroidSolver/web/controllers/solver_web.py ~/web2py/applications/solver/controllers/solver_web.py

# common
[ -L ~/web2py/routes.py ] || ln -s ~/RandomMetroidSolver/web/static/routes.py ~/web2py/routes.py

[ -L ~/web2py/applications/solver/static/favicon.ico ] || ln -s ~/RandomMetroidSolver/web/static/favicon.ico ~/web2py/applications/solver/static/favicon.ico
[ -L ~/web2py/applications/solver/static/favicon.png ] || ln -s ~/RandomMetroidSolver/web/static/favicon.png ~/web2py/applications/solver/static/favicon.png

[ -L ~/web2py/applications/solver/static/preset.js ] || ln -s ~/RandomMetroidSolver/web/static/preset.js ~/web2py/applications/solver/static/preset.js
[ -L ~/web2py/applications/solver/static/css/bootstrap-tour.min.css ] || ln -s ~/RandomMetroidSolver/web/static/bootstrap-tour.min.css ~/web2py/applications/solver/static/css/bootstrap-tour.min.css
[ -L ~/web2py/applications/solver/static/barrating ] || ln -s ~/RandomMetroidSolver/web/static/barrating ~/web2py/applications/solver/static/barrating
[ -L ~/web2py/applications/solver/static/js/bootstrap-tour.min.js ] || ln -s ~/RandomMetroidSolver/web/static/bootstrap-tour.min.js ~/web2py/applications/solver/static/js/bootstrap-tour.min.js
[ -L ~/web2py/applications/solver/static/js/FileSaver.js ] || ln -s ~/RandomMetroidSolver/web/static/FileSaver.js ~/web2py/applications/solver/static/js/FileSaver.js
[ -L ~/web2py/applications/solver/static/dist ] || ln -s ~/RandomMetroidSolver/web/static/dist ~/web2py/applications/solver/static/dist
[ -L ~/web2py/applications/solver/static/highslide ] || ln -s ~/RandomMetroidSolver/web/static/highslide ~/web2py/applications/solver/static/highslide
[ -L ~/web2py/applications/solver/static/js/excellentexport.js ] || ln -s ~/RandomMetroidSolver/web/static/excellentexport.js ~/web2py/applications/solver/static/js/excellentexport.js
[ -L ~/web2py/applications/solver/static/css/chosen.css ] || ln -s ~/RandomMetroidSolver/web/static/chosen.css ~/web2py/applications/solver/static/css/chosen.css
[ -L ~/web2py/applications/solver/static/js/chosen.jquery.min.js ] || ln -s ~/RandomMetroidSolver/web/static/chosen.jquery.min.js ~/web2py/applications/solver/static/js/chosen.jquery.min.js
[ -L ~/web2py/applications/solver/static/js/leader-line.min.js ] || ln -s ~/RandomMetroidSolver/web/static/leader-line.min.js ~/web2py/applications/solver/static/js/leader-line.min.js
[ -L ~/web2py/applications/solver/static/js/jquery.redirect.js ] || ln -s ~/RandomMetroidSolver/web/static/jquery.redirect.js ~/web2py/applications/solver/static/js/jquery.redirect.js
[ -L ~/web2py/applications/solver/static/js/crc32.js ] || ln -s ~/RandomMetroidSolver/web/static/crc32.js ~/web2py/applications/solver/static/js/crc32.js
[ -L ~/web2py/applications/solver/static/css/bootstrap.min.css ] || ln -s ~/RandomMetroidSolver/web/web2py/static/css/bootstrap.min.css ~/web2py/applications/solver/static/css/bootstrap.min.css
[ -L ~/web2py/applications/solver/static/css/calendar.css ] || ln -s ~/RandomMetroidSolver/web/web2py/static/css/calendar.css ~/web2py/applications/solver/static/css/calendar.css
[ -L ~/web2py/applications/solver/static/css/web2py-bootstrap3.css ] || ln -s ~/RandomMetroidSolver/web/web2py/static/css/web2py-bootstrap3.css ~/web2py/applications/solver/static/css/web2py-bootstrap3.css
[ -L ~/web2py/applications/solver/static/css/web2py.css ] || ln -s ~/RandomMetroidSolver/web/web2py/static/css/web2py.css ~/web2py/applications/solver/static/css/web2py.css
[ -L ~/web2py/applications/solver/static/js/bootstrap.min.js ] || ln -s ~/RandomMetroidSolver/web/web2py/static/js/bootstrap.min.js ~/web2py/applications/solver/static/js/bootstrap.min.js
[ -L ~/web2py/applications/solver/static/js/calendar.js ] || ln -s ~/RandomMetroidSolver/web/web2py/static/js/calendar.js ~/web2py/applications/solver/static/js/calendar.js
[ -L ~/web2py/applications/solver/static/js/jquery.js ] || ln -s ~/RandomMetroidSolver/web/web2py/static/js/jquery.js ~/web2py/applications/solver/static/js/jquery.js
[ -L ~/web2py/applications/solver/static/js/modernizr-2.8.3.min.js ] || ln -s ~/RandomMetroidSolver/web/web2py/static/js/modernizr-2.8.3.min.js ~/web2py/applications/solver/static/js/modernizr-2.8.3.min.js
[ -L ~/web2py/applications/solver/static/js/share.js ] || ln -s ~/RandomMetroidSolver/web/web2py/static/js/share.js ~/web2py/applications/solver/static/js/share.js
[ -L ~/web2py/applications/solver/static/js/web2py-bootstrap3.js ] || ln -s ~/RandomMetroidSolver/web/web2py/static/js/web2py-bootstrap3.js ~/web2py/applications/solver/static/js/web2py-bootstrap3.js
[ -L ~/web2py/applications/solver/static/js/web2py.js ] || ln -s ~/RandomMetroidSolver/web/web2py/static/js/web2py.js ~/web2py/applications/solver/static/js/web2py.js
[ -L ~/web2py/applications/solver/static/image-picker ] || ln -s ~/RandomMetroidSolver/web/static/image-picker ~/web2py/applications/solver/static/image-picker
[ -L ~/web2py/applications/solver/static/js/localforage.nopromises.min.js ] || ln -s ~/RandomMetroidSolver/web/static/localforage.nopromises.min.js ~/web2py/applications/solver/static/js/localforage.nopromises.min.js
[ -L ~/web2py/applications/solver/static/js/spc_snes.js ] || ln -s ~/RandomMetroidSolver/web/static/spc_js/spc_snes.js ~/web2py/applications/solver/static/js/spc_snes.js
[ -L ~/web2py/applications/solver/static/js/spc_snes.js.mem ] || ln -s ~/RandomMetroidSolver/web/static/spc_js/spc_snes.js.mem ~/web2py/applications/solver/static/js/spc_snes.js.mem

mkdir -p ~/web2py/applications/solver/static/images/common/
[ -L ~/web2py/applications/solver/static/images/common/area_map_20200112.png ] || ln -s ~/RandomMetroidSolver/web/static/area_map.png ~/web2py/applications/solver/static/images/common/area_map_20200112.png
[ -L ~/web2py/applications/solver/static/images/common/chosen-sprite.png ] || ln -s ~/RandomMetroidSolver/web/static/chosen-sprite.png ~/web2py/applications/solver/static/images/common/chosen-sprite.png
[ -L ~/web2py/applications/solver/static/images/common/chosen-sprite@2x.png ] || ln -s ~/RandomMetroidSolver/web/static/chosen-sprite@2x.png ~/web2py/applications/solver/static/images/common/chosen-sprite@2x.png

# home
mkdir -p ~/web2py/applications/solver/static/images/home/
[ -L ~/web2py/applications/solver/static/images/home/logo_varia.png ] || ln -s ~/RandomMetroidSolver/web/static/logo_varia.png ~/web2py/applications/solver/static/images/home/logo_varia.png
[ -L ~/web2py/applications/solver/static/images/home/donate.png ] || ln -s ~/RandomMetroidSolver/web/static/donate.png ~/web2py/applications/solver/static/images/home/donate.png

# preset
mkdir -p ~/web2py/applications/solver/static/images/preset/
[ -L ~/web2py/applications/solver/static/images/preset/snes-controller.png ] || ln -s ~/RandomMetroidSolver/web/static/snes-controller.png ~/web2py/applications/solver/static/images/preset/snes-controller.png
[ -L ~/web2py/applications/solver/static/images/preset/crystal_flash.png ] || ln -s ~/RandomMetroidSolver/web/static/crystal_flash.png ~/web2py/applications/solver/static/images/preset/crystal_flash.png

# rando
mkdir -p ~/web2py/applications/solver/static/images/rando/
[ -L ~/web2py/applications/solver/static/images/rando/donate_randomizer.png ] || ln -s ~/RandomMetroidSolver/web/static/donate_randomizer.png ~/web2py/applications/solver/static/images/rando/donate_randomizer.png
[ -L ~/web2py/applications/solver/static/images/rando/ajax-loader.gif ] || ln -s ~/RandomMetroidSolver/web/static/ajax-loader.gif ~/web2py/applications/solver/static/images/rando/ajax-loader.gif
[ -L ~/web2py/applications/solver/static/images/rando/vanilla.png ] || ln -s ~/RandomMetroidSolver/web/static/vanilla.png ~/web2py/applications/solver/static/images/rando/vanilla.png
[ -L ~/web2py/applications/solver/static/images/rando/mirror.png ] || ln -s ~/RandomMetroidSolver/web/static/mirror.png ~/web2py/applications/solver/static/images/rando/mirror.png

# rando - help
mkdir -p ~/web2py/applications/solver/static/images/help/
[ -L ~/web2py/applications/solver/static/images/help/area_map_thumbnail.png ] || ln -s ~/RandomMetroidSolver/web/static/area_map_thumbnail.png ~/web2py/applications/solver/static/images/help/area_map_thumbnail.png
[ -L ~/web2py/applications/solver/static/images/help/hud_full.png ] || ln -s ~/RandomMetroidSolver/web/static/help/hud_full.png ~/web2py/applications/solver/static/images/help/hud_full.png
[ -L ~/web2py/applications/solver/static/images/help/hud_chozo_start.png ] || ln -s ~/RandomMetroidSolver/web/static/help/hud_chozo_start.png ~/web2py/applications/solver/static/images/help/hud_chozo_start.png
[ -L ~/web2py/applications/solver/static/images/help/hud_major_energy.png ] || ln -s ~/RandomMetroidSolver/web/static/help/hud_major_energy.png ~/web2py/applications/solver/static/images/help/hud_major_energy.png
[ -L ~/web2py/applications/solver/static/images/help/hud_scav.png ] || ln -s ~/RandomMetroidSolver/web/static/help/hud_scav.png ~/web2py/applications/solver/static/images/help/hud_scav.png
[ -L ~/web2py/applications/solver/static/images/help/hud_scav_over.png ] || ln -s ~/RandomMetroidSolver/web/static/help/hud_scav_over.png ~/web2py/applications/solver/static/images/help/hud_scav_over.png
[ -L ~/web2py/applications/solver/static/images/help/hud_scav_pause.png ] || ln -s ~/RandomMetroidSolver/web/static/help/hud_scav_pause.png ~/web2py/applications/solver/static/images/help/hud_scav_pause.png
[ -L ~/web2py/applications/solver/static/images/help/bt_map.png ] || ln -s ~/RandomMetroidSolver/web/static/help/bt_map.png ~/web2py/applications/solver/static/images/help/bt_map.png
[ -L ~/web2py/applications/solver/static/images/help/cathedral.png ] || ln -s ~/RandomMetroidSolver/web/static/help/cathedral.png ~/web2py/applications/solver/static/images/help/cathedral.png
[ -L ~/web2py/applications/solver/static/images/help/dachora.png ] || ln -s ~/RandomMetroidSolver/web/static/help/dachora.png ~/web2py/applications/solver/static/images/help/dachora.png
[ -L ~/web2py/applications/solver/static/images/help/early_super.png ] || ln -s ~/RandomMetroidSolver/web/static/help/early_super.png ~/web2py/applications/solver/static/images/help/early_super.png
[ -L ~/web2py/applications/solver/static/images/help/high_jump.png ] || ln -s ~/RandomMetroidSolver/web/static/help/high_jump.png ~/web2py/applications/solver/static/images/help/high_jump.png
[ -L ~/web2py/applications/solver/static/images/help/climb_supers.png ] || ln -s ~/RandomMetroidSolver/web/static/help/climb_supers.png ~/web2py/applications/solver/static/images/help/climb_supers.png
[ -L ~/web2py/applications/solver/static/images/help/moat.png ] || ln -s ~/RandomMetroidSolver/web/static/help/moat.png ~/web2py/applications/solver/static/images/help/moat.png
[ -L ~/web2py/applications/solver/static/images/help/red_tower.png ] || ln -s ~/RandomMetroidSolver/web/static/help/red_tower.png ~/web2py/applications/solver/static/images/help/red_tower.png
[ -L ~/web2py/applications/solver/static/images/help/spazer_block.png ] || ln -s ~/RandomMetroidSolver/web/static/help/spazer_block.png ~/web2py/applications/solver/static/images/help/spazer_block.png
[ -L ~/web2py/applications/solver/static/images/help/ln_access.png ] || ln -s ~/RandomMetroidSolver/web/static/help/ln_access.png ~/web2py/applications/solver/static/images/help/ln_access.png
[ -L ~/web2py/applications/solver/static/images/help/ln_gate.png ] || ln -s ~/RandomMetroidSolver/web/static/help/ln_gate.png ~/web2py/applications/solver/static/images/help/ln_gate.png
[ -L ~/web2py/applications/solver/static/images/help/fish_access.png ] || ln -s ~/RandomMetroidSolver/web/static/help/fish_access.png ~/web2py/applications/solver/static/images/help/fish_access.png
[ -L ~/web2py/applications/solver/static/images/help/fish_gate.png ] || ln -s ~/RandomMetroidSolver/web/static/help/fish_gate.png ~/web2py/applications/solver/static/images/help/fish_gate.png
[ -L ~/web2py/applications/solver/static/images/help/tube_access.png ] || ln -s ~/RandomMetroidSolver/web/static/help/tube_access.png ~/web2py/applications/solver/static/images/help/tube_access.png
[ -L ~/web2py/applications/solver/static/images/help/tube_gate.png ] || ln -s ~/RandomMetroidSolver/web/static/help/tube_gate.png ~/web2py/applications/solver/static/images/help/tube_gate.png
[ -L ~/web2py/applications/solver/static/images/help/crab_gate.png ] || ln -s ~/RandomMetroidSolver/web/static/help/crab_gate.png ~/web2py/applications/solver/static/images/help/crab_gate.png
[ -L ~/web2py/applications/solver/static/images/help/greenhill_walljump.png ] || ln -s ~/RandomMetroidSolver/web/static/help/greenhill_walljump.png ~/web2py/applications/solver/static/images/help/greenhill_walljump.png
[ -L ~/web2py/applications/solver/static/images/help/greenhill_gate.png ] || ln -s ~/RandomMetroidSolver/web/static/help/greenhill_gate.png ~/web2py/applications/solver/static/images/help/greenhill_gate.png
[ -L ~/web2py/applications/solver/static/images/help/ws_etank.png ] || ln -s ~/RandomMetroidSolver/web/static/help/ws_etank.png ~/web2py/applications/solver/static/images/help/ws_etank.png
[ -L ~/web2py/applications/solver/static/images/help/ln_chozo.png ] || ln -s ~/RandomMetroidSolver/web/static/help/ln_chozo.png ~/web2py/applications/solver/static/images/help/ln_chozo.png
[ -L ~/web2py/applications/solver/static/images/help/bomb_torizo.png ] || ln -s ~/RandomMetroidSolver/web/static/help/bomb_torizo.png ~/web2py/applications/solver/static/images/help/bomb_torizo.png
[ -L ~/web2py/applications/solver/static/images/help/rando_popup.png ] || ln -s ~/RandomMetroidSolver/web/static/help/rando_popup.png ~/web2py/applications/solver/static/images/help/rando_popup.png
[ -L ~/web2py/applications/solver/static/images/help/item_popup.png ] || ln -s ~/RandomMetroidSolver/web/static/help/item_popup.png ~/web2py/applications/solver/static/images/help/item_popup.png
[ -L ~/web2py/applications/solver/static/images/help/load_popup.png ] || ln -s ~/RandomMetroidSolver/web/static/help/load_popup.png ~/web2py/applications/solver/static/images/help/load_popup.png
[ -L ~/web2py/applications/solver/static/images/help/spore_save.png ] || ln -s ~/RandomMetroidSolver/web/static/help/spore_save.png ~/web2py/applications/solver/static/images/help/spore_save.png
[ -L ~/web2py/applications/solver/static/images/help/ws_save.png ] || ln -s ~/RandomMetroidSolver/web/static/help/ws_save.png ~/web2py/applications/solver/static/images/help/ws_save.png
[ -L ~/web2py/applications/solver/static/images/help/early_super_bis.png ] || ln -s ~/RandomMetroidSolver/web/static/help/early_super_bis.png ~/web2py/applications/solver/static/images/help/early_super_bis.png
[ -L ~/web2py/applications/solver/static/images/help/kraid_save.png ] || ln -s ~/RandomMetroidSolver/web/static/help/kraid_save.png ~/web2py/applications/solver/static/images/help/kraid_save.png
[ -L ~/web2py/applications/solver/static/images/help/backup_locks.png ] || ln -s ~/RandomMetroidSolver/web/static/help/backup_locks.png ~/web2py/applications/solver/static/images/help/backup_locks.png
[ -L ~/web2py/applications/solver/static/images/help/backup_copy.png ] || ln -s ~/RandomMetroidSolver/web/static/help/backup_copy.png ~/web2py/applications/solver/static/images/help/backup_copy.png
[ -L ~/web2py/applications/solver/static/images/help/backup_no_slots.png ] || ln -s ~/RandomMetroidSolver/web/static/help/backup_no_slots.png ~/web2py/applications/solver/static/images/help/backup_no_slots.png
[ -L ~/web2py/applications/solver/static/images/help/mission_impossible.png ] || ln -s ~/RandomMetroidSolver/web/static/help/mission_impossible.png ~/web2py/applications/solver/static/images/help/mission_impossible.png
[ -L ~/web2py/applications/solver/static/images/help/forgotten_all_the_way.png ] || ln -s ~/RandomMetroidSolver/web/static/help/forgotten_all_the_way.png ~/web2py/applications/solver/static/images/help/forgotten_all_the_way.png
[ -L ~/web2py/applications/solver/static/images/help/crab_hole.png ] || ln -s ~/RandomMetroidSolver/web/static/help/crab_hole.png ~/web2py/applications/solver/static/images/help/crab_hole.png
[ -L ~/web2py/applications/solver/static/images/help/ice_door.png ] || ln -s ~/RandomMetroidSolver/web/static/help/ice_door.png ~/web2py/applications/solver/static/images/help/ice_door.png
[ -L ~/web2py/applications/solver/static/images/help/missile_door.png ] || ln -s ~/RandomMetroidSolver/web/static/help/missile_door.png ~/web2py/applications/solver/static/images/help/missile_door.png
[ -L ~/web2py/applications/solver/static/images/help/plasma_door.png ] || ln -s ~/RandomMetroidSolver/web/static/help/plasma_door.png ~/web2py/applications/solver/static/images/help/plasma_door.png
[ -L ~/web2py/applications/solver/static/images/help/powerbomb_door.png ] || ln -s ~/RandomMetroidSolver/web/static/help/powerbomb_door.png ~/web2py/applications/solver/static/images/help/powerbomb_door.png
[ -L ~/web2py/applications/solver/static/images/help/spazer_door.png ] || ln -s ~/RandomMetroidSolver/web/static/help/spazer_door.png ~/web2py/applications/solver/static/images/help/spazer_door.png
[ -L ~/web2py/applications/solver/static/images/help/super_door.png ] || ln -s ~/RandomMetroidSolver/web/static/help/super_door.png ~/web2py/applications/solver/static/images/help/super_door.png
[ -L ~/web2py/applications/solver/static/images/help/wave_door.png ] || ln -s ~/RandomMetroidSolver/web/static/help/wave_door.png ~/web2py/applications/solver/static/images/help/wave_door.png
[ -L ~/web2py/applications/solver/static/images/help/below_botwoon_etank.png ] || ln -s ~/RandomMetroidSolver/web/static/help/below_botwoon_etank.png ~/web2py/applications/solver/static/images/help/below_botwoon_etank.png
[ -L ~/web2py/applications/solver/static/images/help/west_sand_hall_tunnel.png ] || ln -s ~/RandomMetroidSolver/web/static/help/west_sand_hall_tunnel.png ~/web2py/applications/solver/static/images/help/west_sand_hall_tunnel.png
[ -L ~/web2py/applications/solver/static/images/help/west_sand_hall.png ] || ln -s ~/RandomMetroidSolver/web/static/help/west_sand_hall.png ~/web2py/applications/solver/static/images/help/west_sand_hall.png
[ -L ~/web2py/applications/solver/static/images/help/main_street_save.png ] || ln -s ~/RandomMetroidSolver/web/static/help/main_street_save.png ~/web2py/applications/solver/static/images/help/main_street_save.png
[ -L ~/web2py/applications/solver/static/images/help/crab_shaft_save.png ] || ln -s ~/RandomMetroidSolver/web/static/help/crab_shaft_save.png ~/web2py/applications/solver/static/images/help/crab_shaft_save.png
[ -L ~/web2py/applications/solver/static/images/help/objectives.png ] || ln -s ~/RandomMetroidSolver/web/static/help/objectives.png ~/web2py/applications/solver/static/images/help/objectives.png
[ -L ~/web2py/applications/solver/static/images/help/aqueduct_bomb_blocks.png ] || ln -s ~/RandomMetroidSolver/web/static/help/aqueduct_bomb_blocks.png ~/web2py/applications/solver/static/images/help/aqueduct_bomb_blocks.png
[ -L ~/web2py/applications/solver/static/images/help/map.png ] || ln -s ~/RandomMetroidSolver/web/static/help/map.png ~/web2py/applications/solver/static/images/help/map.png
[ -L ~/web2py/applications/solver/static/images/help/inventory.png ] || ln -s ~/RandomMetroidSolver/web/static/help/inventory.png ~/web2py/applications/solver/static/images/help/inventory.png
[ -L ~/web2py/applications/solver/static/images/help/reveal_map.png ] || ln -s ~/RandomMetroidSolver/web/static/help/reveal_map.png ~/web2py/applications/solver/static/images/help/reveal_map.png

# rando - maps
[ -L ~/web2py/applications/solver/static/images/help/minimizer_example.png ] || ln -s ~/RandomMetroidSolver/web/static/help/minimizer_example.png ~/web2py/applications/solver/static/images/help/minimizer_example.png
[ -L ~/web2py/applications/solver/static/images/help/minimizer_example_thumbnail.png ] || ln -s ~/RandomMetroidSolver/web/static/help/minimizer_example_thumbnail.png ~/web2py/applications/solver/static/images/help/minimizer_example_thumbnail.png
[ -L ~/web2py/applications/solver/static/images/help/chozo_map_thumbnail.png ] || ln -s ~/RandomMetroidSolver/web/static/help/chozo_map_thumbnail.png ~/web2py/applications/solver/static/images/help/chozo_map_thumbnail.png
[ -L ~/web2py/applications/solver/static/images/help/chozo_map.png ] || ln -s ~/RandomMetroidSolver/web/static/help/chozo_map.png ~/web2py/applications/solver/static/images/help/chozo_map.png

# rando - start locations
[ -L ~/web2py/applications/solver/static/images/help/gauntlet_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/gauntlet_start.png ~/web2py/applications/solver/static/images/help/gauntlet_start.png
[ -L ~/web2py/applications/solver/static/images/help/green_bt_elevator_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/green_bt_elevator_start.png ~/web2py/applications/solver/static/images/help/green_bt_elevator_start.png
[ -L ~/web2py/applications/solver/static/images/help/bt_reserve_blue_door1.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/bt_reserve_blue_door1.png ~/web2py/applications/solver/static/images/help/bt_reserve_blue_door1.png
[ -L ~/web2py/applications/solver/static/images/help/bt_reserve_blue_door2.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/bt_reserve_blue_door2.png ~/web2py/applications/solver/static/images/help/bt_reserve_blue_door2.png
[ -L ~/web2py/applications/solver/static/images/help/ceres_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/ceres_start.png ~/web2py/applications/solver/static/images/help/ceres_start.png
[ -L ~/web2py/applications/solver/static/images/help/landing_site_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/landing_site_start.png ~/web2py/applications/solver/static/images/help/landing_site_start.png
[ -L ~/web2py/applications/solver/static/images/help/blue_bt_blue_door.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/blue_bt_blue_door.png ~/web2py/applications/solver/static/images/help/blue_bt_blue_door.png
[ -L ~/web2py/applications/solver/static/images/help/watering_hole_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/watering_hole_start.png ~/web2py/applications/solver/static/images/help/watering_hole_start.png
[ -L ~/web2py/applications/solver/static/images/help/big_pink_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/big_pink_start.png ~/web2py/applications/solver/static/images/help/big_pink_start.png
[ -L ~/web2py/applications/solver/static/images/help/etecoons_supers_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/etecoons_supers_start.png ~/web2py/applications/solver/static/images/help/etecoons_supers_start.png
[ -L ~/web2py/applications/solver/static/images/help/etecoons_blue_door.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/etecoons_blue_door.png ~/web2py/applications/solver/static/images/help/etecoons_blue_door.png
[ -L ~/web2py/applications/solver/static/images/help/red_bt_elevator_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/red_bt_elevator_start.png ~/web2py/applications/solver/static/images/help/red_bt_elevator_start.png
[ -L ~/web2py/applications/solver/static/images/help/hellway_blue_door.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/hellway_blue_door.png ~/web2py/applications/solver/static/images/help/hellway_blue_door.png
[ -L ~/web2py/applications/solver/static/images/help/alpha_pb_blue_door.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/alpha_pb_blue_door.png ~/web2py/applications/solver/static/images/help/alpha_pb_blue_door.png
[ -L ~/web2py/applications/solver/static/images/help/business_center_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/business_center_start.png ~/web2py/applications/solver/static/images/help/business_center_start.png
[ -L ~/web2py/applications/solver/static/images/help/hijump_blue_door.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/hijump_blue_door.png ~/web2py/applications/solver/static/images/help/hijump_blue_door.png
[ -L ~/web2py/applications/solver/static/images/help/bubble_mountain_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/bubble_mountain_start.png ~/web2py/applications/solver/static/images/help/bubble_mountain_start.png
[ -L ~/web2py/applications/solver/static/images/help/speed_blue_door1.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/speed_blue_door1.png ~/web2py/applications/solver/static/images/help/speed_blue_door1.png
[ -L ~/web2py/applications/solver/static/images/help/speed_blue_door2.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/speed_blue_door2.png ~/web2py/applications/solver/static/images/help/speed_blue_door2.png
[ -L ~/web2py/applications/solver/static/images/help/wrecked_ship_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/wrecked_ship_start.png ~/web2py/applications/solver/static/images/help/wrecked_ship_start.png
[ -L ~/web2py/applications/solver/static/images/help/sponge_bath_blue_door.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/sponge_bath_blue_door.png ~/web2py/applications/solver/static/images/help/sponge_bath_blue_door.png
[ -L ~/web2py/applications/solver/static/images/help/maridia_tube_opened.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/maridia_tube_opened.png ~/web2py/applications/solver/static/images/help/maridia_tube_opened.png
[ -L ~/web2py/applications/solver/static/images/help/red_bt_blue_door.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/red_bt_blue_door.png ~/web2py/applications/solver/static/images/help/red_bt_blue_door.png
[ -L ~/web2py/applications/solver/static/images/help/aqueduct_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/aqueduct_start.png ~/web2py/applications/solver/static/images/help/aqueduct_start.png
[ -L ~/web2py/applications/solver/static/images/help/mama_turtle_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/mama_turtle_start.png ~/web2py/applications/solver/static/images/help/mama_turtle_start.png
[ -L ~/web2py/applications/solver/static/images/help/aqueduct_save_blue.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/aqueduct_save_blue.png ~/web2py/applications/solver/static/images/help/aqueduct_save_blue.png
[ -L ~/web2py/applications/solver/static/images/help/mama_turtle_blue_door.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/mama_turtle_blue_door.png ~/web2py/applications/solver/static/images/help/mama_turtle_blue_door.png
[ -L ~/web2py/applications/solver/static/images/help/firefleas_top_start.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/firefleas_top_start.png ~/web2py/applications/solver/static/images/help/firefleas_top_start.png
[ -L ~/web2py/applications/solver/static/images/help/fune_removed.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/fune_removed.png ~/web2py/applications/solver/static/images/help/fune_removed.png
[ -L ~/web2py/applications/solver/static/images/help/firefleas_shot_blocks.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/firefleas_shot_blocks.png ~/web2py/applications/solver/static/images/help/firefleas_shot_blocks.png
[ -L ~/web2py/applications/solver/static/images/help/gauntlet_position.png ] || ln -s ~/RandomMetroidSolver/web/static/start_locations/gauntlet_position.png ~/web2py/applications/solver/static/images/help/gauntlet_position.png

# customizer - help
mkdir -p ~/web2py/applications/solver/static/images/customizer/
[ -L ~/web2py/applications/solver/static/images/customizer/palettesRando.png ] || ln -s ~/RandomMetroidSolver/web/static/palettesRando.png ~/web2py/applications/solver/static/images/customizer/palettesRando.png
[ -L ~/web2py/applications/solver/static/images/customizer/samus_degrees.png ] || ln -s ~/RandomMetroidSolver/web/static/samus_degrees.png ~/web2py/applications/solver/static/images/customizer/samus_degrees.png

# plandorepo (stored in tracker inventory as images are reused)
mkdir -p ~/web2py/applications/solver/static/images/tracker/inventory/
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Varia.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Varia.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Varia.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Half_Varia.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Half_Varia.png ~/web2py/applications/solver/static/images/tracker/inventory/Half_Varia.png

# solver - samus running
mkdir -p ~/web2py/applications/solver/static/images/solver/
[ -L ~/web2py/applications/solver/static/images/solver/samus_run_Power.gif ] || ln -s ~/RandomMetroidSolver/web/static/solver/samus_run_Power.gif ~/web2py/applications/solver/static/images/solver/samus_run_Power.gif
[ -L ~/web2py/applications/solver/static/images/solver/samus_run_Varia.gif ] || ln -s ~/RandomMetroidSolver/web/static/solver/samus_run_Varia.gif ~/web2py/applications/solver/static/images/solver/samus_run_Varia.gif
[ -L ~/web2py/applications/solver/static/images/solver/samus_run_Gravity.gif ] || ln -s ~/RandomMetroidSolver/web/static/solver/samus_run_Gravity.gif ~/web2py/applications/solver/static/images/solver/samus_run_Gravity.gif

# solver - empty markers for difficulties
[ -L ~/web2py/applications/solver/static/images/solver/marker_easy.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_easy.png ~/web2py/applications/solver/static/images/solver/marker_easy.png
[ -L ~/web2py/applications/solver/static/images/solver/marker_medium.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_medium.png ~/web2py/applications/solver/static/images/solver/marker_medium.png
[ -L ~/web2py/applications/solver/static/images/solver/marker_hard.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_hard.png ~/web2py/applications/solver/static/images/solver/marker_hard.png
[ -L ~/web2py/applications/solver/static/images/solver/marker_harder.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_harder.png ~/web2py/applications/solver/static/images/solver/marker_harder.png
[ -L ~/web2py/applications/solver/static/images/solver/marker_hardcore.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_hardcore.png ~/web2py/applications/solver/static/images/solver/marker_hardcore.png
[ -L ~/web2py/applications/solver/static/images/solver/marker_mania.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_mania.png ~/web2py/applications/solver/static/images/solver/marker_mania.png

# solver - rooms
mkdir -p ~/web2py/applications/solver/static/images/rooms
[ -L ~/web2py/applications/solver/static/images/rooms/AlphaPowerBombRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/AlphaPowerBombRoom.png ~/web2py/applications/solver/static/images/rooms/AlphaPowerBombRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/Aqueduct.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/Aqueduct.png ~/web2py/applications/solver/static/images/rooms/Aqueduct.png
[ -L ~/web2py/applications/solver/static/images/rooms/BetaPowerBombRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BetaPowerBombRoom.png ~/web2py/applications/solver/static/images/rooms/BetaPowerBombRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/BigPink.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BigPink.png ~/web2py/applications/solver/static/images/rooms/BigPink.png
[ -L ~/web2py/applications/solver/static/images/rooms/BillyMaysRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BillyMaysRoom.png ~/web2py/applications/solver/static/images/rooms/BillyMaysRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/BlueBrinstarEnergyTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BlueBrinstarEnergyTankRoom.png ~/web2py/applications/solver/static/images/rooms/BlueBrinstarEnergyTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/BombTorizoRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BombTorizoRoom.png ~/web2py/applications/solver/static/images/rooms/BombTorizoRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/BotwoonEnergyTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BotwoonEnergyTankRoom.png ~/web2py/applications/solver/static/images/rooms/BotwoonEnergyTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/BowlingAlley.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BowlingAlley.png ~/web2py/applications/solver/static/images/rooms/BowlingAlley.png
[ -L ~/web2py/applications/solver/static/images/rooms/BrinstarReserveTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BrinstarReserveTankRoom.png ~/web2py/applications/solver/static/images/rooms/BrinstarReserveTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/BubbleMountain.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BubbleMountain.png ~/web2py/applications/solver/static/images/rooms/BubbleMountain.png
[ -L ~/web2py/applications/solver/static/images/rooms/Cathedral.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/Cathedral.png ~/web2py/applications/solver/static/images/rooms/Cathedral.png
[ -L ~/web2py/applications/solver/static/images/rooms/CrateriaPowerBombRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/CrateriaPowerBombRoom.png ~/web2py/applications/solver/static/images/rooms/CrateriaPowerBombRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/CrateriaSuperRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/CrateriaSuperRoom.png ~/web2py/applications/solver/static/images/rooms/CrateriaSuperRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/CrocomireEscape.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/CrocomireEscape.png ~/web2py/applications/solver/static/images/rooms/CrocomireEscape.png
[ -L ~/web2py/applications/solver/static/images/rooms/CrocomiresRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/CrocomiresRoom.png ~/web2py/applications/solver/static/images/rooms/CrocomiresRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/CrumbleShaft.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/CrumbleShaft.png ~/web2py/applications/solver/static/images/rooms/CrumbleShaft.png
[ -L ~/web2py/applications/solver/static/images/rooms/DoubleChamber.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/DoubleChamber.png ~/web2py/applications/solver/static/images/rooms/DoubleChamber.png
[ -L ~/web2py/applications/solver/static/images/rooms/DraygonsRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/DraygonsRoom.png ~/web2py/applications/solver/static/images/rooms/DraygonsRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/EarlySupersRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/EarlySupersRoom.png ~/web2py/applications/solver/static/images/rooms/EarlySupersRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/EastSandHole.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/EastSandHole.png ~/web2py/applications/solver/static/images/rooms/EastSandHole.png
[ -L ~/web2py/applications/solver/static/images/rooms/EtecoonEnergyTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/EtecoonEnergyTankRoom.png ~/web2py/applications/solver/static/images/rooms/EtecoonEnergyTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/EtecoonSuperRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/EtecoonSuperRoom.png ~/web2py/applications/solver/static/images/rooms/EtecoonSuperRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/FirstMissileRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/FirstMissileRoom.png ~/web2py/applications/solver/static/images/rooms/FirstMissileRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/GauntletEnergyTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/GauntletEnergyTankRoom.png ~/web2py/applications/solver/static/images/rooms/GauntletEnergyTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/GoldenTorizosRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/GoldenTorizosRoom.png ~/web2py/applications/solver/static/images/rooms/GoldenTorizosRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/GrappleBeamRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/GrappleBeamRoom.png ~/web2py/applications/solver/static/images/rooms/GrappleBeamRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/GravitySuitRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/GravitySuitRoom.png ~/web2py/applications/solver/static/images/rooms/GravitySuitRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/GreenBrinstarMainShaft.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/GreenBrinstarMainShaft.png ~/web2py/applications/solver/static/images/rooms/GreenBrinstarMainShaft.png
[ -L ~/web2py/applications/solver/static/images/rooms/GreenBubblesMissileRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/GreenBubblesMissileRoom.png ~/web2py/applications/solver/static/images/rooms/GreenBubblesMissileRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/GreenHillZone.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/GreenHillZone.png ~/web2py/applications/solver/static/images/rooms/GreenHillZone.png
[ -L ~/web2py/applications/solver/static/images/rooms/GreenPiratesShaft.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/GreenPiratesShaft.png ~/web2py/applications/solver/static/images/rooms/GreenPiratesShaft.png
[ -L ~/web2py/applications/solver/static/images/rooms/HiJumpBootsRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/HiJumpBootsRoom.png ~/web2py/applications/solver/static/images/rooms/HiJumpBootsRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/HiJumpEnergyTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/HiJumpEnergyTankRoom.png ~/web2py/applications/solver/static/images/rooms/HiJumpEnergyTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/HopperEnergyTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/HopperEnergyTankRoom.png ~/web2py/applications/solver/static/images/rooms/HopperEnergyTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/IceBeamRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/IceBeamRoom.png ~/web2py/applications/solver/static/images/rooms/IceBeamRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/KraidRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/KraidRoom.png ~/web2py/applications/solver/static/images/rooms/KraidRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/LowerNorfairEscapePowerBombRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/LowerNorfairEscapePowerBombRoom.png ~/web2py/applications/solver/static/images/rooms/LowerNorfairEscapePowerBombRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/LowerNorfairFirefleaRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/LowerNorfairFirefleaRoom.png ~/web2py/applications/solver/static/images/rooms/LowerNorfairFirefleaRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/LowerNorfairSpringBallMazeRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/LowerNorfairSpringBallMazeRoom.png ~/web2py/applications/solver/static/images/rooms/LowerNorfairSpringBallMazeRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/MainStreet.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/MainStreet.png ~/web2py/applications/solver/static/images/rooms/MainStreet.png
[ -L ~/web2py/applications/solver/static/images/rooms/MamaTurtleRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/MamaTurtleRoom.png ~/web2py/applications/solver/static/images/rooms/MamaTurtleRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/MickeyMouseRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/MickeyMouseRoom.png ~/web2py/applications/solver/static/images/rooms/MickeyMouseRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/MorphBallRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/MorphBallRoom.png ~/web2py/applications/solver/static/images/rooms/MorphBallRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/MotherBrainRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/MotherBrainRoom.png ~/web2py/applications/solver/static/images/rooms/MotherBrainRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/NorfairReserveTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/NorfairReserveTankRoom.png ~/web2py/applications/solver/static/images/rooms/NorfairReserveTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/PhantoonsRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/PhantoonsRoom.png ~/web2py/applications/solver/static/images/rooms/PhantoonsRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/PinkBrinstarPowerBombRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/PinkBrinstarPowerBombRoom.png ~/web2py/applications/solver/static/images/rooms/PinkBrinstarPowerBombRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/PitRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/PitRoom.png ~/web2py/applications/solver/static/images/rooms/PitRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/PlasmaRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/PlasmaRoom.png ~/web2py/applications/solver/static/images/rooms/PlasmaRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/PostCrocomireJumpRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/PostCrocomireJumpRoom.png ~/web2py/applications/solver/static/images/rooms/PostCrocomireJumpRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/PostCrocomireMissileRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/PostCrocomireMissileRoom.png ~/web2py/applications/solver/static/images/rooms/PostCrocomireMissileRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/PostCrocomirePowerBombRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/PostCrocomirePowerBombRoom.png ~/web2py/applications/solver/static/images/rooms/PostCrocomirePowerBombRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/PseudoPlasmaSparkRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/PseudoPlasmaSparkRoom.png ~/web2py/applications/solver/static/images/rooms/PseudoPlasmaSparkRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/RidleysRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/RidleysRoom.png ~/web2py/applications/solver/static/images/rooms/RidleysRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/RidleyTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/RidleyTankRoom.png ~/web2py/applications/solver/static/images/rooms/RidleyTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/ScrewAttackRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/ScrewAttackRoom.png ~/web2py/applications/solver/static/images/rooms/ScrewAttackRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/SpaceJumpRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/SpaceJumpRoom.png ~/web2py/applications/solver/static/images/rooms/SpaceJumpRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/SpazerRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/SpazerRoom.png ~/web2py/applications/solver/static/images/rooms/SpazerRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/SpeedBoosterHall.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/SpeedBoosterHall.png ~/web2py/applications/solver/static/images/rooms/SpeedBoosterHall.png
[ -L ~/web2py/applications/solver/static/images/rooms/SpeedBoosterRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/SpeedBoosterRoom.png ~/web2py/applications/solver/static/images/rooms/SpeedBoosterRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/SporeSpawnSuperRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/SporeSpawnSuperRoom.png ~/web2py/applications/solver/static/images/rooms/SporeSpawnSuperRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/SpringBallRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/SpringBallRoom.png ~/web2py/applications/solver/static/images/rooms/SpringBallRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/TerminatorRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/TerminatorRoom.png ~/web2py/applications/solver/static/images/rooms/TerminatorRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/TheFinalMissile.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/TheFinalMissile.png ~/web2py/applications/solver/static/images/rooms/TheFinalMissile.png
[ -L ~/web2py/applications/solver/static/images/rooms/TheMoat.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/TheMoat.png ~/web2py/applications/solver/static/images/rooms/TheMoat.png
[ -L ~/web2py/applications/solver/static/images/rooms/ThePreciousRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/ThePreciousRoom.png ~/web2py/applications/solver/static/images/rooms/ThePreciousRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/ThreeMuskateersRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/ThreeMuskateersRoom.png ~/web2py/applications/solver/static/images/rooms/ThreeMuskateersRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/VariaSuitRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/VariaSuitRoom.png ~/web2py/applications/solver/static/images/rooms/VariaSuitRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/WarehouseEnergyTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WarehouseEnergyTankRoom.png ~/web2py/applications/solver/static/images/rooms/WarehouseEnergyTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/WarehouseKeyhunterRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WarehouseKeyhunterRoom.png ~/web2py/applications/solver/static/images/rooms/WarehouseKeyhunterRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/Wasteland.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/Wasteland.png ~/web2py/applications/solver/static/images/rooms/Wasteland.png
[ -L ~/web2py/applications/solver/static/images/rooms/WateringHole.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WateringHole.png ~/web2py/applications/solver/static/images/rooms/WateringHole.png
[ -L ~/web2py/applications/solver/static/images/rooms/WaterwayEnergyTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WaterwayEnergyTankRoom.png ~/web2py/applications/solver/static/images/rooms/WaterwayEnergyTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/WaveBeamRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WaveBeamRoom.png ~/web2py/applications/solver/static/images/rooms/WaveBeamRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/WestOcean.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WestOcean.png ~/web2py/applications/solver/static/images/rooms/WestOcean.png
[ -L ~/web2py/applications/solver/static/images/rooms/WestSandHole.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WestSandHole.png ~/web2py/applications/solver/static/images/rooms/WestSandHole.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShipEastMissileRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShipEastMissileRoom.png ~/web2py/applications/solver/static/images/rooms/WreckedShipEastMissileRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShipEastSuperRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShipEastSuperRoom.png ~/web2py/applications/solver/static/images/rooms/WreckedShipEastSuperRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShipEnergyTankRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShipEnergyTankRoom.png ~/web2py/applications/solver/static/images/rooms/WreckedShipEnergyTankRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShipMainShaft.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShipMainShaft.png ~/web2py/applications/solver/static/images/rooms/WreckedShipMainShaft.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShipWestSuperRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShipWestSuperRoom.png ~/web2py/applications/solver/static/images/rooms/WreckedShipWestSuperRoom.png
[ -L ~/web2py/applications/solver/static/images/rooms/XRayScopeRoom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/XRayScopeRoom.png ~/web2py/applications/solver/static/images/rooms/XRayScopeRoom.png

[ -L ~/web2py/applications/solver/static/images/rooms/Brinstar.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/Brinstar.png ~/web2py/applications/solver/static/images/rooms/Brinstar.png
[ -L ~/web2py/applications/solver/static/images/rooms/Crateria.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/Crateria.png ~/web2py/applications/solver/static/images/rooms/Crateria.png
[ -L ~/web2py/applications/solver/static/images/rooms/Maridia.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/Maridia.png ~/web2py/applications/solver/static/images/rooms/Maridia.png
[ -L ~/web2py/applications/solver/static/images/rooms/Tourian.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/Tourian.png ~/web2py/applications/solver/static/images/rooms/Tourian.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShip.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShip.png ~/web2py/applications/solver/static/images/rooms/WreckedShip.png
[ -L ~/web2py/applications/solver/static/images/rooms/Norfair.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/Norfair.png ~/web2py/applications/solver/static/images/rooms/Norfair.png
[ -L ~/web2py/applications/solver/static/images/rooms/LowerNorfair.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/Norfair.png ~/web2py/applications/solver/static/images/rooms/LowerNorfair.png

[ -L ~/web2py/applications/solver/static/images/rooms/BlueBrinstar.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BlueBrinstar.png ~/web2py/applications/solver/static/images/rooms/BlueBrinstar.png
[ -L ~/web2py/applications/solver/static/images/rooms/CrateriaBombs.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/CrateriaBombs.png ~/web2py/applications/solver/static/images/rooms/CrateriaBombs.png
[ -L ~/web2py/applications/solver/static/images/rooms/CrateriaLandingSite.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/CrateriaLandingSite.png ~/web2py/applications/solver/static/images/rooms/CrateriaLandingSite.png
[ -L ~/web2py/applications/solver/static/images/rooms/CrateriaTerminator.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/CrateriaTerminator.png ~/web2py/applications/solver/static/images/rooms/CrateriaTerminator.png
[ -L ~/web2py/applications/solver/static/images/rooms/BrinstarHills.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BrinstarHills.png ~/web2py/applications/solver/static/images/rooms/BrinstarHills.png
[ -L ~/web2py/applications/solver/static/images/rooms/BubbleNorfairBottom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BubbleNorfairBottom.png ~/web2py/applications/solver/static/images/rooms/BubbleNorfairBottom.png
[ -L ~/web2py/applications/solver/static/images/rooms/BubbleNorfairReserve.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BubbleNorfairReserve.png ~/web2py/applications/solver/static/images/rooms/BubbleNorfairReserve.png
[ -L ~/web2py/applications/solver/static/images/rooms/BubbleNorfairSpeed.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BubbleNorfairSpeed.png ~/web2py/applications/solver/static/images/rooms/BubbleNorfairSpeed.png
[ -L ~/web2py/applications/solver/static/images/rooms/BubbleNorfairWave.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/BubbleNorfairWave.png ~/web2py/applications/solver/static/images/rooms/BubbleNorfairWave.png
[ -L ~/web2py/applications/solver/static/images/rooms/CrateriaGauntlet.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/CrateriaGauntlet.png ~/web2py/applications/solver/static/images/rooms/CrateriaGauntlet.png
[ -L ~/web2py/applications/solver/static/images/rooms/Crocomire.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/Crocomire.png ~/web2py/applications/solver/static/images/rooms/Crocomire.png
[ -L ~/web2py/applications/solver/static/images/rooms/GreenBrinstar.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/GreenBrinstar.png ~/web2py/applications/solver/static/images/rooms/GreenBrinstar.png
[ -L ~/web2py/applications/solver/static/images/rooms/GreenBrinstarReserve.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/GreenBrinstarReserve.png ~/web2py/applications/solver/static/images/rooms/GreenBrinstarReserve.png
[ -L ~/web2py/applications/solver/static/images/rooms/KraidSubArea.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/KraidSubArea.png ~/web2py/applications/solver/static/images/rooms/KraidSubArea.png
[ -L ~/web2py/applications/solver/static/images/rooms/LowerNorfairAfterAmphitheater.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/LowerNorfairAfterAmphitheater.png ~/web2py/applications/solver/static/images/rooms/LowerNorfairAfterAmphitheater.png
[ -L ~/web2py/applications/solver/static/images/rooms/LowerNorfairBeforeAmphitheater.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/LowerNorfairBeforeAmphitheater.png ~/web2py/applications/solver/static/images/rooms/LowerNorfairBeforeAmphitheater.png
[ -L ~/web2py/applications/solver/static/images/rooms/LowerNorfairScrewAttack.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/LowerNorfairScrewAttack.png ~/web2py/applications/solver/static/images/rooms/LowerNorfairScrewAttack.png
[ -L ~/web2py/applications/solver/static/images/rooms/LowerNorfairWasteland.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/LowerNorfairWasteland.png ~/web2py/applications/solver/static/images/rooms/LowerNorfairWasteland.png
[ -L ~/web2py/applications/solver/static/images/rooms/MaridiaForgottenHighway.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/MaridiaForgottenHighway.png ~/web2py/applications/solver/static/images/rooms/MaridiaForgottenHighway.png
[ -L ~/web2py/applications/solver/static/images/rooms/MaridiaGreen.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/MaridiaGreen.png ~/web2py/applications/solver/static/images/rooms/MaridiaGreen.png
[ -L ~/web2py/applications/solver/static/images/rooms/MaridiaPinkBottom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/MaridiaPinkBottom.png ~/web2py/applications/solver/static/images/rooms/MaridiaPinkBottom.png
[ -L ~/web2py/applications/solver/static/images/rooms/MaridiaPinkTop.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/MaridiaPinkTop.png ~/web2py/applications/solver/static/images/rooms/MaridiaPinkTop.png
[ -L ~/web2py/applications/solver/static/images/rooms/MaridiaSandpits.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/MaridiaSandpits.png ~/web2py/applications/solver/static/images/rooms/MaridiaSandpits.png
[ -L ~/web2py/applications/solver/static/images/rooms/NorfairEntrance.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/NorfairEntrance.png ~/web2py/applications/solver/static/images/rooms/NorfairEntrance.png
[ -L ~/web2py/applications/solver/static/images/rooms/NorfairCathedral.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/NorfairCathedral.png ~/web2py/applications/solver/static/images/rooms/NorfairCathedral.png
[ -L ~/web2py/applications/solver/static/images/rooms/NorfairGrappleEscape.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/NorfairGrappleEscape.png ~/web2py/applications/solver/static/images/rooms/NorfairGrappleEscape.png
[ -L ~/web2py/applications/solver/static/images/rooms/NorfairIce.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/NorfairIce.png ~/web2py/applications/solver/static/images/rooms/NorfairIce.png
[ -L ~/web2py/applications/solver/static/images/rooms/PinkBrinstar.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/PinkBrinstar.png ~/web2py/applications/solver/static/images/rooms/PinkBrinstar.png
[ -L ~/web2py/applications/solver/static/images/rooms/RedBrinstar.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/RedBrinstar.png ~/web2py/applications/solver/static/images/rooms/RedBrinstar.png
[ -L ~/web2py/applications/solver/static/images/rooms/RedBrinstarTop.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/RedBrinstarTop.png ~/web2py/applications/solver/static/images/rooms/RedBrinstarTop.png
[ -L ~/web2py/applications/solver/static/images/rooms/TourianSubArea.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/TourianSubArea.png ~/web2py/applications/solver/static/images/rooms/TourianSubArea.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShip.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShip.png ~/web2py/applications/solver/static/images/rooms/WreckedShip.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShipBack.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShipBack.png ~/web2py/applications/solver/static/images/rooms/WreckedShipBack.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShipBottom.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShipBottom.png ~/web2py/applications/solver/static/images/rooms/WreckedShipBottom.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShipGravity.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShipGravity.png ~/web2py/applications/solver/static/images/rooms/WreckedShipGravity.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShipMain.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShipMain.png ~/web2py/applications/solver/static/images/rooms/WreckedShipMain.png
[ -L ~/web2py/applications/solver/static/images/rooms/WreckedShipTop.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/WreckedShipTop.png ~/web2py/applications/solver/static/images/rooms/WreckedShipTop.png
[ -L ~/web2py/applications/solver/static/images/rooms/LeftSandpit.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/LeftSandpit.png ~/web2py/applications/solver/static/images/rooms/LeftSandpit.png
[ -L ~/web2py/applications/solver/static/images/rooms/RightSandpit.png ] || ln -s ~/RandomMetroidSolver/web/static/rooms/RightSandpit.png ~/web2py/applications/solver/static/images/rooms/RightSandpit.png

# ui buttons
mkdir -p ~/web2py/applications/solver/static/images/ui/
[ -L ~/web2py/applications/solver/static/images/ui/bin.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/bin.svg ~/web2py/applications/solver/static/images/ui/bin.svg
[ -L ~/web2py/applications/solver/static/images/ui/checkmark.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/checkmark.svg ~/web2py/applications/solver/static/images/ui/checkmark.svg
[ -L ~/web2py/applications/solver/static/images/ui/refresh.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/refresh.svg ~/web2py/applications/solver/static/images/ui/refresh.svg
[ -L ~/web2py/applications/solver/static/images/ui/cloud_download.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/cloud_download.svg ~/web2py/applications/solver/static/images/ui/cloud_download.svg
[ -L ~/web2py/applications/solver/static/images/ui/cloud_upload.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/cloud_upload.png ~/web2py/applications/solver/static/images/ui/cloud_upload.png
[ -L ~/web2py/applications/solver/static/images/ui/help.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/help.svg ~/web2py/applications/solver/static/images/ui/help.svg
[ -L ~/web2py/applications/solver/static/images/ui/repeat.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/repeat.svg ~/web2py/applications/solver/static/images/ui/repeat.svg
[ -L ~/web2py/applications/solver/static/images/ui/warning.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/warning.svg ~/web2py/applications/solver/static/images/ui/warning.svg
[ -L ~/web2py/applications/solver/static/images/ui/play.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/play.svg ~/web2py/applications/solver/static/images/ui/play.svg
[ -L ~/web2py/applications/solver/static/images/ui/save.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/save.svg ~/web2py/applications/solver/static/images/ui/save.svg
[ -L ~/web2py/applications/solver/static/images/ui/locked.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/locked.svg ~/web2py/applications/solver/static/images/ui/locked.svg
[ -L ~/web2py/applications/solver/static/images/ui/fast_forward.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/fast_forward.svg ~/web2py/applications/solver/static/images/ui/fast_forward.svg
[ -L ~/web2py/applications/solver/static/images/ui/right_arrow.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/right_arrow.svg ~/web2py/applications/solver/static/images/ui/right_arrow.svg
[ -L ~/web2py/applications/solver/static/images/ui/games.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/games.svg ~/web2py/applications/solver/static/images/ui/games.svg
[ -L ~/web2py/applications/solver/static/images/ui/skip_forward.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/skip_forward.svg ~/web2py/applications/solver/static/images/ui/skip_forward.svg
[ -L ~/web2py/applications/solver/static/images/ui/link.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/link.svg ~/web2py/applications/solver/static/images/ui/link.svg
[ -L ~/web2py/applications/solver/static/images/ui/record.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/record.svg ~/web2py/applications/solver/static/images/ui/record.svg
[ -L ~/web2py/applications/solver/static/images/ui/record_ko.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/record_ko.svg ~/web2py/applications/solver/static/images/ui/record_ko.svg
[ -L ~/web2py/applications/solver/static/images/ui/record_load.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/record_load.svg ~/web2py/applications/solver/static/images/ui/record_load.svg
[ -L ~/web2py/applications/solver/static/images/ui/record_ok.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/record_ok.svg ~/web2py/applications/solver/static/images/ui/record_ok.svg
[ -L ~/web2py/applications/solver/static/images/ui/shut_down.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/shut_down.svg ~/web2py/applications/solver/static/images/ui/shut_down.svg
[ -L ~/web2py/applications/solver/static/images/ui/television.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/television.svg ~/web2py/applications/solver/static/images/ui/television.svg
[ -L ~/web2py/applications/solver/static/images/ui/puzzle.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/puzzle.svg ~/web2py/applications/solver/static/images/ui/puzzle.svg

# tracker - help
mkdir -p ~/web2py/applications/solver/static/images/tracker/help/
[ -L ~/web2py/applications/solver/static/images/tracker/help/portal.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/portal.png ~/web2py/applications/solver/static/images/tracker/help/portal.png
[ -L ~/web2py/applications/solver/static/images/tracker/help/portal_boss.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/portal_boss.png ~/web2py/applications/solver/static/images/tracker/help/portal_boss.png
[ -L ~/web2py/applications/solver/static/images/tracker/help/portal_escape.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/portal_escape.png ~/web2py/applications/solver/static/images/tracker/help/portal_escape.png
[ -L ~/web2py/applications/solver/static/images/tracker/help/portal_maridia.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/portal_maridia.png ~/web2py/applications/solver/static/images/tracker/help/portal_maridia.png
[ -L ~/web2py/applications/solver/static/images/tracker/help/portal_maridia_vanilla.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/portal_maridia_vanilla.png ~/web2py/applications/solver/static/images/tracker/help/portal_maridia_vanilla.png
[ -L ~/web2py/applications/solver/static/images/tracker/help/portal_maridia_area.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/portal_maridia_area.png ~/web2py/applications/solver/static/images/tracker/help/portal_maridia_area.png

# tracker - markers
mkdir -p ~/web2py/applications/solver/static/images/tracker/markers/
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_easy.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_easy.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_easy.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_medium.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_medium.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_medium.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_hard.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_hard.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_hard.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_harder.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_harder.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_harder.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_hardcore.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_hardcore.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_hardcore.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_mania.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_mania.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_mania.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_easy_major.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_easy_major.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_easy_major.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_medium_major.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_medium_major.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_medium_major.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_hard_major.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_hard_major.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_hard_major.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_harder_major.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_harder_major.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_harder_major.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_hardcore_major.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_hardcore_major.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_hardcore_major.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_mania_major.gif ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_mania_major.gif ~/web2py/applications/solver/static/images/tracker/markers/marker_mania_major.gif
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_over_easy.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_over_easy.png ~/web2py/applications/solver/static/images/tracker/markers/marker_over_easy.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_over_medium.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_over_medium.png ~/web2py/applications/solver/static/images/tracker/markers/marker_over_medium.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_over_hard.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_over_hard.png ~/web2py/applications/solver/static/images/tracker/markers/marker_over_hard.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_over_harder.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_over_harder.png ~/web2py/applications/solver/static/images/tracker/markers/marker_over_harder.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_over_hardcore.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_over_hardcore.png ~/web2py/applications/solver/static/images/tracker/markers/marker_over_hardcore.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_over_mania.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_over_mania.png ~/web2py/applications/solver/static/images/tracker/markers/marker_over_mania.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_easy.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_visited_easy.png ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_easy.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_medium.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_visited_medium.png ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_medium.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_hard.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_visited_hard.png ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_hard.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_harder.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_visited_harder.png ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_harder.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_hardcore.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_visited_hardcore.png ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_hardcore.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_mania.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_visited_mania.png ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_mania.png

[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_break.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_break.png ~/web2py/applications/solver/static/images/tracker/markers/marker_break.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_break_major.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_break_major.png ~/web2py/applications/solver/static/images/tracker/markers/marker_break_major.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_over_break.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_over_break.png ~/web2py/applications/solver/static/images/tracker/markers/marker_over_break.png
[ -L ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_break.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/marker_visited_break.png ~/web2py/applications/solver/static/images/tracker/markers/marker_visited_break.png

# tracker - G4 in the middle
mkdir -p ~/web2py/applications/solver/static/images/tracker/G4/
[ -L ~/web2py/applications/solver/static/images/tracker/G4/draygon.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/draygon.png ~/web2py/applications/solver/static/images/tracker/G4/draygon.png
[ -L ~/web2py/applications/solver/static/images/tracker/G4/golden_four.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/golden_four.png ~/web2py/applications/solver/static/images/tracker/G4/golden_four.png
[ -L ~/web2py/applications/solver/static/images/tracker/G4/kraid.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/kraid.png ~/web2py/applications/solver/static/images/tracker/G4/kraid.png
[ -L ~/web2py/applications/solver/static/images/tracker/G4/phantoon.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/phantoon.png ~/web2py/applications/solver/static/images/tracker/G4/phantoon.png
[ -L ~/web2py/applications/solver/static/images/tracker/G4/ridley.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/ridley.png ~/web2py/applications/solver/static/images/tracker/G4/ridley.png

# tracker - inventory
mkdir -p ~/web2py/applications/solver/static/images/tracker/inventory/
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/background.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/background.png ~/web2py/applications/solver/static/images/tracker/inventory/background.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/background_seedless.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/background_seedless.png ~/web2py/applications/solver/static/images/tracker/inventory/background_seedless.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/background_streaming.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/background_streaming.png ~/web2py/applications/solver/static/images/tracker/inventory/background_streaming.png

[ -L ~/web2py/applications/solver/static/images/tracker/inventory/0.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/numbers/0.png ~/web2py/applications/solver/static/images/tracker/inventory/0.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/1.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/numbers/1.png ~/web2py/applications/solver/static/images/tracker/inventory/1.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/2.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/numbers/2.png ~/web2py/applications/solver/static/images/tracker/inventory/2.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/3.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/numbers/3.png ~/web2py/applications/solver/static/images/tracker/inventory/3.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/4.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/numbers/4.png ~/web2py/applications/solver/static/images/tracker/inventory/4.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/5.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/numbers/5.png ~/web2py/applications/solver/static/images/tracker/inventory/5.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/6.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/numbers/6.png ~/web2py/applications/solver/static/images/tracker/inventory/6.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/7.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/numbers/7.png ~/web2py/applications/solver/static/images/tracker/inventory/7.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/8.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/numbers/8.png ~/web2py/applications/solver/static/images/tracker/inventory/8.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/9.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/numbers/9.png ~/web2py/applications/solver/static/images/tracker/inventory/9.png

[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ibomb.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/ibomb.png ~/web2py/applications/solver/static/images/tracker/inventory/ibomb.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/icharge.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/icharge.png ~/web2py/applications/solver/static/images/tracker/inventory/icharge.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/igravity.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/igravity.png ~/web2py/applications/solver/static/images/tracker/inventory/igravity.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ihijump.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/ihijump.png ~/web2py/applications/solver/static/images/tracker/inventory/ihijump.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/iice.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/iice.png ~/web2py/applications/solver/static/images/tracker/inventory/iice.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/imorph.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/imorph.png ~/web2py/applications/solver/static/images/tracker/inventory/imorph.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/iplasma.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/iplasma.png ~/web2py/applications/solver/static/images/tracker/inventory/iplasma.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/iscrewattack.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/iscrewattack.png ~/web2py/applications/solver/static/images/tracker/inventory/iscrewattack.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ispacejump.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/ispacejump.png ~/web2py/applications/solver/static/images/tracker/inventory/ispacejump.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ispazer.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/ispazer.png ~/web2py/applications/solver/static/images/tracker/inventory/ispazer.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ispeedbooster.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/ispeedbooster.png ~/web2py/applications/solver/static/images/tracker/inventory/ispeedbooster.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ispringball.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/ispringball.png ~/web2py/applications/solver/static/images/tracker/inventory/ispringball.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ivaria.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/ivaria.png ~/web2py/applications/solver/static/images/tracker/inventory/ivaria.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/iwave.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/iwave.png ~/web2py/applications/solver/static/images/tracker/inventory/iwave.png

[ -L ~/web2py/applications/solver/static/images/tracker/inventory/igrapple.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/igrapple.png ~/web2py/applications/solver/static/images/tracker/inventory/igrapple.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/imissile.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/imissile.png ~/web2py/applications/solver/static/images/tracker/inventory/imissile.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ipowerbomb.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/ipowerbomb.png ~/web2py/applications/solver/static/images/tracker/inventory/ipowerbomb.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/isuper.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/isuper.png ~/web2py/applications/solver/static/images/tracker/inventory/isuper.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ixray.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/ixray.png ~/web2py/applications/solver/static/images/tracker/inventory/ixray.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/energy.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/energy.png ~/web2py/applications/solver/static/images/tracker/inventory/energy.png

[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ietank.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/ietank.png ~/web2py/applications/solver/static/images/tracker/inventory/ietank.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ireserve.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/ireserve.png ~/web2py/applications/solver/static/images/tracker/inventory/ireserve.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/auto.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/auto.png ~/web2py/applications/solver/static/images/tracker/inventory/auto.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/reserve_text.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/reserve_text.png ~/web2py/applications/solver/static/images/tracker/inventory/reserve_text.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/0_reserve.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/0_reserve.png ~/web2py/applications/solver/static/images/tracker/inventory/0_reserve.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/1_reserve.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/1_reserve.png ~/web2py/applications/solver/static/images/tracker/inventory/1_reserve.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/2_reserve.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/2_reserve.png ~/web2py/applications/solver/static/images/tracker/inventory/2_reserve.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/3_reserve.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/3_reserve.png ~/web2py/applications/solver/static/images/tracker/inventory/3_reserve.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/4_reserve.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/pause/4_reserve.png ~/web2py/applications/solver/static/images/tracker/inventory/4_reserve.png

# tracker - inventory streaming
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Gravity.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Gravity.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Gravity.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_HiJump.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_HiJump.png ~/web2py/applications/solver/static/images/tracker/inventory/No_HiJump.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Grapple.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Grapple.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Grapple.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_SpringBall.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_SpringBall.png ~/web2py/applications/solver/static/images/tracker/inventory/No_SpringBall.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_SpeedBooster.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_SpeedBooster.png ~/web2py/applications/solver/static/images/tracker/inventory/No_SpeedBooster.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Bomb.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Bomb.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Bomb.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_SpaceJump.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_SpaceJump.png ~/web2py/applications/solver/static/images/tracker/inventory/No_SpaceJump.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Plasma.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Plasma.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Plasma.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_ScrewAttack.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_ScrewAttack.png ~/web2py/applications/solver/static/images/tracker/inventory/No_ScrewAttack.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Spazer.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Spazer.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Spazer.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Wave.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Wave.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Wave.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Varia.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Varia.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Varia.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Charge.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Charge.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Charge.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_ETank.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_ETank.png ~/web2py/applications/solver/static/images/tracker/inventory/No_ETank.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Ice.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Ice.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Ice.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Missile.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Missile.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Missile.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Morph.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Morph.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Morph.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_PowerBomb.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_PowerBomb.png ~/web2py/applications/solver/static/images/tracker/inventory/No_PowerBomb.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Reserve.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Reserve.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Reserve.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_Super.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_Super.png ~/web2py/applications/solver/static/images/tracker/inventory/No_Super.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_XRayScope.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/No_XRayScope.png ~/web2py/applications/solver/static/images/tracker/inventory/No_XRayScope.png

[ -L ~/web2py/applications/solver/static/images/tracker/inventory/draygon_head.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/draygon_head.png ~/web2py/applications/solver/static/images/tracker/inventory/draygon_head.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/kraid_head.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/kraid_head.png ~/web2py/applications/solver/static/images/tracker/inventory/kraid_head.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_draygon_head.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/No_draygon_head.png ~/web2py/applications/solver/static/images/tracker/inventory/No_draygon_head.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_kraid_head.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/No_kraid_head.png ~/web2py/applications/solver/static/images/tracker/inventory/No_kraid_head.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_phantoon_head.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/No_phantoon_head.png ~/web2py/applications/solver/static/images/tracker/inventory/No_phantoon_head.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/No_ridley_head.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/No_ridley_head.png ~/web2py/applications/solver/static/images/tracker/inventory/No_ridley_head.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/phantoon_head.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/phantoon_head.png ~/web2py/applications/solver/static/images/tracker/inventory/phantoon_head.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ridley_head.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/tracker/G4/ridley_head.png ~/web2py/applications/solver/static/images/tracker/inventory/ridley_head.png

# items displayed in tracker and solver (stored in tracker inventory as images are reused)
mkdir -p ~/web2py/applications/solver/static/images/tracker/inventory/
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/HiJump.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/HiJump.png ~/web2py/applications/solver/static/images/tracker/inventory/HiJump.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Grapple.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Grapple.png ~/web2py/applications/solver/static/images/tracker/inventory/Grapple.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/SpringBall.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/SpringBall.png ~/web2py/applications/solver/static/images/tracker/inventory/SpringBall.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/SpeedBooster.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/SpeedBooster.png ~/web2py/applications/solver/static/images/tracker/inventory/SpeedBooster.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Bomb.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Bomb.png ~/web2py/applications/solver/static/images/tracker/inventory/Bomb.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/SpaceJump.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/SpaceJump.png ~/web2py/applications/solver/static/images/tracker/inventory/SpaceJump.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Plasma.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Plasma.png ~/web2py/applications/solver/static/images/tracker/inventory/Plasma.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ScrewAttack.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/ScrewAttack.png ~/web2py/applications/solver/static/images/tracker/inventory/ScrewAttack.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Spazer.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Spazer.png ~/web2py/applications/solver/static/images/tracker/inventory/Spazer.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Wave.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Wave.png ~/web2py/applications/solver/static/images/tracker/inventory/Wave.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Varia.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Varia.png ~/web2py/applications/solver/static/images/tracker/inventory/Varia.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Gravity.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Gravity.png ~/web2py/applications/solver/static/images/tracker/inventory/Gravity.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Charge.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Charge.png ~/web2py/applications/solver/static/images/tracker/inventory/Charge.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/ETank.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/ETank.png ~/web2py/applications/solver/static/images/tracker/inventory/ETank.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Ice.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Ice.png ~/web2py/applications/solver/static/images/tracker/inventory/Ice.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Missile.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Missile.png ~/web2py/applications/solver/static/images/tracker/inventory/Missile.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Morph.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Morph.png ~/web2py/applications/solver/static/images/tracker/inventory/Morph.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/PowerBomb.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/PowerBomb.png ~/web2py/applications/solver/static/images/tracker/inventory/PowerBomb.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Reserve.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Reserve.png ~/web2py/applications/solver/static/images/tracker/inventory/Reserve.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Super.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Super.png ~/web2py/applications/solver/static/images/tracker/inventory/Super.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/XRayScope.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/XRayScope.png ~/web2py/applications/solver/static/images/tracker/inventory/XRayScope.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Nothing.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Nothing.png ~/web2py/applications/solver/static/images/tracker/inventory/Nothing.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/CrystalFlash.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/CrystalFlash.png ~/web2py/applications/solver/static/images/tracker/inventory/CrystalFlash.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Gunship.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Gunship.png ~/web2py/applications/solver/static/images/tracker/inventory/Gunship.png

[ -L ~/web2py/applications/solver/static/images/tracker/inventory/SporeSpawn.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/SporeSpawn.png ~/web2py/applications/solver/static/images/tracker/inventory/SporeSpawn.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Crocomire.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Crocomire.png ~/web2py/applications/solver/static/images/tracker/inventory/Crocomire.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Botwoon.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/Botwoon.png ~/web2py/applications/solver/static/images/tracker/inventory/Botwoon.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/GoldenTorizo.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/items/GoldenTorizo.png ~/web2py/applications/solver/static/images/tracker/inventory/GoldenTorizo.png

[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Draygon.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/bosses/Draygon.png ~/web2py/applications/solver/static/images/tracker/inventory/Draygon.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Kraid.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/bosses/Kraid.png ~/web2py/applications/solver/static/images/tracker/inventory/Kraid.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Phantoon.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/bosses/Phantoon.png ~/web2py/applications/solver/static/images/tracker/inventory/Phantoon.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/Ridley.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/bosses/Ridley.png ~/web2py/applications/solver/static/images/tracker/inventory/Ridley.png
[ -L ~/web2py/applications/solver/static/images/tracker/inventory/MotherBrain.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/bosses/MotherBrain.png ~/web2py/applications/solver/static/images/tracker/inventory/MotherBrain.png

# tracker - doors
mkdir -p ~/web2py/applications/solver/static/images/tracker/doors/
[ -L ~/web2py/applications/solver/static/images/tracker/doors/blue_door.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/blue_door.svg ~/web2py/applications/solver/static/images/tracker/doors/blue_door.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/red_door.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/red_door.svg ~/web2py/applications/solver/static/images/tracker/doors/red_door.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/yellow_door.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/yellow_door.svg ~/web2py/applications/solver/static/images/tracker/doors/yellow_door.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/green_door.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/green_door.svg ~/web2py/applications/solver/static/images/tracker/doors/green_door.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/white_door.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/white_door.svg ~/web2py/applications/solver/static/images/tracker/doors/white_door.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/grey_door.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/grey_door.svg ~/web2py/applications/solver/static/images/tracker/doors/grey_door.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/wave_door_left.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/wave_door_left.svg ~/web2py/applications/solver/static/images/tracker/doors/wave_door_left.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/wave_door_right.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/wave_door_right.svg ~/web2py/applications/solver/static/images/tracker/doors/wave_door_right.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/ice_door.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/ice_door.svg ~/web2py/applications/solver/static/images/tracker/doors/ice_door.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/spazer_door.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/spazer_door.svg ~/web2py/applications/solver/static/images/tracker/doors/spazer_door.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/plasma_door_left.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/plasma_door_left.svg ~/web2py/applications/solver/static/images/tracker/doors/plasma_door_left.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/plasma_door_right.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/plasma_door_right.svg ~/web2py/applications/solver/static/images/tracker/doors/plasma_door_right.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/plasma_door_right.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/plasma_door_right.svg ~/web2py/applications/solver/static/images/tracker/doors/plasma_door_right.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/plasma_door_bottom.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/plasma_door_bottom.svg ~/web2py/applications/solver/static/images/tracker/doors/plasma_door_bottom.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/wave_door_bottom.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/wave_door_bottom.svg ~/web2py/applications/solver/static/images/tracker/doors/wave_door_bottom.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/ice_door_bottom.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/ice_door_bottom.svg ~/web2py/applications/solver/static/images/tracker/doors/ice_door_bottom.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/spazer_door_bottom.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/spazer_door_bottom.svg ~/web2py/applications/solver/static/images/tracker/doors/spazer_door_bottom.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/green_door_bottom.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/green_door_bottom.svg ~/web2py/applications/solver/static/images/tracker/doors/green_door_bottom.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/red_door_bottom.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/red_door_bottom.svg ~/web2py/applications/solver/static/images/tracker/doors/red_door_bottom.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/yellow_door_bottom.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/yellow_door_bottom.svg ~/web2py/applications/solver/static/images/tracker/doors/yellow_door_bottom.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/white_door_bottom.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/white_door_bottom.svg ~/web2py/applications/solver/static/images/tracker/doors/white_door_bottom.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/grey_door_bottom.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/grey_door_bottom.svg ~/web2py/applications/solver/static/images/tracker/doors/grey_door_bottom.svg
[ -L ~/web2py/applications/solver/static/images/tracker/doors/blue_door_bottom.svg ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/doors/blue_door_bottom.svg ~/web2py/applications/solver/static/images/tracker/doors/blue_door_bottom.svg

# tracker - auto tracker
mkdir -p ~/web2py/applications/solver/static/images/tracker/
[ -L ~/web2py/applications/solver/static/images/tracker/samusIcon.png ] || ln -s ~/RandomMetroidSolver/web/static/tracker_sprites/samusIcon.png ~/web2py/applications/solver/static/images/tracker/samusIcon.png

# client files (tracker js+css+images
[ -L ~/web2py/applications/solver/static/client ] || ln -s ~/RandomMetroidSolver/web/client/ ~/web2py/applications/solver/static/
