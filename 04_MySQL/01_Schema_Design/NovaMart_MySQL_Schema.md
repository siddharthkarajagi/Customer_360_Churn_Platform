# NovaMart MySQL Database Schema

## 1. Database Purpose

The MySQL database will store structured transactional and business
data required for Customer 360° analysis.

The database will contain customer, order, product, payment, return,
support, marketing, and store-related information.

---

# 2. Customers Table

Table Name: customers

Purpose:
Stores the master information of NovaMart customers.

Columns:

| Column | Data Type | Key | Description |
|---|---|---|---|
| customer_id | INT | PRIMARY KEY | Unique customer identifier |
| customer_name | VARCHAR(100) | | Customer name |
| gender | VARCHAR(20) | | Customer gender |
| date_of_birth | DATE | | Customer date of birth |
| city | VARCHAR(100) | | Customer city |
| state | VARCHAR(100) | | Customer state |
| registration_date | DATE | | Date customer joined NovaMart |
| customer_status | VARCHAR(30) | | Active or inactive status |

---

# 3. Orders Table

Table Name: orders

Purpose:
Stores customer purchase transactions.

Columns:

| Column | Data Type | Key | Description |
|---|---|---|---|
| order_id | INT | PRIMARY KEY | Unique order identifier |
| customer_id | INT | FOREIGN KEY | Customer who placed the order |
| order_date | DATETIME | | Date and time of order |
| order_channel | VARCHAR(30) | | Website, App, or Store |
| store_id | INT | FOREIGN KEY | Physical store identifier |
| order_status | VARCHAR(30) | | Completed, Cancelled, etc. |
| total_order_amount | DECIMAL(12,2) | | Total order value |

Relationship:

orders.customer_id → customers.customer_id

orders.store_id → stores.store_id

---

# 4. Order Items Table

Table Name: order_items

Purpose:
Stores individual products included in each order.

Columns:

| Column | Data Type | Key | Description |
|---|---|---|---|
| order_item_id | INT | PRIMARY KEY | Unique order item identifier |
| order_id | INT | FOREIGN KEY | Related order |
| product_id | INT | FOREIGN KEY | Purchased product |
| quantity | INT | | Quantity purchased |
| unit_price | DECIMAL(10,2) | | Price per unit |
| discount | DECIMAL(10,2) | | Discount amount |
| final_amount | DECIMAL(12,2) | | Final item amount |

Relationship:

order_items.order_id → orders.order_id

order_items.product_id → products.product_id

---

# 5. Products Table

Table Name: products

Purpose:
Stores product master information.

Columns:

| Column | Data Type | Key | Description |
|---|---|---|---|
| product_id | INT | PRIMARY KEY | Unique product identifier |
| product_name | VARCHAR(150) | | Product name |
| category | VARCHAR(100) | | Product category |
| subcategory | VARCHAR(100) | | Product subcategory |
| brand | VARCHAR(100) | | Product brand |
| cost_price | DECIMAL(10,2) | | Product cost |
| selling_price | DECIMAL(10,2) | | Standard selling price |

---

# 6. Payments Table

Table Name: payments

Purpose:
Stores payment transactions associated with customer orders.

Columns:

| Column | Data Type | Key | Description |
|---|---|---|---|
| payment_id | INT | PRIMARY KEY | Unique payment identifier |
| order_id | INT | FOREIGN KEY | Related order |
| customer_id | INT | FOREIGN KEY | Related customer |
| payment_date | DATETIME | | Payment date and time |
| payment_method | VARCHAR(50) | | UPI, Card, Cash, etc. |
| payment_amount | DECIMAL(12,2) | | Payment amount |
| payment_status | VARCHAR(30) | | Successful, Failed, Refunded |

Relationships:

payments.order_id → orders.order_id

payments.customer_id → customers.customer_id

---

# 7. Returns Table

Table Name: returns

Purpose:
Stores returned products and return-related information.

Columns:

| Column | Data Type | Key | Description |
|---|---|---|---|
| return_id | INT | PRIMARY KEY | Unique return identifier |
| order_id | INT | FOREIGN KEY | Related order |
| customer_id | INT | FOREIGN KEY | Related customer |
| product_id | INT | FOREIGN KEY | Returned product |
| return_date | DATETIME | | Return date |
| return_reason | VARCHAR(150) | | Reason for return |
| return_amount | DECIMAL(12,2) | | Returned amount |
| return_status | VARCHAR(30) | | Requested, Approved, Completed |

Relationships:

returns.order_id → orders.order_id

returns.customer_id → customers.customer_id

returns.product_id → products.product_id

---

# 8. Support Tickets Table

Table Name: support_tickets

Purpose:
Stores customer support cases.

Columns:

| Column | Data Type | Key | Description |
|---|---|---|---|
| ticket_id | INT | PRIMARY KEY | Unique support ticket |
| customer_id | INT | FOREIGN KEY | Customer raising ticket |
| ticket_date | DATETIME | | Ticket creation date |
| issue_type | VARCHAR(100) | | Type of customer issue |
| priority | VARCHAR(30) | | Low, Medium, High |
| resolution_status | VARCHAR(30) | | Open, Resolved, Escalated |
| resolution_time_hours | DECIMAL(8,2) | | Time taken to resolve |
| customer_satisfaction_score | DECIMAL(4,2) | | Customer satisfaction score |

Relationship:

support_tickets.customer_id → customers.customer_id

---

# 9. Marketing Campaigns Table

Table Name: marketing_campaigns

Purpose:
Stores campaign-level information.

Columns:

| Column | Data Type | Key | Description |
|---|---|---|---|
| campaign_id | INT | PRIMARY KEY | Unique campaign |
| campaign_name | VARCHAR(150) | | Campaign name |
| campaign_type | VARCHAR(50) | | Discount, Email, Festival, etc. |
| start_date | DATE | | Campaign start |
| end_date | DATE | | Campaign end |
| marketing_channel | VARCHAR(50) | | Email, SMS, Push, Social |
| campaign_budget | DECIMAL(14,2) | | Campaign budget |

---

# 10. Customer Campaigns Table

Table Name: customer_campaigns

Purpose:
Stores customer-level campaign engagement.

Columns:

| Column | Data Type | Key | Description |
|---|---|---|---|
| customer_campaign_id | INT | PRIMARY KEY | Unique customer campaign record |
| customer_id | INT | FOREIGN KEY | Customer identifier |
| campaign_id | INT | FOREIGN KEY | Campaign identifier |
| sent_date | DATETIME | | Date communication was sent |
| opened | BOOLEAN | | Whether customer opened communication |
| clicked | BOOLEAN | | Whether customer clicked |
| converted | BOOLEAN | | Whether customer converted |
| conversion_amount | DECIMAL(12,2) | | Revenue from conversion |

Relationships:

customer_campaigns.customer_id → customers.customer_id

customer_campaigns.campaign_id → marketing_campaigns.campaign_id

---

# 11. Stores Table

Table Name: stores

Purpose:
Stores information about NovaMart physical stores.

Columns:

| Column | Data Type | Key | Description |
|---|---|---|---|
| store_id | INT | PRIMARY KEY | Unique store identifier |
| store_name | VARCHAR(150) | | Store name |
| city | VARCHAR(100) | | Store city |
| state | VARCHAR(100) | | Store state |
| store_type | VARCHAR(50) | | Mall, High Street, etc. |
| opening_date | DATE | | Store opening date |

---

# 12. Main Relationships

customers
    |
    |--- orders
    |       |
    |       |--- order_items
    |       |       |
    |       |       |--- products
    |       |
    |       |--- payments
    |       |
    |       |--- returns
    |
    |--- support_tickets
    |
    |--- customer_campaigns
              |
              |--- marketing_campaigns

stores
    |
    |--- orders

---

# 13. Primary Business Key

The primary customer-level identifier across the Customer 360°
platform will be:

customer_id

This identifier will allow customer information from multiple
business systems to be connected for unified analysis.