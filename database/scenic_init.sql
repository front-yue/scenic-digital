-- ==================================================
-- 智慧文旅大屏系统 (ScenicScreen) 数据库设计
-- 字符集: utf8mb4
-- ==================================================

CREATE DATABASE IF NOT EXISTS `scenic` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `scenic`;



-- --------------------------------------------------
-- 1. 系统配置表 (system_config)
-- 用途: 存储系统级的全局配置（如：主题设置等）
-- --------------------------------------------------
CREATE TABLE IF NOT EXISTS `system_config` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `config_key` VARCHAR(50) NOT NULL UNIQUE COMMENT '配置键名',
  `config_value` TEXT COMMENT '配置值',
  `description` VARCHAR(255) COMMENT '配置说明',
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';

INSERT IGNORE INTO `system_config` (`config_key`, `config_value`, `description`) VALUES 
('theme', 'default', '全局主题设置');

-- --------------------------------------------------
-- 2. 景区概况信息表 (scenic_info)
-- 用途: 存储左侧面板的“景区全景概况”各个卡片模块的数据。
-- --------------------------------------------------
CREATE TABLE IF NOT EXISTS `scenic_info` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `scenic_name` VARCHAR(100) NOT NULL COMMENT '景区名称',
  `scenic_en_name` VARCHAR(100) DEFAULT NULL COMMENT '景区英文名称',
  `cover_image` VARCHAR(255) DEFAULT NULL COMMENT '景区URL',
  `weather_temp` VARCHAR(20) DEFAULT NULL COMMENT '天气温度，如：24°C',
  `weather_desc` VARCHAR(50) DEFAULT NULL COMMENT '天气描述，如：晴 | AQI 20',
  `introduction` TEXT NOT NULL COMMENT '景区简介',
  `ticket_price` DECIMAL(10,2) DEFAULT 0.00 COMMENT '票价（￥）',
  `opening_hours` VARCHAR(50) DEFAULT NULL COMMENT '营业时间，如：08:00 - 18:00',
  `address` VARCHAR(255) DEFAULT NULL COMMENT '地理位置，详细地址',
  `recommended_routes` TEXT DEFAULT NULL COMMENT '推荐路线(JSON格式)',
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='景区信息表';

-- 插入默认数据
INSERT INTO `scenic_info` (`scenic_name`, `scenic_en_name`, `cover_image`, `weather_temp`, `weather_desc`, `introduction`, `ticket_price`, `opening_hours`, `address`, `recommended_routes`) VALUES 
('杭州西湖风景名胜区', 'WEST LAKE SCENIC AREA', 'https://images.unsplash.com/photo-1541843943716-e41c48c6bb8a?auto=format&fit=crop&w=800&q=80', '26°C', '多云 | AQI 35', '杭州西湖风景名胜区位于浙江省杭州市中心，是首批国家重点风景名胜区，也是中国著名的旅游胜地。以“一山、二塔、三岛、三堤、五湖”的基本格局著称，西湖之美，美在晴中见潋滟，雨中显空蒙。\n\n作为世界文化遗产，西湖承载了丰富的历史与文化底蕴。无论是断桥残雪的凄美传说，还是苏堤春晓的盎然生机，每一处景点都诉说着千年的故事。漫步西湖畔，您可以感受“水光潋滟晴方好，山色空蒙雨亦奇”的绝佳意境。\n\n近年来，西湖景区全面推进智慧文旅建设，将数字导览、实时客流监控、AI数字人服务融入游客体验。在雷峰塔下、岳王庙前，您可以通过我们的系统实时了解景点历史，获取最佳游览路线推荐。\n\n环保与可持续发展是西湖景区的核心理念。我们倡导绿色出行，环湖提供纯电动接驳车及公共自行车服务，努力保持西湖水清、岸绿、景美的生态画卷。欢迎每一位游客在这个人间天堂，开启一段难忘的江南之旅。', 0.00, '全天开放', '浙江省杭州市西湖区西湖风景名胜区', '[{"label":"\u7ecf\u5178\u7ebf","duration":"\u7ea6 3 \u5c0f\u65f6","spots":["\u65ad\u6865\u6b8b\u96ea","\u767d\u5824","\u5b64\u5c71","\u82cf\u5824\u6625\u6653","\u96f7\u5cf0\u5854"]},{"label":"\u6587\u5316\u7ebf","duration":"\u7ea6 2 \u5c0f\u65f6","spots":["\u5cb3\u738b\u5e99","\u897f\u51b7\u5370\u793e","\u66f2\u9662\u98ce\u8377","\u4e09\u6f6d\u5370\u6708"]}]');



-- --------------------------------------------------
-- 3. 景点列表信息表 (scenic_spots)
-- 用途: 存储页面右侧"景点列表"Tab下的数据。
-- 说明: 景点属于景区的子级，通过 scenic_id 关联到 scenic_info。
--       每个景点包含经纬度，用于在前端地图上展示标记点。
-- --------------------------------------------------
CREATE TABLE IF NOT EXISTS `scenic_spots` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `scenic_id` INT NOT NULL COMMENT '景区ID',
  `spot_name` VARCHAR(100) NOT NULL COMMENT '景点名称',
  `en_name` VARCHAR(100) DEFAULT NULL COMMENT '景点英文名称',
  `description` VARCHAR(255) DEFAULT NULL COMMENT '描述',
  `image_url` VARCHAR(255) DEFAULT NULL COMMENT '景点图片URL',
  `latitude` DECIMAL(10,6) DEFAULT NULL COMMENT '纬度',
  `longitude` DECIMAL(10,6) DEFAULT NULL COMMENT '经度',
  `sort_order` INT DEFAULT 0 COMMENT '排序',
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='景点列表表';

INSERT INTO `scenic_spots` (`scenic_id`, `spot_name`, `en_name`, `description`, `image_url`, `latitude`, `longitude`, `sort_order`) VALUES 
(1, '三潭印月', 'THREE POOLS MIRRORING THE MOON', '西湖十景之一，湖中有岛，岛中有湖，一元纸币背面图案', 'https://images.unsplash.com/photo-1574768393582-841f3b39d10e?auto=format&fit=crop&w=200&q=80', 30.236800, 120.147500, 1),
(1, '雷峰塔', 'LEIFENG PAGODA', '西湖著名地标，白娘子传说的发生地', 'https://images.unsplash.com/photo-1549017684-2fcd71542f6c?auto=format&fit=crop&w=200&q=80', 30.231800, 120.148800, 2),
(1, '断桥残雪', 'LINGERING SNOW ON THE BROKEN BRIDGE', '白娘子与许仙相会之地，冬季赏雪胜地', 'https://images.unsplash.com/photo-1517409249063-e3805d21a221?auto=format&fit=crop&w=200&q=80', 30.259000, 120.153900, 3),
(1, '岳王庙', 'YUE FEI TEMPLE', '纪念南宋抗金名将岳飞的庙宇，精忠报国精神象征', 'https://images.unsplash.com/photo-1624606275811-9a7ed1f08149?auto=format&fit=crop&w=200&q=80', 30.256000, 120.141500, 4),
(1, '苏堤春晓', 'DAWN ON THE SU CAUSEWAY', '北宋大文豪苏东坡修筑的林荫大堤，春季漫步绝佳去处', 'https://images.unsplash.com/photo-1602879555134-2e9eb90a6142?auto=format&fit=crop&w=200&q=80', 30.244500, 120.142500, 5);


