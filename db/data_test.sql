-- user 测试数据
INSERT INTO `user`(id, nickname, email, phone, create_time, update_time) VALUES('1', 'Admin', 'admin@gmail.com', '13800001111', '2016-01-11 11:01:05', '2016-01-11 11:01:05');
INSERT INTO `user`(id, nickname, email, phone, create_time, update_time) VALUES('2', 'Guest', 'guest@gmail.com', '13800002222', '2016-01-12 12:25:34', '2016-01-12 12:25:34');
INSERT INTO `user`(id, nickname, email, phone, create_time, update_time) VALUES('3', 'Test', 'test@gmail.com', '13800003333', '2016-01-12 01:43:42', '2016-01-12 01:43:42');

-- user_auth 测试数据
INSERT INTO `user_auth`(user_id, auth_type, auth_key, auth_secret) VALUES('1', 'email', 'admin@gmail.com', '123456');
INSERT INTO `user_auth`(user_id, auth_type, auth_key, auth_secret) VALUES('2', 'email', 'guest@gmail.com', '123456');
INSERT INTO `user_auth`(user_id, auth_type, auth_key, auth_secret, verified) VALUES('3', 'email', 'test@gmail.com', '123456', '1');
