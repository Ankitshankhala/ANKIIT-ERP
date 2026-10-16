import pytest

LIST_ENDPOINTS = [
    "/api/v1/users/",
    "/api/v1/organizations/",
    "/api/v1/roles/",
    "/api/v1/tenants/",
    "/api/v1/dashboard/stats",
    "/api/v1/dashboard/recent-activity",
    "/api/v1/dashboard/quick-stats",
    "/api/v1/finance/accounts",
    "/api/v1/finance/transactions",
    "/api/v1/finance/invoices",
    "/api/v1/finance/payments",
    "/api/v1/finance/reports/summary",
    "/api/v1/finance/reports/cash-flow",
    "/api/v1/finance/reports/metrics",
    "/api/v1/finance/reports/balance-sheet",
    "/api/v1/finance/reports/profit-and-loss",
    "/api/v1/finance/periods",
    "/api/v1/inventory/products",
    "/api/v1/inventory/suppliers",
    "/api/v1/inventory/warehouses",
    "/api/v1/crm/customers",
    "/api/v1/crm/leads",
    "/api/v1/crm/opportunities",
    "/api/v1/crm/opportunities/pipeline",
    "/api/v1/crm/communications",
    "/api/v1/hr/employees",
    "/api/v1/hr/attendance",
    "/api/v1/hr/payrolls",
    "/api/v1/hr/leaves",
]


@pytest.mark.parametrize("path", LIST_ENDPOINTS)
def test_list_endpoint_as_admin(client, admin_headers, path):
    response = client.get(path, headers=admin_headers)
    assert response.status_code == 200, response.text


def test_seeded_accounts_present(client, admin_headers):
    response = client.get("/api/v1/finance/accounts", headers=admin_headers)
    assert response.status_code == 200
    assert "1000_CASH" in response.text


@pytest.mark.parametrize(
    "path, payload, list_key",
    [
        ("/api/v1/crm/customers", {"name": "Smoke Customer", "email": "c@example.com"}, "customers"),
        ("/api/v1/inventory/products", {"sku": "SMOKE-1", "name": "Smoke Product", "cost_price": "5.00", "sale_price": "9.50"}, "products"),
        ("/api/v1/hr/employees", {"first_name": "Smoke", "last_name": "Employee", "email": "e@example.com"}, "employees"),
        ("/api/v1/finance/accounts", {"code": "6100_SMOKE", "name": "Smoke Expense", "account_type": "expense", "category": "operating_expenses"}, "accounts"),
    ],
)
def test_create_then_list(client, admin_headers, path, payload, list_key):
    created = client.post(path, json=payload, headers=admin_headers)
    assert created.status_code == 201, created.text
    created_id = created.json()["id"]

    listed = client.get(path, headers=admin_headers)
    assert listed.status_code == 200, listed.text
    body = listed.json()
    items = body[list_key] if isinstance(body, dict) else body
    assert created_id in [item["id"] for item in items]
