DROP DATABASE IF EXISTS `wechat`;
CREATE DATABASE `wechat` /*!40100 DEFAULT CHARACTER SET utf8 */;


use wechat;


DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `nickname` varchar(20) DEFAULT '' COMMENT '职位标题',
  `avatar_url` varchar(60) DEFAULT '' COMMENT '地区',
  `email` varchar(60) DEFAULT '' COMMENT '薪资范围',
  `phone` varchar(60) DEFAULT '' COMMENT '职位关键字',
  `birthday` TIMESTAMP DEFAULT '0000-00-00 00:00:00' COMMENT '发布时间',
  `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `last_ip` varchar(45) DEFAULT '' COMMENT '来源用户id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户表';


DROP TABLE IF EXISTS `user_auth`;
CREATE TABLE `user_auth` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `nickname` varchar(20) DEFAULT '' COMMENT '职位标题',
  `avatar_url` varchar(60) DEFAULT '' COMMENT '地区',
  `email` varchar(60) DEFAULT '' COMMENT '薪资范围',
  `phone` varchar(60) DEFAULT '' COMMENT '职位关键字',
  `birthday` TIMESTAMP DEFAULT '0000-00-00 00:00:00' COMMENT '发布时间',
  `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `last_ip` varchar(45) DEFAULT '' COMMENT '来源用户id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户表';
