USE dbproject;

CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL
);

ALTER TABLE items 
ADD COLUMN expiration_date DATE DEFAULT NULL;

SELECT * FROM items;
SELECT * FROM items_nutrition;
SELECT * FROM recipes;

CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS items_nutrition (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    calories DECIMAL(10, 2),
    protein DECIMAL(10, 2),
    carbs DECIMAL(10, 2),
    fat DECIMAL(10, 2),
    sugars DECIMAL(10, 2),
    fiber DECIMAL(10, 2),
    FOREIGN KEY (item_id) REFERENCES items(id)
);