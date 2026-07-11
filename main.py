from fastapi import FastAPI
from app.db.database import  Base
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.routes.book_routes import router as book_router
from app.routes.borrow_routes import router as borrow_router
from app.routes.admin_routes import router as admin_router

app = FastAPI()
@app.get("/health")
async def health():
    return {"status": "healthy"}


print(Base.metadata.tables.keys())


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(book_router)
app.include_router(borrow_router)
app.include_router(admin_router)

for route in app.routes:
    print(route.path)
