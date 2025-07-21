package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

func collectData() {

	resp, err := http.Get("https://jsonplaceholder.typicode.com/posts")
	if err != nil {
		log.Fatalln(err)
	}

	return resp, err
}

func tranformData() {

	var posts []Post
	err = json.NewDecoder(resp.Body).Decode(&posts)
	if err != nil {
		return http.StatusInternalServerError, posts
	}

	for i := range posts {
		posts[i].IngestedAt = time.Now().UTC().Format(time.RFC3339)
		posts[i].Source = "https://jsonplaceholder.typicode.com/posts"
	}

	return http.StatusOK, posts

}

func storeData() {

	// implement mongodb integration

}

func main() {

	// Initialize the router
	r := mux.NewRouter()

	// Define the endpoints
	r.HandleFunc("/v1/data_ingestion/", getBooks).Methods("GET")

	// Start the server
	fmt.Println("Start server at 8080 port")
	log.Fatal(http.ListenAndServe(":8080", r))
}
