---
arguments:
- description: What the API is for (e.g., 'user management', 'product catalog', 'blog
    posts')
  name: api_purpose
  required: true
- description: Optional description of expected parameters/fields for the API resource
  name: expected_parameters
  required: false
- description: Optional custom API reference code to use as the structure template
    instead of the default
  name: custom_api_reference
  required: false
- description: Whether to generate test cases for the API (default is yes - tests will be created unless explicitly set to no)
  name: include_tests
  required: false
description: Assists developers in creating a FastAPI-based API following best practices
  with Pydantic models, database abstraction, and CRUD endpoints
name: create_api
keywords:
- api
- fastapi
- rest
- crud
- endpoints
- create
- build
- generate
- backend
- server
- database
- student
- user
- management
- information
- storage
- web service
triggers:
- "create api"
- "build api"
- "generate api"
- "create rest api"
- "build backend"
- "create endpoints"
- "student information"
- "user management"
- "api for storing"
- "api for managing"
---

You are an expert FastAPI developer. Create a complete REST API based on the following requirements:

**API Purpose**: {{api_purpose}}

{% if expected_parameters %}
**Expected Parameters**: {{expected_parameters}}
{% endif %}

Please generate a complete FastAPI application following the structure and patterns shown in this reference implementation:

{% if custom_api_reference %}
## Custom Reference Implementation

```python
{{custom_api_reference}}
```
{% else %}
## Default Reference Implementation (User Management API)

```python
from fastapi import FastAPI, HTTPException, Depends, Query, Path, Body, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict
from uuid import uuid4

app = FastAPI()

# Models
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, description="User's name")
    email: EmailStr = Field(...)
    is_active: bool = Field(default=True)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: str

# In-memory DB abstraction
class UserDB:
    def __init__(self):
        self.users: Dict[str, User] = {}

    def list(self, skip: int = 0, limit: int = 10, active: Optional[bool] = None) -> List[User]:
        users = list(self.users.values())
        if active is not None:
            users = [u for u in users if u.is_active == active]
        return users[skip:skip+limit]

    def get(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def create(self, user: UserCreate) -> User:
        user_id = str(uuid4())
        new_user = User(id=user_id, **user.dict())
        self.users[user_id] = new_user
        return new_user

    def update(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        user = self.users.get(user_id)
        if not user:
            return None
        updated_data = user.dict()
        update_fields = user_update.dict(exclude_unset=True)
        updated_data.update(update_fields)
        updated_user = User(**updated_data)
        self.users[user_id] = updated_user
        return updated_user

    def delete(self, user_id: str) -> bool:
        return self.users.pop(user_id, None) is not None

# Dependency
def get_db():
    return db

db = UserDB()

# Exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

# Endpoints
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: UserDB = Depends(get_db)):
    # Unique email check
    if any(u.email == user.email for u in db.users.values()):
        raise HTTPException(status_code=400, detail="Email already registered")
    return db.create(user)

@app.get("/users", response_model=List[User])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    active: Optional[bool] = Query(None),
    db: UserDB = Depends(get_db)
):
    return db.list(skip=skip, limit=limit, active=active)

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str = Path(...), db: UserDB = Depends(get_db)):
    user = db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user_update: UserUpdate, db: UserDB = Depends(get_db)):
    user = db.update(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: UserDB = Depends(get_db)):
    if not db.delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return

# Example usage:
# uvicorn sample_api:app --reload
```
{% endif %}

## Instructions

Using the reference implementation above as a template, create a new API for the specified purpose. Follow these key patterns from the reference:

### 1. Analyze the Reference Structure
- Identify the main resource model and its fields
- Note the model inheritance patterns (Base, Create, Update, Response models)
- Observe the database class structure and methods
- Study the endpoint patterns and HTTP methods used
- Notice validation rules, error handling, and business logic

### 2. Adapt the Pattern for Your Domain
- Replace the resource name with your specified API purpose
- Adapt field names and types to match your domain requirements
- Maintain the same model inheritance structure
- Keep similar database class methods but adapt for your data
- Update endpoint paths and variable names accordingly

### 3. Key Features to Preserve
- Proper HTTP status codes and error handling
- Dependency injection patterns
- Input validation and business rule checks
- Query parameters for filtering and pagination
- Exception handling with meaningful error messages
- Response model specifications
- Proper use of Pydantic models and FastAPI features

### 4. Domain-Specific Adaptations
{% if expected_parameters %}
- Incorporate the specified expected parameters: {{expected_parameters}}
{% endif %}
- Add appropriate validation rules for your domain
- Include relevant business logic and constraints
- Ensure field types match your data requirements
- Add domain-specific filtering and query options

### 5. Complete Implementation
Generate a complete, working FastAPI application that:
- Follows the exact structural patterns from the reference
- Is fully adapted for your specified domain
- Includes all CRUD operations
- Has proper error handling and validation
- Contains example usage comments
- Is ready to run with `uvicorn filename:app --reload`

Make sure the generated API maintains the same quality and completeness as the reference implementation while being perfectly suited for your specified use case.

{% if include_tests != "no" %}
## 6. Test Generation

Additionally, create comprehensive test cases for the API using pytest and FastAPI's TestClient. Include:

- Test fixtures for the database and FastAPI app
- Unit tests for all CRUD operations
- Validation testing for input data
- Error handling tests (404, 400, etc.)
- Edge cases and boundary conditions
- Integration tests for complete workflows

Generate tests following this structure:

```python
import pytest
from fastapi.testclient import TestClient
from your_api_module import app, get_db, YourDBClass

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_db():
    return YourDBClass()

@pytest.fixture
def override_db(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    yield test_db
    app.dependency_overrides.clear()

# Include comprehensive test cases for all endpoints
```

Make sure tests cover:
- All HTTP methods and endpoints
- Valid and invalid request data
- Database state verification
- Response format validation
- Status code verification
{% endif %}