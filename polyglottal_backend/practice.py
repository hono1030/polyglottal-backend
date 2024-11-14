from fastapi import FastAPI, HTTPException, Path,  Query
from pydantic import BaseModel
from enum import Enum
import uvicorn

# app = FastAPI(title="Polyglottal project")
app = FastAPI()

# You can give your API a title and add additional metadata sduch as a description, version
# The description also supports markdown formatting.

app = FastAPI(
    title="Polyglottal project",
    description="A Real-Time Chat Application using WebSockets",
    version="0.1.0",
)

class Item(BaseModel):
    text: str = None
    is_done: bool = False
    
items = []

@app.get("/hello-world")
def hello():
    return {"Message": "Hello world!"}

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

@app.get("/items", response_model=list[Item])
def list_items(limit: int=  10):
    return items[0:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"

# Inheriting from Pydantic's BaseModels gives us built-in validation.
# Even if we were to user a refular 2dataclass validation would still work 

class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category

items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES),
}

@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"item": items}

@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} does not exist."
        )
    return items[item_id]

Selection = dict[
    str, str | int | float | Category | None
]

@app.get("/items/")
def query_items_by_parameters(
    name: str | None = None, 
    price: float | None = None,
    count: int | None = None,
    category: Category | None = None,    
) -> dict[str, Selection]:
    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count != count,
                category is None or item.category is category,
            )
        )
    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection,
    }

@app.post("/item")
def add_item(item: Item) -> dict[str, Item]:

    if item.id in items:
        HTTPException(status_code=400, details=f"Item with {item.id=} already exists.")

    items[item.id] = item
    return {"added": item}

# We can place further restictions on allowed arduments by using the Query and Oath class
# In this case we are setting a lower bound for valid values and a minimal and maximal length
@app.put("/items/{item_id}")
def update(
    item_id: int = Path(ge=0), #ge= grater or equal
    name: str | None =  Query(default=None, min_length=1, max_length=8),
    price: float | None = Query(default=None, gt=0.0),
    count: int | None = Query(default=None, ge=0),
    # count: int | None = None,
) -> dict[str, Item]:
    
    if item_id not in items:
        HTTPException(status_code=404, detail=f"Item with {item_id=} dies not exist.")
    if all(info is None for info in (name, price, count)):
        raise HTTPException(status_code=404, detail="No parameters provided for update.")
    
    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count

    return {"updated": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:

    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} does not exist."
        )
    
    item = items.pop(item_id)
    return {"deleted": item}

# def start():
#     """Launched with `poetry run start` at root level"""
#     uvicorn.run("polyglottal_backend.main:app", port=8000, reload=True)