/* 
    schema.sql
    ~~~~~~~~~~
    SQL script for initialize the structure of the database. This script is
    executed by `init_db.py`.
    We have two main entities: sellers and products.
    Sellers can have many products but one product can only have one owner.
*/
CREATE TABLE seller (
    seller_id INT AUTO_INCREMENT PRIMARY KEY,
    seller_name VARCHAR(150) NOT NULL UNIQUE,
    seller_pass VARCHAR(100) NOT NULL,
    start_hour INT DEFAULT 0,
    end_our INT DEFAULT 0
);

CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    product_owner INT,
    product_name VARCHAR(150) NOT NULL,
    product_price INT DEFAULT 0 NOT NULL,
    product_desc VARCHAR(255) NOT NULL,
    num_products INT DEFAULT 0 NOT NULL,

    FOREIGN KEY (product_owner) REFERENCES user(user_id) ON DELETE CASCADE
);