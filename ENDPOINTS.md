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

## CRUD endpoints

## **0. Authentication and Permissions**
- **All endpoints require authentication.**
- **Only admin users** (`IsAdminUser` permission) can access these endpoints.
- **Token Authentication is used**, so requests must include:
```sh
curl -X GET "http://127.0.0.1:8000/protected-endpoint/" \
     -H "Authorization: Token <YOUR_AUTH_TOKEN>"
```

## **1. User API** (`UserViewSet`)

### **Endpoint:** `/users/`
**Description:**
- Allows **admin users** to view, create, update, and delete user accounts.
- Requires **admin privileges** (`IsAdminUser` permission).
- Supports **pagination** (`BasicPagination`).

### **Allowed Methods:**
```yaml
- GET /users/  # List all users (paginated)
- POST /users/  # Create a new user
- GET /users/{id}/  # Retrieve a specific user
- PUT /users/{id}/  # Update a user (full update)
- PATCH /users/{id}/  # Partially update a user
- DELETE /users/{id}/  # Delete a user
```

### **Example Request:**
```sh
curl -X GET "http://127.0.0.1:8000/users/" \
     -H "Authorization: Token <YOUR_AUTH_TOKEN>"
```

### **Example Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "snoop",
            "first_name": "Snoop",
            "last_name": "Dogg",
            "email": "snoop@snoop.com",
            "phone_number": "+639185550123",
            "role": "admin",
            "is_active": true
        },
    ]
}
```

---

## **2. Ride API** (`RideViewSet`)

### **Endpoint:** `/rides/`
**Description:**
- Allows **admin users** to view, create, update, and delete rides.
- Supports **filters**, **sorting**, and **distance annotation**.
- Supports **pagination** (`BasicPagination`).

### **Allowed Methods:**
```yaml
- GET /rides/  # List all rides (paginated, with optional filters)
- POST /rides/  # Create a new ride
- GET /rides/{id}/  # Retrieve a specific ride
- PUT /rides/{id}/  # Update a ride (full update)
- PATCH /rides/{id}/  # Partially update a ride
- DELETE /rides/{id}/  # Delete a ride
```

### **Filters:** (via query parameters)
```yaml
status: string  # Filter rides by status (case-sensitive). Must be in ['init', 'pickup', 'enroute', 'droppoff']
email: string  # Filter rides by rider email (case-insensitive) but must match whole string.
lat: float # Latitude coordinate of the driver presently.
lon: float  # Longitude coordinate of the driver presently.
sort_by: string  # Sort by `pickup_time` (default) or `distance`.
```

### **Example Request:**
```sh
curl -X GET "http://127.0.0.1:8000/rides/?status=init&email=johndoe@example.com&sort_by=distance" \
     -H "Authorization: Token <YOUR_AUTH_TOKEN>"
```

### **Example Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "status": "init",
            "rider": {
                "id": 4,
                "username": "missdaisy",
                "first_name": "Miss",
                "last_name": "Daisy",
                "email": "miss@daisy.com",
                "phone_number": "+639180876543",
                "role": "regular",
                "is_active": true
            },
            "driver": {
                "id": 3,
                "username": "speedracer",
                "first_name": "Speed",
                "last_name": "Racer",
                "email": "speed@racer.com",
                "phone_number": "+639189876543",
                "role": "regular",
                "is_active": true
            },
            "pickup_latitude": 10.352651,
            "pickup_longitude": 123.945389,
            "dropoff_latitude": 14.6091,
            "dropoff_longitude": 121.0223,
            "pickup_time": "2025-03-01T14:30:00Z",
            "distance": 11.059547836721924,
            "todays_ride_events": [
                {
                    "id": 1,
                    "ride": 1,
                    "description": "Burnout",
                    "created_at": "2025-03-02T11:38:37.356811Z",
                }
            ],
        }
    ]
}
```

---

## **3. Ride Event API** (`RideEventViewSet`)

### **Endpoint:** `/ride-events/`
**Description:**
- Allows **admin users** to view, create, update, and delete ride events.
- Supports **pagination** (`BasicPagination`).

### **Allowed Methods:**
```yaml
- GET /ride-events/  # List all ride events (paginated)
- POST /ride-events/  # Create a new ride event
- GET /ride-events/{id}/  # Retrieve a specific ride event
- PUT /ride-events/{id}/  # Update a ride event (full update)
- PATCH /ride-events/{id}/  # Partially update a ride event
- DELETE /ride-events/{id}/  # Delete a ride event
```

### **Example Request:**
```sh
curl -X GET "http://127.0.0.1:8000/ride-events/" \
     -H "Authorization: Token <YOUR_AUTH_TOKEN>"
```

### **Example Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 301,
      "ride": 1,
      "description": "Ride started",
      "created_at": "2025-03-01T14:31:00Z"
    }
  ]
}
```
