from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field

# Product Schemas
class ProductBase(BaseModel):
	sku: str = Field(..., min_length=1, max_length=64)
	name: str = Field(..., min_length=1, max_length=200)
	description: Optional[str] = Field(None, max_length=2000)
	category: Optional[str] = Field(None, max_length=100)
	unit_of_measure: str = Field("ea", max_length=20)
	cost_price: Decimal = Field(Decimal('0.00'), ge=Decimal('0.00'))
	sale_price: Decimal = Field(Decimal('0.00'), ge=Decimal('0.00'))
	is_active: bool = True
	valuation_method: Optional[str] = Field("fifo")

class ProductCreate(ProductBase):
	pass

class ProductUpdate(BaseModel):
	name: Optional[str] = Field(None, min_length=1, max_length=200)
	description: Optional[str] = Field(None, max_length=2000)
	category: Optional[str] = Field(None, max_length=100)
	unit_of_measure: Optional[str] = Field(None, max_length=20)
	cost_price: Optional[Decimal] = Field(None, ge=Decimal('0.00'))
	sale_price: Optional[Decimal] = Field(None, ge=Decimal('0.00'))
	is_active: Optional[bool] = None

class ProductResponse(ProductBase):
	id: int
	created_at: datetime
	updated_at: datetime
	class Config:
		from_attributes = True

class ProductList(BaseModel):
	products: List[ProductResponse]
	total: int
	page: int
	size: int

# Supplier Schemas
class SupplierBase(BaseModel):
	name: str = Field(..., min_length=1, max_length=200)
	email: Optional[str] = Field(None, max_length=200)
	phone: Optional[str] = Field(None, max_length=50)
	address: Optional[str] = Field(None, max_length=2000)
	website: Optional[str] = Field(None, max_length=200)
	is_active: bool = True

class SupplierCreate(SupplierBase):
	pass

class SupplierUpdate(BaseModel):
	name: Optional[str] = Field(None, min_length=1, max_length=200)
	email: Optional[str] = Field(None, max_length=200)
	phone: Optional[str] = Field(None, max_length=50)
	address: Optional[str] = Field(None, max_length=2000)
	website: Optional[str] = Field(None, max_length=200)
	is_active: Optional[bool] = None

class SupplierResponse(SupplierBase):
	id: int
	created_at: datetime
	updated_at: datetime
	class Config:
		from_attributes = True

class SupplierList(BaseModel):
	suppliers: List[SupplierResponse]
	total: int
	page: int
	size: int

# Warehouse Schemas
class WarehouseBase(BaseModel):
	code: str = Field(..., min_length=1, max_length=20)
	name: str = Field(..., min_length=1, max_length=200)
	location: Optional[str] = Field(None, max_length=200)
	description: Optional[str] = Field(None, max_length=2000)
	is_active: bool = True

class WarehouseCreate(WarehouseBase):
	pass

class WarehouseUpdate(BaseModel):
	name: Optional[str] = Field(None, min_length=1, max_length=200)
	location: Optional[str] = Field(None, max_length=200)
	description: Optional[str] = Field(None, max_length=2000)
	is_active: Optional[bool] = None

class WarehouseResponse(WarehouseBase):
	id: int
	created_at: datetime
	updated_at: datetime
	class Config:
		from_attributes = True

class WarehouseList(BaseModel):
	warehouses: List[WarehouseResponse]
	total: int
	page: int
	size: int

# Stock Level Schemas
class StockLevelResponse(BaseModel):
	id: int
	product_id: int
	warehouse_id: int
	quantity: Decimal
	reorder_point: Decimal
	reorder_quantity: Decimal
	created_at: datetime
	updated_at: datetime
	class Config:
		from_attributes = True

class StockLevelList(BaseModel):
	stock_levels: List[StockLevelResponse]
	total: int
	page: int
	size: int

# Stock Movement Schemas
class StockMovementBase(BaseModel):
	product_id: int
	quantity: Decimal = Field(..., gt=Decimal('0'))
	movement_type: str
	from_warehouse_id: Optional[int] = None
	to_warehouse_id: Optional[int] = None
	supplier_id: Optional[int] = None
	reference: Optional[str] = Field(None, max_length=100)
	movement_date: datetime = Field(default_factory=datetime.now)
	notes: Optional[str] = Field(None, max_length=2000)

class StockReceipt(StockMovementBase):
	movement_type: str = "receipt"
	to_warehouse_id: int

class StockIssue(StockMovementBase):
	movement_type: str = "issue"
	from_warehouse_id: int

class StockTransfer(StockMovementBase):
	movement_type: str = "transfer"
	from_warehouse_id: int
	to_warehouse_id: int

class StockAdjustment(StockMovementBase):
	movement_type: str = "adjustment"

class StockMovementResponse(StockMovementBase):
	id: int
	movement_number: str
	cost_amount: Optional[Decimal]
	created_at: datetime
	updated_at: datetime
	class Config:
		from_attributes = True

class StockMovementList(BaseModel):
	movements: List[StockMovementResponse]
	total: int
	page: int
	size: int

# Procurement Schemas
class POLineCreate(BaseModel):
	product_id: int
	description: Optional[str] = None
	quantity: Decimal = Field(..., gt=Decimal('0'))
	unit_price: Decimal = Field(..., ge=Decimal('0'))

class POCreate(BaseModel):
	supplier_id: int
	expected_date: Optional[datetime] = None
	notes: Optional[str] = None
	lines: List[POLineCreate]

class POResponse(BaseModel):
	id: int
	po_number: str
	supplier_id: int
	status: str
	order_date: datetime
	expected_date: Optional[datetime]
	total_amount: Decimal
	notes: Optional[str]
	created_at: datetime
	updated_at: datetime
	class Config:
		from_attributes = True

class GRNLineCreate(BaseModel):
	product_id: int
	po_line_id: Optional[int] = None
	quantity: Decimal = Field(..., gt=Decimal('0'))
	unit_cost: Decimal = Field(..., ge=Decimal('0'))

class GRNCreate(BaseModel):
	purchase_order_id: Optional[int] = None
	warehouse_id: int
	receipt_date: Optional[datetime] = None
	notes: Optional[str] = None
	lines: List[GRNLineCreate]

class GRNResponse(BaseModel):
	id: int
	grn_number: str
	warehouse_id: int
	purchase_order_id: Optional[int]
	receipt_date: datetime
	notes: Optional[str]
	created_at: datetime
	updated_at: datetime
	class Config:
		from_attributes = True

# Outbound schemas
class SOLineCreate(BaseModel):
	product_id: int
	description: Optional[str] = None
	quantity: Decimal = Field(..., gt=Decimal('0'))
	unit_price: Decimal = Field(..., ge=Decimal('0'))

class SOCreate(BaseModel):
	customer_name: str
	customer_email: Optional[str] = None
	expected_ship_date: Optional[datetime] = None
	notes: Optional[str] = None
	lines: List[SOLineCreate]

class SOResponse(BaseModel):
	id: int
	so_number: str
	customer_name: str
	status: str
	order_date: datetime
	expected_ship_date: Optional[datetime]
	total_amount: Decimal
	notes: Optional[str]
	created_at: datetime
	updated_at: datetime
	class Config:
		from_attributes = True

class ShipmentLineCreate(BaseModel):
	product_id: int
	quantity: Decimal = Field(..., gt=Decimal('0'))

class ShipmentCreate(BaseModel):
	sales_order_id: Optional[int] = None
	warehouse_id: int
	ship_date: Optional[datetime] = None
	lines: List[ShipmentLineCreate]

class ShipmentResponse(BaseModel):
	id: int
	ship_number: str
	warehouse_id: int
	sales_order_id: Optional[int]
	ship_date: datetime
	created_at: datetime
	updated_at: datetime
	class Config:
		from_attributes = True
