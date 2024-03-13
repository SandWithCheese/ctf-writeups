USE serial_killer;

CREATE TABLE users (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE (`username`)
);

INSERT INTO users (`username`, `password`) VALUES ("admin", "REDACTED");

CREATE TABLE flag (
    `id` INT NOT NULL AUTO_INCREMENT,
    `flag` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
);

INSERT INTO flag (`flag`) VALUES ("REDACTED");