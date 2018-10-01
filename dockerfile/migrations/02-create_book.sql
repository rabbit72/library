CREATE TABLE book (
	id serial NOT NULL,
	title zdb.fulltext NOT NULL,
	year int,
  last_update timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT book_pk PRIMARY KEY (id)
) WITH (
  OIDS=FALSE
);

CREATE INDEX idx_book
          ON book
       USING zombodb ((book.*))
        WITH (url='elasticsearch:9200/');

CREATE TRIGGER last_update_modification_book
    BEFORE UPDATE ON book
    FOR EACH ROW
    EXECUTE PROCEDURE update_last_update(last_update);
