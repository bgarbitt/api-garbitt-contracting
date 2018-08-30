DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS fleet;
DROP TABLE IF EXISTS fleet_images;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE services (
    id INT AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    explanation TEXT,
    PRIMARY KEY (id)
) ENGINE=INNODB;

CREATE TABLE images (
    id INT,
    url VARCHAR(255),
    PRIMARY KEY (id, url),
    FOREIGN KEY(id) REFERENCES services(id) ON DELETE CASCADE
) ENGINE=INNODB;

CREATE TABLE videos (
    id INT,
    url VARCHAR(255),
    PRIMARY KEY (id, url),
    FOREIGN KEY (id) REFERENCES services(id) ON DELETE CASCADE
) ENGINE=INNODB;

CREATE TABLE fleet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    machine TEXT NOT NULL
);

CREATE TABLE fleet_images (
    id INT,
    url VARCHAR(255),
    size INT,
    PRIMARY KEY (id, url, size),
    FOREIGN KEY (id) REFERENCES fleet(id) ON DELETE CASCADE
);