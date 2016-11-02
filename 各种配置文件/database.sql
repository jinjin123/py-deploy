CREATE TABLE `fb_fabric` (
  `id` varchar(40) NOT NULL DEFAULT '' COMMENT '主键',
  `tag` varchar(100) NOT NULL DEFAULT '' COMMENT '要发布的TAG',
  `project_id` varchar(40) NOT NULL DEFAULT '' COMMENT '项目ID',
  `desc` varchar(255) DEFAULT '' COMMENT '发布文案',
  `status` varchar(50) NOT NULL DEFAULT '' COMMENT '发布状态',
  `type` varchar(30) NOT NULL DEFAULT '' COMMENT '发布类型',
  `create_time` int(11) NOT NULL COMMENT '记录创建时间',
  `fabric_time` int(11) DEFAULT NULL COMMENT '点击发布按钮的时间',
  `finish_time` int(11) DEFAULT NULL COMMENT '发布结束时间',
  `total` int(11) NOT NULL DEFAULT '0' COMMENT '总量',
  `success_num` int(11) NOT NULL DEFAULT '0' COMMENT '成功量',
  `error_num` int(11) NOT NULL DEFAULT '0' COMMENT '失败',
  `error` varchar(255) DEFAULT NULL COMMENT '发布时候的错误文案',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `fb_fabric_relation` (
  `id` varchar(40) NOT NULL DEFAULT '' COMMENT '主键',
  `fabric_id` varchar(40) NOT NULL DEFAULT '' COMMENT '发布计划id',
  `project_id` varchar(40) NOT NULL DEFAULT '' COMMENT '项目id',
  `machine_id` varchar(40) NOT NULL DEFAULT '' COMMENT '机器id',
  `status` varchar(50) DEFAULT NULL COMMENT '发布状态',
  `error` varchar(255) DEFAULT NULL COMMENT '发布错误，捕捉到的异常消息',
  `create_time` int(11) NOT NULL COMMENT '消息创建时间',
  `fabric_time` int(11) DEFAULT NULL COMMENT '真正发布时间',
  `finish_time` int(11) DEFAULT NULL COMMENT '发布结束时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `fb_machine` (
  `id` varchar(40) NOT NULL DEFAULT '' COMMENT '主键',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT '机器名称',
  `desc` text COMMENT '描述',
  `account` varchar(255) DEFAULT '' COMMENT '登陆名称',
  `password` varchar(255) DEFAULT '' COMMENT '密码',
  `create_time` int(11) NOT NULL COMMENT '添加时间',
  `ip` varchar(30) NOT NULL DEFAULT '' COMMENT '服务器IP地址',
  `auth_type` varchar(10) NOT NULL DEFAULT 'password' COMMENT '服务器验证方式，密码或者秘钥',
  `is_valid` varchar(10) NOT NULL DEFAULT 'yes' COMMENT '是否已经被删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `fb_machine_relation` (
  `id` varchar(40) NOT NULL DEFAULT '' COMMENT '主键',
  `project_id` varchar(40) NOT NULL DEFAULT '' COMMENT '项目id',
  `machine_id` varchar(40) NOT NULL DEFAULT '' COMMENT '机器id',
  `create_time` int(11) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `fb_project` (
  `id` varchar(40) NOT NULL DEFAULT '' COMMENT '主键',
  `name` varchar(255) NOT NULL COMMENT '项目名称',
  `gituser` varchar(30) NOT NULL COMMENT 'Git仓库用户名',
  `gitaddress` varchar(255) NOT NULL DEFAULT '' COMMENT 'Git仓库地址',
  `localaddress` varchar(255) NOT NULL DEFAULT '' COMMENT '本地仓库地址',
  `remoteaddress` varchar(255) NOT NULL DEFAULT '' COMMENT '远程机器存放地址',
  `deployaddress` varchar(255) NOT NULL DEFAULT '' COMMENT '项目部署地址',
  `desc` text COMMENT '项目描述',
  `error` varchar(255) DEFAULT NULL COMMENT '如果clone发生错误，这里是捕获到的错误异常',
  `status` varchar(20) NOT NULL DEFAULT 'cloneing' COMMENT '当前项目状态',
  `create_time` int(11) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `fb_user` (
  `id` varchar(40) NOT NULL DEFAULT '' COMMENT '主键',
  `loginname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_estonian_ci NOT NULL DEFAULT '' COMMENT '登录名',
  `nickname` varchar(50) NOT NULL DEFAULT '' COMMENT '昵称',
  `password` varchar(255) NOT NULL DEFAULT '' COMMENT '密码',
  `avatar` varchar(200) DEFAULT NULL COMMENT '头像',
  `create_time` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;