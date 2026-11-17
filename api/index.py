import os
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Literal
from pathlib import Path
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")
API_KEYS = {
    "list": os.getenv("API_KEY_NOVA"),
    "comparison": os.getenv("API_KEY_TOTETELLY"),
    "personality": os.getenv("API_KEY_BAGITUP")
} 

#For guest and logged in user testing
TEST_ACCOUNT = os.getenv("TEST_ACCOUNT")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("ENGKKKK wrong.")
    
serializer = URLSafeTimedSerializer(SECRET_KEY)
bearer_scheme = HTTPBearer(auto_error=False)


API_VERSION = "1.0"

app = FastAPI(
    title="Bags",
    description="A beginner-friendly REST API containing simple information about bags.",
    version= API_VERSION #balikan mo toh elai
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#FUNCTIONS
def get_bags_db():
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM bags ORDER BY id;")
                rows = cur.fetchall()

        return [Bags.model_validate(row).model_dump() for row in rows]
    # Database connection failure
    except psycopg.OperationalError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to the database.")
    #Database query or operation failure.
    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed.")

#--------------------------------------------------------------------------------------------------------

def create_bag_db(bag):
    bag_data = bag.model_dump()

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO bags (
                        name, brand, size, material, rating, price,
                        collection, shape, color, type, origin, availability,
                        description, buyer_notes, strap_type, closure,
                        compartments, water_resistant, weight_g
                    )
                    VALUES (
                        %(name)s, %(brand)s, %(size)s, %(material)s,
                        %(rating)s, %(price)s, %(collection)s, %(shape)s,
                        %(color)s, %(type)s, %(origin)s, %(availability)s,
                        %(description)s, %(buyer_notes)s, %(strap_type)s,
                        %(closure)s, %(compartments)s, %(water_resistant)s,
                        %(weight_g)s
                    )
                    RETURNING *;
                    """,
                    bag_data
                )

                created_bag = cur.fetchone()

        return Bags.model_validate(created_bag).model_dump()

    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A bag with this ID already exists."
        )

    except psycopg.OperationalError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to the database."
        )

    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed."
        )

 #--------------------------------------------------------------------------------------------------------
def update_bag_db(bag_id, bag):
    # Get only the fields submitted by the client
    bag_data = bag.model_dump(exclude_unset=True)

    # Check if the client submitted anything to update
    if not bag_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update."
        )

    # Generate the SQL SET statements
    set_update = ", ".join(
        f"{field} = %({field})s" for field in bag_data
    )

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    UPDATE bags
                    SET {set_update}
                    WHERE id = %(bag_id)s
                    RETURNING *;
                    """,
                    {**bag_data, "bag_id": bag_id}
                )

                updated_bag = cur.fetchone()

    except psycopg.OperationalError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to the database."
        )

    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Database update failed."
        )

    # Check if the requested ID exists
    if updated_bag is None:
        raise HTTPException(
            status_code=404,
            detail="Bag not found."
        )

    return Bags.model_validate(updated_bag).model_dump()

 #--------------------------------------------------------------------------------------------------------

def delete_bag_db(bag_id):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM bags WHERE id = %(bag_id)s RETURNING *;",
                    {"bag_id": bag_id}
                )

                deleted_bag = cur.fetchone()

    except psycopg.OperationalError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to the database."
        )

    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Deleting record failed."
        )

    # Check if the requested ID exists
    if deleted_bag is None:
        raise HTTPException(
            status_code=404,
            detail="Bag does not exist."
        )

    return Bags.model_validate(deleted_bag).model_dump()

 #--------------------------------------------------------------------------------------------------------

# DATA MODEL
# Field para validation , Literal pag may options na fixed 
class Bags(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=1)
    brand: str = Field(min_length=1)
    size: Literal["Mini", "Small", "Medium", "Large"]
    material: str = Field(min_length=1)
    rating: float = Field(ge=0, le=5)
    price: float = Field(gt=0)
    collection: str = Field(min_length=1)
    shape: str = Field(min_length=1)
    color: str = Field(min_length=1)
    type: str = Field(min_length=1)
    origin: str = Field(min_length=1)
    availability: str = Field(min_length=1)
    description: str = Field(min_length=1)
    buyer_notes: str = Field(min_length=1)

    strap_type: str = Field(min_length=1)
    closure: str = Field(min_length=1)
    compartments: int
    water_resistant: bool
    weight_g: int

class UpdateBags(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    brand: Optional[str] = Field(default=None, min_length=1)
    size: Optional[Literal["Mini", "Small", "Medium", "Large"]] = None
    material: Optional[str] = Field(default=None, min_length=1)
    rating: Optional[float]= Field(default=None, ge=0, le=5)
    price: Optional[float] = Field(default=None, gt=0)
    collection: Optional[str] = Field(default=None, min_length=1)
    shape: Optional[str] = Field(default=None, min_length=1)
    color: Optional[str] = Field(default=None, min_length=1)
    type: Optional[str] = Field(default=None, min_length=1)
    origin: Optional[str] = Field(default=None, min_length=1)
    availability: Optional[str]= Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    buyer_notes: Optional[str]= Field(default=None, min_length=1)

    strap_type: Optional[str] = Field(default=None, min_length=1)
    closure: Optional[str] = Field(default=None, min_length=1)
    compartments: Optional[int] = None
    water_resistant: Optional[bool] = None
    weight_g: Optional[int] = None   

#GUEST AND LOGGED IN USER TESTING
class LoginRequest(BaseModel):
    username: str
    password: str

#--------------------------------------------------------------------------------------------------------

# API KEY AUTHENTICATION
def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    for website, api_key in API_KEYS.items():
        if api_key and x_api_key == api_key:
            return website
        
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key.")

#--------------------------------------------------------------------------------------------------------

def verify_optional_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
):
    # No token means the visitor is a guest
    if not credentials:
        return False

    token = credentials.credentials

    try:
        user = serializer.loads(token, max_age=3600)

        if user.get("username") != TEST_ACCOUNT:
            raise HTTPException(
                status_code=401,
                detail="Invalid login session."
            )

        return True

    except SignatureExpired:
        raise HTTPException(
            status_code=401,
            detail="Login session expired. Please log in again."
        )

    except BadSignature:
        raise HTTPException(
            status_code=401,
            detail="Invalid login session."
        )

def check_access(website: str, is_admin: bool):
    if is_admin:
        return True
    if website == "list":
        return "limited"
    if website == "comparison":
        return False
    if website == "personality":
        return False
    return False

# CHECKING USER ACCESS
def verify_user_access(
    website: str = Depends(verify_api_key),
    is_admin: bool = Depends(verify_optional_admin)
):
    access = check_access(website, is_admin)

    if access is False:
        raise HTTPException(
            status_code=403,
            detail="Login is required to access this feature."
        )

    return access
#--------------------------------------------------------------------------------------------------------

# HOME
@app.get("/")
def home():

    return {
        "message": "Welcome to the Bag Retailer API!",
        "endpoints": [
            "/bags",
            "/bags/{id}",
            "/bags/search"
        ]
    }

#-----------------------------------------------------------------------------
#HEALTH CHECK (Public)
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Simple Bag API",
        "version": API_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
#-----------------------------------------------------------------------------

# GET ALL BAGS (Protected)
@app.get("/api/v1/bags")
def get_bags(access: str = Depends(verify_user_access)):
    bags = get_bags_db()

    # Nova guests can only see the first 5 bags
    if access == "limited":
        bags = bags[:5]

    return {
        "count": len(bags),
        "bags": bags
    }
#--------------------------------------------------------------------------------------------------------

# SEARCH BAGS
@app.get("/api/v1/bags/search")
def search_bags(q: str = Query(..., min_length=1), access: str = Depends(verify_user_access)):
    bags = get_bags_db()
    if access == "limited":
        bags = bags[:5]
        
    q = q.lower()
    results = []
    try: 
        for bag in bags:
            searchable_text = (
                f"{bag['name']} "
                f"{bag['brand']} "
                f"{bag['size']} "
                f"{bag['material']} "
                f"{bag['collection']} "
                f"{bag['shape']} "
                f"{bag['color']} "
                f"{bag['type']} "
                f"{bag['origin']}"
            ).lower()
    
            if q in searchable_text:
                results.append(bag)
    
        if not results:
            raise HTTPException(
                status_code=404,
                detail="Bag does not exist.")
    
        return {
            "query": q,
            "count": len(results),
            "results": results
        }
    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Deleting record failed."
        )
#--------------------------------------------------------------------------------------------------------
  
# GET ONE BAG
@app.get("/api/v1/bags/{bag_id}")
def get_bag(bag_id: int,access: str = Depends(verify_user_access)):
    if access == "limited":
        raise HTTPException(
            status_code=403,
            detail="Please log in to view bag details."
        )

    bags = get_bags_db()

    for bag in bags:
        if bag["id"] == bag_id:
            return bag

    raise HTTPException(
        status_code=404,
        detail="Bag not found."
    )
#--------------------------------------------------------------------------------------------------------

# CREATE A NEW BAG (POST)
@app.post("/api/v1/bags", status_code=201)
def create_bag(bag: Bags,access: str = Depends(verify_user_access)
):
    if access is not True:
        raise HTTPException(
            status_code=403,
            detail="Admin login is required to add bags."
        )

    return create_bag_db(bag)

#--------------------------------------------------------------------------------------------------------

# UPDATE AN EXISTING BAG
@app.patch("/api/v1/bags/{bag_id}", status_code=200)
def update_bag(bag_id: int,bag: UpdateBags,access: str = Depends(verify_user_access)):
    if access is not True:
        raise HTTPException(
            status_code=403,
            detail="Admin login is required to update bags."
        )

    return update_bag_db(bag_id, bag)
  

#--------------------------------------------------------------------------------------------------------
@app.delete("/api/v1/bags/{bag_id}", status_code=200)
def delete_bag(bag_id: int, access: str = Depends(verify_user_access)):
    if access is not True:
        raise HTTPException(
            status_code=403,
            detail="Admin login is required to delete bags."
        )

    return delete_bag_db(bag_id)
#--------------------------------------------------------------------------------------------------------

#GUEST AND LOGGED IN USER TESTING
@app.post("/api/v1/login")
def login(credentials: LoginRequest, website: str = Depends(verify_api_key)):
    if credentials.username != TEST_ACCOUNT or credentials.password != TEST_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password. Please try again."
        )
    token = serializer.dumps({"username": credentials.username})
    return{
        "message": "Login successful.",
        "access_token": token,
        "token_type": "bearer"
    }
