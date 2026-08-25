from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Video Game Dictionary",
    description="A beginner-friendly REST API containing simple information about video games.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    "collection": "Fall Winter 2026",
    "shape": "envelope",
    "color": "wine",
    "type": "Handbag",
    "origin": "France",
    "availability": "Available online",
    "description": "Iconic Chanel flap bag in wine lambskin.",
    "buyer_notes": "Classic investment piece."
  },
  {
    "id": 2,
    "name": "Neverfull MM",
    "brand": "Louis Vuitton",
    "size": "medium",
    "material": "monogram canvas",
    "rating": 4.7,
    "price": "$2,030",
    "collection": "Permanent",
    "shape": "tote",
    "color": "brown monogram",
    "type": "Tote Bag",
    "origin": "France",
    "availability": "Available online & boutiques",
    "description": "Spacious LV tote with monogram canvas.",
    "buyer_notes": "Perfect everyday bag."
  },
  {
    "id": 3,
    "name": "Dionysus GG Small",
    "brand": "Gucci",
    "size": "small",
    "material": "GG supreme canvas",
    "rating": 4.6,
    "price": "$2,890",
    "collection": "Resort 2026",
    "shape": "structured",
    "color": "beige/ebony",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Gucci Dionysus with tiger head closure.",
    "buyer_notes": "Statement piece."
  },
  {
    "id": 4,
    "name": "Lady Dior Medium",
    "brand": "Dior",
    "size": "medium",
    "material": "cannage lambskin",
    "rating": 4.9,
    "price": "$6,000",
    "collection": "Fall Winter 2026",
    "shape": "structured",
    "color": "black",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Boutique exclusive",
    "description": "Elegant Dior bag with cannage stitching.",
    "buyer_notes": "Timeless elegance."
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
    "buyer_notes": "Ultimate luxury."
  },
  {
    "id": 6,
    "name": "Prada Galleria",
    "brand": "Prada",
    "size": "large",
    "material": "saffiano leather",
    "rating": 4.5,
    "price": "$3,200",
    "collection": "Permanent",
    "shape": "structured",
    "color": "red",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Prada’s signature saffiano leather tote.",
    "buyer_notes": "Durable and chic."
  },
  {
    "id": 7,
    "name": "Puzzle Bag",
    "brand": "Loewe",
    "size": "small",
    "material": "calfskin",
    "rating": 4.7,
    "price": "$3,500",
    "collection": "Fall Winter 2026",
    "shape": "geometric",
    "color": "tan",
    "type": "Shoulder Bag",
    "origin": "Spain",
    "availability": "Available online",
    "description": "Innovative Loewe Puzzle design.",
    "buyer_notes": "Modern and versatile."
  },
  {
    "id": 8,
    "name": "Antigona Small",
    "brand": "Givenchy",
    "size": "small",
    "material": "grained leather",
    "rating": 4.6,
    "price": "$2,450",
    "collection": "Permanent",
    "shape": "structured",
    "color": "black",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Givenchy Antigona with sharp lines.",
    "buyer_notes": "Edgy yet classic."
  },
  {
    "id": 9,
    "name": "Rockstud Tote",
    "brand": "Valentino",
    "size": "medium",
    "material": "calfskin",
    "rating": 4.4,
    "price": "$2,800",
    "collection": "Fall Winter 2026",
    "shape": "tote",
    "color": "ivory",
    "type": "Tote Bag",
    "origin": "Italy",
    "availability": "Boutique exclusive",
    "description": "Valentino tote with signature rockstuds.",
    "buyer_notes": "Bold and stylish."
  },
  {
    "id": 10,
    "name": "Peekaboo Iconic",
    "brand": "Fendi",
    "size": "medium",
    "material": "nappa leather",
    "rating": 4.8,
    "price": "$4,500",
    "collection": "Fall Winter 2026",
    "shape": "structured",
    "color": "taupe",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Fendi Peekaboo with dual compartments.",
    "buyer_notes": "Sophisticated design."
  },
  {
    "id": 11,
    "name": "Kate Tassel Bag",
    "brand": "Saint Laurent",
    "size": "small",
    "material": "grain de poudre leather",
    "rating": 4.7,
    "price": "$2,200",
    "collection": "Permanent",
    "shape": "envelope",
    "color": "black",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "YSL Kate bag with gold tassel.",
    "buyer_notes": "Evening essential."
  },
  {
    "id": 12,
    "name": "Hourglass Small",
    "brand": "Balenciaga",
    "size": "small",
    "material": "croc-embossed leather",
    "rating": 4.5,
    "price": "$2,600",
    "collection": "Fall Winter 2026",
    "shape": "curved",
    "color": "emerald green",
    "type": "Handbag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Balenciaga Hourglass with curved silhouette.",
    "buyer_notes": "Trendy statement."
  },
  {
    "id": 13,
    "name": "Capucines BB",
    "brand": "Louis Vuitton",
    "size": "small",
    "material": "full-grain leather",
    "rating": 4.9,
    "price": "$6,400",
    "collection": "Fall Winter 2026",
    "shape": "structured",
    "color": "pink",
    "type": "Handbag",
    "origin": "France",
    "availability": "Boutique exclusive",
    "description": "LV Capucines with refined details.",
    "buyer_notes": "Elegant and feminine."
  },
  {
    "id": 14,
    "name": "GG Marmont Matelassé",
    "brand": "Gucci",
    "size": "medium",
    "material": "matelassé leather",
    "rating": 4.6,
    "price": "$2,350",
    "collection": "Permanent",
    "shape": "soft",
    "color": "white",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Gucci Marmont with double G logo.",
    "buyer_notes": "Casual chic."
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
    "color": "
  },
  {
    "id": 16,
    "name": "Baguette Bag",
    "brand": "Fendi",
    "size": "small",
    "material": "beaded embroidery",
    "rating": 4.8,
    "price": "$4,200",
    "collection": "Resort 2026",
    "shape": "rectangular",
    "color": "multicolor",
    "type": "Shoulder Bag",
    "origin": "Italy",
    "availability": "Boutique exclusive",
    "description": "Iconic Fendi Baguette with hand embroidery.",
    "buyer_notes": "Playful and collectible."
  },
  {
    "id": 17,
    "name": "Le Chiquito",
    "brand": "Jacquemus",
    "size": "mini",
    "material": "smooth leather",
    "rating": 4.3,
    "price": "$650",
    "collection": "Spring Summer 2026",
    "shape": "top handle",
    "color": "white",
    "type": "Mini Bag",
    "origin": "France",
    "availability": "Available online",
    "description": "Jacquemus Le Chiquito in mini size.",
    "buyer_notes": "Fashion-forward micro bag."
  },
  {
    "id": 18,
    "name": "Voyageur Backpack",
    "brand": "Tumi",
    "size": "large",
    "material": "nylon",
    "rating": 4.5,
    "price": "$495",
    "collection": "Permanent",
    "shape": "backpack",
    "color": "black",
    "type": "Backpack",
    "origin": "USA",
    "availability": "Available online",
    "description": "Functional Tumi backpack for travel.",
    "buyer_notes": "Practical luxury."
  },
  {
    "id": 19,
    "name": "PS1 Satchel",
    "brand": "Proenza Schouler",
    "size": "medium",
    "material": "suede",
    "rating": 4.4,
    "price": "$1,650",
    "collection": "Fall Winter 2026",
    "shape": "satchel",
    "color": "burgundy",
    "type": "Satchel",
    "origin": "USA",
    "availability": "Available online",
    "description": "Proenza Schouler PS1 in rich suede.",
    "buyer_notes": "Cool and casual."
  },
  {
    "id": 20,
    "name": "Metropolis Mini",
    "brand": "Furla",
    "size": "small",
    "material": "textured leather",
    "rating": 4.6,
    "price": "$350",
    "collection": "Permanent",
    "shape": "flap",
    "color": "powder pink",
    "type": "Crossbody",
    "origin": "Italy",
    "availability": "Available online",
    "description": "Furla Metropolis mini crossbody.",
    "buyer_notes": "Affordable luxury."
  }
]

# HOME
@app.get("/")
def home():

    return {
        "message": "Welcome to the Video Game Dictionary!",
        "endpoints": [
            "/vgames",
            "/vgames/{id}",
            "/vgames/search"
        ]
    }


# GET ALL BAGS
@app.get("/vgames")
def get_vgames():

    return {
        "count": len(vgames),
        "vgames": vgames
    }

# SEARCH BAGS
@app.get("/vgames/search")
def search_vgames( q: str = Query(..., min_length=1)):
    q = q.lower()
    results = []
    for games in vgames:
        searchable_text = (
            f"{games['title']} "
            f"{games['genre']} "
            f"{games['year']} "
            f"{games['platform']}"
        ).lower()

        if q in searchable_text:
            results.append(games)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }
    
# GET ONE BAGS
@app.get("/vgames/{game_id}")
def get_game(game_id: int):

    for games in vgames:

        if games["id"] == game_id:
            return games

    raise HTTPException(
        status_code=404,
        detail="Game not found."
    )


