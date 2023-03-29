CREATE TABLE movies
(
    id bigint NOT NULL,
    name text COLLATE pg_catalog."default",
    CONSTRAINT movies_pkey PRIMARY KEY (id)
);