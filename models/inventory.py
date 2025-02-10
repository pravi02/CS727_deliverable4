from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from db import Base


class InventoryLocation(Base):
    __tablename__ = 'inventory_location'

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    aisle_number = Column(String(50), nullable=False)
    bin_location = Column(String(50), nullable=False)

    # Unique constraint for aisle_number and bin_location
    __table_args__ = (UniqueConstraint('aisle_number', 'bin_location', name='uq_inventory_location'),)

    # Relationship
    inventories = relationship("Inventory", back_populates="inventory_location")

    def __repr__(self):
        return f"<InventoryLocation(aisle={self.aisle_number}, bin={self.bin_location})>"

class Inventory(Base):
    __tablename__ = 'inventory'

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.product_id', ondelete="RESTRICT"), nullable=False)
    available_quantity = Column(Integer, nullable=False)
    reorder_trigger_quantity = Column(Integer, default=10, nullable=False)
    inventory_status = Column(Boolean, default=True, nullable=False)
    inventory_location_id = Column(Integer, ForeignKey('inventory_location.location_id', ondelete="RESTRICT"), nullable=False)

    # Unique constraint for product and inventory location
    __table_args__ = (UniqueConstraint('product_id', 'inventory_location_id', name='uq_inventory_product_location'),)

    # Relationships
    product = relationship("Product")
    inventory_location = relationship("InventoryLocation", back_populates="inventories")

    def __repr__(self):
        return f"<Inventory(product_id={self.product_id}, quantity={self.available_quantity})>"