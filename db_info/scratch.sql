-- SQLite

-- INSERT INTO users (username, user_email, password_hash) VALUES ('Alia.Atreides', 'alia@atreides.com', 'scrypt:32768:8:1$rm5c2IUumuLmjBrJ$5d862e073daf741363183a74476119272b8115991ff89b275ee443138b178b8eec5cda98a4025577e609ad0ec481349c6e40fb5a4848c6b2b774149093463d2c');
SELECT * FROM users WHERE username='Alia.Atreides';
SELECT user_email FROM users WHERE username LIKE 'Alia%';
UPDATE users SET username = 'Alia.Idaho' WHERE username='Alia.Atreides';
UPDATE users SET username = 'Alia.Atreides' WHERE username='Alia.Idaho';
DELETE FROM users WHERE username='Alia.Atreides';