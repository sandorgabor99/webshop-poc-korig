from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from .database import Base, engine, get_db
from .config import settings
from .security import hash_password
from .models import User, UserRole
from .routers import auth, products, orders, upload, customers, reviews
from .logging_config import setup_logging, get_auth_logger
import os

auth_logger = get_auth_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    Base.metadata.create_all(bind=engine)
    db: Session = next(get_db())
    admin_email = settings.admin_email
    admin_password = settings.admin_password

    if admin_email and admin_password:
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if not existing_admin:
            hashed_password = hash_password(admin_password)
            # Create username from admin email
            admin_username = admin_email.split('@')[0]
            admin_user = User(
                email=admin_email,
                username=admin_username,
                password_hash=hashed_password, 
                role=UserRole.ADMINISTRATOR
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            auth_logger.info(f"ADMIN_SEED_OK user_id={admin_user.id} email={admin_email} username={admin_username}")
        else:
            auth_logger.info(f"ADMIN_SEED_SKIP email={admin_email} (already exists)")
    else:
        auth_logger.warning("ADMIN_EMAIL or ADMIN_PASSWORD not set. Admin user not seeded.")
    db.close()
    
    yield
    
    # Shutdown
    pass


app = FastAPI(title="Webshop API", lifespan=lifespan)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # React dev server (common)
    "http://localhost:5173",  # Vite dev server (common)
    "http://localhost:5174",  # Vite dev server (fallback)
    "http://localhost:5175",  # Vite dev server (current)
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])


@app.get("/")
def root():
	return {"message": "Webshop API running"}
