--
-- File generated with SQLiteStudio v3.4.13 on Wed Feb 5 21:38:18 2025
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: associations
DROP TABLE IF EXISTS associations;
CREATE TABLE IF NOT EXISTS associations (
	course_id INTEGER NOT NULL,
	role_id INTEGER NOT NULL,
	member_id INTEGER NOT NULL,
	PRIMARY KEY (course_id, role_id, member_id),
	CONSTRAINT uq_course_member UNIQUE (course_id, member_id),
	FOREIGN KEY(course_id) REFERENCES courses (course_id),
	FOREIGN KEY(role_id) REFERENCES roles (role_id),
	FOREIGN KEY(member_id) REFERENCES members (member_id)
);
INSERT INTO associations (course_id, role_id, member_id) VALUES (1, 5, 2);
INSERT INTO associations (course_id, role_id, member_id) VALUES (1, 4, 3);
INSERT INTO associations (course_id, role_id, member_id) VALUES (1, 3, 4);
INSERT INTO associations (course_id, role_id, member_id) VALUES (1, 3, 5);
INSERT INTO associations (course_id, role_id, member_id) VALUES (1, 2, 6);
INSERT INTO associations (course_id, role_id, member_id) VALUES (1, 2, 7);
INSERT INTO associations (course_id, role_id, member_id) VALUES (1, 2, 8);
INSERT INTO associations (course_id, role_id, member_id) VALUES (2, 5, 9);
INSERT INTO associations (course_id, role_id, member_id) VALUES (2, 4, 10);
INSERT INTO associations (course_id, role_id, member_id) VALUES (2, 3, 11);
INSERT INTO associations (course_id, role_id, member_id) VALUES (2, 3, 12);
INSERT INTO associations (course_id, role_id, member_id) VALUES (2, 2, 13);
INSERT INTO associations (course_id, role_id, member_id) VALUES (2, 2, 14);
INSERT INTO associations (course_id, role_id, member_id) VALUES (2, 2, 15);
INSERT INTO associations (course_id, role_id, member_id) VALUES (3, 5, 16);
INSERT INTO associations (course_id, role_id, member_id) VALUES (3, 4, 2);
INSERT INTO associations (course_id, role_id, member_id) VALUES (3, 3, 3);
INSERT INTO associations (course_id, role_id, member_id) VALUES (3, 3, 4);
INSERT INTO associations (course_id, role_id, member_id) VALUES (3, 2, 5);
INSERT INTO associations (course_id, role_id, member_id) VALUES (3, 2, 6);
INSERT INTO associations (course_id, role_id, member_id) VALUES (3, 2, 7);
INSERT INTO associations (course_id, role_id, member_id) VALUES (4, 5, 8);
INSERT INTO associations (course_id, role_id, member_id) VALUES (4, 4, 9);
INSERT INTO associations (course_id, role_id, member_id) VALUES (4, 3, 10);
INSERT INTO associations (course_id, role_id, member_id) VALUES (4, 3, 11);
INSERT INTO associations (course_id, role_id, member_id) VALUES (4, 2, 12);
INSERT INTO associations (course_id, role_id, member_id) VALUES (4, 2, 13);
INSERT INTO associations (course_id, role_id, member_id) VALUES (4, 2, 14);
INSERT INTO associations (course_id, role_id, member_id) VALUES (5, 5, 15);
INSERT INTO associations (course_id, role_id, member_id) VALUES (5, 4, 16);
INSERT INTO associations (course_id, role_id, member_id) VALUES (5, 3, 2);
INSERT INTO associations (course_id, role_id, member_id) VALUES (5, 3, 3);
INSERT INTO associations (course_id, role_id, member_id) VALUES (5, 2, 4);
INSERT INTO associations (course_id, role_id, member_id) VALUES (5, 2, 5);
INSERT INTO associations (course_id, role_id, member_id) VALUES (5, 2, 6);
INSERT INTO associations (course_id, role_id, member_id) VALUES (6, 5, 7);
INSERT INTO associations (course_id, role_id, member_id) VALUES (6, 4, 8);
INSERT INTO associations (course_id, role_id, member_id) VALUES (6, 3, 9);
INSERT INTO associations (course_id, role_id, member_id) VALUES (6, 3, 10);
INSERT INTO associations (course_id, role_id, member_id) VALUES (6, 2, 11);
INSERT INTO associations (course_id, role_id, member_id) VALUES (6, 2, 12);
INSERT INTO associations (course_id, role_id, member_id) VALUES (6, 2, 13);
INSERT INTO associations (course_id, role_id, member_id) VALUES (7, 5, 14);
INSERT INTO associations (course_id, role_id, member_id) VALUES (7, 4, 15);
INSERT INTO associations (course_id, role_id, member_id) VALUES (7, 3, 16);
INSERT INTO associations (course_id, role_id, member_id) VALUES (7, 3, 2);
INSERT INTO associations (course_id, role_id, member_id) VALUES (7, 2, 3);
INSERT INTO associations (course_id, role_id, member_id) VALUES (7, 2, 4);
INSERT INTO associations (course_id, role_id, member_id) VALUES (7, 2, 5);
INSERT INTO associations (course_id, role_id, member_id) VALUES (8, 5, 6);
INSERT INTO associations (course_id, role_id, member_id) VALUES (8, 4, 7);
INSERT INTO associations (course_id, role_id, member_id) VALUES (8, 3, 8);
INSERT INTO associations (course_id, role_id, member_id) VALUES (8, 3, 9);
INSERT INTO associations (course_id, role_id, member_id) VALUES (8, 2, 10);
INSERT INTO associations (course_id, role_id, member_id) VALUES (8, 2, 11);
INSERT INTO associations (course_id, role_id, member_id) VALUES (8, 2, 12);
INSERT INTO associations (course_id, role_id, member_id) VALUES (9, 5, 13);
INSERT INTO associations (course_id, role_id, member_id) VALUES (9, 4, 14);
INSERT INTO associations (course_id, role_id, member_id) VALUES (9, 3, 15);
INSERT INTO associations (course_id, role_id, member_id) VALUES (9, 3, 16);
INSERT INTO associations (course_id, role_id, member_id) VALUES (9, 2, 2);
INSERT INTO associations (course_id, role_id, member_id) VALUES (9, 2, 3);
INSERT INTO associations (course_id, role_id, member_id) VALUES (9, 2, 4);
INSERT INTO associations (course_id, role_id, member_id) VALUES (10, 5, 5);
INSERT INTO associations (course_id, role_id, member_id) VALUES (10, 4, 6);
INSERT INTO associations (course_id, role_id, member_id) VALUES (10, 3, 7);
INSERT INTO associations (course_id, role_id, member_id) VALUES (10, 3, 8);
INSERT INTO associations (course_id, role_id, member_id) VALUES (10, 2, 9);
INSERT INTO associations (course_id, role_id, member_id) VALUES (10, 2, 10);
INSERT INTO associations (course_id, role_id, member_id) VALUES (10, 2, 11);
INSERT INTO associations (course_id, role_id, member_id) VALUES (11, 5, 12);
INSERT INTO associations (course_id, role_id, member_id) VALUES (11, 4, 13);
INSERT INTO associations (course_id, role_id, member_id) VALUES (11, 3, 14);
INSERT INTO associations (course_id, role_id, member_id) VALUES (11, 3, 15);
INSERT INTO associations (course_id, role_id, member_id) VALUES (11, 2, 16);
INSERT INTO associations (course_id, role_id, member_id) VALUES (11, 2, 2);
INSERT INTO associations (course_id, role_id, member_id) VALUES (11, 2, 3);
INSERT INTO associations (course_id, role_id, member_id) VALUES (12, 5, 4);
INSERT INTO associations (course_id, role_id, member_id) VALUES (12, 4, 5);
INSERT INTO associations (course_id, role_id, member_id) VALUES (12, 3, 6);
INSERT INTO associations (course_id, role_id, member_id) VALUES (12, 3, 7);
INSERT INTO associations (course_id, role_id, member_id) VALUES (12, 2, 8);
INSERT INTO associations (course_id, role_id, member_id) VALUES (12, 2, 9);
INSERT INTO associations (course_id, role_id, member_id) VALUES (12, 2, 10);
INSERT INTO associations (course_id, role_id, member_id) VALUES (13, 5, 11);
INSERT INTO associations (course_id, role_id, member_id) VALUES (13, 4, 12);
INSERT INTO associations (course_id, role_id, member_id) VALUES (13, 3, 13);
INSERT INTO associations (course_id, role_id, member_id) VALUES (13, 3, 14);
INSERT INTO associations (course_id, role_id, member_id) VALUES (13, 2, 15);
INSERT INTO associations (course_id, role_id, member_id) VALUES (13, 2, 16);
INSERT INTO associations (course_id, role_id, member_id) VALUES (13, 2, 2);
INSERT INTO associations (course_id, role_id, member_id) VALUES (14, 5, 3);
INSERT INTO associations (course_id, role_id, member_id) VALUES (14, 4, 4);
INSERT INTO associations (course_id, role_id, member_id) VALUES (14, 3, 5);
INSERT INTO associations (course_id, role_id, member_id) VALUES (14, 3, 6);
INSERT INTO associations (course_id, role_id, member_id) VALUES (14, 2, 7);
INSERT INTO associations (course_id, role_id, member_id) VALUES (14, 2, 8);
INSERT INTO associations (course_id, role_id, member_id) VALUES (14, 2, 9);
INSERT INTO associations (course_id, role_id, member_id) VALUES (15, 5, 10);
INSERT INTO associations (course_id, role_id, member_id) VALUES (15, 4, 11);
INSERT INTO associations (course_id, role_id, member_id) VALUES (15, 3, 12);
INSERT INTO associations (course_id, role_id, member_id) VALUES (15, 3, 13);
INSERT INTO associations (course_id, role_id, member_id) VALUES (15, 2, 14);
INSERT INTO associations (course_id, role_id, member_id) VALUES (15, 2, 15);
INSERT INTO associations (course_id, role_id, member_id) VALUES (15, 2, 16);
INSERT INTO associations (course_id, role_id, member_id) VALUES (16, 5, 2);
INSERT INTO associations (course_id, role_id, member_id) VALUES (16, 4, 3);
INSERT INTO associations (course_id, role_id, member_id) VALUES (16, 3, 4);
INSERT INTO associations (course_id, role_id, member_id) VALUES (16, 3, 5);
INSERT INTO associations (course_id, role_id, member_id) VALUES (16, 2, 6);
INSERT INTO associations (course_id, role_id, member_id) VALUES (16, 2, 7);
INSERT INTO associations (course_id, role_id, member_id) VALUES (16, 2, 8);

-- Table: courses
DROP TABLE IF EXISTS courses;
CREATE TABLE IF NOT EXISTS courses (
	course_id INTEGER NOT NULL,
	course_name VARCHAR(64) NOT NULL,
	course_code VARCHAR(64) NOT NULL,
	course_group VARCHAR(64),
	course_key BLOB NOT NULL,
	course_desc VARCHAR(256),
	PRIMARY KEY (course_id),
	CONSTRAINT uq_course_name_code UNIQUE (course_name, course_code)
);
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (1, 'Introductory Programming', 'CMSC 115', 'CMSC', X'DA5140E58B2A3703041B5CB750C3389FB474732D99508C69885686065971E3517C1F062391C1960A8C', 'A study of structured and object-oriented programming using the Java language.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (2, 'Intermediate Programming', 'CMSC 215', 'CMSC', X'2B4CCA2A8D115B93761D74AAFB6949B89E30EF72D42D715F6C522B7F0B51E6A1DC572B2D75EF127A02', 'Further study of the Java programming language.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (3, 'Relational Database Concepts and Applications', 'CMSC 320', 'CMSC', X'227146D2ACC39080461BBC35B5F7FE17A650AB5A684AF08D76A732D0C892A743C3DC4D517AC8CB9346', 'A study of the functions, underlying concepts, and applications of enterprise relational database management systems (RDBMS) in a business environment.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (4, 'Capstone in Computer Science', 'CMSC 495', 'CMSC', X'5AB13B80BDEC08429CCACC507C6AC68F2815438FF6815F9A6797FE32D43227CD9AF59C099DF3C28BA4', 'An overview of computer technologies, with an emphasis on integration of concepts, practical application, and critical thinking.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (5, 'Building Secure Python Applications', 'SDEV 300', 'SDEV', X'0715766159650B673CC1A48ECC6FD51B697DBCF115A058A2DFDA3AC1AE1AF5C5C79D46D17022609DD6', 'A hands-on study of best practices and strategies for building secure Python desktop and web applications.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (6, 'Detecting Software Vulnerabilities', 'SDEV 325', 'SDEV', X'7AFAE3AF53BE6C72DB1C4591AB9277A5F86CD65B7D649629E6537966AE30325E4BCACA01D86901CE76', 'An in-depth, practical application of techniques and tools for detecting and documenting software vulnerabilities and risks.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (7, 'Database Security', 'SDEV 350', 'SDEV', X'B5D8B160751E19260E29A478A9D0DAD9A1C8B350A52427497A97381CBB71BEDCBD9A7F8108B4F3EE33', 'A study of processes and techniques for securing databases.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (8, 'Fundamentals of Computer Troubleshooting', 'CMIT 202', 'CMIT', X'B25F646F0FF4F4FBAECDC50C44F7FF83DE41C6792B8070B18479CC3D0B728EEFE0C3A2072135669611', 'A thorough review of computer hardware and software, with emphasis on the application of current and appropriate computing safety and environmental practices.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (9, 'Fundamentals of Networking', 'CMIT 265', 'CMIT', X'F80C67FC65C1CD4AF234890502FE81795F43519F4634939ADF718CD2DE9D896D74F371EAF89184125C', 'An introduction to networking technologies for local area networks, wide area networks, and wireless networks.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (10, 'Introduction to Linux', 'CMIT 291', 'CMIT', X'484953C3666CE927D72AFB26A207EB0F4B05CEF1BEF9DB94E5A7C86672440E8CC7736263E7F10AEA73', 'A study of the Linux operating system.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (11, 'Mathematics for Data Science', 'DATA 230', 'DATA', X'39DAF7C2238459290C715092543493397984AEC0A686F6B6A5FC7E3F0ADB9628DC10B14DB73571682F', 'A practical introduction to the mathematical principles applied within the context of data science.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (12, 'Foundations of Data Science', 'DATA 300', 'DATA', X'24149C157097B483BD56B72DC21687AD240962B865025D0DFAAD08B21B1A34B4A35D0E6530BE7C5190', 'An examination of the role of data science within business and society.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (13, 'Introduction to Data Analytics', 'DATA 320', 'DATA', X'4DF3ABD0E4C9EF822842F07A657BCC58946F20E88D01349552B5FEF6C88A003D4993872FDF51AEDE82', 'A practical introduction to the methodology, practices, and requirements of data science to ensure that data is relevant and properly manipulated to solve problems and address a variety of real-world projects and business scenarios.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (14, 'Cybersecurity for Leaders and Managers', 'CSIA 300', 'CSIA', X'06C3D6BFEC66A7A0C4103E6B7B728F1B78E41E95660566F929602D4ECED7DC114D7EC8F7C9DDB5F44B', 'A foundational study of cybersecurity principles, practices, and strategies in the establishment, management, and governance of an enterprise''s cybersecurity program.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (15, 'Cybersecurity Processes and Technologies', 'CSIA 310', 'CSIA', X'A82535743A2219DCE8C5EC7602094FCAA613E0769A63920F4007E9A190C38F3663F50EC60438E034A7', 'A study of the processes and technologies used to implement and manage enterprise IT security operations.');
INSERT INTO courses (course_id, course_name, course_code, course_group, course_key, course_desc) VALUES (16, 'Cybersecurity in Business and Industry', 'CSIA 350', 'CSIA', X'751821C669AFEF6012FE03707BAB1943530FDA4F410359067EAA13060748BDE14666C15C37015711D9', 'A study of the application and integration of cybersecurity principles, frameworks, standards, and best practices to the management, governance, and policy development processes for businesses.');

-- Table: members
DROP TABLE IF EXISTS members;
CREATE TABLE IF NOT EXISTS members (
	member_id INTEGER NOT NULL,
	member_name VARCHAR(64) NOT NULL,
	member_email VARCHAR(320) NOT NULL,
	member_group VARCHAR(256),
	password_hash VARCHAR(128) NOT NULL,
	is_admin BOOLEAN NOT NULL,
	PRIMARY KEY (member_id),
	UNIQUE (member_email)
);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (1, 'Admin', 'admin@tracker.com', 'admins', 'scrypt:32768:8:1$TPHjP3e5urHhQxCX$94fbf10ec7b7a5a8379210ba2136172423ee8869c38991a0e143cca065bc5da997d24f4537e059bbd53addf0bad11f90719a207d5198b9ac27229705c5d145ee', 1);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (2, 'Leto.Atreides', 'leto.atreides@atreides.com', 'atreides', 'scrypt:32768:8:1$k7SmljiwOWFdJDfT$fb24d0ff3da9f263c0be6e892f6968d851585f8c064cef38500db461c0db47a117e4680ec6c0cd46efc0daf148abee869af0dfdb4b94bce5ef5bfaf4c5add106', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (3, 'Paul.Atreides', 'paul.atreides@atreides.com', 'atreides, fremen', 'scrypt:32768:8:1$oTDu2i81wvOzSw1Y$f7b2f4ed6ad14178c1ec80f86a125e650bbdf50ae660c5de95e234d8c20e69baeed0a11a8fc2be61c8df5b079fa3c169b2d97f128c603bddf8d451f0911936ab', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (4, 'Jessica.Nerus', 'jessica.nerus@atreides.com', 'atreides, fremen', 'scrypt:32768:8:1$hyLkEQy1S04Gx0Kx$a5f878f20f76e0163ed387c199bd1a1c5f695cf266e4694a750c7ef75dfb3156b8687c23edb3c50da5492ad13d7c2c6f037d829d6fa35664fad5d6f4c1b100aa', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (5, 'Thufir.Hawat', 'thufir.hawat@atreides.com', 'atreides', 'scrypt:32768:8:1$kyPZ57noTtmXQRtX$3f2975d61c6652aab775412d98c588f46bfa59db4002f5655e75901ba7afcbfecc3527274a9b367af0ec3a221d886aa6a56c366aa812b6b2cfd7ccf455e2a802', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (6, 'Gurney.Halleck', 'gurney.halleck@atreides.com', 'atreides', 'scrypt:32768:8:1$fe7UK3fbqE7DS9aD$2a98e54d0ec8fac54f583dd78af01c99d91c19e6eb0545ed4152c1a75f4db3479954abd165b4ae005e13c7e86dd5d2913f72d5bd897dd3e095bf86845ec65155', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (7, 'Duncan.Idaho', 'duncan.idaho@atreides.com', 'atreides', 'scrypt:32768:8:1$adrPabnlzLVqFWEV$644b4b025aabb9ab1fa0928f3c31066e3b1ac204147e6ee1dfeee166cd21c604134b7653a5707750d0a657ad5c18ddf75db90773be9205583e620d42f17f6f44', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (8, 'Vladimir.Harkonnen', 'vladmir.harkonnen@harkonnen.com', 'harkonnen', 'scrypt:32768:8:1$Zh6Sn42OkhfUzMf1$4d0fc45c4e2ba8fd65bae775323bf608921d2d2d4664f9fe7e654216c7f01bb36b75f005e039b37bc1e19e4398eff6f404f2104cbefb4e3ef057fe98c1316536', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (9, 'Glossu.Rabban', 'glossu.rabban@harkonnen.com', 'harkonnen', 'scrypt:32768:8:1$OB057Capri5LauE4$61da5cf107dad37f12b0045b5660123a1d1b12fedb1fc652f2fdf744380882ec13f7492646ce92772f333fc5de950f6e5bc2e8e926f3dce843c097ae10811c57', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (10, 'Feyd-Rautha.Rabban', 'feyd-rautha.rabban@harkonnen.com', 'harkonnen', 'scrypt:32768:8:1$lV9z2p60IVxRooku$b88a6658b3f99e1d7ee5deb09cae899caf5f3442a83306f2aac3a89aad765bb0ea6bdf8f4b40efcaf35e726cfa167a49c6526ac8fa66443fa7574a3c0cf05e3f', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (11, 'Piter.DeVries', 'piter.devries@harkonnen.com', 'harkonnen', 'scrypt:32768:8:1$sSBdPOYcAHktRRPS$2a1ad11cde4118b79db7dcae9d1be8d75b2df928984b186b69b30678daffe66b29364ee0d7023c6453841e8ee57ad16c23f48fa16e2cbdff1b09dae28b329993', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (12, 'Shaddam.Corrino', 'shaddam.corrino@corrino.com', 'corrino', 'scrypt:32768:8:1$6R4beUdP7zxHdPEf$1ec95a4a5f14ee79136ab5c8e0253623b747cdd702f3d272fb69c99fecbe483617d89cd482ad66d1e7ab9e7cc50c70d986b4cc3ca75eb96222700910aa21253b', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (13, 'Irulan.Corrino', 'irulan.corrino@corrino.com', 'corrino', 'scrypt:32768:8:1$8iLiLzRBCanb7EAa$70582709e031870075d283605c9c3ca47e50f49752ed9bcfab75b25fbe0026947606d54a966fd472ad9aa7289f825f78c2046bbfd61ffb21c3fa075dbe5fc404', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (14, 'Liet.Kynes', 'liet.kynes@fremen.com', 'fremen', 'scrypt:32768:8:1$wWmc7bRFmeCtft8D$8f0d41704ed5cb8e8f70c0e84f9e0e063e3e6b31153d0a8feecf71ba80146735f4f2c4664785ddc114397d0a714457501736b6dc61adbfb1d9af26e57d337698', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (15, 'Chani.Kynes', 'chani.kynes@fremen.com', 'fremen, atreides', 'scrypt:32768:8:1$RSdXoW7hc2Z0esQ9$bd173195fbc0f94dae2b4577f23d821072fce25e8bb6a7341bc5f85409315659ecd3d009afda5ae51c5d302e106723006433a6d46d08833be2c683410fef303a', 0);
INSERT INTO members (member_id, member_name, member_email, member_group, password_hash, is_admin) VALUES (16, 'Stilgar.Tabr', 'stilgar.tabr@fremen.com', 'fremen, atreides', 'scrypt:32768:8:1$oas3xnujvxqQUpqv$4f84b4b648c11d15629a8e987bd800fe76b074267e0a885addc7c6dcd693d1b41db3f28d1907a9ecdbcd3fd114930eacfaa32ec1ca68ec1cf2dcb8474a7d3d98', 0);

-- Table: roles
DROP TABLE IF EXISTS roles;
CREATE TABLE IF NOT EXISTS roles (
	role_id INTEGER NOT NULL,
	role_name VARCHAR(64) NOT NULL,
	role_privilege INTEGER NOT NULL,
	PRIMARY KEY (role_id),
	UNIQUE (role_name),
	UNIQUE (role_privilege)
);
INSERT INTO roles (role_id, role_name, role_privilege) VALUES (2, 'Student', 1);
INSERT INTO roles (role_id, role_name, role_privilege) VALUES (3, 'Associate', 10);
INSERT INTO roles (role_id, role_name, role_privilege) VALUES (4, 'Teacher', 20);
INSERT INTO roles (role_id, role_name, role_privilege) VALUES (5, 'Chair', 30);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
