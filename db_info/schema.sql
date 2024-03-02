DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS assoc;

CREATE TABLE course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT UNIQUE NOT NULL,
    course_code TEXT UNIQUE NOT NULL,
    course_desc TEXT
);

CREATE TABLE role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE NOT NULL
);

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    user_group TEXT,
    user_email TEXT,
    password_hash TEXT NOT NULL
);

CREATE TABLE assoc (
    course_id INTEGER,
    role_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (course_id) REFERENCES users(course_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES users(role_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    /* CONSTRAINT assoc_con UNIQUE (course_id, role_id, user_id) */
    PRIMARY KEY (course_id, role_id, user_id)
);

INSERT INTO course (course_name, course_code, course_desc) VALUES
('Building Secure Python Applications', 'SDEV300', 'A hands-on study of best practices and strategies for building secure Python desktop and web applications.'),
('Detecting Software Vulnerabilities', 'SDEV325', 'An in-depth, practical application of techniques and tools for detecting and documenting software vulnerabilities and risks.'),
('Database Security', 'SDEV350', 'A study of processes and techniques for securing databases.'),
('Securing Mobile Apps', 'SDEV355', 'A hands-on study of best practices for designing and building secure mobile applications.'),
('Secure Software Engineering', 'SDEV360', 'An in-depth study of the processes, standards, and regulations associated with secure software engineering.'),
('Secure Programming in the Cloud', 'SDEV400', 'A hands-on study of programming secure applications in the cloud.'),
('Mitigating Software Vulnerabilities', 'SDEV425', 'An in-depth analysis and evaluation of the mitigation of software vulnerabilities.'),
('Risk Analysis and Threat Modeling', 'SDEV455', 'An examination of the risks and threats associated with application development.'),
('Software Security Testing', 'SDEV460', 'A hands-on study of exploits, attacks, and techniques used to penetrate application security defenses and strategies for mitigating such attacks.');

INSERT INTO role (role_name) VALUES ('Administrator'), ('Teacher'), ('Student');
