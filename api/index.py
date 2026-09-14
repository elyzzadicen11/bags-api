from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Literal

API_KEY = "student-api-key-123"  #balikan mo toh elai
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
    size: Literal["mini", "small", "medium", "large"]
    material: str = Field(min_length=1)
    rating: float = Field(ge=0, le=5)
    price: str = Field(min_length=1)
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
       
# BAGS DATA
bags = [
  {
    "id": 1,
    "name": "Maxi Flap Bag",
    "brand": "Chanel",
    "size": "small",
    "material": "lambskin leather",
    "rating": 4.8,
    "price": "$7,800",
    "collection": "New Arrival",
    "shape": "envelope",
    "color": "wine",
    "type": "Handbag",
    "origin": "France",
    "availability": "Available online",
    "description": "Iconic Chanel flap bag in wine lambskin.",
    "buyer_notes": "Classic investment piece.",
    "strap_type": "Chain strap",
    "closure": "Turn-lock",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 900
  },
  {
    "id": 2,
    "name": "Neverfull MM",
    "brand": "Louis Vuitton",
    "size": "medium",
    "material": "monogram canvas",
    "rating": 4.7,
    "price": "$2,030",
    "collection": "Best Seller",
    "shape": "tote",
    "color": "brown monogram",
    "type": "Tote Bag",
    "origin": "France",
    "availability": "Available online & boutiques",
    "description": "Spacious LV tote with monogram canvas.",
    "buyer_notes": "Perfect everyday bag.",
    "strap_type": "Shoulder straps",
    "closure": "Open top",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 650
  },
  {
    "id": 3,
    "name": "Dionysus GG Small",
    "brand": "Gucci",
    "size": "small",
    "material": "GG supreme canvas",
    "rating": 4.6,
    "price": "$2,890",
    "collection": "Trending",
    "shape": "structured",
    "color": "beige/ebony",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Gucci Dionysus with tiger head closure.",
    "buyer_notes": "Statement piece.",
    "strap_type": "Chain strap",
    "closure": "Push-lock",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 700
  },
  {
    "id": 4,
    "name": "Lady Dior Medium",
    "brand": "Dior",
    "size": "medium",
    "material": "cannage lambskin",
    "rating": 4.9,
    "price": "$6,000",
    "collection": "Classic",
    "shape": "structured",
    "color": "black",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Boutique exclusive",
    "description": "Elegant Dior bag with cannage stitching.",
    "buyer_notes": "Timeless elegance.",
    "strap_type": "Top handle and shoulder strap",
    "closure": "Zip closure",
    "compartments": 3,
    "water_resistant": False,
    "weight_g": 950
  },
  {
    "id": 5,
    "name": "Birkin 30",
    "brand": "Hermès",
    "size": "medium",
    "material": "togo leather",
    "rating": 5.0,
    "price": "$12,000",
    "collection": "Classic",
    "shape": "structured",
    "color": "gold",
    "type": "Handbag",
    "origin": "France",
    "availability": "Waitlist only",
    "description": "Coveted Hermès Birkin in gold togo leather.",
    "buyer_notes": "Ultimate luxury.",
    "strap_type": "Top handle",
    "closure": "Turn-lock",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 900
  },
  {
    "id": 6,
    "name": "Prada Galleria",
    "brand": "Prada",
    "size": "large",
    "material": "saffiano leather",
    "rating": 4.5,
    "price": "$3,200",
    "collection": "Everyday Essentials",
    "shape": "structured",
    "color": "red",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Prada’s signature saffiano leather tote.",
    "buyer_notes": "Durable and chic.",
    "strap_type": "Top handles and shoulder strap",
    "closure": "Zip closure",
    "compartments": 3,
    "water_resistant": False,
    "weight_g": 1000
  },
  {
    "id": 7,
    "name": "Puzzle Bag",
    "brand": "Loewe",
    "size": "small",
    "material": "calfskin",
    "rating": 4.7,
    "price": "$3,500",
    "collection": "Featured",
    "shape": "geometric",
    "color": "tan",
    "type": "Shoulder Bag",
    "origin": "Spain",
    "availability": "Available online",
    "description": "Innovative Loewe Puzzle design.",
    "buyer_notes": "Modern and versatile.",
    "strap_type": "Adjustable shoulder strap",
    "closure": "Zip closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 700
  },
  {
    "id": 8,
    "name": "Antigona Small",
    "brand": "Givenchy",
    "size": "small",
    "material": "grained leather",
    "rating": 4.6,
    "price": "$2,450",
    "collection": "Best Seller",
    "shape": "structured",
    "color": "black",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Givenchy Antigona with sharp lines.",
    "buyer_notes": "Edgy yet classic.",
    "strap_type": "Top handles and shoulder strap",
    "closure": "Zip closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 950
  },
  {
    "id": 9,
    "name": "Rockstud Tote",
    "brand": "Valentino",
    "size": "medium",
    "material": "calfskin",
    "rating": 4.4,
    "price": "$2,800",
    "collection": "Trending",
    "shape": "tote",
    "color": "ivory",
    "type": "Tote Bag",
    "origin": "Italy",
    "availability": "Boutique exclusive",
    "description": "Valentino tote with signature rockstuds.",
    "buyer_notes": "Bold and stylish.",
    "strap_type": "Shoulder straps",
    "closure": "Open top",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 800
  },
  {
    "id": 10,
    "name": "Peekaboo Iconic",
    "brand": "Fendi",
    "size": "medium",
    "material": "nappa leather",
    "rating": 4.8,
    "price": "$4,500",
    "collection": "Featured",
    "shape": "structured",
    "color": "taupe",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Fendi Peekaboo with dual compartments.",
    "buyer_notes": "Sophisticated design.",
    "strap_type": "Top handle and shoulder strap",
    "closure": "Twist-lock",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 950
  },
  {
    "id": 11,
    "name": "Kate Tassel Bag",
    "brand": "Saint Laurent",
    "size": "small",
    "material": "grain de poudre leather",
    "rating": 4.7,
    "price": "$2,200",
    "collection": "Classic",
    "shape": "envelope",
    "color": "black",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "YSL Kate bag with gold tassel.",
    "buyer_notes": "Evening essential.",
    "strap_type": "Chain strap",
    "closure": "Snap closure",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 500
  },
  {
    "id": 12,
    "name": "Hourglass Small",
    "brand": "Balenciaga",
    "size": "small",
    "material": "croc-embossed leather",
    "rating": 4.5,
    "price": "$2,600",
    "collection": "New Arrival",
    "shape": "curved",
    "color": "emerald green",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Balenciaga Hourglass with curved silhouette.",
    "buyer_notes": "Trendy statement.",
    "strap_type": "Top handle and shoulder strap",
    "closure": "Magnetic closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 750
  },
  {
    "id": 13,
    "name": "Capucines BB",
    "brand": "Louis Vuitton",
    "size": "small",
    "material": "full-grain leather",
    "rating": 4.9,
    "price": "$6,400",
    "collection": "Featured",
    "shape": "structured",
    "color": "pink",
    "type": "Handbag",
    "origin": "France",
    "availability": "Boutique exclusive",
    "description": "LV Capucines with refined details.",
    "buyer_notes": "Elegant and feminine.",
    "strap_type": "Top handle and shoulder strap",
    "closure": "Flap closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 850
  },
  {
    "id": 14,
    "name": "GG Marmont Matelassé",
    "brand": "Gucci",
    "size": "medium",
    "material": "matelassé leather",
    "rating": 4.6,
    "price": "$2,350",
    "collection": "Everyday Essentials",
    "shape": "soft",
    "color": "white",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Gucci Marmont with double G logo.",
    "buyer_notes": "Casual chic.",
    "strap_type": "Chain shoulder strap",
    "closure": "Snap closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 650
  },
  {
    "id": 15,
    "name": "Kelly 28",
    "brand": "Hermès",
    "size": "medium",
    "material": "epsom leather",
    "rating": 5.0,
    "price": "$11,500",
    "collection": "Classic",
    "shape": "structured",
    "color": "black",
    "type": "Handbag",
    "origin": "France",
    "availability": "Waitlist only",
    "description": "Iconic Hermès Kelly bag in structured epsom leather.",
    "buyer_notes": "Timeless and highly coveted.",
    "strap_type": "Top handle and shoulder strap",
    "closure": "Turn-lock",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 850
  },
  {
    "id": 16,
    "name": "Baguette Bag",
    "brand": "Fendi",
    "size": "small",
    "material": "beaded embroidery",
    "rating": 4.8,
    "price": "$4,200",
    "collection": "Limited Edition",
    "shape": "rectangular",
    "color": "multicolor",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Boutique exclusive",
    "description": "Iconic Fendi Baguette with hand embroidery.",
    "buyer_notes": "Playful and collectible.",
    "strap_type": "Shoulder strap",
    "closure": "Flap closure",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 600
  },
  {
    "id": 17,
    "name": "Le Chiquito",
    "brand": "Jacquemus",
    "size": "mini",
    "material": "smooth leather",
    "rating": 4.3,
    "price": "$650",
    "collection": "Trending",
    "shape": "top handle",
    "color": "white",
    "type": "Mini Bag",
    "origin": "France",
    "availability": "Available online",
    "description": "Jacquemus Le Chiquito in mini size.",
    "buyer_notes": "Fashion-forward micro bag.",
    "strap_type": "Top handle",
    "closure": "Flap closure",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 200
  },
  {
    "id": 18,
    "name": "Voyageur Backpack",
    "brand": "Tumi",
    "size": "large",
    "material": "nylon",
    "rating": 4.5,
    "price": "$495",
    "collection": "Everyday Essentials",
    "shape": "backpack",
    "color": "black",
    "type": "Backpack",
    "origin": "USA",
    "availability": "Available online",
    "description": "Functional Tumi backpack for travel.",
    "buyer_notes": "Practical luxury.",
    "strap_type": "Adjustable backpack straps",
    "closure": "Zip closure",
    "compartments": 4,
    "water_resistant": True,
    "weight_g": 900
  },
  {
    "id": 19,
    "name": "PS1 Satchel",
    "brand": "Proenza Schouler",
    "size": "medium",
    "material": "suede",
    "rating": 4.4,
    "price": "$1,650",
    "collection": "Featured",
    "shape": "satchel",
    "color": "burgundy",
    "type": "Satchel",
    "origin": "USA",
    "availability": "Available online",
    "description": "Proenza Schouler PS1 in rich suede.",
    "buyer_notes": "Cool and casual.",
    "strap_type": "Top handle and shoulder strap",
    "closure": "Buckle closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 850
  },
  {
    "id": 20,
    "name": "Metropolis Mini",
    "brand": "Furla",
    "size": "small",
    "material": "textured leather",
    "rating": 4.6,
    "price": "$350",
    "collection": "Best Seller",
    "shape": "flap",
    "color": "powder pink",
    "type": "Crossbody",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Furla Metropolis mini crossbody.",
    "buyer_notes": "Affordable luxury.",
    "strap_type": "Chain shoulder strap",
    "closure": "Push-lock",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 400
  }
]
#--------------------------------------------------------------------------------------------------------

#Validate the starting data set when the app launches
validated_bags = [Bags(**bag).model_dump() for bag in bags]
bags = validated_bags

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
    return {
        "count": len(bags),
        "bags": bags
    }

#--------------------------------------------------------------------------------------------------------

# SEARCH BAGS
@app.get("/bags/search")
def search_bags(q: str = Query(..., min_length=1)):
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

    return {
        "query": q,
        "count": len(results),
        "results": results
    }
#--------------------------------------------------------------------------------------------------------
  
# GET ONE BAG
@app.get("/api/v1/bags/{bag_id}", dependencies = [Depends(verify_api_key)]) #balikan mo toh elai
def get_bag(bag_id: int):
    for bag in bags:
        if bag["id"] == bag_id:
            return bag
    raise HTTPException(status_code=404, detail="Bag not found.")
#--------------------------------------------------------------------------------------------------------
# API KEY AUTHENTICATION
def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="invalid or missing API Key."
        )
    return True
