```bash
scs@fedora:~/fuseraft-demo-api/fakeapi$ ./start.sh 
==> FakeProd API
    Swagger UI : http://localhost:8000/docs
    ReDoc      : http://localhost:8000/redoc
    Bearer key : dev-secret-token-abc123

INFO:     Will watch for changes in these directories: ['/home/scs/fuseraft-demo-api/fakeapi']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [35074] using WatchFiles
INFO:     Started server process [35076]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:58528 - "GET /incidents HTTP/1.1" 200 OK
INFO:     127.0.0.1:58528 - "GET /users/003379a8 HTTP/1.1" 200 OK
INFO:     127.0.0.1:43152 - "GET /incidents HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:39384 - "GET /incidents HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:39394 - "GET /incidents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54036 - "GET /incidents HTTP/1.1" 200 OK
INFO:     127.0.0.1:54052 - "PATCH /incidents/INC-1004 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54058 - "PATCH /incidents/INC-1007 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54072 - "PATCH /incidents/INC-1009 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54078 - "PATCH /incidents/INC-1010 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54082 - "PATCH /incidents/INC-1014 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54098 - "GET /users/4863a6b9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54102 - "GET /users/4863a6b9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54112 - "GET /users/671b7c10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54120 - "GET /users/045729d0 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54126 - "GET /users/003379a8 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54128 - "GET /incidents/INC-1004 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36662 - "GET /incidents HTTP/1.1" 200 OK
INFO:     127.0.0.1:36664 - "PATCH /incidents/INC-1004 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36678 - "PATCH /incidents/INC-1007 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36682 - "PATCH /incidents/INC-1009 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36690 - "PATCH /incidents/INC-1010 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36700 - "PATCH /incidents/INC-1014 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36706 - "GET /users/4863a6b9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36712 - "GET /users/4863a6b9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36724 - "GET /users/671b7c10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36730 - "GET /users/045729d0 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36746 - "GET /users/003379a8 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36748 - "GET /incidents/INC-1004 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36748 - "GET /incidents/INC-1007 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36748 - "GET /incidents/INC-1009 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36748 - "GET /incidents/INC-1010 HTTP/1.1" 200 OK
INFO:     127.0.0.1:36748 - "GET /incidents/INC-1014 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53798 - "GET /incidents HTTP/1.1" 200 OK
INFO:     127.0.0.1:53800 - "PATCH /incidents/INC-1004 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53812 - "PATCH /incidents/INC-1007 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53828 - "PATCH /incidents/INC-1009 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53840 - "PATCH /incidents/INC-1010 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53850 - "PATCH /incidents/INC-1014 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53852 - "GET /users/4863a6b9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53858 - "GET /users/4863a6b9 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53866 - "GET /users/671b7c10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53872 - "GET /users/045729d0 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53884 - "GET /users/003379a8 HTTP/1.1" 200 OK
```