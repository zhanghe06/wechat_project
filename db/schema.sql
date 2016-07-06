DROP TABLE IF EXISTS user;
CREATE TABLE user (
  id          INTEGER PRIMARY KEY  AUTOINCREMENT,
  nickname    VARCHAR(20),
  avatar_url  VARCHAR(80),
  email       VARCHAR(20),
  phone       VARCHAR(20),
  birthday    DATE,
  create_time DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_ip     VARCHAR(15)
);

DROP TABLE IF EXISTS user_auth;
CREATE TABLE user_auth (
  id           INTEGER PRIMARY KEY   AUTOINCREMENT,
  user_id      INTEGER      NOT NULL,
  auth_type    VARCHAR(20)  NOT NULL,
  auth_key     VARCHAR(64)  NOT NULL,
  auth_secret  VARCHAR(256) NOT NULL,
  verified     TINYINT      DEFAULT 0
);
