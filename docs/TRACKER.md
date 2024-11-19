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

The Foo Academy is a fictitious learning platform that allows its members to create and share online courses, and it needs a way for members to control access to their courses. The Tracker application on the Academy's website allows content creators and assistants to manage access to their online courses using a role-based access control (RBAC) system.

-----

### Desired Outcomes

As the site owner, I want to restrict membership creation to administrators and prevent anonymous users from creating profiles, so I can mitigate Sybil attacks and maintain the integrity of the user base.
As the site owner, I want anonymous users to complete a CAPTCHA form before requesting membership, so I can prevent email flooding attacks and ensure legitimate requests.
As the site owner, I want to limit course enrollment to eight members, so I can ensure optimal performance and prevent overwhelming IT resources.

As a site administrator, I want to be able to add new members to the Tracker application.
As a site administrator, I want to be able to view a member profile on the Tracker application.
As a site administrator, I want to be able to edit a member profile on the Tracker application.
As a site administrator, I want to be able to delete a member from the Tracker application.

As an Academy member, I want to be able to view my member profile on the Tracker application.
As an Academy member, I want to be able to edit my member profile on the Tracker application.
As an Academy member, I want to be able to add a course to the list of courses in the Tracker application.

As a content creator, I want to be able to view a list of my courses in the Tracker application.
As a content creator, I want to be able to view the details of any of my courses on the Tracker application.
As a content creator, I want to be able to edit the details of any of my courses on the Tracker application.
As a content creator, I want to be able to assign other members as editors of one or more of my courses through the Tracker application.
As a content creator, I want to be able to assign other members as teachers of one or more of my courses through the Tracker application.
As a content creator, I want to be able to assign other members as students of one or more of my courses through the Tracker application.
As a content creator, I want to be able to reassign editors, teachers, and students to other roles within one of my courses through the Tracker application.
As a content creator, I want to be able to remove editors, teachers, and students from any of my courses through the Tracker application.
As a content creator, I want to be able to delete any of my courses from the list of courses in the Tracker application.

As an editor, I want to be able to view a list of the courses assigned to me on the Tracker application.
As an editor, I want to be able to view the details of any course assigned to me on the Tracker application.
As an editor, I want to be able to edit the details of any course assigned to me on the Tracker application.
As an editor, I want to be able to assign other members as teachers of any course assigned to me through the Tracker application.
As an editor, I want to be able to assign other members as students of any course assigned to me through the Tracker application.
As an editor, I want to be able to reassign teachers to students and students to teachers within one of my courses through the Tracker application.
As an editor, I want to be able to remove teachers and students from any course assigned to me through the Tracker application.

As a teacher, I want to be able to view a list of the courses assigned to me on the Tracker application.
As a teacher, I want to be able to view the details of any course assigned to me on the Tracker application.
As a teacher, I want to be able to assign other members as students of any course assigned to me through the Tracker application.
As a teacher, I want to be able to remove students from any course assigned to me through the Tracker application.

As a student, I want to be able to view a list of the courses assigned to me on the Tracker application.
As a student, I want to be able to view the details of any courses assigned to me on the Tracker application.

-----

### Stakeholders

Interested parties throughout the company will benefit from the Tracker application.

| Stakeholder    | Value from Application |
| -------------- | ---------------------- |
| Members        | Control access to their courses. |
| Administrators |  |
| Foo Academy    |  |

-----

### Personas

| Persona | Value from Application |
| ----------- | ---------------------- |
| Creators | |
| Editors  | |
| Teacher  | |
| Students | |

-----

+-----------------------------------+
|     course                        |
+-----------------------------------+
| PK  course_id       INTEGER NN UQ |<---1:N---|
+-----------------------------------+          |
|     course_name     TEXT    NN UQ |          |
|     course_code     TEXT    NN UQ |          |
|     course_group    TEXT          |          |
|     course_desc     TEXT          |          |
+-----------------------------------+          |
                                               |
+-----------------------------------+          |
|     role                          |          |
+-----------------------------------+          |
| PK  role_id         INTEGER NN UQ |<---1:N---|
+-----------------------------------+          |
|     role_name       TEXT    NN UQ |          |
|     role_privilege  INTEGER NN UQ |          |
+-----------------------------------+          |
                                               |
+-----------------------------------+          |
|     user                          |          |
+-----------------------------------+          |
| PK  user_id         INTEGER NN UQ |<---1:N---|
+-----------------------------------+          |
|     user_name       TEXT    NN UQ |          |
|     user_email      TEXT    NN UQ |          |
|     user_is_flagged INTEGER NN    |          |
|     user_flagged_by TEXT          |          |
|     password_hash   TEXT    NN    |          |
+-----------------------------------+          |
                                               |
+-----------------------------------+          |
|     association                   |          |
+-----------------------------------+          |
| PK  course_id       INTEGER NN    | FK -|    |
| PK  role_id         INTEGER NN    | FK -|<---+ (ON DELETE CASCADE, ON UPDATE CASCADE)
| PK  user_id         INTEGER NN    | FK -|
+-----------------------------------+

-----

Roles:
Administrator: Can remove users
Creator: Delete a course
Editor: Edit a course
Teacher: Can view all students and assign them to classes
Student: View own course

Only administrators can create an account. You cannot create your own account. You must contact an administrator to create your account.

DAVE (delete, add, view, edit)

User(username='Admin', user_email='admin@example.com', is_admin=True, flagged_for_del=False, flagged_by=null)

To delete an administrator, another administrator must flag the account for deletion first. Once flagged for deletion, another administrator cna delete the account.

Delete any user: Admin
Delete myself: Self
Add a user: Admin
View a list of all users: Admin, Creator, Teacher
View any user profile: Admin
View my user profile: Self
Edit any user profile: Admin
Edit my user profile: Self

Delete any course: Admin
Delete my courses: Admin, Creator
Add a course: Self
View a list of all courses: Admin
View the details of any course: Admin
View a list of my courses: Admin, Creator, Teacher, Student
View the details of my courses: Admin, Creator, Teacher, Student
Edit any course: Admin
Edit my courses: Admin, Creator, Teacher

Assign a student to any course: Admin
Assign a student to my courses: Admin, Creator, Teacher
Remove a student from any course: Admin
Remove a student from my courses: Admin, Creator, Teacher
Assign a teacher to any course: Admin
Assign a teacher to my courses: Admin, Creator
Remove a teacher from any course: Admin
Remove a teacher from my courses: Admin, Creator, Teacher

Cannot remove myself from one of my course: Creator

The site administrator can delete, add, view, and edit user accounts.



Anyone with an account can create a course.
The creator can view, edit, and delete the course.
The creator can assign teachers and students to the course.
The creator can unassign teachers and students to the course.

The teachers can view and edit the course.
The teachers cannot delete the course.
The teachers can assign students to the course.
The teachers can unassign students to the course.
The teachers cannot assign a teacher to the course.
The teachers cannot unassign a teacher from the course.



I can create a credential. I can also view, assign, edit, and  delete the credential.
I can assign editors who can edit the credential, but editors cannot delete it.
I can assign viewers who can view the credential, but viewers cannot edit or delete it.
Editors can also assign or unassign viewers.


The Tracker application itself allows you to administer course access for students.

-----

## Roles

- ***Chair:*** Owns the course.
- ***Teacher:*** Can administer a course.
- ***Student:*** Can view a course.

## Administration

Course Administration:

- ***Add a Course:*** Anyone; the creator becomes the Chair of the Course
- ***View Courses:*** Chairs, Teachers, and Students who are assigned to the Courses
- ***View a Course:*** Chairs, Teachers, and Students who are assigned to the Course
- ***Edit a Course:*** Chairs and Teachers who are assigned to the Course
- ***Delete a Course:*** Chairs who are assigned to the Course

Role and User Administration: Administrators only.

Create a User database and view users
Add, view, edit, and delete a User

