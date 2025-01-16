# API Notes

Tracker can provide information to other applications through API requests.

To make a request, an administrator or authorized member must first send a log in request to the application with their username and password:

```sh
curl --request POST --header "Content-Type: application/json" --data '{"username":"leto.atreides","password":"Change.Me.123"}' http://127.0.0.1:5000/api/login
```

The application will authenticate the requestor and return a JSON Web Token (JWT) or a message stating the credentials were invalid:

```txt
{"auth_token":"json.web.token","message":"Login successful."}
```

```txt
{"error":"Invalid credentials."}
```

Afterwards, the requestor will use the token to make API requests for information using the following format:

```sh
curl -X GET -H "Authorization: Bearer json.web.token" http://127.0.0.1:5000/api/courses/get/17
```

```txt
{"course":{"course_code":"FOO 101","course_desc":"An introduction to Foo.","course_group":"FOO","course_id":17,"course_name":"Intro to Foo"}}
```

-----

## Rules

- Administrators can add, view, edit, or delete any member.
- Members can only view their own member data.
- Members can only edit their own member data.
- Administrators can add, view, edit, or delete any course.
- Members can only view courses assigned to them.
- Members can only edit courses if they are assigned as a chair or teacher.
- Members can only delete courses if they are assigned as a chair.
- Only administrators can add, view, edit, or delete roles.

-----

## HTTP Methods Used

- `GET`: To view all items or a single item.
- `POST`: To add an item.
- `PUT`: To edit and item.
- `DELETE`: To delete an item.

-----

## API Endpoints

- /api/login - Get JSON WEb Token
- /api/courses/all - View all courses (Admin) or assigned courses
- /api/courses/add - Add a course
- /api/courses/get/<int:course_id> - View an assigned course
- /api/courses/edit/<int:course_id> - Edit an assigned course (if privileged)
- /api/courses/delete/<int:course_id> - Delete an assigned course (if privileged)
- /api/members/all - View all members (Admin only)
- /api/members/add - Add a member (Admin only)
- /api/members/get/<int:member_id> - View a member (Admin) or your own profile
- /api/members/edit/<int:member_id> - Edit a member (Admin) or your own profile
- /api/members/delete/<int:member_id> - Delete a member (Admin only)
