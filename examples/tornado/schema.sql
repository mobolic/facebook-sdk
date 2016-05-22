-- Copyright 2010 Facebook
--
-- Licensed under the Apache License, Version 2.0 (the "License"); you may
-- not use this file except in compliance with the License. You may obtain
-- a copy of the License at
--
--     https://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
-- WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
-- License for the specific language governing permissions and limitations
-- under the License.

-- To create the database:
--   CREATE DATABASE example;
--   GRANT ALL PRIVILEGES ON example.* TO 'example'@'localhost' IDENTIFIED BY 'example';
--
-- To reload the tables:
--   mysql --user=example --password=example --database=example < schema.sql

SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id VARCHAR(25) NOT NULL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    profile_url VARCHAR(512) NOT NULL,
    access_token VARCHAR(512) NOT NULL,
    updated TIMESTAMP NOT NULL
);
