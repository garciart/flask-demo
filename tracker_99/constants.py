"""Values used throughout the application that will remain constant
regardless of the configuration used.
"""

COURSES_PAGE = 'main_bp.courses'

# Only members with role_privileges greater than or equal to 10,
# like chairs and teachers of the course and admins, can edit a course
CUTOFF_PRIVILEGE_EDITOR = 10
# Only members with role_privileges greater than or equal to 20,
# like chairs of the course and admins, can edit a course
CUTOFF_PRIVILEGE_OWNER = 20

EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$'

INDEX_PAGE = 'main_bp.index'
INVALID_EMAIL_MSG = 'Email address already exists.'
INVALID_NAME_MSG = (
    'Names must Be at least 3 characters long, start with a letter, '
    + 'and contain only letters, numbers, periods, underscores, and dashes.'
)
INVALID_PASSWORD_MSG = (
    'Password must be between 8-15 characters long, '
    + 'contain at least one uppercase letter, one lowercase letter, and one number.'
)
INVALID_TEXT_MSG = (
    'Text fields must Be at least 3 characters long, start with a letter or number, '
    + 'and contain only letters, numbers, periods, underscores, dashes, and spaces.'
)
LOGIN_PAGE = 'auth_bp.login'
MEMBERS_PAGE = 'main_bp.index'

# Member names must:
# - Start with a letter
# - Contain only letters, numbers, underscores, and periods
# - Be at least 3 characters long
NAME_REGEX = r'^[A-Za-z][A-Za-z0-9\.\_\-]{2,}$'

NOT_AUTH_MSG = 'You do not have permission to perform that action.'
NOT_FOUND_MSG = 'No courses found.'
PASSWORD_FIELD_LABEL = 'Repeat Password'

# Ensure the password meets validation criteria:
# - A minimum of eight characters
# - A maximum of fifteen characters
# - At least one uppercase letter, one lowercase letter and one number
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,15}$'

ROLES_PAGE = 'main_bp.roles'

# Text fields must:
# - Start with a letter or number
# - Contain only letters, numbers, periods, underscores, dashes, and spaces
# - Be at least 3 characters long
TEXT_REGEX = r'^[A-Za-z0-9][A-Za-z0-9 \.\_\-]{2,}$'
