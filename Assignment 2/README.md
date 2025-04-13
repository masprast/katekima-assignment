# ASSIGNMENT 2

Di Assignment 2 ini adalah membuat backend menggunakan Django dengan django-rest-framework.

### # Prerequisites
1. Django v5.1 atau lebih baru
2. django-rest-framework v3.12 atau lebih baru
3. virtualenv v20 atau lebih baru

### # Testing
Untuk melakukan pengetesan, cukup dengan menjalankan file run_assignment2, karena skrip tersebut sudah mencakup
setup environtment untuk menjalankan backend.
> * Dijalankan pada komputer dengan sistem operasi linux

```shell
./run_assignment2.sh
```

#### # Database
Database yang digunakan adalah konfigurasi default dari Django yang menggunakan SQLite, sehingga tidak
perlu konfigurasi koneksi database lain.

#### # Endpoint
Sesuai dengan yang ada pada assignment, endpoint yang telah penulis tes dan konfirmasi berfungsi dengan baik.

---
### ## Items
- Endpoint: `[GET]` `items/`
- Payload: -
- Response:
```json
[
  {
    "code": "I-001",
    "name": "History Book",
    "unit": "Pcs",
    "description": "Books that tells history of the ancient",
    "stock": 2,
    "balance": 120000
  },
  {
    "code": "I-002",
    "name": "Math Book",
    "unit": "Pcs",
    "description": "Books that teach how to do Math",
    "stock": 8,
    "balance": 340000
  },
  ...
]
```
---
- Endpoint: `[POST]` `items/`
- Payload:
```json
{
	"code": "I-001",
	"name": "History Book",
	"unit": "Pcs",
	"description": "Books that tells history of the ancient"
}
```
- Response:
```json
{
    "code": "I-001",
    "name": "History Book",
    "unit": "Pcs",
    "description": "Books that tells history of the ancient"
}
```
---
- Endpoint: `[GET]` `items/{code}` >>>> `items/i-002`
- Query: -
- Payload: -
- Response:
```json
{
  "code": "I-002",
  "name": "Math Book",
  "unit": "Pcs",
  "description": "Books that teach how to do Math",
  "stock": 8,
  "balance": 340000
}
```
---
- Endpoint: `[PUT]` `items/{code}/` >>>> `items/i-001/`
- Payload:
```json
{
	"code": "I-001",
	"name": "History Book about Traditional receipt",
	"unit": "Pcs",
	"description": "Books that tells history of the ancient"
}
```
- Response:
```json
{
	"code": "I-001",
	"name": "History Book about Traditional receipt",
	"unit": "Pcs",
	"description": "Books that tells history of the ancient"
}
```
- Endpoint: `[DELETE]` `items/{code}/`
- Payload: -
- Response: -

---
---
---
### ## Purchases
- Endpoint: `[GET]` `purchase/`
- Payload: -
- Response:
```json
[
  {
    "code": "P-001",
    "date": "2025-01-01",
    "description": "Buy history books",
    "details": [
      {
        "item_code": "I-001",
        "quantity": 10,
        "unit_price": 60000,
        "header_code": "P-001"
      },
      {
        "item_code": "I-002",
        "quantity": 4,
        "unit_price": 50000,
        "header_code": "P-001"
      }
    ]
  },
  {
    "code": "P-002",
    "date": "2025-01-01",
    "description": "Buy math books",
    "details": [
      {
        "item_code": "I-002",
        "quantity": 12,
        "unit_price": 45000,
        "header_code": "P-002"
      }
    ]
  },
  ...
]

```
---
- Endpoint: `[POST]` `purchase/`
- Payload:
```json
{
  "code": "P-005",
  "date": "2025-03-01",
  "description": "Restock cookbooks"
}
```
- Response:
```json
{
  "code": "P-005",
  "date": "2025-03-01",
  "description": "Restock cookbooks"
}
```
---
- Endpoint: `[GET]` `purchase/{code}` >>>> `purchase/p-001`
- Payload: -
- Response:
```json
{
  "code": "P-001",
  "date": "2025-01-01",
  "description": "Buy history books",
  "details": [
    {
      "item_code": "I-001",
      "quantity": 10,
      "unit_price": 60000,
      "header_code": "P-001"
    },
    {
      "item_code": "I-002",
      "quantity": 4,
      "unit_price": 50000,
      "header_code": "P-001"
    }
  ]
}
```
---
- Endpoint: `[PUT]` `purchase/{code}/` >>>> `purchase/p-002/`
- Payload:
```json
{
  "code": "P-002",
  "date": "2025-01-01",
  "description": "Buy math books"
}

```
- Response:
```json
{
  "code": "P-002",
  "date": "2025-01-01",
  "description": "Buy math books"
}
```
---
- Endpoint: `[DELETE]` `purchase/{code}/` >>>> `purchase/p-003`
- Payload: -
- Response: -

---
- Endpoint: `[GET]` `purchase/{code}/details` >>>> `purchase/p-001/details`
- Payload: -
- Response:
```json
[
  {
    "item_code": "I-001",
    "quantity": 10,
    "unit_price": 60000,
    "header_code": "P-001"
  },
  {
    "item_code": "I-002",
    "quantity": 4,
    "unit_price": 50000,
    "header_code": "P-001"
  }
]
```
---
- Endpoint: `[POST]` `purchase/{code}/details` >>>> `purchase/p-004/details`
- Payload:
```json
{
  "item_code": "I-005",
  "quantity": 4,
  "unit_price": 50000
}
```
- Response:
```json
{
  "item_code": "I-005",
  "quantity": 4,
  "unit_price": 50000,
  "header_code": "P-004"
}
```
---
---
---
### ## Sells
- Endpoint: `[GET]` `sell/`
- Payload: -
- Response:
```json
[
  {
    "code": "S-001",
    "date": "2025-03-01",
    "description": "Sell history books to library",
    "details": [
      {
        "item_code": "I-001",
        "quantity": 4,
        "header_code": "S-001"
      },
      {
        "item_code": "I-001",
        "quantity": 4,
        "header_code": "S-001"
      }
    ]
  },
  ...
]
```
---
- Endpoint: `[POST]` `sell/`
- Payload:
```json
{
  "code": "S-004",
  "date": "2025-03-01",
  "description": "Sell cookbooks to a restaurant owner"
}
```
- Response:
```json
{
  "code": "S-004",
  "date": "2025-03-01",
  "description": "Sell cookbooks to a restaurant owner"
}
```
---
- Endpoint: `[GET]` `sell/{code}` >>>> `sell/s-002`
- Payload: -
- Response:
```json
{
  "code": "S-002",
  "date": "2025-03-02",
  "description": "Sell math books to a customer",
  "details": [
    {
      "item_code": "I-002",
      "quantity": 1,
      "header_code": "S-002"
    }
  ]
}
```
---
- Endpoint: `[PUT]` `sell/{code}/` >>>> `sell/s-001/`
- Payload:
```json
{
  "code": "S-001",
  "date": "2025-03-01",
  "description": "Sell history books to restaurant owner's daughter"
}

```
- Response:
```json
{
  "code": "S-001",
  "date": "2025-03-01",
  "description": "Sell history books to restaurant owner's daughter"
}
```
---
- Endpoint: `[DELETE]` `sell/{code}/`
- Payload: -
- Response: -

---
- Endpoint: `[GET]` `sell/{code}/details` >>>> `sell/s-002/details`
- Payload: -
- Response:
```json
[
  {
    "item_code": "I-002",
    "quantity": 1,
    "header_code": "S-002"
  }
]
```
---
- Endpoint: `[POST]` `sell/{code}/details` >>>> `sell/s-002/details`
- Payload:
```json
{
  "item_code": "I-005",
  "quantity": 5
}
```
- Response:
```json
{
  "item_code": "I-005",
  "quantity": 5,
  "header_code": "S-002"
}
```
---
### ## Report
- Endpoint: `[GET]` `report/`
- Query: *'start_date=2025-01-01&end_date=2025-03-31'*
- Response:
```json
{
  "result": {
    "items": [
      {
        "date": "01-01-2025",
        "description": "Buy history books",
        "code": "P-001",
        "in_qty": 4,
        "in_price": 50000,
        "in_total": 200000,
        "out_qty": 0,
        "out_price": 0,
        "out_total": 0,
        "stock_qty": [],
        "stock_price": [],
        "stock_total": [],
        "balance_qty": 4,
        "balance": 200000
      },
      {
        "date": "01-01-2025",
        "description": "Buy math books",
        "code": "P-002",
        "in_qty": 12,
        "in_price": 45000,
        "in_total": 540000,
        "out_qty": 0,
        "out_price": 0,
        "out_total": 0,
        "stock_qty": [
          4
        ],
        "stock_price": [
          50000
        ],
        "stock_total": [
          200000
        ],
        "balance_qty": 16,
        "balance": 740000
      },
      {
        "date": "02-03-2025",
        "description": "Sell math books to a customer",
        "code": "S-002",
        "in_qty": 0,
        "in_price": 0,
        "in_total": 0,
        "out_qty": 1,
        "out_price": 50000,
        "out_total": 50000,
        "stock_qty": [
          4,
          12
        ],
        "stock_price": [
          50000,
          45000
        ],
        "stock_total": [
          200000,
          540000
        ],
        "balance_qty": 15,
        "balance": 690000
      },
      {
        "date": "03-03-2025",
        "description": "Sell cookbooks to a chef",
        "code": "S-003",
        "in_qty": 0,
        "in_price": 0,
        "in_total": 0,
        "out_qty": 2,
        "out_price": 50000,
        "out_total": 100000,
        "stock_qty": [
          3,
          12
        ],
        "stock_price": [
          50000,
          45000
        ],
        "stock_total": [
          150000,
          540000
        ],
        "balance_qty": 13,
        "balance": 590000
      },
      {
        "date": "03-03-2025",
        "description": "Sell cookbooks to a chef",
        "code": "S-003",
        "in_qty": 0,
        "in_price": 0,
        "in_total": 0,
        "out_qty": 2,
        "out_price": 47500,
        "out_total": 95000,
        "stock_qty": [
          1,
          12
        ],
        "stock_price": [
          50000,
          45000
        ],
        "stock_total": [
          50000,
          540000
        ],
        "balance_qty": 11,
        "balance": 495000
      },
      {
        "date": "03-03-2025",
        "description": "Sell cookbooks to a chef",
        "code": "S-003",
        "in_qty": 0,
        "in_price": 0,
        "in_total": 0,
        "out_qty": 3,
        "out_price": 45000,
        "out_total": 135000,
        "stock_qty": [
          0,
          11
        ],
        "stock_price": [
          50000,
          45000
        ],
        "stock_total": [
          0,
          495000
        ],
        "balance_qty": 8,
        "balance": 360000
      }
    ],
    "item_code": "I-002",
    "name": "Math Book",
    "unit": "Pcs",
    "summary": {
      "in_qty": 16,
      "out_qty": 8,
      "balance_qty": 8,
      "balance": 360000
    }
  }
}
```

---
---

> <br/>
> * NOTE: endpoint harus sesuai dan lengkap beserta trailing slash-nya, atau garis miring di akhir URL.
>
> <br/>