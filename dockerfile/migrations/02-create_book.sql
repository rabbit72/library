CREATE TABLE "book" (
	"id" serial NOT NULL,
	"title" varchar(256) NOT NULL,
	"year" int,
  "last_update" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT book_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TRIGGER last_update_modification_book
    BEFORE UPDATE ON book
    FOR EACH ROW
    EXECUTE PROCEDURE update_last_update(last_update);