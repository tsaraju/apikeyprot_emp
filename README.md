API Key Protected Employee API

Create an Employee Management API where certain endpoints are protected using an API key.

Example

GET /employees

POST /employees

PUT /employees/{employee_id}

DELETE /employees/{employee_id}

For protected endpoints, expect a header such as

X-API-Key: super30-secret-key

If the API key is missing or incorrect, return an appropriate 401/403 response. Add Pydantic validation for employee data.

Sample Output:
(.venv) PS F:\Euron\GitHub\api\apikeyprot_emp> uv run uvicorn main:app --reload                                                                         
INFO:     Will watch for changes in these directories: ['F:\\Euron\\GitHub\\api\\apikeyprot_emp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [16040] using StatReload
INFO:     Started server process [14684]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:61570 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:61570 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:61682 - "GET /employees HTTP/1.1" 200 OK
INFO:     127.0.0.1:56028 - "POST /employees HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:55814 - "POST /employees HTTP/1.1" 403 Forbidden
INFO:     127.0.0.1:57314 - "POST /employees HTTP/1.1" 201 Created
INFO:     127.0.0.1:56836 - "GET /employees HTTP/1.1" 200 OK
INFO:     127.0.0.1:64612 - "POST /employees HTTP/1.1" 201 Created
INFO:     127.0.0.1:64915 - "GET /employees HTTP/1.1" 200 OK
INFO:     127.0.0.1:53183 - "GET /employees/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:62594 - "PUT /employees/2 HTTP/1.1" 200 OK
INFO:     127.0.0.1:63223 - "GET /employees HTTP/1.1" 200 OK
INFO:     127.0.0.1:62240 - "DELETE /employees/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52522 - "GET /employees HTTP/1.1" 200 OK
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [14684]
INFO:     Stopping reloader process [16040]