package main

import (
	"fmt"
	"log"
	"os"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
)

const tableCreationQuery = `CREATE TABLE IF NOT EXISTS users
(
id SERIAL,
name TEXT NOT NULL,
email TEXT NOT NULL,
password TEXT NOT NULL,
CONSTRAINT users_pkey PRIMARY KEY (id)
)`

func main() {
	fmt.Println("Starting User migration")
	db, err := sqlx.Open("postgres", os.Getenv("DATABASE_URL"))
	if err != nil {
		log.Fatal(err)
	}
	if _, err = db.Exec(tableCreationQuery); err != nil {
		log.Fatal(err)
	}
	fmt.Println("Finished User migration")
}
