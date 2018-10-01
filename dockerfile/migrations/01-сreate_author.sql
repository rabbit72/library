CREATE TABLE author (
	id serial NOT NULL,
	name zdb.fulltext NOT NULL UNIQUE,
  last_update timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT author_pk PRIMARY KEY (id)
) WITH (
  OIDS=FALSE
);

CREATE INDEX idx_author
          ON author
       USING zombodb ((author.*))
        WITH (url='elasticsearch:9200/');

CREATE TRIGGER last_update_modification_author
    BEFORE UPDATE ON author
    FOR EACH ROW
    EXECUTE PROCEDURE update_last_update(last_update);






