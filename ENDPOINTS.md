# Endpoints
## Auth-related endpoints
### Signup
Signup for a non-super user on http://localhost:8000/auth/signup/ . Django server must be up and running.

### Login
Request:
```
curl --request POST \
  --url http://localhost:8000/auth/login/ \
  --header 'Content-Type: multipart/form-data' \
  --header 'User-Agent: insomnia/10.3.0' \
  --form username=<username> \
  --form password=<password>
```

Response:
```
"{"token":"<YOUR_AUTH_TOKEN>"}"
```

### Logout
Request:
```
curl --request DELETE \
  --url http://localhost:8000/auth/logout/ \
  --header 'Authorization: Token <YOUR_AUTH_TOKEN>' \
  --header 'User-Agent: insomnia/10.3.0'
```

Response:
```
{ Union["Invalid token", "...logged out", "Goodbye"] }
```
