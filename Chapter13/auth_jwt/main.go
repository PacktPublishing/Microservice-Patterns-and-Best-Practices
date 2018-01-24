package main

import (
	"fmt"
	"log"
	"time"

	jwt "github.com/dgrijalva/jwt-go"
)

type MyCustomClaims struct {
	UserID int    `json:"ID"`
	Name   string `json:"name"`
	Rule   string `json:"rule"`
	jwt.StandardClaims
}

func createToken() string {
	mySigningKey := []byte("AllYourBase")

	// Create the Claims
	claims := MyCustomClaims{
		1,
		"Vinicius Pacheco",
		"Admin",
		jwt.StandardClaims{
			ExpiresAt: time.Now().Add(time.Hour * 72).Unix(),
			Issuer:    "Localhost",
			IssuedAt:  time.Now().Unix(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	ss, err := token.SignedString(mySigningKey)
	if err != nil {
		log.Fatal(err.Error())
	}
	return ss
}

func readToken(tokenString string) {

	token, err := jwt.ParseWithClaims(
		tokenString,
		&MyCustomClaims{},
		func(token *jwt.Token) (interface{}, error) {
			return []byte("AllYourBase"), nil
		},
	)

	if claims, ok := token.Claims.(*MyCustomClaims); ok && token.Valid {
		fmt.Printf(
			"%v %v %v %v\n",
			claims.UserID,
			claims.Name,
			claims.Rule,
			claims.StandardClaims.ExpiresAt,
		)
	} else {
		fmt.Println(err)
	}
}

func main() {
	token := createToken()
	fmt.Println(token)
	readToken(token)
}
