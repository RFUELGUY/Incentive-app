from backend.db.database import Base, engine

# ✅ Import all models
from backend.models.sale import Sale
from backend.models.actual_sale import ActualSale
from backend.models.product import Product
from backend.models.incentive import Incentive
from backend.models.trait_config import TraitConfig
from backend.models.salesman import Salesman  # <== most likely missing

Base.metadata.create_all(bind=engine)
print("✅ All tables created.")