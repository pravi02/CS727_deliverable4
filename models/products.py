
from sqlalchemy import Column, Integer, String, UniqueConstraint, Float, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class ProductCategory(Base):
    __tablename__ = 'product_category'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(50), nullable=False, unique=True)

    # Relationship
    products = relationship("Product", back_populates="product_category")

    def __repr__(self):
        return f"<ProductCategory(name={self.category_name})>"

class Supplier(Base):
    __tablename__ = 'supplier'

    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_name = Column(String(50), nullable=False)
    supplier_contact_number = Column(String(20), nullable=False)

    # Unique constraint for supplier name and contact number
    __table_args__ = (UniqueConstraint('supplier_name', 'supplier_contact_number', name='uq_supplier_name_contact'),)

    # Relationship
    products = relationship("Product", back_populates="product_supplier")

    def __repr__(self):
        return f"<Supplier(name={self.supplier_name}, contact={self.supplier_contact_number})>"

class Product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    serial_no = Column(String(50), nullable=False)
    product_name = Column(String(50), nullable=False)
    product_weight = Column(Float, nullable=False)
    price_per_unit = Column(DECIMAL(10, 2), nullable=False)
    product_category_id = Column(Integer, ForeignKey('product_category.category_id', ondelete="RESTRICT"), nullable=False)
    product_supplier_id = Column(Integer, ForeignKey('supplier.supplier_id', ondelete="RESTRICT"), nullable=False)

    # Unique constraint for product name and category
    __table_args__ = (UniqueConstraint('product_name', 'product_category_id', name='uq_product_name_category'),)

    # Relationships
    product_category = relationship("ProductCategory", back_populates="products")
    product_supplier = relationship("Supplier", back_populates="products")

    def __repr__(self):
        return f"<Product(name={self.product_name}, category={self.product_category_id}, supplier={self.product_supplier_id})>"