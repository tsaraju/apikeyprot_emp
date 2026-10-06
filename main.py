from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

app = FastAPI(title="Employee Management API")

# ---------------------------------------------------------
# 1. API Key Security Setup
# ---------------------------------------------------------
API_KEY = "super30-secret-key"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Dependency that validates the X-API-Key header."""
    if api_key is None:
        # Key not provided at all -> 401 Unauthorized
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Provide 'X-API-Key' header.",
        )
    if api_key != API_KEY:
        # Key provided but wrong -> 403 Forbidden
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key.",
        )
    return api_key


# ---------------------------------------------------------
# 2. Pydantic Models (validation)
# ---------------------------------------------------------
class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    department: str = Field(..., min_length=2, max_length=30)
    salary: float = Field(..., gt=0, description="Salary must be positive")
    age: int = Field(..., ge=18, le=65)


class EmployeeUpdate(BaseModel):
    """All fields optional — supports partial updates."""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, min_length=2, max_length=30)
    salary: Optional[float] = Field(None, gt=0)
    age: Optional[int] = Field(None, ge=18, le=65)


class EmployeeResponse(EmployeeCreate):
    id: int


# ---------------------------------------------------------
# 3. In-memory "database"
# ---------------------------------------------------------
employees_db: dict[int, dict] = {}
next_id: int = 1


# ---------------------------------------------------------
# 4. Endpoints
# ---------------------------------------------------------

# PUBLIC — anyone can list employees
@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees():
    return [{"id": emp_id, **data} for emp_id, data in employees_db.items()]


# PUBLIC — anyone can view a single employee
@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"id": employee_id, **employees_db[employee_id]}


# PROTECTED — create employee
@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    employee: EmployeeCreate,
    api_key: str = Security(verify_api_key),
):
    global next_id
    employees_db[next_id] = employee.model_dump()
    response = {"id": next_id, **employees_db[next_id]}
    next_id += 1
    return response


# PROTECTED — update employee (partial update supported)
@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    api_key: str = Security(verify_api_key),
):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Only update fields the client actually sent
    update_data = employee.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    employees_db[employee_id].update(update_data)
    return {"id": employee_id, **employees_db[employee_id]}


# PROTECTED — delete employee
@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    api_key: str = Security(verify_api_key),
):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    del employees_db[employee_id]
    return {"message": f"Employee {employee_id} deleted successfully"}