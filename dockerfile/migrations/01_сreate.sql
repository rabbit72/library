CREATE TABLE "author" (
	"id" serial NOT NULL,
	"name" varchar(128) NOT NULL UNIQUE,
	CONSTRAINT author_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "book" (
	"id" serial NOT NULL,
	"title" varchar(256) NOT NULL,
	"year" int,
	CONSTRAINT book_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "books_authors" (
	"book_id" int NOT NULL,
	"author_id" int
) WITH (
  OIDS=FALSE
);



CREATE UNIQUE INDEX books_authors_book_id_author_id_uindex
  ON public.books_authors (book_id, author_id);

ALTER TABLE "books_authors" ADD CONSTRAINT
  "books_authors_fk0" FOREIGN KEY ("book_id") REFERENCES "book"("id")
  ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "books_authors" ADD CONSTRAINT
  "books_authors_fk1" FOREIGN KEY ("author_id") REFERENCES "author"("id")
  ON DELETE CASCADE ON UPDATE CASCADE;


