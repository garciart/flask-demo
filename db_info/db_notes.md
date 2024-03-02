# Database Notes

## Get a list of all courses

```sql
SELECT courses.course_id, course_name, course_code, course_desc from courses
```

## Get a list of all courses and their teachers

```sql
SELECT courses.course_id, course_name, course_code, course_desc, username from associations
JOIN courses ON courses.course_id = associations.course_id
JOIN users ON users.user_id = associations.user_id
WHERE associations.role_id = 2
```

## Get courses based on user_id

```sql
SELECT courses.course_id, course_name, course_code, course_desc, role_name from associations
JOIN courses ON courses.course_id = associations.course_id
JOIN roles ON roles.role_id = associations.role_id
WHERE associations.user_id = 8
```

## Pass; can edit based on ID and Role

```sql
SELECT courses.course_id, course_name, course_code, course_desc from associations
JOIN courses ON courses.course_id = associations.course_id
WHERE associations.user_id = 2 AND associations.course_id = 1 AND associations.role_id = 2
```

## Pass, but cannot edit based on ID and Role

```sql
SELECT courses.course_id, course_name, course_code, course_desc from associations
JOIN courses ON courses.course_id = associations.course_id
WHERE associations.user_id = 2 AND associations.course_id = 8 AND associations.role_id = 3
```

## Fail based on ID and Role

```sql
SELECT courses.course_id, course_name, course_code, course_desc from associations
JOIN courses ON courses.course_id = associations.course_id
WHERE associations.user_id = 2 AND associations.course_id = 1 AND associations.role_id = 3
```
