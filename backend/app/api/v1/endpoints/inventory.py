from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import require_permission
from ....models.user import User
from ....services.inventory_service import InventoryService
from ....schemas.inventory import (
	ProductCreate, ProductUpdate, ProductResponse, ProductList,
	SupplierCreate, SupplierUpdate, SupplierResponse, SupplierList,
	WarehouseCreate, WarehouseUpdate, WarehouseResponse, WarehouseList,
	StockReceipt, StockIssue, StockTransfer, StockAdjustment, StockMovementResponse, StockMovementList,
	StockLevelResponse, StockLevelList,
	POCreate, POResponse, GRNCreate, GRNResponse,
	SOCreate, SOResponse, ShipmentCreate, ShipmentResponse
)
from ....core.exceptions import BusinessLogicError, ValidationError, NotFoundError

router = APIRouter()

# Products
@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:product:create"))):
	service = InventoryService(db)
	try:
		return service.create_product(data)
	except ValidationError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/products", response_model=ProductList)
async def list_products(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), q: Optional[str] = Query(None), sort_by: Optional[str] = Query(None), sort_dir: Optional[str] = Query("desc"), db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:product:read"))):
	service = InventoryService(db)
	products = service.get_products(skip=skip, limit=limit, q=q, sort_by=sort_by, sort_dir=sort_dir)
	total = service.count_products(q=q)
	return ProductList(products=products, total=total, page=skip // limit + 1, size=limit)

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:product:read"))):
	service = InventoryService(db)
	product = service.get_product(product_id)
	if not product:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
	return product

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:product:update"))):
	service = InventoryService(db)
	product = service.update_product(product_id, data)
	if not product:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
	return product

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:product:delete"))):
	service = InventoryService(db)
	success = service.delete_product(product_id)
	if not success:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
	return None

# Suppliers
@router.post("/suppliers", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
async def create_supplier(data: SupplierCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:supplier:create"))):
	service = InventoryService(db)
	return service.create_supplier(data)

@router.get("/suppliers", response_model=SupplierList)
async def list_suppliers(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), q: Optional[str] = Query(None), sort_by: Optional[str] = Query(None), sort_dir: Optional[str] = Query("desc"), db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:supplier:read"))):
	service = InventoryService(db)
	suppliers = service.get_suppliers(skip=skip, limit=limit, q=q, sort_by=sort_by, sort_dir=sort_dir)
	total = service.count_suppliers(q=q)
	return SupplierList(suppliers=suppliers, total=total, page=skip // limit + 1, size=limit)

@router.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(supplier_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:supplier:read"))):
	service = InventoryService(db)
	supplier = service.get_supplier(supplier_id)
	if not supplier:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
	return supplier

@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(supplier_id: int, data: SupplierUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:supplier:update"))):
	service = InventoryService(db)
	supplier = service.update_supplier(supplier_id, data)
	if not supplier:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
	return supplier

@router.delete("/suppliers/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(supplier_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:supplier:delete"))):
	service = InventoryService(db)
	success = service.delete_supplier(supplier_id)
	if not success:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
	return None

# Warehouses
@router.post("/warehouses", response_model=WarehouseResponse, status_code=status.HTTP_201_CREATED)
async def create_warehouse(data: WarehouseCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:warehouse:create"))):
	service = InventoryService(db)
	try:
		return service.create_warehouse(data)
	except ValidationError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/warehouses", response_model=WarehouseList)
async def list_warehouses(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), q: Optional[str] = Query(None), sort_by: Optional[str] = Query(None), sort_dir: Optional[str] = Query("desc"), db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:warehouse:read"))):
	service = InventoryService(db)
	warehouses = service.get_warehouses(skip=skip, limit=limit, q=q, sort_by=sort_by, sort_dir=sort_dir)
	total = service.count_warehouses(q=q)
	return WarehouseList(warehouses=warehouses, total=total, page=skip // limit + 1, size=limit)

@router.get("/warehouses/{warehouse_id}", response_model=WarehouseResponse)
async def get_warehouse(warehouse_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:warehouse:read"))):
	service = InventoryService(db)
	warehouse = service.get_warehouse(warehouse_id)
	if not warehouse:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
	return warehouse

@router.put("/warehouses/{warehouse_id}", response_model=WarehouseResponse)
async def update_warehouse(warehouse_id: int, data: WarehouseUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:warehouse:update"))):
	service = InventoryService(db)
	warehouse = service.update_warehouse(warehouse_id, data)
	if not warehouse:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
	return warehouse

@router.delete("/warehouses/{warehouse_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:warehouse:delete"))):
	service = InventoryService(db)
	success = service.delete_warehouse(warehouse_id)
	if not success:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
	return None

# Stock operations
@router.post("/stock/receive", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED)
async def receive_stock(data: StockReceipt, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:stock:receive"))):
	service = InventoryService(db)
	try:
		return service.receive_stock(data)
	except (BusinessLogicError, ValidationError, NotFoundError) as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/stock/issue", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED)
async def issue_stock(data: StockIssue, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:stock:issue"))):
	service = InventoryService(db)
	try:
		return service.issue_stock(data)
	except (BusinessLogicError, ValidationError, NotFoundError) as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/stock/transfer", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED)
async def transfer_stock(data: StockTransfer, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:stock:transfer"))):
	service = InventoryService(db)
	try:
		return service.transfer_stock(data)
	except (BusinessLogicError, ValidationError, NotFoundError) as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/stock/adjust", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED)
async def adjust_stock(data: StockAdjustment, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:stock:adjust"))):
	service = InventoryService(db)
	try:
		return service.adjust_stock(data)
	except (BusinessLogicError, ValidationError, NotFoundError) as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Procurement endpoints
@router.post("/purchase-orders", response_model=POResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase_order(data: POCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:po:create"))):
    service = InventoryService(db)
    try:
        return service.create_purchase_order(data)
    except (BusinessLogicError, ValidationError, NotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/goods-receipts", response_model=GRNResponse, status_code=status.HTTP_201_CREATED)
async def create_goods_receipt(data: GRNCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:grn:create"))):
    service = InventoryService(db)
    try:
        return service.receive_goods(data)
    except (BusinessLogicError, ValidationError, NotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Outbound endpoints
@router.post("/sales-orders", response_model=SOResponse, status_code=status.HTTP_201_CREATED)
async def create_sales_order(data: SOCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:so:create"))):
    service = InventoryService(db)
    try:
        return service.create_sales_order(data)
    except (BusinessLogicError, ValidationError, NotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/shipments", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(data: ShipmentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:shipment:create"))):
    service = InventoryService(db)
    try:
        return service.create_shipment(data)
    except (BusinessLogicError, ValidationError, NotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/shipments/{shipment_id}/invoice", response_model=dict)
async def invoice_shipment(shipment_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("inventory:shipment:invoice"))):
    service = InventoryService(db)
    try:
        invoice = service.create_invoice_for_shipment(shipment_id)
        return {"invoice_id": invoice.id, "invoice_number": invoice.invoice_number}
    except (BusinessLogicError, ValidationError, NotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
