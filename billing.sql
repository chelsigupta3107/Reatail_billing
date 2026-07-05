-- Database for ShopBill Pro - JOY GURU BHANDAR

CREATE DATABASE IF NOT EXISTS joy_guru_bhandar;
USE joy_guru_bhandar;

-- 1. Products Table
CREATE TABLE products (
    pid INT AUTO_INCREMENT PRIMARY KEY,
    pname VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    category VARCHAR(50)
);

-- 2. Bills Table
CREATE TABLE bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_name VARCHAR(100),
    total_amount DECIMAL(10,2),
    gst_amount DECIMAL(10,2)
);

-- 3. Bill Items Table
CREATE TABLE bill_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT,
    pid INT,
    quantity INT,
    rate DECIMAL(10,2),
    amount DECIMAL(10,2),
    gst_amt DECIMAL(10,2),
    cgst DECIMAL(10,2),
    sgst DECIMAL(10,2),
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
    FOREIGN KEY (pid) REFERENCES products(pid)
);
