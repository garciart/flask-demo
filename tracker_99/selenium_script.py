"""Selenium Tester

Activate the virtual environment:
source .venv/bin/activate or .venv/Scripts/activate

Start the Flask application:
python -B -m flask --app "tracker_99:create_app(log_events=False)" run

Open a new terminal and navigate to the application directory:
cd tracker_99

Run the Selenium script:
python selenium_script.py
"""

from selenium import webdriver

driver = webdriver.Chrome()

tracker_pages = [
    'login',
    'oops',
    'doh',
    'about',
    'logout',
    'courses',
    'index',
    'members',
    'roles',
    'admin/add_course',
    'admin/add_member',
    'admin/add_role',
    'admin/assign_course/1',
    'admin/delete_course/1',
    'admin/delete_member/1',
    'admin/delete_role/1',
    'admin/edit_course/1',
    'admin/edit_member/1',
    'admin/edit_role/1',
    'admin/update_profile/1',
    'admin/view_course/1',
    'admin/view_member/1',
    'admin/view_role/1',
    'api/test',
    'api/members/all',
    'api/members/1',
    'api/members/1',
]

for t in tracker_pages:
    driver.get(f'http://127.0.0.1:5000/{t}')
    url = driver.current_url
    title = driver.title
    print(url, title)
