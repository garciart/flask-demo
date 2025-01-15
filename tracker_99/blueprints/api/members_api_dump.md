# Members API Dump

```txt
curl --request POST --header "Content-Type: application/json" --data '{"username":"admin","password":"Change.Me.321"}' http://127.0.0.1:5000/api/login

{"auth_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA","message":"Login successful."}

curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA" http://127.0.0.1:5000/api/members/all

{"members":[{"is_admin":true,"member_email":"admin@tracker.com","member_id":1,"member_name":"Admin"},{"is_admin":false,"member_email":"leto.atreides@atreides.com","member_id":2,"member_name":"Leto.Atreides"},{"is_admin":false,"member_email":"paul.atreides@atreides.com","member_id":3,"member_name":"Paul.Atreides"},{"is_admin":false,"member_email":"jessica.nerus@atreides.com","member_id":4,"member_name":"Jessica.Nerus"},{"is_admin":false,"member_email":"thufir.hawat@atreides.com","member_id":5,"member_name":"Thufir.Hawat"},{"is_admin":false,"member_email":"gurney.halleck@atreides.com","member_id":6,"member_name":"Gurney.Halleck"},{"is_admin":false,"member_email":"duncan.idaho@atreides.com","member_id":7,"member_name":"Duncan.Idaho"},{"is_admin":false,"member_email":"vladmir.harkonnen@harkonnen.com","member_id":8,"member_name":"Vladimir.Harkonnen"},{"is_admin":false,"member_email":"glossu.rabban@harkonnen.com","member_id":9,"member_name":"Glossu.Rabban"},{"is_admin":false,"member_email":"feyd-rautha.rabban@harkonnen.com","member_id":10,"member_name":"Feyd-Rautha.Rabban"},{"is_admin":false,"member_email":"piter.devries@harkonnen.com","member_id":11,"member_name":"Piter.DeVries"},{"is_admin":false,"member_email":"shaddam.corrino@corrino.com","member_id":12,"member_name":"Shaddam.Corrino"},{"is_admin":false,"member_email":"irulan.corrino@corrino.com","member_id":13,"member_name":"Irulan.Corrino"},{"is_admin":false,"member_email":"liet.kynes@fremen.com","member_id":14,"member_name":"Liet.Kynes"},{"is_admin":false,"member_email":"chani.kynes@fremen.com","member_id":15,"member_name":"Chani.Kynes"},{"is_admin":false,"member_email":"stilgar.tabr@fremen.com","member_id":16,"member_name":"Stilgar.Tabr"}]}

curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA" -H "Content-Type: application/json" -d '{"member_name": "foo.bar", "member_email": "foo.bar@foo.com", "is_admin": false, "password": "Change.Me.123"}' http://localhost:5000/api/members/add

{"message":"POST: Successfully added foo.bar (17)."}

curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA" http://127.0.0.1:5000/api/members/get/17

{"member":{"is_admin":false,"member_email":"foo.bar@foo.com","member_id":17,"member_name":"foo.bar"}}

curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA" http://127.0.0.1:5000/api/members/all

{"members":[{"is_admin":true,"member_email":"admin@tracker.com","member_id":1,"member_name":"Admin"},{"is_admin":false,"member_email":"leto.atreides@atreides.com","member_id":2,"member_name":"Leto.Atreides"},{"is_admin":false,"member_email":"paul.atreides@atreides.com","member_id":3,"member_name":"Paul.Atreides"},{"is_admin":false,"member_email":"jessica.nerus@atreides.com","member_id":4,"member_name":"Jessica.Nerus"},{"is_admin":false,"member_email":"thufir.hawat@atreides.com","member_id":5,"member_name":"Thufir.Hawat"},{"is_admin":false,"member_email":"gurney.halleck@atreides.com","member_id":6,"member_name":"Gurney.Halleck"},{"is_admin":false,"member_email":"duncan.idaho@atreides.com","member_id":7,"member_name":"Duncan.Idaho"},{"is_admin":false,"member_email":"vladmir.harkonnen@harkonnen.com","member_id":8,"member_name":"Vladimir.Harkonnen"},{"is_admin":false,"member_email":"glossu.rabban@harkonnen.com","member_id":9,"member_name":"Glossu.Rabban"},{"is_admin":false,"member_email":"feyd-rautha.rabban@harkonnen.com","member_id":10,"member_name":"Feyd-Rautha.Rabban"},{"is_admin":false,"member_email":"piter.devries@harkonnen.com","member_id":11,"member_name":"Piter.DeVries"},{"is_admin":false,"member_email":"shaddam.corrino@corrino.com","member_id":12,"member_name":"Shaddam.Corrino"},{"is_admin":false,"member_email":"irulan.corrino@corrino.com","member_id":13,"member_name":"Irulan.Corrino"},{"is_admin":false,"member_email":"liet.kynes@fremen.com","member_id":14,"member_name":"Liet.Kynes"},{"is_admin":false,"member_email":"chani.kynes@fremen.com","member_id":15,"member_name":"Chani.Kynes"},{"is_admin":false,"member_email":"stilgar.tabr@fremen.com","member_id":16,"member_name":"Stilgar.Tabr"},{"is_admin":false,"member_email":"foo.bar@foo.com","member_id":17,"member_name":"foo.bar"}]}

curl -X PUT -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA" -H "Content-Type: application/json" -d '{"is_admin": true, "password": "Change.Me.999"}' http://localhost:5000/api/members/edit/17

{"message":"PUT: Successfully updated foo.bar ."}

curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA" http://127.0.0.1:5000/api/members/get/17

{"member":{"is_admin":true,"member_email":"foo.bar@foo.com","member_id":17,"member_name":"foo.bar"}}

curl -X PUT -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA" -H "Content-Type: application/json" -d '{"is_admin": false, "password": "Change.Me.123"}' http://localhost:5000/api/members/edit/17

{"message":"PUT: Successfully updated foo.bar ."}

curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA" http://127.0.0.1:5000/api/members/get/17

{"member":{"is_admin":false,"member_email":"foo.bar@foo.com","member_id":17,"member_name":"foo.bar"}}

curl -X DELETE -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA" http://127.0.0.1:5000/api/members/delete/17

{"message":"PUT: Successfully deleted foo.bar ."}

curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA" http://127.0.0.1:5000/api/members/get/17

{"error":"404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."}

curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIwODEyMjQsImlhdCI6MTczNjg5NzIyNCwic3ViIjoiMSJ9.dAbkhTkli4B96WBCridEgtvYYjFUFyMXn9uDC1qCQFA" http://127.0.0.1:5000/api/members/all

{"members":[{"is_admin":true,"member_email":"admin@tracker.com","member_id":1,"member_name":"Admin"},{"is_admin":false,"member_email":"leto.atreides@atreides.com","member_id":2,"member_name":"Leto.Atreides"},{"is_admin":false,"member_email":"paul.atreides@atreides.com","member_id":3,"member_name":"Paul.Atreides"},{"is_admin":false,"member_email":"jessica.nerus@atreides.com","member_id":4,"member_name":"Jessica.Nerus"},{"is_admin":false,"member_email":"thufir.hawat@atreides.com","member_id":5,"member_name":"Thufir.Hawat"},{"is_admin":false,"member_email":"gurney.halleck@atreides.com","member_id":6,"member_name":"Gurney.Halleck"},{"is_admin":false,"member_email":"duncan.idaho@atreides.com","member_id":7,"member_name":"Duncan.Idaho"},{"is_admin":false,"member_email":"vladmir.harkonnen@harkonnen.com","member_id":8,"member_name":"Vladimir.Harkonnen"},{"is_admin":false,"member_email":"glossu.rabban@harkonnen.com","member_id":9,"member_name":"Glossu.Rabban"},{"is_admin":false,"member_email":"feyd-rautha.rabban@harkonnen.com","member_id":10,"member_name":"Feyd-Rautha.Rabban"},{"is_admin":false,"member_email":"piter.devries@harkonnen.com","member_id":11,"member_name":"Piter.DeVries"},{"is_admin":false,"member_email":"shaddam.corrino@corrino.com","member_id":12,"member_name":"Shaddam.Corrino"},{"is_admin":false,"member_email":"irulan.corrino@corrino.com","member_id":13,"member_name":"Irulan.Corrino"},{"is_admin":false,"member_email":"liet.kynes@fremen.com","member_id":14,"member_name":"Liet.Kynes"},{"is_admin":false,"member_email":"chani.kynes@fremen.com","member_id":15,"member_name":"Chani.Kynes"},{"is_admin":false,"member_email":"stilgar.tabr@fremen.com","member_id":16,"member_name":"Stilgar.Tabr"}]}
```