from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user,category,product,order,orderitem,cart,cartitem

models.Base.metadata.create_all(bind=engine)

app =FastAPI()

app.include_router(user.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(orderitem.router)
app.include_router(cart.router)
app.include_router(cartitem.router)