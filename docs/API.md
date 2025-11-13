# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

TODO: Add authentication documentation

## Endpoints

### Health Checks

#### GET /health
Liveness probe - checks if service is running.

**Response**
```json
{
  "status": "healthy"
}
```

#### GET /ready
Readiness probe - checks if service can handle requests.

**Response**
```json
{
  "status": "ready"
}
```

### Users

#### GET /api/v1/users
List all users with pagination.

**Query Parameters**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 100)

**Response**
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
]
```

#### POST /api/v1/users
Create a new user.

**Request Body**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe"
}
```

**Response** (201 Created)
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

#### GET /api/v1/users/{user_id}
Get user by ID.

**Response**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### Items

#### GET /api/v1/items
List all items with pagination.

**Query Parameters**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 100)

**Response**
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "MacBook Pro",
    "owner_id": 1,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
]
```

#### POST /api/v1/items
Create a new item.

**Request Body**
```json
{
  "name": "Laptop",
  "description": "MacBook Pro"
}
```

**Response** (201 Created)
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "MacBook Pro",
  "owner_id": 1,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

#### GET /api/v1/items/{item_id}
Get item by ID.

**Response**
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "MacBook Pro",
  "owner_id": 1,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Interactive Documentation

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc
