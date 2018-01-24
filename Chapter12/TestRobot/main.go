package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"
)

const (
	baseURL           string = "http://localhost/"
	newsURL           string = baseURL + "v1/news/"
	usersURL          string = baseURL + "v1/users/"
	recommendationURL string = baseURL + "v1/recommendation/"
)

// News - it's the struct of the news response
type News struct {
	ID       int      `json:"id"`
	Author   string   `json:"author"`
	Content  string   `json:"content"`
	NewsType string   `json:"news_type"`
	Tags     []string `json:"tags"`
	Title    string   `json:"title"`
	Version  int      `json:"version"`
}

// RespNewsBody - It's the struct of the response from the orchestrator
type RespNewsBody struct {
	News   News   `json:"news"`
	Status string `json:"status"`
}

// Users - it's the struct of the response from UsersService
type Users struct {
	ID       int    `json:"id"`
	Name     string `json:"name"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

// RecommendationByUser - it's the struct of the response from RecommendatioService by user ID
type RecommendationByUser struct {
	ID string `json:"id"`
}

// StartToEndTestMininalFlow - simulate a minimal business application
func StartToEndTestMininalFlow() {
	log.Println("### Starting minimal validation flow ###")
	log.Println("Validating user creation")
	reqBody := []byte(`{
		"name": "end-to-end User",
		"email": "end-to-end@test.com",
		"password": "123456"
	}`)
	resp, err := http.Post(usersURL, "Application/json", bytes.NewBuffer(reqBody))
	if err != nil {
		os.Exit(1)
	}
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	var respUser Users
	if err := json.Unmarshal(body, &respUser); err != nil {
		log.Fatalln(err)
	}
	if respUser.Email != "end-to-end@test.com" {
		log.Fatalln("Inconsistent value checking the user email: ", respUser.Email)
	}
	log.Println("User creation validadted with success")

	mapNews := map[string][]byte{
		"famous": []byte(`{
			"author": "Famous end-to-end Test",
			"content": "This content is just a test using the famous end-to-end test robot",
			"tags": ["Famous test"],
			"title": "FamousNews test end-to-end"
		}`),
		"politics": []byte(`{
			"author": "Politics end-to-end Test",
			"content": "This content is just a test using the politics end-to-end test robot",
			"tags": ["Politics test"],
			"title": "PoliticsNews test end-to-end"
		}`),
		"sports": []byte(`{
			"author": "Sports end-to-end Test",
			"content": "This content is just a test using the sports end-to-end test robot",
			"tags": ["Sports test"],
			"title": "SportsNews test end-to-end"
		}`),
	}
	newsTypeID := make(map[string]int)
	for newsType, reqBody := range mapNews {
		log.Println("Validating news creation:", newsType)
		resp, err := http.Post(newsURL+newsType, "Application/json", bytes.NewBuffer(reqBody))
		if err != nil {
			os.Exit(1)
		}

		respBody, err := newsUnmarshaler(resp)
		if err != nil {
			log.Fatalln(err)
		}

		if err := newsIntegrityValidator(respBody, newsType); err != nil {
			log.Fatalln(err)
		}
		log.Println("News creation validated with success:", newsType)

		log.Println("Validating news get:", newsType)
		client := &http.Client{}
		req, err := http.NewRequest("GET", fmt.Sprintf("%s%s/%d", newsURL, newsType, respBody.News.ID), nil)
		if err != nil {
			log.Fatalln(err)
		}
		req.Header.Set("Cookie", fmt.Sprintf("user_id=%d", respUser.ID))
		resp, err = client.Do(req)
		if err != nil {
			log.Fatalln(err)
		}
		respBody, err = newsUnmarshaler(resp)
		if err != nil {
			log.Fatalln(err)
		}

		if err := newsIntegrityValidator(respBody, newsType); err != nil {
			log.Fatalln(err)
		}
		log.Println("Got news with success:", newsType)

		newsTypeID[newsType] = respBody.News.ID
	}

	log.Println("Validating recommendations")
	time.Sleep(1 * time.Second)
	resp, err = http.Get(fmt.Sprintf("%s%s/%d", recommendationURL, "user", respUser.ID))
	if err != nil {
		log.Fatalln(err)
	}
	recommendationByUser, err := recommendationUnmarshaler(resp)
	if err != nil {
		log.Fatalln(err)
	}
	if err := recommendationIntegrityValidator(recommendationByUser); err != nil {
		log.Fatalln(err)
	}
	log.Println("Recommendations validated with success")
	log.Println("### Finished minimal validation flow ###")
}

func newsUnmarshaler(resp *http.Response) (RespNewsBody, error) {
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	var respBody RespNewsBody
	if err := json.Unmarshal(body, &respBody); err != nil {
		return respBody, err
	}
	return respBody, nil
}

func newsIntegrityValidator(respBody RespNewsBody, newsType string) error {
	if respBody.News.Version < 1 {
		return errors.New("News wasn't created")
	}
	if strings.Title(newsType)+" end-to-end Test" != respBody.News.Author {
		return fmt.Errorf("Inconsistent value checking the author: %s", respBody.News.Author)
	}
	return nil
}

func recommendationUnmarshaler(resp *http.Response) ([]RecommendationByUser, error) {
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	var respBody []RecommendationByUser
	if err := json.Unmarshal(body, &respBody); err != nil {
		return respBody, err
	}
	return respBody, nil
}

func recommendationIntegrityValidator(recommendations []RecommendationByUser) error {
	if len(recommendations) < 3 {
		return fmt.Errorf("Fail. The quantity of recommendations was less then spected. expected: 3 received: %d", len(recommendations))
	}
	return nil
}

func main() {
	StartToEndTestMininalFlow()
}
