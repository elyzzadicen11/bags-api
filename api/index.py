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

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_bags_db():
  with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
    with conn.cursor() as cur:
      cur.execute("SELECT * FROM bags ORDER BY id;") # Database query, getting all da bags
      rows = cur.fetchall()
      
  return[Bags.model_validate(row).model_dump() for row in rows]      
      
      
API_KEYS = {
    "list": os.getenv("API_KEY_NOVA"),
    "comparison": os.getenv("API_KEY_TOTETELLY"),
    "personality": os.getenv("API_KEY_BAGITUP")
} 

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
# DATA MODEL
# Field para validation , Literal pag may options na fixed 
class Bags(BaseModel):
    id: int
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
    id: int
    name: Optional[str] = Field(min_length=1)
    brand: Optional[str] = Field(min_length=1)
    size: Optional[Literal["Mini", "Small", "Medium", "Large"]]
    material: Optional[str] = Field(min_length=1)
    rating: Optional[float]= Field(ge=0, le=5)
    price: Optional[float] = Field(gt=0)
    collection: Optional[str] = Field(min_length=1)
    shape: Optional[str] = Field(min_length=1)
    color: Optional[str] = Field(min_length=1)
    type: Optional[str] = Field(min_length=1)
    origin: Optional[str] = Field(min_length=1)
    availability: Optional[str]= Field(min_length=1)
    description: Optional[str] = Field(min_length=1)
    buyer_notes: Optional[str]= Field(min_length=1)

    strap_type: Optional[str] = Field(min_length=1)
    closure: Optional[str] = Field(min_length=1)
    compartments: Optional[int]
    water_resistant: Optional[bool]
    weight_g: Optional[int]      

#--------------------------------------------------------------------------------------------------------

# API KEY AUTHENTICATION
def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key not in API_KEYS.values(): #checking if API key is in API key list
        raise HTTPException(
            status_code=401,
            detail="invalid or missing API Key."
        )
    return True

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
@app.get("/api/v1/bags", dependencies = [Depends(verify_api_key)])
def get_bags():
  bags = get_bags_db()
  
  return {
        "count": len(bags),
        "bags": bags
    }

#--------------------------------------------------------------------------------------------------------

# SEARCH BAGS
@app.get("/api/v1/bags/search", dependencies=[Depends(verify_api_key)])
def search_bags(q: str = Query(..., min_length=1)):
    bags = get_bags_db()
    q = q.lower()
    results = []

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
        return {
            "query": q,
            "message": "No bags exist matching your search.",
            "count": 0,
            "results": []
        }

    return {
        "query": q,
        "count": len(results),
        "results": results
    }
#--------------------------------------------------------------------------------------------------------
  
# GET ONE BAG
@app.get("/api/v1/bags/{bag_id}", dependencies = [Depends(verify_api_key)]) #balikan mo toh elai
def get_bag(bag_id: int):
  bags = get_bags_db()
  for bag in bags:
        if bag["id"] == bag_id:
            return bag
  raise HTTPException(status_code=404, detail="Bag not found.")
#--------------------------------------------------------------------------------------------------------

# CREATE A NEW BAG (POST)
@app.post("/api/v1/bags", status_code=201, dependencies=[Depends(verify_api_key)]
)
def create_bag(bag: Bags):

    bag_data = bag.model_dump()

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO bags (
                        id, name, brand, size, material, rating, price,
                        collection, shape, color, type, origin, availability,
                        description, buyer_notes, strap_type, closure,
                        compartments, water_resistant, weight_g
                    )
                    VALUES (
                        %(id)s, %(name)s, %(brand)s, %(size)s, %(material)s,
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

    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A bag with this ID already exists."
        )

    return Bags.model_validate(created_bag).model_dump()

#--------------------------------------------------------------------------------------------------------

# UPDATE AN EXISTING BAG
@app.patch("/api/v1/bags/{bag_id}", status_code=200, dependencies=[Depends(verify_api_key)])
def update_bag(bag_id: int, bag: UpdateBags):

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
