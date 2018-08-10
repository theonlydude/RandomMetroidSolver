
-- solver
create table if not exists solver (
  action_time datetime not null,
  id unsigned int not null auto increment,
  primary key (id),
);
create unique index solver_idx01 on solver(action_time);

create table if not exists solver_params (
  solver_id unsigned int not null
  romFileName tinytext,
  preset tinytext,
  difficultyTarget unsigned tinyint,
  pickupStrategy tinytext,
  primary key (solver_id),
  foreign key (solver_id) references solver(id)
);

create table if not exists solver_items_forbidden (
  solver_id unsigned int not null,
  item tinytext not null,
  primary key (solver_id, item),
  foreign key (solver_id) references solver(id)
);

create table if not exists solver_result (
  solver_id unsigned int not null,
  return_code tinyint,
  duration time,
  randomized_rom tinytext,
  difficulty int,
  knows_used tinyint,
  knows_known tinyint,
  items_ok bool,
  len_remainTry unsigned tinyint,
  len_remainMajors unsigned tinyint,
  len_remainMinors unsigned tinyint,
  len_skippedMajors unsigned tinyint,
  len_unavailMajors unsigned tinyint,
  primary key (solver_id),
  foreign key (solver_id) references solver(id)
);

create table if not exists solver_collected_items (
  solver_id unsigned int not null,
  item tinytext not null,
  count tinyint not null,
  primary key (solver_id, item),
  foreign key (solver_id) references solver(id)
);

--randomizer
create table if not exists randomizer (
  id unsigned int not null auto increment,
  action_time datetime not null,
  primary key (id),
);
create unique index randomizer_idx01 on randomizer(action_time);

create table if not exists randomizer_params (
  randomizer_id unsigned int not null,
  name tinytext not null,
  value text,
  primary key (id, tinytext),
  foreign key (randomizer_id) references randomizer(id)
);

create table if not exists randomizer_result (
  randomizer_id unsigned int not null,
  return_code tinyint,
  duration time,
  error_msg text,
  primary key (randomizer_id),
  foreign key (randomizer_id) references randomizer(id)
);
