from fastapi import APIRouter

# Example
# from app.route.transaction_route import router as transaction_router

api_router = APIRouter(prefix="/api/v1")

# api_router.include_router(transaction_router)