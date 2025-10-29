Drop table if exists order_details;
Drop table if exists Orders;
Drop table if exists Products;
Drop table if exists Suppliers;
Drop table if exists Shippers;
Drop table if exists Customers; 
Drop table if exists Categories;
Drop table if exists Employees;

-- Create table `categories`
CREATE TABLE
  Categories (
    categoryID int PRIMARY KEY,
    categoryName TEXT,
    description TEXT,
    picture TEXT,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

-- Create table `customers`
CREATE TABLE
  Customers (
    customerID int PRIMARY KEY,
    customerName TEXT,
    contactName TEXT,
    address TEXT,
    city TEXT,
    postalCode TEXT,
    country TEXT,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

-- Create table `employees`
CREATE TABLE
  Employees (
    employeeID int PRIMARY KEY,
    lastName TEXT,
    firstName TEXT,
    birthDate DATE,
    photo TEXT,
    notes TEXT,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

-- Create table `shippers`
CREATE TABLE
  Shippers (
    shipperID int PRIMARY KEY,
    shipperName TEXT,
    phone TEXT,
    picture TEXT,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

-- Create table `suppliers`
CREATE TABLE
  Suppliers (
    supplierID int PRIMARY KEY,
    supplierName TEXT,
    contactName TEXT,
    address TEXT,
    city TEXT,
    postalCode TEXT,
    country TEXT,
    phone TEXT,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

-- Create table `products`
CREATE TABLE
  Products (
    productID int PRIMARY KEY,
    productName TEXT,
    supplierID int REFERENCES suppliers (supplierID),
    categoryID int REFERENCES categories (categoryID),
    unit TEXT,
    price NUMERIC,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

-- Create table `orders`
CREATE TABLE
  Orders (
    orderID int PRIMARY KEY,
    customerID int REFERENCES customers (customerID),
    employeeID int REFERENCES employees (employeeID),
    orderDate DATE DEFAULT CURRENT_DATE,
    shipperID int REFERENCES shippers (shipperID),
    delivered BOOLEAN DEFAULT false,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

-- Create table `order_details`
CREATE TABLE
  Order_details (
    orderDetailID int PRIMARY KEY,
    orderID int REFERENCES orders (orderID),
    productID int REFERENCES products (productID),
    quantity INTEGER,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

