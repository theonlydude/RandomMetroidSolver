
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

create table if not exists solver_collected_items (
  solver_id int unsigned not null,
  item varchar(255) not null,
  count tinyint not null,
  primary key (solver_id, item),
  foreign key (solver_id) references solver(id)
);

-- randomizer
create table if not exists randomizer (
  id int unsigned not null auto_increment,
  action_time datetime not null,
  primary key (id)
);
create unique index randomizer_idx01 on randomizer(action_time);

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
  primary key (init_time, preset)
);
