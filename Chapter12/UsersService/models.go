package main

import (
	"github.com/jmoiron/sqlx"
	"golang.org/x/crypto/bcrypt"
)

// User is the struct resposible to represent the database entity
type User struct {
	ID       int    `json:"id" db:"id"`
	Name     string `json:"name" db:"name"`
	Email    string `json:"email" db:"email"`
	Password string `json:"password" db:"password"`
}

// Get return just update the User instance with the data from db
func (u *User) get(db *sqlx.DB) error {
	return db.Get(u, "SELECT name, email, password FROM users WHERE id=$1", u.ID)
}

// Update the data in the db using the instance values
func (u *User) update(db *sqlx.DB) error {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(u.Password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	_, err = db.Exec("UPDATE users SET name=$1, email=$2, password=$3 WHERE id=$4",
		u.Name, u.Email, string(hashedPassword), u.ID)
	return err
}

// Delete the date from the db using the instance values
func (u *User) delete(db *sqlx.DB) error {
	_, err := db.Exec("DELETE FROM users WHERE id=$1", u.ID)
	return err
}

// Create a new user in the db using the instance values
func (u *User) create(db *sqlx.DB) error {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(u.Password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	return db.QueryRow(
		"INSERT INTO users(id, name, email, password) VALUES($1, $2, $3, $4) RETURNING id",
		u.ID, u.Name, u.Email, string(hashedPassword)).Scan(&u.ID)
}

// List return a list of users. Could be applied pagination
func list(db *sqlx.DB, start, count int) ([]User, error) {
	users := []User{}
	err := db.Select(&users, "SELECT id, name, email, password FROM users LIMIT $1 OFFSET $2", count, start)
	if err != nil {
		return nil, err
	}
	return users, nil
}
