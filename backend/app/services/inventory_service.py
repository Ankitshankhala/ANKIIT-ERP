from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
import uuid

from ..models.inventory import (
	Product, Supplier, Warehouse, StockLevel, StockMovement, StockMovementType,
	PurchaseOrder, PurchaseOrderLine,
	GoodsReceipt, GoodsReceiptLine,
	SalesOrder, SalesOrderLine,
	Shipment, ShipmentLine,
	InventoryValuationLayer, ValuationMethod
)
from ..schemas.inventory import (
	ProductCreate, ProductUpdate,
	SupplierCreate, SupplierUpdate,
	WarehouseCreate, WarehouseUpdate,
	StockReceipt, StockIssue, StockTransfer, StockAdjustment,
	POCreate, GRNCreate, SOCreate, ShipmentCreate
)
from ..core.exceptions import BusinessLogicError, ValidationError, NotFoundError

class InventoryService:
	def __init__(self, db: Session):
		self.db = db

	# Product Management
	def create_product(self, data: ProductCreate) -> Product:
		if self.db.query(Product).filter(Product.sku == data.sku).first():
			raise ValidationError(f"Product with SKU '{data.sku}' already exists")
		product = Product(**data.dict())
		self.db.add(product)
		self.db.commit()
		self.db.refresh(product)
		return product

	def update_product(self, product_id: int, data: ProductUpdate) -> Optional[Product]:
		product = self.db.query(Product).filter(Product.id == product_id).first()
		if not product:
			return None
		for field, value in data.dict(exclude_unset=True).items():
			setattr(product, field, value)
		self.db.commit()
		self.db.refresh(product)
		return product

	def get_products(self, skip: int = 0, limit: int = 100, q: Optional[str] = None, sort_by: Optional[str] = None, sort_dir: Optional[str] = None) -> List[Product]:
		query = self.db.query(Product)
		if q:
			like = f"%{q}%"
			query = query.filter((Product.name.ilike(like)) | (Product.sku.ilike(like)))
		# sorting
		colmap = {
			"created_at": Product.created_at,
			"updated_at": Product.updated_at,
			"name": Product.name,
			"sku": Product.sku,
			"cost_price": Product.cost_price,
			"sale_price": Product.sale_price,
		}
		col = colmap.get((sort_by or "created_at"))
		if sort_dir == "asc":
			query = query.order_by(col.asc())
		else:
			query = query.order_by(col.desc())
		return query.offset(skip).limit(limit).all()

	def count_products(self, q: Optional[str] = None) -> int:
		query = self.db.query(Product)
		if q:
			like = f"%{q}%"
			query = query.filter((Product.name.ilike(like)) | (Product.sku.ilike(like)))
		return query.count()

	def get_product(self, product_id: int) -> Optional[Product]:
		return self.db.query(Product).filter(Product.id == product_id).first()

	def delete_product(self, product_id: int) -> bool:
		product = self.get_product(product_id)
		if not product:
			return False
		self.db.delete(product)
		self.db.commit()
		return True

	# Supplier Management
	def create_supplier(self, data: SupplierCreate) -> Supplier:
		supplier = Supplier(**data.dict())
		self.db.add(supplier)
		self.db.commit()
		self.db.refresh(supplier)
		return supplier

	def update_supplier(self, supplier_id: int, data: SupplierUpdate) -> Optional[Supplier]:
		supplier = self.db.query(Supplier).filter(Supplier.id == supplier_id).first()
		if not supplier:
			return None
		for field, value in data.dict(exclude_unset=True).items():
			setattr(supplier, field, value)
		self.db.commit()
		self.db.refresh(supplier)
		return supplier

	def get_suppliers(self, skip: int = 0, limit: int = 100, q: Optional[str] = None, sort_by: Optional[str] = None, sort_dir: Optional[str] = None) -> List[Supplier]:
		query = self.db.query(Supplier)
		if q:
			like = f"%{q}%"
			query = query.filter((Supplier.name.ilike(like)) | (Supplier.email.ilike(like)))
		colmap = {
			"created_at": Supplier.created_at,
			"updated_at": Supplier.updated_at,
			"name": Supplier.name,
			"email": Supplier.email,
		}
		col = colmap.get((sort_by or "created_at"))
		if sort_dir == "asc":
			query = query.order_by(col.asc())
		else:
			query = query.order_by(col.desc())
		return query.offset(skip).limit(limit).all()

	def count_suppliers(self, q: Optional[str] = None) -> int:
		query = self.db.query(Supplier)
		if q:
			like = f"%{q}%"
			query = query.filter((Supplier.name.ilike(like)) | (Supplier.email.ilike(like)))
		return query.count()

	def get_supplier(self, supplier_id: int) -> Optional[Supplier]:
		return self.db.query(Supplier).filter(Supplier.id == supplier_id).first()

	def delete_supplier(self, supplier_id: int) -> bool:
		supplier = self.get_supplier(supplier_id)
		if not supplier:
			return False
		self.db.delete(supplier)
		self.db.commit()
		return True

	# Warehouse Management
	def create_warehouse(self, data: WarehouseCreate) -> Warehouse:
		if self.db.query(Warehouse).filter(Warehouse.code == data.code).first():
			raise ValidationError(f"Warehouse code '{data.code}' already exists")
		warehouse = Warehouse(**data.dict())
		self.db.add(warehouse)
		self.db.commit()
		self.db.refresh(warehouse)
		return warehouse

	def update_warehouse(self, warehouse_id: int, data: WarehouseUpdate) -> Optional[Warehouse]:
		warehouse = self.db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
		if not warehouse:
			return None
		for field, value in data.dict(exclude_unset=True).items():
			setattr(warehouse, field, value)
		self.db.commit()
		self.db.refresh(warehouse)
		return warehouse

	def get_warehouses(self, skip: int = 0, limit: int = 100, q: Optional[str] = None, sort_by: Optional[str] = None, sort_dir: Optional[str] = None) -> List[Warehouse]:
		query = self.db.query(Warehouse)
		if q:
			like = f"%{q}%"
			query = query.filter((Warehouse.name.ilike(like)) | (Warehouse.code.ilike(like)) | (Warehouse.location.ilike(like)))
		colmap = {
			"created_at": Warehouse.created_at,
			"updated_at": Warehouse.updated_at,
			"name": Warehouse.name,
			"code": Warehouse.code,
		}
		col = colmap.get((sort_by or "created_at"))
		if sort_dir == "asc":
			query = query.order_by(col.asc())
		else:
			query = query.order_by(col.desc())
		return query.offset(skip).limit(limit).all()

	def count_warehouses(self, q: Optional[str] = None) -> int:
		query = self.db.query(Warehouse)
		if q:
			like = f"%{q}%"
			query = query.filter((Warehouse.name.ilike(like)) | (Warehouse.code.ilike(like)) | (Warehouse.location.ilike(like)))
		return query.count()

	def get_warehouse(self, warehouse_id: int) -> Optional[Warehouse]:
		return self.db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

	def delete_warehouse(self, warehouse_id: int) -> bool:
		warehouse = self.get_warehouse(warehouse_id)
		if not warehouse:
			return False
		self.db.delete(warehouse)
		self.db.commit()
		return True

	# Stock utilities
	def _get_or_create_stock_level(self, product_id: int, warehouse_id: int) -> StockLevel:
		stock = self.db.query(StockLevel).filter(
			StockLevel.product_id == product_id,
			StockLevel.warehouse_id == warehouse_id
		).first()
		if stock is None:
			stock = StockLevel(product_id=product_id, warehouse_id=warehouse_id, quantity=Decimal('0'))
			self.db.add(stock)
			self.db.flush()
		return stock

	def _create_movement(self, product_id: int, qty: Decimal, movement_type: StockMovementType, from_wh: Optional[int], to_wh: Optional[int], supplier_id: Optional[int], reference: Optional[str], notes: Optional[str]) -> StockMovement:
		movement_number = f"STK-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
		movement = StockMovement(
			movement_number=movement_number,
			product_id=product_id,
			quantity=qty,
			movement_type=movement_type,
			from_warehouse_id=from_wh,
			to_warehouse_id=to_wh,
			supplier_id=supplier_id,
			reference=reference,
			notes=notes
		)
		self.db.add(movement)
		return movement

	# Valuation utilities
	def _push_layer(self, product_id: int, warehouse_id: int, quantity: Decimal, unit_cost: Decimal, source_type: str, source_id: Optional[int]):
		layer = InventoryValuationLayer(
			product_id=product_id,
			warehouse_id=warehouse_id,
			quantity_remaining=quantity,
			unit_cost=unit_cost,
			source_type=source_type,
			source_id=source_id,
		)
		self.db.add(layer)
		self.db.flush()
		return layer

	def _consume_layers_fifo(self, product_id: int, warehouse_id: int, quantity: Decimal) -> Decimal:
		remaining = quantity
		total_cost = Decimal('0.00')
		layers = self.db.query(InventoryValuationLayer).filter(
			InventoryValuationLayer.product_id == product_id,
			InventoryValuationLayer.warehouse_id == warehouse_id,
			InventoryValuationLayer.quantity_remaining > 0
		).order_by(InventoryValuationLayer.created_at.asc()).all()
		for layer in layers:
			if remaining <= 0:
				break
			use_qty = min(layer.quantity_remaining, remaining)
			total_cost += use_qty * layer.unit_cost
			layer.quantity_remaining = layer.quantity_remaining - use_qty
			remaining = remaining - use_qty
		if remaining > 0:
			raise BusinessLogicError("Insufficient valuation layers for FIFO issue")
		return total_cost

	def _consume_layers_average(self, product_id: int, warehouse_id: int, quantity: Decimal) -> Decimal:
		# Compute weighted avg from all remaining layers
		layers = self.db.query(InventoryValuationLayer).filter(
			InventoryValuationLayer.product_id == product_id,
			InventoryValuationLayer.warehouse_id == warehouse_id,
			InventoryValuationLayer.quantity_remaining > 0
		).all()
		total_qty = sum((l.quantity_remaining for l in layers), Decimal('0.0000'))
		if total_qty <= 0:
			raise BusinessLogicError("No stock available for average issue")
		total_value = sum((l.quantity_remaining * l.unit_cost for l in layers), Decimal('0.00'))
		avg_cost = (total_value / total_qty).quantize(Decimal('0.01'))
		# consume proportionally from layers
		remaining = quantity
		for layer in layers:
			if remaining <= 0:
				break
			use_qty = min(layer.quantity_remaining, remaining)
			layer.quantity_remaining = layer.quantity_remaining - use_qty
			remaining = remaining - use_qty
		if remaining > 0:
			raise BusinessLogicError("Insufficient stock for average issue")
		return (quantity * avg_cost).quantize(Decimal('0.01'))

	# Receipts (increase stock)
	def receive_stock(self, data: StockReceipt) -> StockMovement:
		product = self.get_product(data.product_id)
		if not product or not product.is_active:
			raise NotFoundError("Product not found or inactive")
		warehouse = self.get_warehouse(data.to_warehouse_id)
		if not warehouse or not warehouse.is_active:
			raise NotFoundError("Warehouse not found or inactive")
		stock = self._get_or_create_stock_level(product.id, warehouse.id)
		stock.quantity = (stock.quantity or Decimal('0')) + data.quantity
		movement = self._create_movement(product.id, data.quantity, StockMovementType.RECEIPT, None, warehouse.id, data.supplier_id, data.reference, data.notes)
		# push valuation layer using provided product cost or default cost_price
		unit_cost = product.cost_price
		self._push_layer(product.id, warehouse.id, data.quantity, unit_cost, "adjustment" if not data.supplier_id else "grn", None)
		self.db.commit()
		self.db.refresh(movement)
		return movement

	# Issues (decrease stock)
	def issue_stock(self, data: StockIssue) -> StockMovement:
		product = self.get_product(data.product_id)
		if not product or not product.is_active:
			raise NotFoundError("Product not found or inactive")
		warehouse = self.get_warehouse(data.from_warehouse_id)
		if not warehouse or not warehouse.is_active:
			raise NotFoundError("Warehouse not found or inactive")
		stock = self._get_or_create_stock_level(product.id, warehouse.id)
		if (stock.quantity or Decimal('0')) < data.quantity:
			raise BusinessLogicError("Insufficient stock for issue")
		stock.quantity = stock.quantity - data.quantity
		# valuation
		if product.valuation_method == ValuationMethod.FIFO:
			cost_amount = self._consume_layers_fifo(product.id, warehouse.id, data.quantity)
		else:
			cost_amount = self._consume_layers_average(product.id, warehouse.id, data.quantity)
		movement = self._create_movement(product.id, data.quantity, StockMovementType.ISSUE, warehouse.id, None, None, data.reference, data.notes)
		movement.cost_amount = cost_amount
		self.db.commit()
		self.db.refresh(movement)
		return movement

	# Transfer between warehouses
	def transfer_stock(self, data: StockTransfer) -> StockMovement:
		product = self.get_product(data.product_id)
		if not product or not product.is_active:
			raise NotFoundError("Product not found or inactive")
		from_wh = self.get_warehouse(data.from_warehouse_id)
		to_wh = self.get_warehouse(data.to_warehouse_id)
		if not from_wh or not to_wh:
			raise NotFoundError("Invalid warehouse for transfer")
		if not from_wh.is_active or not to_wh.is_active:
			raise BusinessLogicError("Warehouse inactive")
		from_stock = self._get_or_create_stock_level(product.id, from_wh.id)
		to_stock = self._get_or_create_stock_level(product.id, to_wh.id)
		if (from_stock.quantity or Decimal('0')) < data.quantity:
			raise BusinessLogicError("Insufficient stock for transfer")
		from_stock.quantity = from_stock.quantity - data.quantity
		to_stock.quantity = (to_stock.quantity or Decimal('0')) + data.quantity
		movement = self._create_movement(product.id, data.quantity, StockMovementType.TRANSFER, from_wh.id, to_wh.id, None, data.reference, data.notes)
		self.db.commit()
		self.db.refresh(movement)
		return movement

	# Adjustment (increase or decrease based on sign)
	def adjust_stock(self, data: StockAdjustment) -> StockMovement:
		product = self.get_product(data.product_id)
		if not product or not product.is_active:
			raise NotFoundError("Product not found or inactive")
		# Choose warehouse: prefer to_warehouse_id then from_warehouse_id
		warehouse_id = data.to_warehouse_id or data.from_warehouse_id
		if not warehouse_id:
			raise ValidationError("Warehouse must be provided for adjustment")
		warehouse = self.get_warehouse(warehouse_id)
		if not warehouse or not warehouse.is_active:
			raise NotFoundError("Warehouse not found or inactive")
		stock = self._get_or_create_stock_level(product.id, warehouse.id)
		# Positive quantity increases stock, negative decreases
		qty = data.quantity
		new_qty = (stock.quantity or Decimal('0')) + qty
		if new_qty < 0:
			raise BusinessLogicError("Adjustment would make stock negative")
		stock.quantity = new_qty
		movement = self._create_movement(product.id, qty, StockMovementType.ADJUSTMENT, None, warehouse.id, None, data.reference, data.notes)
		if qty > 0:
			# add valuation layer at current product cost
			self._push_layer(product.id, warehouse.id, qty, product.cost_price, "adjustment", None)
		self.db.commit()
		self.db.refresh(movement)
		return movement

	# Procurement Flow: PO -> GRN
	def create_purchase_order(self, data: POCreate) -> PurchaseOrder:
		supplier = self.get_supplier(data.supplier_id)
		if not supplier or not supplier.is_active:
			raise NotFoundError("Supplier not found or inactive")
		po_number = f"PO-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
		po = PurchaseOrder(
			po_number=po_number,
			supplier_id=data.supplier_id,
			expected_date=data.expected_date,
			notes=data.notes,
		)
		total = Decimal('0.00')
		for line in data.lines:
			pol = PurchaseOrderLine(
				product_id=line.product_id,
				description=line.description,
				quantity=line.quantity,
				unit_price=line.unit_price,
			)
			po.lines.append(pol)
			total += (line.quantity or Decimal('0')) * (line.unit_price or Decimal('0'))
		po.total_amount = total
		self.db.add(po)
		self.db.commit()
		self.db.refresh(po)
		return po

	def receive_goods(self, data: GRNCreate) -> GoodsReceipt:
		warehouse = self.get_warehouse(data.warehouse_id)
		if not warehouse or not warehouse.is_active:
			raise NotFoundError("Warehouse not found or inactive")
		po = None
		if data.purchase_order_id:
			po = self.db.query(PurchaseOrder).filter(PurchaseOrder.id == data.purchase_order_id).first()
		grn_number = f"GRN-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
		grn = GoodsReceipt(
			grn_number=grn_number,
			purchase_order_id=data.purchase_order_id,
			warehouse_id=data.warehouse_id,
			receipt_date=data.receipt_date or datetime.now(),
			notes=data.notes,
		)
		self.db.add(grn)
		self.db.flush()
		for line in data.lines:
			product = self.get_product(line.product_id)
			if not product or not product.is_active:
				raise NotFoundError("Product not found or inactive")
			pol = self.db.query(PurchaseOrderLine).filter(PurchaseOrderLine.id == line.po_line_id).first() if line.po_line_id else None
			grn_line = GoodsReceiptLine(
				goods_receipt_id=grn.id,
				product_id=product.id,
				po_line_id=pol.id if pol else None,
				quantity=line.quantity,
				unit_cost=line.unit_cost,
			)
			self.db.add(grn_line)
			# update stock and valuation layer
			stock = self._get_or_create_stock_level(product.id, warehouse.id)
			stock.quantity = (stock.quantity or Decimal('0')) + line.quantity
			self._push_layer(product.id, warehouse.id, line.quantity, line.unit_cost, "grn", grn.id)
			# update PO received qty
			if pol:
				pol.received_quantity = (pol.received_quantity or Decimal('0')) + line.quantity
		self.db.commit()
		self.db.refresh(grn)
		# if PO fully received, mark received
		if po:
			all_received = all((ln.received_quantity or Decimal('0')) >= (ln.quantity or Decimal('0')) for ln in po.lines)
			if all_received:
				po.status = "received"
				self.db.commit()
		return grn

	# Outbound Flow: SO -> Shipment -> AR Invoice (created in finance module)
	def create_sales_order(self, data: SOCreate) -> SalesOrder:
		so_number = f"SO-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
		so = SalesOrder(
			so_number=so_number,
			customer_name=data.customer_name,
			customer_email=data.customer_email,
			expected_ship_date=data.expected_ship_date,
			notes=data.notes,
		)
		total = Decimal('0.00')
		for line in data.lines:
			item = SalesOrderLine(
				product_id=line.product_id,
				description=line.description,
				quantity=line.quantity,
				unit_price=line.unit_price,
			)
			so.lines.append(item)
			total += (line.quantity or Decimal('0')) * (line.unit_price or Decimal('0'))
		so.total_amount = total
		self.db.add(so)
		self.db.commit()
		self.db.refresh(so)
		return so

	def create_shipment(self, data: ShipmentCreate) -> Shipment:
		warehouse = self.get_warehouse(data.warehouse_id)
		if not warehouse or not warehouse.is_active:
			raise NotFoundError("Warehouse not found or inactive")
		so = None
		if data.sales_order_id:
			so = self.db.query(SalesOrder).filter(SalesOrder.id == data.sales_order_id).first()
		ship_number = f"SHP-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
		shipment = Shipment(
			ship_number=ship_number,
			sales_order_id=data.sales_order_id,
			warehouse_id=data.warehouse_id,
			ship_date=data.ship_date or datetime.now(),
		)
		self.db.add(shipment)
		self.db.flush()
		total_issue_cost = Decimal('0.00')
		for line in data.lines:
			product = self.get_product(line.product_id)
			if not product or not product.is_active:
				raise NotFoundError("Product not found or inactive")
			# issue stock with valuation
			stock = self._get_or_create_stock_level(product.id, warehouse.id)
			if (stock.quantity or Decimal('0')) < line.quantity:
				raise BusinessLogicError("Insufficient stock for shipment")
			# value the issue
			if product.valuation_method == ValuationMethod.FIFO:
				cost_amount = self._consume_layers_fifo(product.id, warehouse.id, line.quantity)
			else:
				cost_amount = self._consume_layers_average(product.id, warehouse.id, line.quantity)
			stock.quantity = stock.quantity - line.quantity
			move = self._create_movement(product.id, line.quantity, StockMovementType.ISSUE, warehouse.id, None, None, ship_number, None)
			move.cost_amount = cost_amount
			sl = ShipmentLine(
				shipment_id=shipment.id,
				product_id=product.id,
				quantity=line.quantity,
				unit_cost=(cost_amount / line.quantity).quantize(Decimal('0.01')),
				stock_movement_id=move.id,
			)
			self.db.add(sl)
			total_issue_cost += cost_amount
			# update SO shipped qty
			if so:
				for sline in so.lines:
					if sline.product_id == product.id:
						sline.shipped_quantity = (sline.shipped_quantity or Decimal('0')) + line.quantity
		self.db.commit()
		self.db.refresh(shipment)
		# mark SO shipped if fully shipped
		if so:
			fully = all((ln.shipped_quantity or Decimal('0')) >= (ln.quantity or Decimal('0')) for ln in so.lines)
			if fully:
				so.status = "shipped"
				self.db.commit()
		return shipment

	def create_invoice_for_shipment(self, shipment_id: int):
		from ..services.finance_service import FinanceService
		from ..schemas.finance import InvoiceCreate, InvoiceLineItemCreate
		shipment = self.db.query(Shipment).filter(Shipment.id == shipment_id).first()
		if not shipment:
			raise NotFoundError("Shipment not found")
		so = None
		if shipment.sales_order_id:
			so = self.db.query(SalesOrder).filter(SalesOrder.id == shipment.sales_order_id).first()
		# Build invoice payload
		customer_name = so.customer_name if so else "Walk-in Customer"
		customer_email = so.customer_email if so else None
		items: List[InvoiceLineItemCreate] = []
		for line in shipment.lines or []:
			product = self.get_product(line.product_id)
			if not product:
				raise NotFoundError("Product not found for shipment line")
			items.append(InvoiceLineItemCreate(
				description=product.name,
				quantity=line.quantity,
				unit_price=product.sale_price,
				discount_amount=Decimal('0.00'),
				tax_rate=Decimal('0.0000'),
				product_sku=product.sku,
			))
		payload = InvoiceCreate(
			customer_name=customer_name,
			customer_email=customer_email,
			customer_address=None,
			invoice_date=datetime.now(),
			due_date=datetime.now(),
			invoice_type="sale",
			notes=f"Invoice for shipment {shipment.ship_number}",
			items=items,
		)
		fin = FinanceService(self.db)
		invoice = fin.create_invoice(payload)
		fin.post_invoice(invoice.id)
		return invoice
