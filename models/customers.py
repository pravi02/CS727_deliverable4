from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, String, DateTime
from sqlalchemy.orm import relationship

from db import Base

class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(100), nullable=False)
    customer_location = Column(String(100), nullable=False)
    customer_email = Column(String(100), unique=True, nullable=False)
    customer_telephone = Column(String(20), unique=True, nullable=False)

    # Define a unique constraint
    __table_args__ = (UniqueConstraint('customer_name', 'customer_location', 'customer_telephone', name='uq_customer'),)

    # Relationship
    orders = relationship("CustomerOrder", back_populates="customer")

    def __repr__(self):
        return f"<Customer(name={self.customer_name}, location={self.customer_location})>"


class CustomerOrder(Base):
    __tablename__ = 'customer_order'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id', ondelete="RESTRICT"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)

    # Relationship
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("CustomerOrderItems", back_populates="customer_order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CustomerOrder(id={self.order_id}, customer={self.customer_id}, date={self.order_date})>"

class CustomerOrderItems(Base):
    __tablename__ = 'customer_order_items'

    line_item_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_order_id = Column(Integer, ForeignKey('customer_order.order_id', ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey('product.product_id', ondelete="CASCADE"), nullable=False)
    request_quantity = Column(Integer, nullable=False)

    # Relationship
    customer_order = relationship("CustomerOrder", back_populates="order_items")
    product = relationship("Product")

    def __repr__(self):
        return f"<CustomerOrderItems(line_item_id={self.line_item_id}, quantity={self.request_quantity})>"

