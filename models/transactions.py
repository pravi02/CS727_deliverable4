from sqlalchemy import Column, Integer, ForeignKey, Boolean, Date, Float
from sqlalchemy.orm import relationship, backref
from models.user import User
from models.customers import CustomerOrder
from db import Base


class OrderProcess(Base):
    __tablename__ = 'order_process'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_date = Column(Date, nullable=False)
    sales_amount = Column(Float, nullable=False)
    processed_by_id = Column(Integer, ForeignKey('user.id', ondelete="SET NULL"), nullable=True)
    customer_order_id = Column(Integer, ForeignKey('customer_order.order_id', ondelete="CASCADE"), nullable=False, unique=True)
    order_processed = Column(Boolean, default=False)

    # Relationships
    processed_by = relationship("User")
    customer_order = relationship(CustomerOrder, backref=backref('processed_order_info', uselist=False), lazy=True)
    # customer_order = relationship("CustomerOrder", back_populates="order_process")
    processed_line_items = relationship("ProcessedLineItems", back_populates="processed_order")

    def __repr__(self):
        return f"<OrderProcess(transaction_id={self.transaction_id}, processed_by={self.processed_by_id})>"

    @classmethod
    def get_all(cls, session):
        return session.query(cls).filter(cls.order_processed == True).all()

    @classmethod
    def get_specific(cls, session, transaction_id):
        return session.query(cls).filter(cls.transaction_id == transaction_id).first()

class ProcessedLineItems(Base):
    __tablename__ = 'processed_line_items'

    line_item_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_line_item_id = Column(Integer, ForeignKey('customer_order_items.line_item_id', ondelete="RESTRICT"), nullable=False)
    process_id_id = Column(Integer, ForeignKey('order_process.transaction_id', ondelete="CASCADE"), nullable=False)
    inventory_id = Column(Integer, ForeignKey('inventory.inventory_id', ondelete="CASCADE"), nullable=False)
    allocated_quantity = Column(Integer, nullable=False)

    # Relationships
    customer_line_item = relationship("CustomerOrderItems")
    process_id = relationship("OrderProcess", back_populates="processed_line_items")
    inventory = relationship("Inventory")

    def __repr__(self):
        return f"<ProcessedLineItems(line_item_id={self.line_item_id}, process_id={self.process_id_id})>"


