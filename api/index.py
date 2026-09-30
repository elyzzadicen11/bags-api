from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Literal

API_KEYS = {
    "list": "ey-pi-ay",
    "comparison": "compareBags",
    "personality": "masungit"
} #balikan mo toh elai

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
    "size": "Small",
    "material": "Lambskin Leather",
    "rating": 4.8,
    "price": "$7,800",
    "collection": "New Arrival",
    "shape": "Envelope",
    "color": "Wine",
    "type": "Handbag",
    "origin": "France",
    "availability": "Available Online",
    "description": "Iconic Chanel flap bag in wine lambskin.",
    "buyer_notes": "Classic investment piece.",
    "strap_type": "Chain Strap",
    "closure": "Turn-Lock",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 900
  },
  {
    "id": 2,
    "name": "Neverfull MM",
    "brand": "Louis Vuitton",
    "size": "Medium",
    "material": "Monogram Canvas",
    "rating": 4.7,
    "price": "$2,030",
    "collection": "Best Seller",
    "shape": "Tote",
    "color": "Brown Monogram",
    "type": "Tote Bag",
    "origin": "France",
    "availability": "Available Online & Boutiques",
    "description": "Spacious LV tote with monogram canvas.",
    "buyer_notes": "Perfect everyday bag.",
    "strap_type": "Shoulder Straps",
    "closure": "Open Top",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 650
  },
  {
    "id": 3,
    "name": "Dionysus GG Small",
    "brand": "Gucci",
    "size": "Small",
    "material": "GG Supreme Canvas",
    "rating": 4.6,
    "price": "$2,890",
    "collection": "Trending",
    "shape": "Structured",
    "color": "Beige/Ebony",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Available Online",
    "description": "Gucci Dionysus with tiger head closure.",
    "buyer_notes": "Statement piece.",
    "strap_type": "Chain Strap",
    "closure": "Push-Lock",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 700
  },
  {
    "id": 4,
    "name": "Lady Dior Medium",
    "brand": "Dior",
    "size": "Medium",
    "material": "Cannage Lambskin",
    "rating": 4.9,
    "price": "$6,000",
    "collection": "Classic",
    "shape": "Structured",
    "color": "Black",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Boutique Exclusive",
    "description": "Elegant Dior bag with cannage stitching.",
    "buyer_notes": "Timeless elegance.",
    "strap_type": "Top Handle and Shoulder Strap",
    "closure": "Zip Closure",
    "compartments": 3,
    "water_resistant": False,
    "weight_g": 950
  },
  {
    "id": 5,
    "name": "Birkin 30",
    "brand": "Hermès",
    "size": "Medium",
    "material": "Togo Leather",
    "rating": 5.0,
    "price": "$12,000",
    "collection": "Classic",
    "shape": "Structured",
    "color": "Gold",
    "type": "Handbag",
    "origin": "France",
    "availability": "Waitlist Only",
    "description": "Coveted Hermès Birkin in gold togo leather.",
    "buyer_notes": "Ultimate luxury.",
    "strap_type": "Top Handle",
    "closure": "Turn-Lock",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 900
  },
  {
    "id": 6,
    "name": "Prada Galleria",
    "brand": "Prada",
    "size": "Large",
    "material": "Saffiano Leather",
    "rating": 4.5,
    "price": "$3,200",
    "collection": "Everyday Essentials",
    "shape": "Structured",
    "color": "Red",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available Online",
    "description": "Prada’s signature saffiano leather tote.",
    "buyer_notes": "Durable and chic.",
    "strap_type": "Top Handles and Shoulder Strap",
    "closure": "Zip Closure",
    "compartments": 3,
    "water_resistant": False,
    "weight_g": 1000
  },
  {
    "id": 7,
    "name": "Puzzle Bag",
    "brand": "Loewe",
    "size": "Small",
    "material": "Calfskin",
    "rating": 4.7,
    "price": "$3,500",
    "collection": "Featured",
    "shape": "Geometric",
    "color": "Tan",
    "type": "Shoulder Bag",
    "origin": "Spain",
    "availability": "Available Online",
    "description": "Innovative Loewe Puzzle design.",
    "buyer_notes": "Modern and versatile.",
    "strap_type": "Adjustable Shoulder Strap",
    "closure": "Zip Closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 700
  },
  {
    "id": 8,
    "name": "Antigona Small",
    "brand": "Givenchy",
    "size": "Small",
    "material": "Grained Leather",
    "rating": 4.6,
    "price": "$2,450",
    "collection": "Best Seller",
    "shape": "Structured",
    "color": "Black",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available Online",
    "description": "Givenchy Antigona with sharp lines.",
    "buyer_notes": "Edgy yet classic.",
    "strap_type": "Top Handles and Shoulder Strap",
    "closure": "Zip Closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 950
  },
  {
    "id": 9,
    "name": "Rockstud Tote",
    "brand": "Valentino",
    "size": "Medium",
    "material": "Calfskin",
    "rating": 4.4,
    "price": "$2,800",
    "collection": "Trending",
    "shape": "Tote",
    "color": "Ivory",
    "type": "Tote Bag",
    "origin": "Italy",
    "availability": "Boutique Exclusive",
    "description": "Valentino tote with signature rockstuds.",
    "buyer_notes": "Bold and stylish.",
    "strap_type": "Shoulder Straps",
    "closure": "Open Top",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 800
  },
  {
    "id": 10,
    "name": "Peekaboo Iconic",
    "brand": "Fendi",
    "size": "Medium",
    "material": "Nappa Leather",
    "rating": 4.8,
    "price": "$4,500",
    "collection": "Featured",
    "shape": "Structured",
    "color": "Taupe",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available Online",
    "description": "Fendi Peekaboo with dual compartments.",
    "buyer_notes": "Sophisticated design.",
    "strap_type": "Top Handle and Shoulder Strap",
    "closure": "Twist-Lock",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 950
  },
  {
    "id": 11,
    "name": "Kate Tassel Bag",
    "brand": "Saint Laurent",
    "size": "Small",
    "material": "Grain de Poudre Leather",
    "rating": 4.7,
    "price": "$2,200",
    "collection": "Classic",
    "shape": "Envelope",
    "color": "Black",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Available Online",
    "description": "YSL Kate bag with gold tassel.",
    "buyer_notes": "Evening essential.",
    "strap_type": "Chain Strap",
    "closure": "Snap Closure",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 500
  },
  {
    "id": 12,
    "name": "Hourglass Small",
    "brand": "Balenciaga",
    "size": "Small",
    "material": "Croc-Embossed Leather",
    "rating": 4.5,
    "price": "$2,600",
    "collection": "New Arrival",
    "shape": "Curved",
    "color": "Emerald Green",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available Online",
    "description": "Balenciaga Hourglass with curved silhouette.",
    "buyer_notes": "Trendy statement.",
    "strap_type": "Top Handle and Shoulder Strap",
    "closure": "Magnetic Closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 750
  },
  {
    "id": 13,
    "name": "Capucines BB",
    "brand": "Louis Vuitton",
    "size": "Small",
    "material": "Full-Grain Leather",
    "rating": 4.9,
    "price": "$6,400",
    "collection": "Featured",
    "shape": "Structured",
    "color": "Pink",
    "type": "Handbag",
    "origin": "France",
    "availability": "Boutique Exclusive",
    "description": "LV Capucines with refined details.",
    "buyer_notes": "Elegant and feminine.",
    "strap_type": "Top Handle and Shoulder Strap",
    "closure": "Flap Closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 850
  },
  {
    "id": 14,
    "name": "GG Marmont Matelassé",
    "brand": "Gucci",
    "size": "Medium",
    "material": "Matelassé Leather",
    "rating": 4.6,
    "price": "$2,350",
    "collection": "Everyday Essentials",
    "shape": "Soft",
    "color": "White",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Available Online",
    "description": "Gucci Marmont with double G logo.",
    "buyer_notes": "Casual chic.",
    "strap_type": "Chain Shoulder Strap",
    "closure": "Snap Closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 650
  },
  {
    "id": 15,
    "name": "Kelly 28",
    "brand": "Hermès",
    "size": "Medium",
    "material": "Epsom Leather",
    "rating": 5.0,
    "price": "$11,500",
    "collection": "Classic",
    "shape": "Structured",
    "color": "Black",
    "type": "Handbag",
    "origin": "France",
    "availability": "Waitlist Only",
    "description": "Iconic Hermès Kelly bag in structured epsom leather.",
    "buyer_notes": "Timeless and highly coveted.",
    "strap_type": "Top Handle and Shoulder Strap",
    "closure": "Turn-Lock",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 850
  },
  {
    "id": 16,
    "name": "Baguette Bag",
    "brand": "Fendi",
    "size": "Small",
    "material": "Beaded Embroidery",
    "rating": 4.8,
    "price": "$4,200",
    "collection": "Limited Edition",
    "shape": "Rectangular",
    "color": "Multicolor",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Boutique Exclusive",
    "description": "Iconic Fendi Baguette with hand embroidery.",
    "buyer_notes": "Playful and collectible.",
    "strap_type": "Shoulder Strap",
    "closure": "Flap Closure",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 600
  },
  {
    "id": 17,
    "name": "Le Chiquito",
    "brand": "Jacquemus",
    "size": "Mini",
    "material": "Smooth Leather",
    "rating": 4.3,
    "price": "$650",
    "collection": "Trending",
    "shape": "Top Handle",
    "color": "White",
    "type": "Mini Bag",
    "origin": "France",
    "availability": "Available Online",
    "description": "Jacquemus Le Chiquito in mini size.",
    "buyer_notes": "Fashion-forward micro bag.",
    "strap_type": "Top Handle",
    "closure": "Flap Closure",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 200
  },
  {
    "id": 18,
    "name": "Voyageur Backpack",
    "brand": "Tumi",
    "size": "Large",
    "material": "Nylon",
    "rating": 4.5,
    "price": "$495",
    "collection": "Everyday Essentials",
    "shape": "Backpack",
    "color": "Black",
    "type": "Backpack",
    "origin": "USA",
    "availability": "Available Online",
    "description": "Functional Tumi backpack for travel.",
    "buyer_notes": "Practical luxury.",
    "strap_type": "Adjustable Backpack Straps",
    "closure": "Zip Closure",
    "compartments": 4,
    "water_resistant": True,
    "weight_g": 900
  },
  {
    "id": 19,
    "name": "PS1 Satchel",
    "brand": "Proenza Schouler",
    "size": "Medium",
    "material": "Suede",
    "rating": 4.4,
    "price": "$1,650",
    "collection": "Featured",
    "shape": "Satchel",
    "color": "Burgundy",
    "type": "Satchel",
    "origin": "USA",
    "availability": "Available Online",
    "description": "Proenza Schouler PS1 in rich suede.",
    "buyer_notes": "Cool and casual.",
    "strap_type": "Top Handle and Shoulder Strap",
    "closure": "Buckle Closure",
    "compartments": 2,
    "water_resistant": False,
    "weight_g": 850
  },
  {
    "id": 20,
    "name": "Metropolis Mini",
    "brand": "Furla",
    "size": "Small",
    "material": "Textured Leather",
    "rating": 4.6,
    "price": "$350",
    "collection": "Best Seller",
    "shape": "Flap",
    "color": "Powder Pink",
    "type": "Crossbody",
    "origin": "Italy",
    "availability": "Available Online",
    "description": "Furla Metropolis mini crossbody.",
    "buyer_notes": "Affordable luxury.",
    "strap_type": "Chain Shoulder Strap",
    "closure": "Push-Lock",
    "compartments": 1,
    "water_resistant": False,
    "weight_g": 400
  }
]
#--------------------------------------------------------------------------------------------------------

#Validate the starting data set when the app launches
validated_bags = [Bags(**bag).model_dump() for bag in bags]
bags = validated_bags

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
    return {
        "count": len(bags),
        "bags": bags
    }

#--------------------------------------------------------------------------------------------------------

# SEARCH BAGS
@app.get("/api/v1/bags/search", dependencies = [Depends(verify_api_key)])
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
