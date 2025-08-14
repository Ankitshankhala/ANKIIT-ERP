from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from decimal import Decimal
import enum
from .base import BaseModel, Base

class StockMovementType(str, enum.Enum):
	RECEIPT = "receipt"  # inbound
	ISSUE = "issue"      # outbound
	TRANSFER = "transfer"
	ADJUSTMENT = "adjustment"

class ValuationMethod(str, enum.Enum):
	FIFO = "fifo"
	AVERAGE = "average"

class Product(BaseModel, Base):
	__tablename__ = "products"
	
	sku = Column(String(64), unique=True, nullable=False, index=True)
	name = Column(String(200), nullable=False)
	description = Column(Text, nullable=True)
	category = Column(String(100), nullable=True)
	unit_of_measure = Column(String(20), nullable=False, default="ea")
	cost_price = Column(Numeric(12, 2), nullable=False, default=Decimal('0.00'))
	sale_price = Column(Numeric(12, 2), nullable=False, default=Decimal('0.00'))
	is_active = Column(Boolean, default=True)
	valuation_method = Column(Enum(ValuationMethod), nullable=False, default=ValuationMethod.FIFO)

	# Relationships
	stock_levels = relationship("StockLevel", back_populates="product", cascade="all, delete-orphan")
	movements = relationship("StockMovement", back_populates="product")

class Supplier(BaseModel, Base):
	__tablename__ = "suppliers"
	
	name = Column(String(200), nullable=False)
	email = Column(String(200), nullable=True)
	phone = Column(String(50), nullable=True)
	address = Column(Text, nullable=True)
	website = Column(String(200), nullable=True)
	is_active = Column(Boolean, default=True)

	# Relationships
	purchase_movements = relationship("StockMovement", back_populates="supplier")

class Warehouse(BaseModel, Base):
	__tablename__ = "warehouses"
	
	code = Column(String(20), unique=True, nullable=False, index=True)
	name = Column(String(200), nullable=False)
	location = Column(String(200), nullable=True)
	description = Column(Text, nullable=True)
	is_active = Column(Boolean, default=True)

	# Relationships
	stock_levels = relationship("StockLevel", back_populates="warehouse", cascade="all, delete-orphan")
	movements_from = relationship("StockMovement", back_populates="from_warehouse", foreign_keys="StockMovement.from_warehouse_id")
	movements_to = relationship("StockMovement", back_populates="to_warehouse", foreign_keys="StockMovement.to_warehouse_id")

class StockLevel(BaseModel, Base):
	__tablename__ = "stock_levels"
	
	product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
	warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, index=True)
	quantity = Column(Numeric(14, 4), nullable=False, default=Decimal('0.0000'))
	reorder_point = Column(Numeric(14, 4), nullable=False, default=Decimal('0.0000'))
	reorder_quantity = Column(Numeric(14, 4), nullable=False, default=Decimal('0.0000'))

	# Relationships
	product = relationship("Product", back_populates="stock_levels")
	warehouse = relationship("Warehouse", back_populates="stock_levels")

class StockMovement(BaseModel, Base):
	__tablename__ = "stock_movements"
	
	movement_number = Column(String(50), unique=True, nullable=False, index=True)
	product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
	quantity = Column(Numeric(14, 4), nullable=False)
	movement_type = Column(Enum(StockMovementType), nullable=False)
	from_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
	to_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
	supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
	reference = Column(String(100), nullable=True)
	movement_date = Column(DateTime, nullable=False, default=func.now())
	notes = Column(Text, nullable=True)
	# For issues/shipments, store the extended cost calculated by valuation engine
	cost_amount = Column(Numeric(15, 2), nullable=True)

	# Relationships
	product = relationship("Product", back_populates="movements")
	from_warehouse = relationship("Warehouse", foreign_keys=[from_warehouse_id], back_populates="movements_from")
	to_warehouse = relationship("Warehouse", foreign_keys=[to_warehouse_id], back_populates="movements_to")
	supplier = relationship("Supplier", back_populates="purchase_movements")

	def __repr__(self):
		return f"<StockMovement(number='{self.movement_number}', product_id={self.product_id}, qty={self.quantity}, type='{self.movement_type}')>"

# Procurement: Purchase Order and Goods Receipt
class PurchaseOrderStatus(str, enum.Enum):
	DRAFT = "draft"
	APPROVED = "approved"
	RECEIVED = "received"
	CLOSED = "closed"
	CANCELLED = "cancelled"

class PurchaseOrder(BaseModel, Base):
	__tablename__ = "purchase_orders"

	po_number = Column(String(50), unique=True, nullable=False, index=True)
	supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
	status = Column(Enum(PurchaseOrderStatus), nullable=False, default=PurchaseOrderStatus.DRAFT)
	order_date = Column(DateTime, nullable=False, default=func.now())
	expected_date = Column(DateTime, nullable=True)
	notes = Column(Text, nullable=True)
	total_amount = Column(Numeric(15, 2), nullable=False, default=Decimal('0.00'))

	supplier = relationship("Supplier")
	lines = relationship("PurchaseOrderLine", back_populates="purchase_order", cascade="all, delete-orphan")

class PurchaseOrderLine(BaseModel, Base):
	__tablename__ = "purchase_order_lines"

	purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False, index=True)
	product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
	description = Column(String(255), nullable=True)
	quantity = Column(Numeric(14, 4), nullable=False, default=Decimal('0.0000'))
	unit_price = Column(Numeric(12, 2), nullable=False, default=Decimal('0.00'))
	received_quantity = Column(Numeric(14, 4), nullable=False, default=Decimal('0.0000'))

	purchase_order = relationship("PurchaseOrder", back_populates="lines")
	product = relationship("Product")

class GoodsReceipt(BaseModel, Base):
	__tablename__ = "goods_receipts"

	grn_number = Column(String(50), unique=True, nullable=False, index=True)
	Supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
	purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=True)
	warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
	receipt_date = Column(DateTime, nullable=False, default=func.now())
	notes = Column(Text, nullable=True)

	supplier = relationship("Supplier")
	purchase_order = relationship("PurchaseOrder")
	warehouse = relationship("Warehouse")
	lines = relationship("GoodsReceiptLine", back_populates="goods_receipt", cascade="all, delete-orphan")

class GoodsReceiptLine(BaseModel, Base):
	__tablename__ = "goods_receipt_lines"

	goods_receipt_id = Column(Integer, ForeignKey("goods_receipts.id"), nullable=False, index=True)
	product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
	po_line_id = Column(Integer, ForeignKey("purchase_order_lines.id"), nullable=True)
	quantity = Column(Numeric(14, 4), nullable=False, default=Decimal('0.0000'))
	unit_cost = Column(Numeric(12, 2), nullable=False, default=Decimal('0.00'))

	goods_receipt = relationship("GoodsReceipt", back_populates="lines")
	product = relationship("Product")
	po_line = relationship("PurchaseOrderLine")

# Outbound: Sales Order and Shipment
class SalesOrderStatus(str, enum.Enum):
	DRAFT = "draft"
	CONFIRMED = "confirmed"
	SHIPPED = "shipped"
	CLOSED = "closed"
	CANCELLED = "cancelled"

class SalesOrder(BaseModel, Base):
	__tablename__ = "sales_orders"

	so_number = Column(String(50), unique=True, nullable=False, index=True)
	customer_name = Column(String(200), nullable=False)
	customer_email = Column(String(200), nullable=True)
	status = Column(Enum(SalesOrderStatus), nullable=False, default=SalesOrderStatus.DRAFT)
	order_date = Column(DateTime, nullable=False, default=func.now())
	expected_ship_date = Column(DateTime, nullable=True)
	notes = Column(Text, nullable=True)
	total_amount = Column(Numeric(15, 2), nullable=False, default=Decimal('0.00'))

	lines = relationship("SalesOrderLine", back_populates="sales_order", cascade="all, delete-orphan")

class SalesOrderLine(BaseModel, Base):
	__tablename__ = "sales_order_lines"

	sales_order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=False, index=True)
	product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
	description = Column(String(255), nullable=True)
	quantity = Column(Numeric(14, 4), nullable=False, default=Decimal('0.0000'))
	unit_price = Column(Numeric(12, 2), nullable=False, default=Decimal('0.00'))
	shipped_quantity = Column(Numeric(14, 4), nullable=False, default=Decimal('0.0000'))

	sales_order = relationship("SalesOrder", back_populates="lines")
	product = relationship("Product")

class Shipment(BaseModel, Base):
	__tablename__ = "shipments"

	ship_number = Column(String(50), unique=True, nullable=False, index=True)
	sales_order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=True)
	warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
	ship_date = Column(DateTime, nullable=False, default=func.now())
	notes = Column(Text, nullable=True)

	sales_order = relationship("SalesOrder")
	warehouse = relationship("Warehouse")
	lines = relationship("ShipmentLine", back_populates="shipment", cascade="all, delete-orphan")

class ShipmentLine(BaseModel, Base):
	__tablename__ = "shipment_lines"

	shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False, index=True)
	product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
	quantity = Column(Numeric(14, 4), nullable=False, default=Decimal('0.0000'))
	unit_cost = Column(Numeric(12, 2), nullable=True)  # filled by valuation on issue
	stock_movement_id = Column(Integer, ForeignKey("stock_movements.id"), nullable=True)

	shipment = relationship("Shipment", back_populates="lines")
	product = relationship("Product")
	stock_movement = relationship("StockMovement")

# Valuation layers for FIFO/AVERAGE
class ValuationSourceType(str, enum.Enum):
	GRN = "grn"
	ADJUSTMENT = "adjustment"
	OPENING = "opening"

class InventoryValuationLayer(BaseModel, Base):
	__tablename__ = "inventory_valuation_layers"

	product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
	warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, index=True)
	quantity_remaining = Column(Numeric(14, 4), nullable=False, default=Decimal('0.0000'))
	unit_cost = Column(Numeric(12, 2), nullable=False, default=Decimal('0.00'))
	source_type = Column(Enum(ValuationSourceType), nullable=False)
	source_id = Column(Integer, nullable=True)
	created_at = Column(DateTime, nullable=False, default=func.now())

	product = relationship("Product")
	warehouse = relationship("Warehouse")
