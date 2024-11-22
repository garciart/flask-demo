# Application Design

-----

## Business Problem

The Foo Academy is a fictitious learning platform that will allow users to upload and share online courses. The Academy would like an application to manage membership and course access.

Tracker is a user and course management system that will allow authenticated and authorized users to manage membership and course access
through a web-based user interface. It will also provide information to other authenticated and authorized applications in the Foo Academy ecosystem (website, mobile, etc.) through an application programming interface (API) service.

-----

## Requirements

- The application must store member information, including but not limited to username, email address, and password hash.
- The application must store course information, including but not limited to course number, course owner, and a list of students, teachers, and editors assigned to the course.
- The application must have an authentication system (e.g., token-based or session-based) that verifies member credentials before granting access to course and member information.
- The application must have a role-based access control (RBAC) system, with predefined roles (i.e., administrator, owner, editor, teacher, student) that restricts access to course and member information based on privilege level.
- The application must have a web-based front-end that allows authenticated members to directly add, assign, view, edit, and delete courses and other members based on privilege level.
- The application must have an application programming interface (API) that allows authenticated and authorized applications (web, mobile, etc.) to interact with the application for tasks like verifying member access, getting a list of courses, etc.
- The application must be secure and tested and analyzed for bugs, latency, and vulnerabilities (e.g., functional, performance, security, etc.) before deployment.
- The application must be able to be containerized and ran on-premise or on a cloud platform.

-----

## Desired Outcomes

A fully-functional, easy-to-use, secure, and easily-deployable membership and course access management system that is updated in real time and is accessible from different types of devices.

-----

## Stakeholders

Interested parties who will benefit from the Tracker application:

| Stakeholder | Value from Application                                                                                                     |
| ----------- | -------------------------------------------------------------------------------------------------------------------------- |
| Foo Academy | Provides a single location to manage membership in real time from different types of devices.                              |
|             | Provides an API endpoint for other applications in the Foo Academy eco-system to access membership and course information. |
| Members     | Provides a single location to register courses and manage enrollment.                                                      |

-----

## Personas

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

## Inputs

| Page | Authentication Required | Description |
| ----- | ----- | ----- |
| Login Form | No | Default page for unauthenticated users. Accepts and checks credentials before allowing access to Tracker features and content. |
| Add Course Form | Yes | Allows members to add a course to the list of available courses. |
| Assign Users to Course Form | Yes | Allows course owners, editors, and teachers to assign other members to one of their courses. |
| Edit Course Form | Yes | Allows course owners and editors to edit information about one of their courses. |
| Delete Course Form | Yes | Allows course owners to remove a course from the list of available courses |
| Update Profile Form | Yes | Allows members to update their email address and password. |
| Add User Form | Yes | Allows administrators to directly add members without a request for membership. |
| Edit User Form | Yes | Allows administrators to edit member profiles. |
| Delete User Form | Yes | Allows administrators to remove member access to Tracker features and content. |
| Request Membership Form | No | Accepts requests for membership in the Foo Academy from anonymous users. |
| Approve User Form | Yes | Allows administrators to approve requests for membership in the Foo Academy from anonymous users. |

-----

## Outputs

| Page | Authentication Required | Description |
| ----- | ----- | ----- |
| List of Current Courses (Web UI) | Yes | Landing page for authenticated members. Displays a sortable and searchable list of courses owned and assigned by a member, with links to add, view, assign, edit, and delete courses. |
| List of Current Courses (API) | Yes | Displays a list of courses owned and assigned by a member in JSON format. |
| View Course Details (Web UI) | Yes | Display the details of a course, like course number and description. |
| View Course Details (API) | Yes | Display the details of a course, like course number and description, in JSON format. |
| List of Available Courses (Web UI) | Yes | Displays a list of available courses and owner details, like email address. |
| List of Available Courses (API) | Yes | Displays a list of available courses and owner details, like email address, in JSON format. |
| List of Users (Web UI) | Yes | Displays a sortable and searchable list of members in the Foo Academy, with links to add, edit, and delete users. |
| List of Users (API) | Yes | Display a list of users and their details in JSON format. |
| View User Profile (Web UI) | Yes | Display the details of a user, like username and email. |
| View User Profile (API) | Yes | Display the details of a user, like username and email, in JSON format. |
| About Page | No | Provides a description of the Foo Academy and the Tracker application. |

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

> **NOTES:**
>
> - Only administrators can create an account. You cannot create your own account. You must contact an administrator to create your account.
> - To delete an administrator, another administrator must flag the account for deletion first. Once flagged for deletion, another administrator cna delete the account.
> - Only owners, editors, and teachers can assign members to a course. Members cannot assign themselves to a course and must request access via email.
> - Owners cannot remove themselves from one of their course.

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
