CREATE DATABASE IF NOT EXISTS money_heist;

USE money_heist;

CREATE TABLE IF NOT EXISTS cyber_heist_crew (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    expertise VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS flag (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag VARCHAR(255) NOT NULL
);

INSERT INTO cyber_heist_crew (name, role, expertise) VALUES
('Professor', 'Mastermind', 'Strategist'),
('Tokyo', 'Hacker', 'Cryptography'),
('Berlin', 'Co-leader', 'Social Engineering'),
('Nairobi', 'Logistics Expert', 'Supply Chain'),
('Rio', 'Hacker', 'Network Security'),
('Denver', 'Muscle', 'Physical Security'),
('Moscow', 'Technician', 'Engineering'),
('Stockholm', 'Psychological Operations', 'Negotiation');

INSERT INTO flag (flag) VALUES
('TCF{fake_flag}')