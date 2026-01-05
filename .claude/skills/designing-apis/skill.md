---
name: designing-apis
description: Knowledge and patterns for designing RESTful and GraphQL APIs.
---

# Designing APIs Skill

This skill provides patterns and best practices for API design.

## REST API Design

### URL Structure
```
# Resources (nouns, plural)
GET    /users              # List users
POST   /users              # Create user
GET    /users/{id}         # Get user
PUT    /users/{id}         # Update user
DELETE /users/{id}         # Delete user

# Nested resources
GET    /users/{id}/orders  # User's orders
POST   /users/{id}/orders  # Create order for user

# Actions (when CRUD doesn't fit)
POST   /users/{id}/activate
POST   /orders/{id}/cancel
```

### HTTP Methods
| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Read resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

### Status Codes
| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Authenticated but not allowed |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate, version conflict |
| 422 | Unprocessable | Valid format, invalid data |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Error | Server error |

### Request/Response Format

#### Request
```json
POST /users
Content-Type: application/json
Authorization: Bearer <token>

{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user"
}
```

#### Success Response
```json
HTTP/1.1 201 Created
Content-Type: application/json

{
  "data": {
    "id": "usr_123",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Error Response
```json
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### Pagination
```json
GET /users?page=2&limit=20

{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": true
  }
}
```

### Filtering & Sorting
```
GET /users?status=active&role=admin
GET /users?created_at_gte=2024-01-01
GET /users?sort=created_at:desc
GET /users?fields=id,name,email
```

### Versioning
```
# URL versioning
GET /v1/users
GET /v2/users

# Header versioning
Accept: application/vnd.api+json;version=1
```

## GraphQL Design

### Schema Design
```graphql
type User {
  id: ID!
  email: String!
  name: String!
  orders: [Order!]!
  createdAt: DateTime!
}

type Order {
  id: ID!
  user: User!
  items: [OrderItem!]!
  total: Decimal!
  status: OrderStatus!
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

type Query {
  user(id: ID!): User
  users(filter: UserFilter, pagination: PaginationInput): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): UserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UserPayload!
}
```

### Input Types
```graphql
input CreateUserInput {
  email: String!
  name: String!
  role: UserRole = USER
}

input UserFilter {
  status: UserStatus
  role: UserRole
  searchTerm: String
}

input PaginationInput {
  first: Int
  after: String
  last: Int
  before: String
}
```

### Connections (Pagination)
```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

## Authentication

### JWT
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Keys
```
X-API-Key: sk_live_...
```

### OAuth 2.0 Flows
- Authorization Code (web apps)
- PKCE (mobile/SPA)
- Client Credentials (service-to-service)

## Rate Limiting
```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640000000
Retry-After: 60
```

## API Documentation

### OpenAPI Example
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
```

## Best Practices

1. **Use consistent naming** - snake_case or camelCase, pick one
2. **Version your API** - Plan for breaking changes
3. **Validate input** - Never trust client data
4. **Use proper status codes** - Be specific and consistent
5. **Document everything** - Include examples
6. **Rate limit** - Protect your service
7. **Use HTTPS** - Always
8. **Handle errors gracefully** - Provide useful messages
