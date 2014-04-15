CREATE TABLE IF NOT EXISTS user (
  user_id integer,
  reg_id integer,
  password char(40),
  martial_status char(40),
  PRIMARY KEY(user_id)
);

insert into user values('1', '1', 'password1', 'Married');
insert into user values('2', '2', 'password2', 'Married');
insert into user values('3', '3', 'password3', 'Married');
insert into user values('4', '4', 'password4', 'Married');
insert into user values('5', '5', 'password5', 'Single');
insert into user values('6', '6', 'password6', 'Single');
insert into user values('7', '7', 'password7', 'Single');
insert into user values('8', '8', 'password8', 'Single');

CREATE TABLE IF NOT EXISTS post (
  post_id integer,
  title varchar(140),
  post_type varchar(140),
  PRIMARY KEY(post_id)
);

insert into post values('1', 'Some Text', 'text');
insert into post values('2', 'A Picture', 'img');

CREATE TABLE IF NOT EXISTS post_info (
  post_id integer,
  image_path varchar(140),
  text_body varchar(149)
  PRIMARY KEY(post_id)
);

insert into post_info values('1', '', 'Post text about some title.');
insert into post_info values('2', '2', 'Pretty picture.');

CREATE TABLE IF NOT EXISTS comment (
  comment_id integer,
  content varchar(140),
  PRIMARY KEY(comment_id)
);

insert into comment values('1', 'Comment text about some title.');
insert into comment values('2', 'Comment text about a title.');

CREATE TABLE IF NOT EXISTS group (
  group_id integer,
  group_name varchar(140),
  PRIMARY KEY(group_id)
);

insert into group values('1', 'Group 1');
insert into group values('2', 'Group 2');

CREATE TABLE IF NOT EXISTS group_post (
  gpost_id integer,
  title varchar(140),
  gpost_type varchar(140),
  PRIMARY KEY(gpost_id)
);

insert into group_post values('1', 'Some Group Title', 'text');
insert into group_post values('2', 'A Group Pic', 'img');

CREATE TABLE IF NOT EXISTS group_post_info (
  gpost_id integer,
  g_image_path varchar(140),
  text_body varchar(140),
  PRIMARY KEY(gpost_id),
  FOREIGN KEY (gpost_id) REFERENCES group_post(gpost_id)
);

insert into gpost_info values('1', '', 'Group post text about some title.');
insert into gpost_info values('2', 'path/to/pic', 'Group pic.');

CREATE TABLE IF NOT EXISTS profile (
  user_id integer,
  email varchar(140),
  profile_pic varchar(140),
  PRIMARY KEY(user_id),
  FOREIGN KEY (user_id) REFERENCES user(user_id)
);

insert into profile values('1', 'user1@gmail.com', 'path/to/pic1');
insert into profile values('2', 'user2@gmail.com', 'path/to/pic2');
insert into profile values('3', 'user3@gmail.com', 'path/to/pic3');
insert into profile values('4', 'user4@gmail.com', 'path/to/pic4');
insert into profile values('5', 'user5@gmail.com', 'path/to/pic5');
insert into profile values('6', 'user6@gmail.com', 'path/to/pic6');
insert into profile values('7', 'user7@gmail.com', 'path/to/pic7');
insert into profile values('8', 'user8@gmail.com', 'path/to/pic8');


CREATE TABLE IF NOT EXISTS profile_info (
  fname varchar(140),
  lname varchar(140),
  email varchar(140),
  dob date,
  PRIMARY KEY(email)
  FOREIGN KEY (email) REFERENCES profile(email)
);

insert into profile_info values('Bea', 'Breanne', 'user1@gmail.com', '1981-01-01');
insert into profile_info values('Kerry', 'Daniel', 'user2@gmail.com', '1982-02-02');
insert into profile_info values('Darryl', 'Shayne', 'user3@gmail.com', '1983-03-03');
insert into profile_info values('Finnegan', 'Makenna', 'user4@gmail.com', '1984-04-04');
insert into profile_info values('Annalee', 'Abby', 'user5@gmail.com', '1985-05-05');
insert into profile_info values('Emmanuel', 'Purdie', 'user6@gmail.com', '1986-06-06');
insert into profile_info values('Davinia', 'Lauren', 'user7@gmail.com', '1987-07-07');
insert into profile_info values('Shawnda', 'Laryn', , 'user8@gmail.com', '1988-08-08');

CREATE TABLE IF NOT EXISTS mood (
	user_id integer,
	user_mood varchar(140),
	FOREIGN KEY (user_id) REFERENCES user(user_id)
);

insert into mood values('1', 'happy');
insert into mood values('2', 'happy');
insert into mood values('3', 'happy');
insert into mood values('4', 'sad');
insert into mood values('5', 'angry');
insert into mood values('6', 'sad');
insert into mood values('7', 'sad');
insert into mood values('8', 'angry');

CREATE TABLE IF NOT EXISTS creates_post (
  post_id integer,
  user_id integer,
  date_created date,
  PRIMARY KEY(post_id, user_id),
  FOREIGN KEY (post_id) REFERENCES post(post_id),
  FOREIGN KEY (user_id) REFERENCES user(user_id)
);

insert into creates_post values('1','1', NOW());
insert into creates_post values('2','2', NOW());

CREATE TABLE IF NOT EXISTS comments_on (
  post_id integer,
  user_id integer,
  comment_id integer,
  date_created date,
  PRIMARY_KEY(post_id, user_id),
  FOREIGN KEY (post_id) REFERENCES post(post_id),
  FOREIGN KEY (user_id) REFERENCES user(user_id),
  FOREIGN KEY (comment_id) REFERENCES comment(comment_id)
);

insert into comments_on('1','3', '1', NOW());
insert into comments_on('2','4', '2', NOW());

CREATE TABLE IF NOT EXISTS friend_of (
  friend_owner integer,
  friend integer,
  category varchar(140),
  PRIMARY KEY(friend, friend_owner),
  FOREIGN KEY (friend) REFERENCES user(user_id),
  FOREIGN KEY (friend_owner) REFERENCES user(user_id)
);

insert into friend_of('1', '2', 'family');
insert into friend_of('1', '3', 'work');
insert into friend_of('2', '4', 'family');
insert into friend_of('2', '3', 'work');
insert into friend_of('3', '4', 'work');
insert into friend_of('3', '8', 'family');

CREATE TABLE IF NOT EXISTS add_editors_group (
  group_owner integer,
  user_added integer,
  date_created date,
  PRIMARY KEY(group_owner, user_added),
  FOREIGN KEY(group_owner) REFERENCES user(user_id),
  FOREIGN KEY(user_added) REFERENCES user(user_id)
);

insert into add_editors_group('1','5',NOW());
insert into add_editors_group('1','4',NOW());
insert into add_editors_group('2','1',NOW());
insert into add_editors_group('4','8',NOW());
insert into add_editors_group('7','5',NOW());

CREATE TABLE IF NOT EXISTS add_to_group (
  user_id integer,
  group_id integer,
  date_added date,
  PRIMARY KEY(user_id, friend_group_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id),
  FOREIGN KEY(group_id) REFERENCES friend_group(group_id)
);

insert into add_to_group('3','1', NOW());
insert into add_to_group('1','1', NOW());
insert into add_to_group('4','1', NOW());
insert into add_to_group('5','2', NOW());
insert into add_to_group('6','1', NOW());
insert into add_to_group('2','2', NOW());
insert into add_to_group('7','2', NOW());

CREATE TABLE IF NOT EXISTS create_group (
  group_id integer,
  user_id integer,
  date_created date,
  PRIMARY_KEY(group_id, user_id),
  FOREIGN KEY(group_id) REFERENCES friend_group(group_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id)
);

insert into create_group('1','1');
insert into create_group('2','2');

CREATE TABLE IF NOT EXISTS create_content (
  user_id integer,
  group_id integer,
  gpost_id integer,
  date_created date,
  PRIMARY KEY(user_id, group_id, gpost_id),
  FOREIGN KEY user_id REFERENCES user(user_id),
  FOREIGN KEY group_id REFERENCES friend_group(group_id),
  FOREIGN KEY gpost_id REFERENCES group_post(gpost_id)
);

insert into create_content('1','1','1',NOW());
insert into create_content('2','2','2',NOW());
