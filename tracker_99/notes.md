# Notes

-----

## Use Case

Web-based, role-based course look-up, accessible by all members

-----

## Guidelines

Ensure pyLint score is 10/10
Ensure all methods and functions have docstrings and type hints
Add comments as necessary for maintainability
Use constants.py file for easy modification important or repeated values
Ensure all browser functionality has an API equivalent
Use JSON Web Tokens (JWT) with 15-minute expiration
Ensure no SonarLint issues in preparation for integration with pipeline with quality gates
Include plain SQL in comments with SQLAlchemy code
Include example cURL and Invoke-WebRequest commands in API endpoint docstrings
Attempt to reach 100% code-coverage on unit tests (using PyTest and Coverage)

-----

Routes to check:

127.0.0.1:5000/login
127.0.0.1:5000/oops
127.0.0.1:5000/doh
127.0.0.1:5000/about
127.0.0.1:5000/logout
127.0.0.1:5000/courses
127.0.0.1:5000/index
127.0.0.1:5000/members
127.0.0.1:5000/roles
127.0.0.1:5000/admin/add_course
127.0.0.1:5000/admin/add_member
127.0.0.1:5000/admin/add_role
127.0.0.1:5000/admin/assign_course/1
127.0.0.1:5000/admin/delete_course/1
127.0.0.1:5000/admin/delete_member/1
127.0.0.1:5000/admin/delete_role/1
127.0.0.1:5000/admin/edit_course/1
127.0.0.1:5000/admin/edit_member/1
127.0.0.1:5000/admin/edit_role/1
127.0.0.1:5000/admin/update_profile/1
127.0.0.1:5000/admin/view_course/1
127.0.0.1:5000/admin/view_member/1
127.0.0.1:5000/admin/view_role/1
127.0.0.1:5000/api/test
127.0.0.1:5000/api/members/all
127.0.0.1:5000/api/members/1
127.0.0.1:5000/api/members/1

-----

127.0.0.1:5000/about
- Check if page appears
- Check that Return Home link redirects to Login page if anonymous
- Check that Return Home link redirects to Index page if authenticated

127.0.0.1:5000/oops
- Check if page appears
- Check that the Home link redirects to Login page if anonymous
- Check that the Home link redirects to Index page if authenticated

127.0.0.1:5000/doh
- Check if page appears
- Check that the Home link redirects to Login page if anonymous
- Check that the Home link redirects to Index page if authenticated

127.0.0.1:5000/login
- Check if page appears
- Submit empty fields
- Submit wrong username
- Submit wrong password
- Submit SQL injection
- Submit correct credentials

127.0.0.1:5000/index
- Check if page appears
- Check if changing the number of entries per page works
- Check if sorting by name, ID, code, group, and description work
- Check if searching for a course works
- Check if the action links (View, Assign, Edit, Delete) work
- Check if menu links (Home, Add Course, Add Member, View Courses, View Members, View Roles, Update Profile, Log Out, and About) work


127.0.0.1:5000/logout
127.0.0.1:5000/courses

127.0.0.1:5000/members
127.0.0.1:5000/roles
127.0.0.1:5000/admin/add_course
127.0.0.1:5000/admin/add_member
127.0.0.1:5000/admin/add_role
127.0.0.1:5000/admin/assign_course/1
127.0.0.1:5000/admin/delete_course/1
127.0.0.1:5000/admin/delete_member/1
127.0.0.1:5000/admin/delete_role/1
127.0.0.1:5000/admin/edit_course/1
127.0.0.1:5000/admin/edit_member/1
127.0.0.1:5000/admin/edit_role/1
127.0.0.1:5000/admin/update_profile/1
127.0.0.1:5000/admin/view_course/1
127.0.0.1:5000/admin/view_member/1
127.0.0.1:5000/admin/view_role/1
127.0.0.1:5000/api/test
127.0.0.1:5000/api/members/all
127.0.0.1:5000/api/members/1
127.0.0.1:5000/api/members/1

INVALID_NAME_MSG = (
    'Names must Be at least 3 characters long, start with a letter, '
    + 'and contain only letters, numbers, periods, underscores, and dashes.'
)
INVALID_PASSWORD_MSG = (
    'Password and keys must be between 8-15 characters long, '
    + 'contain at least one uppercase letter, one lowercase letter, and one number.'
)
INVALID_TEXT_MSG = (
    'Text fields must Be at least 3 characters long, start with a letter or number, '
    + 'and contain only letters, numbers, periods, underscores, dashes, and spaces.'
)

Attempt to add the following:
Course Name: fo
Course Code: 2

Attempt to add an existing course:
