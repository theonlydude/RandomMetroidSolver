
-- solver
create table if not exists solver (
  action_time datetime not null,
  id int unsigned not null auto_increment,
  primary key (id)
);
create unique index solver_idx01 on solver(action_time);

create table if not exists solver_params (
  solver_id int unsigned not null,
  romFileName tinytext,
  preset tinytext,
  difficultyTarget tinyint unsigned,
  pickupStrategy tinytext,
  primary key (solver_id),
  foreign key (solver_id) references solver(id)
);

create table if not exists solver_items_forbidden (
  solver_id int unsigned not null,
  item varchar(255) not null,
  primary key (solver_id, item),
  foreign key (solver_id) references solver(id)
);

create table if not exists solver_result (
  solver_id int unsigned not null,
  return_code tinyint unsigned,
  duration float,
  difficulty int,
  knows_used tinyint,
  knows_known tinyint,
  items_ok bool,
  len_remainTry tinyint unsigned,
  len_remainMajors tinyint unsigned,
  len_remainMinors tinyint unsigned,
  len_skippedMajors tinyint unsigned,
  len_unavailMajors tinyint unsigned,
  primary key (solver_id),
  foreign key (solver_id) references solver(id)
);

-- randomizer
create table if not exists randomizer (
  id int unsigned not null auto_increment,
  action_time datetime not null,
  -- local: the ips is stored localy, will be set to pending if the user ask for the permalink, else will be deleted after 7 days
  -- pending: use has asked for the permalink, to be uploaded during next upload
  -- uploaded: uploaded in gdrive / stored in git repo
  -- deleted: local ips deleted
  -- null: failed randomization
  -- local -> pending -> uploaded
  -- local -> deleted
  upload_status varchar(8),
  filename varchar(128),
  guid char(36),
  primary key (id)
);
create index randomizer_idx01 on randomizer(action_time);
create index randomizer_idx02 on randomizer(upload_status);
create index randomizer_idx03 on randomizer(guid);
-- alter table randomizer add upload_status varchar(8) after action_time;
-- alter table randomizer add filename varchar(128);
-- alter table randomizer add guid char(36);

create table if not exists randomizer_params (
  randomizer_id int unsigned not null,
  name varchar(255) not null,
  value text,
  primary key (randomizer_id, name),
  foreign key (randomizer_id) references randomizer(id)
);
create index randomizer_params_idx01 on randomizer_params(name);
create index randomizer_params_idx02 on randomizer_params(name, value(255));

create table if not exists randomizer_result (
  randomizer_id int unsigned not null,
  return_code tinyint unsigned,
  duration float,
  error_msg text,
  primary key (randomizer_id),
  foreign key (randomizer_id) references randomizer(id)
);

create table if not exists preset_action (
  preset varchar(32) not null,
  action_time datetime not null,
  action varchar(6) not null,
  primary key (preset, action_time)
);

-- will loose one entry if same preset at the same second, can live with that
create table if not exists isolver (
  init_time datetime not null,
  preset varchar(32) not null,
  romFileName tinytext,
  type varchar(8),
  primary key (init_time, preset)
);
-- alter table isolver add type varchar(8);

-- plandository
create table if not exists plando_repo (
  plando_name varchar(32) not null,
  init_time datetime not null,
  author varchar(32) not null,
  long_desc varchar(2048) not null,
  suggested_preset varchar(32) not null,
  update_key varchar(8) not null,
  ips_max_size int unsigned not null,
  download_count int unsigned not null default 0,
  primary key (plando_name)
);

create table if not exists plando_rating (
  plando_name varchar(32) not null,
  rating int unsigned not null,
  ipv4 int unsigned not null,
  primary key (plando_name, ipv4)
);
-- drop index plando_rating_idx01 on plando_rating;
-- alter table plando_rating add primary key (plando_name, ipv4);

-- custom sprites
create table if not exists sprites (
  init_time datetime not null,
  sprite varchar(32) not null,
  primary key (init_time, sprite)
);

-- custom ships
create table if not exists ships (
  init_time datetime not null,
  ship varchar(32) not null,
  primary key (init_time, ship)
);

-- plando rando
-- we just store usage to know if someone use it
create table if not exists plando_rando (
  init_time datetime not null,
  return_code tinyint unsigned,
  duration float,
  error_msg text,
  primary key (init_time)
);
