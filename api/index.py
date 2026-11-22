import os
import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Path as PathParam
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Literal
from pathlib import Path
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pwdlib import PasswordHash
import secrets

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
password_hasher = PasswordHash.recommended()

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
                        compartments, water_resistant, weight_g, image_url
                    )
                    VALUES (
                        %(name)s, %(brand)s, %(size)s, %(material)s,
                        %(rating)s, %(price)s, %(collection)s, %(shape)s,
                        %(color)s, %(type)s, %(origin)s, %(availability)s,
                        %(description)s, %(buyer_notes)s, %(strap_type)s,
                        %(closure)s, %(compartments)s, %(water_resistant)s,
                        %(weight_g)s, %(image_url)s
                    )
                    RETURNING *;
                    """,
                    bag_data
                )

                created_bag = cur.fetchone()

        return {
            "message": "Bag added successfully!",
            "bag": Bags.model_validate(created_bag).model_dump()
        }

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
        
    return {
        "message": "Updated bag successfully!",
        "bag": Bags.model_validate(updated_bag).model_dump()
    }

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

    return {
        "message": "Deleted bag successfully!",
        "bag": Bags.model_validate(deleted_bag).model_dump()
       }


#--------------------------------------------------------------------------------------------------------
       
# USER ACCCOUNTS 

def create_user_db(username, password, role):
    hashed_password = password_hasher.hash(password)

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (username, password_hash, role)
                    VALUES (%s, %s, %s)
                    RETURNING user_id, username, role, created_at;
                    """,
                    (username, hashed_password, role)
                )

                return cur.fetchone()

    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Username already exists."
        )

    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed."
        )

#--------------------------------------------------------------------------------------------------------

def get_user_db(username):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT user_id, username, password_hash, role
                    FROM users
                    WHERE username = %s;
                    """,
                    (username,)
                )

                return cur.fetchone()

    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed."
        )


#--------------------------------------------------------------------------------------------------------
# WISHLIST DATABASE FUNCTIONS
# ADD TO WISHLIST
def add_to_wishlist_db(user_id, bag_id):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO wishlist (user_id, bag_id)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id, bag_id) DO NOTHING
                    RETURNING wishlist_id, user_id, bag_id, added_at;
                    """,
                    (user_id, bag_id)
                )

                result = cur.fetchone()

                if result is None:
                    raise HTTPException(
                        status_code=409,
                        detail="This bag is already in your wishlist."
                    )

                return result

    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(
            status_code=404,
            detail="Bag not found."
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
# GET WISHLIST
def get_wishlist_db(user_id):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        w.wishlist_id,
                        w.added_at,
                        b.*
                    FROM wishlist w
                    JOIN bags b ON w.bag_id = b.id
                    WHERE w.user_id = %s
                    ORDER BY w.added_at DESC;
                    """,
                    (user_id,)
                )

                return cur.fetchall()

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
# REMOVE FROM WISHLIST
def remove_from_wishlist_db(user_id, bag_id):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM wishlist
                    WHERE user_id = %s AND bag_id = %s
                    RETURNING wishlist_id, bag_id;
                    """,
                    (user_id, bag_id)
                )

                result = cur.fetchone()

                if result is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Bag not found in your wishlist."
                    )

                return result

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
#SHOP CART STUFF
def add_to_cart_db(user_id, bag_id):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:

                # Create a cart if the user doesn't have one
                cur.execute(
                    """
                    INSERT INTO cart (user_id)
                    VALUES (%s)
                    ON CONFLICT (user_id) DO NOTHING;
                    """,
                    (user_id,)
                )

                # Get the user's cart ID to add items to the cart
                cur.execute(
                    """
                    SELECT cart_id
                    FROM cart
                    WHERE user_id = %s;
                    """,
                    (user_id,)
                )

                cart_id = cur.fetchone()["cart_id"]

                # Add bag or increase its quantity if already present
                cur.execute(
                    """
                    INSERT INTO cart_items (cart_id, bag_id, quantity)
                    VALUES (%s, %s, 1)
                    ON CONFLICT (cart_id, bag_id)
                    DO UPDATE SET quantity = cart_items.quantity + 1
                    RETURNING cart_item_id, cart_id, bag_id, quantity, added_at;
                    """,
                    (cart_id, bag_id)
                )

                return cur.fetchone()

    except psycopg.errors.ForeignKeyViolation:
        raise HTTPException(
            status_code=404,
            detail="Bag not found."
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
#============================================================================================================= 
def get_cart_db(user_id):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:

                # Get all items in the user's cart
                cur.execute(
                    """
                    SELECT
                        ci.cart_item_id,
                        ci.cart_id,
                        ci.bag_id,
                        ci.quantity,
                        ci.added_at,
                        b.*
                    FROM cart c
                    JOIN cart_items ci ON c.cart_id = ci.cart_id
                    JOIN bags b ON ci.bag_id = b.id
                    WHERE c.user_id = %s
                    ORDER BY ci.added_at DESC;
                    """,
                    (user_id,)
                )

                return cur.fetchall()

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

#==================================================================================================
def update_cart_item_db(user_id, bag_id, quantity):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:

                # Update the quantity of a bag in the user's cart
                cur.execute(
                    """
                    UPDATE cart_items ci
                    SET quantity = %s
                    FROM cart c
                    WHERE ci.cart_id = c.cart_id
                      AND c.user_id = %s
                      AND ci.bag_id = %s
                    RETURNING ci.cart_item_id, ci.cart_id, ci.bag_id, ci.quantity, ci.added_at;
                    """,
                    (quantity, user_id, bag_id)
                )

                result = cur.fetchone()

                if result is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Bag not found in cart."
                    )

                return result

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

#================================================================================================================
#Multiple select deletion H
def remove_from_cart_db(user_id, bag_ids):
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:

                # Remove selected bags from the user's cart
                cur.execute(
                    """
                    DELETE FROM cart_items ci
                    USING cart c
                    WHERE ci.cart_id = c.cart_id
                      AND c.user_id = %s
                      AND ci.bag_id = ANY(%s)
                    RETURNING ci.cart_item_id, ci.bag_id;
                    """,
                    (user_id, bag_ids)
                )

                result = cur.fetchall()

                if not result:
                    raise HTTPException(
                        status_code=404,
                        detail="No matching bags found in cart."
                    )

                return result

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
#VERIFICATION STUFF UNDER HERE
# API KEY AUTHENTICATION
def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    for website, api_key in API_KEYS.items():
        if api_key and x_api_key == api_key:
            return website
        
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key.")

#--------------------------------------------------------------------------------------------------------


# VERIFY OPTIONAL USER LOGIN
def verify_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
):
    # No token means the visitor is a guest
    if not credentials:
        return None

    token = credentials.credentials

    try:
        user = serializer.loads(token, max_age=3600)

        if not all(key in user for key in ("user_id", "username", "role")):
            raise HTTPException(
                status_code=401,
                detail="Invalid login session."
            )

        return user

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

# VERIFY REQUIRED USER LOGIN
def verify_required_user(
    current_user: Optional[dict] = Depends(verify_optional_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Please log in to access this feature."
        )

    return current_user

#--------------------------------------------------------------------------------------------------------

# CHECKING USER ACCESS
def check_access(website: str, is_admin: bool):
    if is_admin:
        return True

    return "limited"


def verify_user_access(
    website: str = Depends(verify_api_key),
    current_user: Optional[dict] = Depends(verify_optional_user)
):
    is_admin = (
        current_user is not None
        and current_user["role"] == "admin"
    )

    access = check_access(website, is_admin)

    if access is False:
        raise HTTPException(
            status_code=403,
            detail="Login is required to access this feature."
        )

    return access

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
    image_url: Optional[str] = None

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
    image_url: Optional[str] = None

#GUEST AND LOGGED IN USER TESTING
class LoginRequest(BaseModel):
    username: str
    password: str

class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)

class CartItemsDelete(BaseModel):
    bag_ids: list[int] = Field(min_length=1)
    
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


# GET ALL BAGS
@app.get("/api/v1/bags")
def get_bags(access: str = Depends(verify_user_access)):
    bags = get_bags_db()

    return {
        "count": len(bags),
        "bags": bags
    }

#--------------------------------------------------------------------------------------------------------


# SEARCH BAGS
@app.get("/api/v1/bags/search")
def search_bags(
    q: str = Query(..., min_length=1),
    access: str = Depends(verify_user_access)
):
    bags = get_bags_db()

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
                detail="Bag does not exist."
            )

        return {
            "query": q,
            "count": len(results),
            "results": results
        }

    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Searching record failed."
        )

#--------------------------------------------------------------------------------------------------------
  

# GET ONE BAG
@app.get("/api/v1/bags/{bag_id}")
def get_bag(
    bag_id: int,
    access: str = Depends(verify_user_access)
):
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

    user = get_user_db(credentials.username)

    if user is None or not password_hasher.verify(
        credentials.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password. Please try again."
        )

    token = serializer.dumps({
        "user_id": user["user_id"],
        "username": user["username"],
        "role": user["role"]
    })

    return {
        "message": "Login successful.",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"]
        }
    }

#--------------------------------------------------------------------------------------------------------
# WISHLIST ENDPOINTS
# ADD TO WISHLIST
@app.post("/api/v1/wishlist/{bag_id}", status_code=201)
def add_to_wishlist(
    bag_id: int = PathParam(..., ge=1),
    website: str = Depends(verify_api_key),
    current_user: dict = Depends(verify_required_user)
):
    result = add_to_wishlist_db(
        current_user["user_id"],
        bag_id
    )

    return {
        "message": "Bag added to wishlist successfully!",
        "wishlist": result
    }


# VIEW WISHLIST
@app.get("/api/v1/wishlist")
def get_wishlist(
    website: str = Depends(verify_api_key),
    current_user: dict = Depends(verify_required_user)
):
    wishlist = get_wishlist_db(current_user["user_id"])

    return {
        "count": len(wishlist),
        "wishlist": wishlist
    }


# REMOVE FROM WISHLIST
@app.delete("/api/v1/wishlist/{bag_id}")
def remove_from_wishlist(
    bag_id: int = PathParam(..., ge=1),
    website: str = Depends(verify_api_key),
    current_user: dict = Depends(verify_required_user)
):
    result = remove_from_wishlist_db(
        current_user["user_id"],
        bag_id
    )

    return {
        "message": "Bag removed from wishlist successfully!",
        "wishlist": result
    }

#--------------------------------------------------------------------------------------------------------
# ADD TO CART ENDPOINTS

#GET  CART
@app.get("/api/v1/cart")
def get_cart(
    website: str = Depends(verify_api_key),
    current_user: dict = Depends(verify_required_user)
):
    cart = get_cart_db(current_user["user_id"])

    return {
        "count": len(cart),
        "cart": cart
    }

# ADD TO CART
@app.post("/api/v1/cart/{bag_id}", status_code=201)
def add_to_cart(
    bag_id: int = PathParam(..., ge=1),
    website: str = Depends(verify_api_key),
    current_user: dict = Depends(verify_required_user)
):
    result = add_to_cart_db(
        current_user["user_id"],
        bag_id
    )

    return {
        "message": "Bag added to cart successfully!",
        "cart_item": result
    }

#UPDATE CART
@app.patch("/api/v1/cart/{bag_id}")
def update_cart_item(
    request: CartItemUpdate,
    bag_id: int = PathParam(..., ge=1),
    website: str = Depends(verify_api_key),
    current_user: dict = Depends(verify_required_user)
):
    result = update_cart_item_db(
        current_user["user_id"],
        bag_id,
        request.quantity
    )

    return {
        "message": "Cart item quantity updated successfully!",
        "cart_item": result
    }

#REMOCING FROM CART
@app.delete("/api/v1/cart")
def remove_from_cart(
    request: CartItemsDelete,
    website: str = Depends(verify_api_key),
    current_user: dict = Depends(verify_required_user)
):
    result = remove_from_cart_db(
        current_user["user_id"],
        request.bag_ids
    )

    return {
        "message": "Selected bags removed from cart successfully!",
        "count": len(result),
        "removed_items": result
    }
