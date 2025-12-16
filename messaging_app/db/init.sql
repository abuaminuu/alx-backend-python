-- Create additional users and permissions
CREATE USER IF NOT EXISTS 'alx_user'@'%' IDENTIFIED BY 'alx_password';
GRANT ALL PRIVILEGES ON alx_travel.* TO 'alx_user'@'%';
FLUSH PRIVILEGES;

-- Create test database
CREATE DATABASE IF NOT EXISTS alx_travel_test;
GRANT ALL PRIVILEGES ON alx_travel_test.* TO 'alx_user'@'%';
FLUSH PRIVILEGES;