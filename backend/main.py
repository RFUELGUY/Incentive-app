from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine, Base
from api import actual_sale_router
from api.claim_router import router as claim_router
from api import (
    auth_router,
    sales_router,
    incentive_router,
    admin_router,
    upload_router,
    trait_router,
    product_router,
    secure_test_router,
    outlet_router,
    public_router,
    streak_router,
    leaderboard_router,
    salesman_router
)
import logging
logging.basicConfig(level=logging.DEBUG)
# Initialize FastAPI app
app = FastAPI(title="Incentive Management System")

# Enable CORS (adjust allowed origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔐 Replace with actual frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables in the database


# Mount API routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["Auth"])
app.include_router(sales_router.router, prefix="/api/sales", tags=["Sales"])
app.include_router(incentive_router.router, prefix="/api/incentives", tags=["Incentives"])
app.include_router(upload_router.router, prefix="/api/upload", tags=["Upload"])
app.include_router(admin_router.router, prefix="/api/admin", tags=["Admin"])
app.include_router(trait_router.router, prefix="/api/admin", tags=["TraitConfig"])  # Shares 'admin' prefix
app.include_router(actual_sale_router.router, prefix="/api", tags=["ActualSale"])
app.include_router(product_router.router, prefix="/api/products", tags=["Products"])
app.include_router(secure_test_router.router)
app.include_router(outlet_router.router, prefix="/api/admin", tags=["Outlet"])
app.include_router(public_router.router, prefix="/api")
app.include_router(streak_router.router, prefix="/api")
app.include_router(leaderboard_router.router, prefix="/api/leaderboard", tags=["Leaderboard"])
app.include_router(claim_router)
app.include_router(claim_router.router, prefix="/api/claims", tags=["Claims"])
app.include_router(public_router.router, prefix="/api/public", tags=["Public"])
app.include_router(salesman_router.router, prefix="", tags=["Salesman"])
