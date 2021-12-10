CREATE TABLE `Users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255),
  `password` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `Windows` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `openDirection` int,
  `openAngle` double,
  `integrity` double,
  `created_at` timestamp
);

CREATE TABLE `Intervals` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `window_id` int,
  `start` timestamp,
  `end` timestamp,
  `luminosity` double,
  `created_at` timestamp
);

CREATE TABLE `Notifications` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `window_id` int,
  `type_id` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `NotificationTypes` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `description` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `Statistics` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `window_id` int,
  `is_exterior` boolean,
  `min_temperature` double,
  `max_temperature` double,
  `humidity` double,
  `pressure` double,
  `created_at` timestamp
);

ALTER TABLE `Intervals` ADD FOREIGN KEY (`window_id`) REFERENCES `Windows` (`id`);

ALTER TABLE `Notifications` ADD FOREIGN KEY (`type_id`) REFERENCES `NotificationTypes` (`id`);

ALTER TABLE `Notifications` ADD FOREIGN KEY (`window_id`) REFERENCES `Windows` (`id`);

ALTER TABLE `Statistics` ADD FOREIGN KEY (`window_id`) REFERENCES `Windows` (`id`);
