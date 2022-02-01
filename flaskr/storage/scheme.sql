DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS userRole;
DROP TABLE IF EXISTS interval;
DROP TABLE IF EXISTS swNotification;
DROP TABLE IF EXISTS notificationType;
DROP TABLE IF EXISTS swStatistics;

CREATE TABLE userRole (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  permissions NVARCHAR(5) DEFAULT 'R',  -- Create Read Update Delete 
  roleName NVARCHAR(25) NOT NULL,
  createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username NVARCHAR(25) UNIQUE NOT NULL,
  password NVARCHAR(100) NOT NULL, -- WE SHOULD CHANGE TO BINARY(64) WHEN WE IMPLEMENT THE SECURE PASSWORD STORING
  roleID INTEGER NOT NULL DEFAULT 1, -- 0 ADMIN, 1 USER
  createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (roleID) REFERENCES userRole(id)
);

CREATE TABLE interval (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name NVARCHAR(20),
  iStart TIMESTAMP NOT NULL,
  iEnd TIMESTAMP NOT NULL,
  luminosity FLOAT(2),
  createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK(iStart <= iEnd)
);

CREATE TABLE notificationType (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description NVARCHAR(255) NOT NULL,
  createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE swNotification (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content NVARCHAR(255) NOT NULL,
  typeID INTEGER NOT NULL,
  createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (typeID) REFERENCES notificationType(id)
);

CREATE TABLE swStatistics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  isExterior INTEGER,
  minTemperature FLOAT(2),
  maxTemperature FLOAT(2),
  humidity FLOAT(2),
  pressure FLOAT(2),
  createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);