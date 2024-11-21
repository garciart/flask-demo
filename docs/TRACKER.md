# Tracker

This demo is a feature-by-feature walkthrough of how to create and deploy a Flask application that allows you to control course assignments using role-based access control (RBAC).

![Assign Users to Course Screenshot](img/assign-users-screenshot.png)

-----

## Quick Start

To start:

1. Ensure you are using Python 3.8 or later: `python --version` or `python3 -V`. If not, install the latest version of Python available for your operating system.
2. Clone this repository: `git clone https://github.com/garciart/flask-demo`
3. Navigate to your copy of the repository (this will be your project directory): `cd flask-demo`
4. Create a Python virtual environment in the project directory: `python<version> -m venv $PWD/.venv`
5. Activate the Python virtual environment: `source .venv/bin/activate` (Linux) or `.venv/Scripts/activate` (Windows)
6. Install pip: `python -m pip install --upgrade pip`
7. Install required packages: `python -m pip install -r requirements.txt`
8. Each version of the **Tracker** application has its own package within your project directory:
   - Review the `README.md` file in the `tracker_01` package using an editor of your choice (`tracker_01/README.md`)
   - Run the application from the project directory using the directions in the `README.md` file: `python -B -m flask --app tracker_01 run`
   - Continue the next version.

-----

## Application Design

-----

### Business Problem

The Foo Academy is a fictitious learning platform that will allow users to upload and share online courses. The Academy would like an application to manage membership and course access.

Tracker is a user and course management system that will allow authenticated and authorized users to manage membership and course access
through a web-based user interface. It will also provide information to other authenticated and authorized applications in the Foo Academy ecosystem (website, mobile, etc.) through an application programming interface (API) service.

-----

### Requirements

- The application must store member information, including but not limited to username, email address, and password hash.
- The application must store course information, including but not limited to course number, course owner, and a list of students, teachers, and editors assigned to the course.
- The application must have an authentication system (e.g., token-based or session-based) that verifies member credentials before granting access to course and member information.
- The application must have a role-based access control (RBAC) system, with predefined roles (i.e., administrator, owner, editor, teacher, student) that restricts access to course and member information based on privilege level.
- The application must have a web-based front-end that allows authenticated members to directly add, assign, view, edit, and delete courses and other members based on privilege level.
- The application must have an application programming interface (API) that allows authenticated and authorized applications (web, mobile, etc.) to interact with the application for tasks like verifying member access, getting a list of courses, etc.
- The application must be secure and tested and analyzed for bugs, latency, and vulnerabilities (e.g., functional, performance, security, etc.) before deployment.
- The application must be able to be containerized and ran on-premise or on a cloud platform.

-----

### Desired Outcomes

An intuitive, secure, fully-functional, and easily-deployable membership and course access management system.

-----

### Stakeholders

Interested parties throughout the company who will benefit from the Tracker application:

| Stakeholder | Value from Application                                                                                                     |
| ----------- | -------------------------------------------------------------------------------------------------------------------------- |
| Foo Academy | Provides a single location to manage membership in real time.                                                              |
|             | Provides a location that is accessible from different types of devices.                                                    |
|             | Provides an API endpoint for other applications in the Foo Academy eco-system to access membership and course information. |
| Members     | Provides a single location to register courses and manage enrollment.                                                      |

-----

### Personas

Roles of the users who will interact with the Tracker application:

| Persona        | Privileges                                                                                            |
| -------------- | ----------------------------------------------------------------------------------------------------- |
| Administrator  | Can add, view, edit, and delete members.                                                              |
| Owner          | Can view, edit, and delete their courses, and assign members to a course up to their privilege level. |
| Editor         | Can view and edit courses assigned to them, and assign members up to their privilege level.           |
| Teacher        | Can view courses assigned to them, and assign members up to their privilege level.                    |
| Student        | Can view courses assigned to them.                                                                    |
| Member         | Can register courses.                                                                                 |
| Anonymous User | Can request access to the application.                                                                |

-----

### Inputs

Request Access Form
Login Form
Update Profile Form
Approve User Form
Add User Form
Edit User Form
Delete User Form
Add Course Form
Edit Course Form
Assign Users to Course Form
Delete Course Form

-----

### Outputs

List of Users (HTML)
List of Users (JSON/API)
User Details (HTML)
User Details (JSON/API)
List of Courses (HTML)
List of Courses (JSON/API)
Course Details (HTML)
Course Details (JSON/API)

-----

## User Stories

As an anonymous user, I want to be able to submit a request for membership through the Tracker application.

As a site administrator, I want anonymous users to complete a CAPTCHA form when creating a profile to mitigate Sybil attacks.
As a site administrator, I want to be able to approve membership requests.
As a site administrator, I want to be able to add new members.
As a site administrator, I want to be able to view member profiles.
As a site administrator, I want to be able to edit member profiles.
As a site administrator, I want to be able to delete members.

As an Academy member, I want to be able to view my member profile.
As an Academy member, I want to be able to edit my member profile.
As an Academy member, I want to be able to add a course to the list of available courses.
As an Academy member, I want to receive a notification if I have been reassigned or dropped from a course.

As a content creator, I want to be able to view a list of my courses.
As a content creator, I want to be able to view the details of my courses.
As a content creator, I want to be able to edit the details of my courses.
As a content creator, I want to be able to assign another member as an editor of one or more of my courses.
As a content creator, I want to be able to assign another member as a teacher of one or more of my courses.
As a content creator, I want to be able to assign another member as a student of one or more of my courses.
As a content creator, I want to be able to reassign an editor, teacher, or student of one or more of my courses to another role within the course.
As a content creator, I want to be able to remove an editor, teacher, or student from one or more of my courses.
As a content creator, I want to be able to delete any of my courses from the list of available courses.

As an editor, I want to be able to view a list of the courses assigned to me.
As an editor, I want to be able to view the details of any course assigned to me.
As an editor, I want to be able to edit the details of any course assigned to me.
As an editor, I want to be able to assign another member as a teacher of any course assigned to me.
As an editor, I want to be able to assign another member as a student of any course assigned to me.
As an editor, I want to be able to reassign a teacher or student of any course assigned to me to another role within the course.
As an editor, I want to be able to remove a teacher or student from any course assigned to me.

As a teacher, I want to be able to view a list of the courses assigned to me.
As a teacher, I want to be able to view the details of any course assigned to me.
As a teacher, I want to be able to assign another member as a student of any course assigned to me.
As a teacher, I want to be able to remove a student from any course assigned to me.

As a student, I want to be able to view a list of the courses assigned to me.
As a student, I want to be able to view the details of any courses assigned to me.

-----

## Database Schema

+-----------------------------------+
|     course                        |
+-----------------------------------+
| PK  course_id       INTEGER NN UQ |<----1:N----|
+-----------------------------------+            |
|     course_name     TEXT    NN UQ |            |
|     course_code     TEXT    NN UQ |            |
|     course_group    TEXT          |            |
|     course_desc     TEXT          |            |
+-----------------------------------+            |
                                                 |
+-----------------------------------+            |
|     role                          |            |
+-----------------------------------+            |
| PK  role_id         INTEGER NN UQ |<----1:N----|
+-----------------------------------+            |
|     role_name       TEXT    NN UQ |            |
|     role_privilege  INTEGER NN UQ |            |
+-----------------------------------+            |
                                                 |
+-------------------------------------+          |
|     user                            |          |
+-------------------------------------+          |
| PK  user_id           INTEGER NN UQ |<---1:N---|
+-------------------------------------+          |
|     user_name         TEXT    NN UQ |          |
|     user_email        TEXT    NN UQ |          |
|     user_is_approved  INTEGER NN    |          |
|     user_is_admin     INTEGER NN    |          |
|     user_is_flagged   INTEGER NN    |          |
|     user_flagged_by   TEXT          |          |
|     password_hash     TEXT    NN    |          |
+-------------------------------------+          |
                                                 |
+-----------------------------------+            |
|     association                   |            |
+-----------------------------------+            |
| PK  course_id       INTEGER NN    | FK -|      |
| PK  role_id         INTEGER NN    | FK -|<-----+ (ON DELETE CASCADE, ON UPDATE CASCADE)
| PK  user_id         INTEGER NN    | FK -|
+-----------------------------------+

-----

## Miscellaneous

- Only administrators can create an account. You cannot create your own account. You must contact an administrator to create your account.
- To delete an administrator, another administrator must flag the account for deletion first. Once flagged for deletion, another administrator cna delete the account.
- Owners cannot remove themselves from one of their course.
