-- create search table 
CREATE VIRTUAL TABLE 
product_search USING  fts5(
	name, category, content = product, content_rowid = product_id, 
	tokenize = "porter unicode61"
);

-- create triggers to add product 
CREATE TRIGGER product_ai AFTER INSERT ON product BEGIN	
INSERT INTO product_search(row_id, name, category) VALUES (
	new.product_id, new.name, new.category);
END;

-- create trigger to delete product 
CREATE TRIGGER product_ad AFTER DELETE ON product BEGIN	
INSERT INTO product_search(product_search, row_id, name, category) 
VALUES ('delete', old.product_id, old.name, old.category);
END;

-- create trigger to update product
CREATE TRIGGER product_au AFTER UPDATE ON product BEGIN	
INSERT INTO product_search(product_search, row_id, name, category) 
	VALUES ('delete', old.product_id, old.name, old.category);
INSERT INTO product_search(row_id, name, category) 
	VALUES (new.product_id, new.name, new.category);
END;

-- rebuild article search 
INSERT INTO product_search(product_search) VALUES('rebuild');

-- search for query in category
SELECT rowid, * from product_search where category MATCH "c*";

-- search for query in product name 
SELECT rowid, * from product_search where name MATCH "c*";