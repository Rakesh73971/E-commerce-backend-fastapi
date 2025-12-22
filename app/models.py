from .database import Base
from sqlalchemy import Column, Integer, String, Boolean,DECIMAL,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="customer")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    price = Column(DECIMAL(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True
    )

    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )


class Order(Base):
    __tablename__='orders'

    id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    total_amount = Column(DECIMAL(10,2),nullable=False)
    status = Column(String,server_default='pending',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())



class OrderItem(Base):
    __tablename__="orderitems"

    id = Column(Integer,primary_key=True,nullable=False)
    order_id = Column(Integer,ForeignKey('orders.id',ondelete='CASCADE'),nullable=False,index=True)
    product_id = Column(Integer,ForeignKey('products.id',ondelete='CASCADE'),nullable=False,index=True)
    quantity = Column(Integer,nullable=False)
    price_at_purchase = Column(DECIMAL(10,2),nullable=False)


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False,unique=True,index=True)


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer,ForeignKey("carts.id", ondelete="CASCADE"),nullable=False,index=True)
    product_id = Column(Integer,ForeignKey("products.id", ondelete="CASCADE"),nullable=False,index=True)
    quantity = Column(Integer, nullable=False)
