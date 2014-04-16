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
CREATE TABLE IF NOT EXISTS group (
  group_id integer not null,
  group_name varchar(140),
  PRIMARY KEY(group_id)
);

insert into group values(1, 'We Love Cats');
insert into group values(2, 'Gladiators in Suits');

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

CREATE TABLE IF NOT EXISTS profile (
  user_id integer not null,
  email varchar(200),
  profile_pic varchar(140),
  PRIMARY KEY(user_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

insert into profile values(1, 'user1@gmail.com', 'path/to/pic1');
insert into profile values(2, 'user2@gmail.com', 'path/to/pic2');
insert into profile values(3, 'user3@gmail.com', 'path/to/pic3');
insert into profile values(4, 'user4@gmail.com', 'path/to/pic4');
insert into profile values(5, 'user5@gmail.com', 'path/to/pic5');
insert into profile values(6, 'user6@gmail.com', 'path/to/pic6');
insert into profile values(7, 'user7@gmail.com', 'path/to/pic7');
insert into profile values(8, 'user8@gmail.com', 'path/to/pic8');

CREATE TABLE IF NOT EXISTS profile_info(
  fname varchar(140),
  lname varchar(140),
  email varchar(200),
  dob date,
  PRIMARY KEY(email)
);

/* FOREIGN KEY (email) REFERENCES profile(email) */

insert into profile_info values('Bea', 'Breanne', 'user1@gmail.com', '1981-01-01');
insert into profile_info values('Kerry', 'Daniel', 'user2@gmail.com', '1982-02-02');
insert into profile_info values('Darryl', 'Shayne', 'user3@gmail.com', '1983-03-03');
insert into profile_info values('Finnegan', 'Makenna', 'user4@gmail.com', '1984-04-04');
insert into profile_info values('Annalee', 'Abby', 'user5@gmail.com', '1985-05-05');
insert into profile_info values('Emmanuel', 'Purdie', 'user6@gmail.com', '1986-06-06');
insert into profile_info values('Davinia', 'Lauren', 'user7@gmail.com', '1987-07-07');
insert into profile_info values('Shawnda', 'Laryn', 'user8@gmail.com', '1988-08-08');

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
  FOREIGN KEY(group_id) REFERENCES group(group_id)
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
  FOREIGN KEY(group_id) REFERENCES group(group_id),
  FOREIGN KEY(user_id) REFERENCES users(user_id)
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
  FOREIGN KEY (group_id) REFERENCES group(group_id),
  FOREIGN KEY (gpost_id) REFERENCES group_post(gpost_id)
);

insert into create_content values(1,1,1,NOW());
insert into create_content values(2,2,2,NOW());
