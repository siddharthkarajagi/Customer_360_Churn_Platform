# Data Requirements

## 1. Purpose

The purpose of this document is to identify the datasets required
to build the Customer 360° Intelligence & Churn Prevention Platform
for NovaMart.

Each dataset is required for a specific business purpose and will
contribute to customer behaviour analysis, churn analysis, customer
segmentation, revenue analysis, and retention decision-making.

---

## 2. Customer Master Data

### Dataset
Customers

### Purpose
Stores the basic profile and demographic information of customers.

### Key Information
- Customer ID
- Customer Name
- Gender
- Date of Birth
- City
- State
- Customer Registration Date
- Customer Status

### Business Questions
- Who are our customers?
- When did they join NovaMart?
- Where are customers located?
- What is the overall customer base?

---

## 3. Orders Data

### Dataset
Orders

### Purpose
Stores customer purchase transactions.

### Key Information
- Order ID
- Customer ID
- Order Date
- Order Channel
- Store ID
- Order Status
- Total Order Amount

### Business Questions
- How frequently does a customer purchase?
- When was the customer's last purchase?
- Which sales channel does the customer use?
- How much revenue is generated?

---

## 4. Order Items Data

### Dataset
Order Items

### Purpose
Stores product-level details for every order.

### Key Information
- Order Item ID
- Order ID
- Product ID
- Quantity
- Unit Price
- Discount
- Final Amount

### Business Questions
- Which products do customers purchase?
- How many products are purchased?
- What is the customer's average order value?
- Which products are associated with valuable customers?

---

## 5. Product Data

### Dataset
Products

### Purpose
Stores information about products sold by NovaMart.

### Key Information
- Product ID
- Product Name
- Category
- Subcategory
- Brand
- Cost Price
- Selling Price

### Business Questions
- Which product categories are popular?
- Which products generate higher revenue?
- Which products are commonly purchased by valuable customers?

---

## 6. Payment Data

### Dataset
Payments

### Purpose
Stores payment transaction information.

### Key Information
- Payment ID
- Order ID
- Customer ID
- Payment Date
- Payment Method
- Payment Amount
- Payment Status

### Business Questions
- Which payment methods are preferred?
- Are payment failures affecting customers?
- What is the successful payment value?

---

## 7. Returns Data

### Dataset
Returns

### Purpose
Stores information about returned products and orders.

### Key Information
- Return ID
- Order ID
- Customer ID
- Product ID
- Return Date
- Return Reason
- Return Amount
- Return Status

### Business Questions
- Which customers return products frequently?
- Which products have higher return rates?
- Is return behaviour associated with customer churn?

---

## 8. Customer Support Data

### Dataset
Support Tickets

### Purpose
Stores customer service interactions and complaints.

### Key Information
- Ticket ID
- Customer ID
- Ticket Date
- Issue Type
- Priority
- Resolution Status
- Resolution Time
- Customer Satisfaction Score

### Business Questions
- Which customers contact support frequently?
- What are the most common issues?
- Does poor support experience relate to churn?

---

## 9. Marketing Campaign Data

### Dataset
Marketing Campaigns

### Purpose
Stores information about marketing campaigns conducted by NovaMart.

### Key Information
- Campaign ID
- Campaign Name
- Campaign Type
- Start Date
- End Date
- Marketing Channel
- Campaign Budget

### Business Questions
- Which campaigns are being conducted?
- Which marketing channels are used?
- What type of campaigns are targeting customers?

---

## 10. Customer Campaign Data

### Dataset
Customer Campaigns

### Purpose
Stores customer-level marketing interactions.

### Key Information
- Customer Campaign ID
- Customer ID
- Campaign ID
- Sent Date
- Opened
- Clicked
- Converted
- Conversion Amount

### Business Questions
- Which customers engage with campaigns?
- Which customers ignore marketing communication?
- Does marketing engagement relate to retention?

---

## 11. Store Data

### Dataset
Stores

### Purpose
Stores information about NovaMart physical stores.

### Key Information
- Store ID
- Store Name
- City
- State
- Store Type
- Opening Date

### Business Questions
- Which stores generate customer activity?
- Which customers purchase through physical stores?
- How does store behaviour compare with online behaviour?

---

# 12. MongoDB Data

## Website Events

Stores semi-structured customer website activity.

Examples:
- Page View
- Product View
- Search
- Add to Cart
- Remove from Cart
- Checkout
- Login
- Logout

### Business Questions
- How active are customers on the website?
- Which customers are browsing but not purchasing?
- What behaviours occur before purchase or churn?

---

## Mobile App Events

Stores semi-structured customer mobile application activity.

Examples:
- App Open
- Product View
- Search
- Add to Cart
- Checkout
- Push Notification Interaction

### Business Questions
- How frequently do customers use the mobile application?
- Does app engagement indicate customer loyalty?
- Are inactive customers showing early churn signals?

---

## Customer Interactions

Stores additional customer interaction events.

Examples:
- Chat Interaction
- Email Interaction
- Notification Interaction
- Contact Centre Interaction

### Business Questions
- How do customers interact with NovaMart?
- Which customers have declining engagement?
- Does interaction behaviour indicate churn risk?

---

# 13. Core Customer 360° Objective

The datasets above will be connected using common business identifiers,
primarily Customer ID and relevant transaction identifiers.

The final Customer 360° view should combine:

Customer Profile
+
Purchase Behaviour
+
Payment Behaviour
+
Return Behaviour
+
Support Experience
+
Marketing Engagement
+
Website Behaviour
+
Mobile App Behaviour

This unified view will be used for:

- Customer segmentation
- Customer value analysis
- Churn analysis
- Churn-risk identification
- Revenue-at-risk analysis
- Retention strategy development