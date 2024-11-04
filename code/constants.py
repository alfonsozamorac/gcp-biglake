
class Constants:

    FORMAT = "iceberg"
    CATALOG = "lakehouse"
    CUSTOMERS_TABLE_NAME = "customers"
    SALES_TABLE_NAME = "sales"
    CUSTOMERS_FIELDS = {
        "customer_id": "bigint",
        "name": "string",
        "email": "string"
    }
    SALES_FIELDS = {
        "order_id": "BIGINT",
        "product": "STRING",
        "price": "STRING",
        "amount": "BIGINT",
        "customer_id": "BIGINT",
        "year": "INT",
        "month": "INT",
        "day": "INT"
    }
    PARTITIONS = ["year", "month", "day"]
    CUSTOMERS_DATA = [
        (6, "John Doe", "john.doe@example.com"),
        (7, "Alice Smith", "alice.smith@example.com"),
        (8, "Carlos Rodriguez", "carlos.rodriguez@example.com"),
        (9, "Emily Johnson", "emily.johnson@example.com"),
        (10, "Miguel Garcia", "miguel.garcia@example.com")
    ]
    CUSTOMERS_COLUMS = ["customer_id", "name", "email"]
    SALES_DATA = [
        (101, "Laptop", 2500.10, 2, 1, 2024, 11, 1),
        (102, "Smartphone", 800.00, 1, 3, 2024, 11, 2),
        (103, "Headphones", 150.35, 4, 2, 2024, 11, 3),
        (104, "Tablet", 500.99, 1, 4, 2024, 11, 4),
        (105, "Printer", 300.00, 1, 5, 2024, 11, 5)
    ]
    SALES_COLUMNS = ["order_id", "product", "price",
                     "amount", "customer_id", "year", "month", "day"]
