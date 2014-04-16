CREATE TABLE IF NOT EXISTS users(
  user_id integer not null auto_increment,
  hpassword varchar(40),
  marital_status varchar(20),
  PRIMARY KEY(user_id)
);

insert into users (hpassword, marital_status) values('password1', 'Married');
insert into users (hpassword, marital_status) values('password2', 'Married');
insert into users (hpassword, marital_status) values('password3', 'Married');
insert into users (hpassword, marital_status) values('password4', 'Married');
insert into users (hpassword, marital_status) values('password5', 'Single');
insert into users (hpassword, marital_status) values('password6', 'Single');
insert into users (hpassword, marital_status) values('password7', 'Single');
insert into users (hpassword, marital_status) values('password8', 'Single');

CREATE TABLE IF NOT EXISTS post(
  post_id integer not null auto_increment,
  title varchar(140),
  post_type varchar(140),
  image_path varchar(140),
  text_body varchar(200),
  PRIMARY KEY(post_id)
);

insert into post values(1, 'Some Text', 'text',  '', 'Post text about some title.' );
insert into post values(2, 'A Picture', 'img','2', 'Pretty picture.' );



CREATE TABLE IF NOT EXISTS comments (
  comment_id integer not null auto_increment,
  content varchar(140),
  PRIMARY KEY(comment_id)
);

insert into comments values(1, 'Comment text about some title.');
insert into comments values(2, 'Comment text about a title.');

CREATE TABLE IF NOT EXISTS groups (
  group_id integer not null,
  group_name varchar(140),
  PRIMARY KEY(group_id)
);

insert into groups values(1, 'We Love Cats');
insert into groups values(2, 'Gladiators in Suits');

CREATE TABLE IF NOT EXISTS group_post (
  gpost_id integer not null auto_increment,
  title varchar(140),
  gpost_type varchar(140),
  g_image_path varchar(140),
  text_body varchar(140),
  PRIMARY KEY(gpost_id)
);

insert into group_post values(1, 'Cats are Awesome', 'text','', 'cats <3.');
insert into group_post values(2, 'A Group Pic', 'img', 'path/to/pic', 'Group pic.');

CREATE TABLE IF NOT EXISTS profile_pic (
  user_id integer not null,
  profile_pic_path varchar(140),
  PRIMARY KEY(user_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

insert into profile_pic values(1, 'path/to/pic1');
insert into profile_pic values(2, 'path/to/pic2');
insert into profile_pic values(3, 'path/to/pic3');
insert into profile_pic values(4, 'path/to/pic4');
insert into profile_pic values(5, 'path/to/pic5');
insert into profile_pic values(6, 'path/to/pic6');
insert into profile_pic values(7, 'path/to/pic7');
insert into profile_pic values(8, 'path/to/pic8');

CREATE TABLE IF NOT EXISTS profile_info(
  user_id integer not null,
  fname varchar(140),
  lname varchar(140),
  email varchar(200),
  dob date,
  PRIMARY KEY(user_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
  
);



insert into profile_info values(1,'Bea', 'Breanne', 'user1@gmail.com', '1981-01-01');
insert into profile_info values(2,'Kerry', 'Daniel', 'user2@gmail.com', '1982-02-02');
insert into profile_info values(3,'Darryl', 'Shayne', 'user3@gmail.com', '1983-03-03');
insert into profile_info values(4,'Finnegan', 'Makenna', 'user4@gmail.com', '1984-04-04');
insert into profile_info values(5,'Annalee', 'Abby', 'user5@gmail.com', '1985-05-05');
insert into profile_info values(6,'Emmanuel', 'Purdie', 'user6@gmail.com', '1986-06-06');
insert into profile_info values(7,'Davinia', 'Lauren', 'user7@gmail.com', '1987-07-07');
insert into profile_info values(8,'Shawnda', 'Laryn', 'user8@gmail.com', '1988-08-08');

CREATE TABLE IF NOT EXISTS mood (
	user_id integer not null,
	user_mood varchar(40),
	PRIMARY KEY (user_id),
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);

insert into mood values(1, 'happy');
insert into mood values(2, 'happy');
insert into mood values(3, 'happy');
insert into mood values(4, 'sad');
insert into mood values(5, 'angry');
insert into mood values(6, 'sad');
insert into mood values(7, 'sad');
insert into mood values(8, 'angry');

CREATE TABLE IF NOT EXISTS creates_post (
  post_id integer not null,
  user_id integer not null,
  date_created date,
  PRIMARY KEY(post_id, user_id),
  FOREIGN KEY (post_id) REFERENCES post(post_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

insert into creates_post values(1,1, NOW());
insert into creates_post values(2,2, NOW());

CREATE TABLE IF NOT EXISTS comments_on (
  post_id integer not null,
  user_id integer not null,
  comment_id integer not null,
  date_commented date,
  PRIMARY KEY(post_id, user_id, comment_id),
  FOREIGN KEY (post_id) REFERENCES post(post_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (comment_id) REFERENCES comments(comment_id)
);

insert into comments_on values(1,3, 1, NOW());
insert into comments_on values(2,4, 2, NOW());

CREATE TABLE IF NOT EXISTS friend_of (
  friend_owner integer not null,
  friend integer not null,
  category varchar(140),
  PRIMARY KEY(friend_owner, friend),
  FOREIGN KEY (friend) REFERENCES users(user_id),
  FOREIGN KEY (friend_owner) REFERENCES users(user_id)
);

insert into friend_of values(1, 2, 'family');
insert into friend_of values(1, 3, 'work');
insert into friend_of values(2, 1, 'family');
insert into friend_of values(2, 4, 'family');
insert into friend_of values(2, 3, 'work');
insert into friend_of values(3, 4, 'work');
insert into friend_of values(3, 8, 'family');

CREATE TABLE IF NOT EXISTS add_editors_group (
  group_owner integer not null,
  user_added integer not null,
  date_added date,
  PRIMARY KEY(group_owner, user_added),
  FOREIGN KEY(group_owner) REFERENCES users(user_id),
  FOREIGN KEY(user_added) REFERENCES users(user_id)
);

insert into add_editors_group values(1,5,NOW());
insert into add_editors_group values(1,4,NOW());
insert into add_editors_group values(2,1,NOW());
insert into add_editors_group values(4,8,NOW());
insert into add_editors_group values(7,5,NOW());

CREATE TABLE IF NOT EXISTS add_to_group (
  user_id integer not null,
  group_id integer not null,
  date_added date,
  PRIMARY KEY(user_id, group_id),
  FOREIGN KEY(user_id) REFERENCES users(user_id),
  FOREIGN KEY(group_id) REFERENCES groups(group_id)
);

insert into add_to_group values(3,1, NOW());
insert into add_to_group values(1,1, NOW());
insert into add_to_group values(4,1, NOW());
insert into add_to_group values(5,2, NOW());
insert into add_to_group values(6,1, NOW());
insert into add_to_group values(2,2, NOW());
insert into add_to_group values(7,2, NOW());

CREATE TABLE IF NOT EXISTS create_group (
  group_id integer not null,
  user_id integer not null,
  date_created date,
  PRIMARY KEY(group_id, user_id),
  FOREIGN KEY(group_id) REFERENCES groups(group_id) ON UPDATE CASCADE,
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON UPDATE CASCADE
);

insert into create_group values(1,1, NOW());
insert into create_group values(2,2, NOW());

CREATE TABLE IF NOT EXISTS create_content (
  user_id integer not null,
  group_id integer not null,
  gpost_id integer not null,
  date_created date,
  PRIMARY KEY(user_id, group_id, gpost_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (group_id) REFERENCES groups(group_id),
  FOREIGN KEY (gpost_id) REFERENCES group_post(gpost_id)
);

insert into create_content values(1,1,1,NOW());
insert into create_content values(2,2,2,NOW());

DELIMITER $$
  CREATE PROCEDURE add_friend(IN friend_owner_id varchar(40), IN friend_id varchar(40))
  BEGIN
  INSERT INTO friend_of VALUES (friend_owner_id, friend_id, category);
  END; $$
DELIMITER ;

DELIMITER $$
  CREATE PROCEDURE create_group(IN owner_id varchar(40), IN group_name varchar(40))
  BEGIN
  START TRANSACTION;
    INSERT INTO groups (group_id, group_name) 
      values(owner_id, group_name);
    INSERT INTO create_group (group_id, user_id, date_created) 
      values(owner_id, owner_id, NOW());
  COMMIT;
  END; $$
DELIMITER ;
