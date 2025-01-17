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
