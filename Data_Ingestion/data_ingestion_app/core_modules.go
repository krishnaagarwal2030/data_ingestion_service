package main

import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "time"
    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
)

var (
    mongoUser     = os.Getenv("MONGODB_USERNAME")
    mongoPassword = os.Getenv("MONGODB_PASSWORD")
    mongoPort     = os.Getenv("MONGODB_PORT")
    mongoDB       = os.Getenv("MONGODB_DATABASE")
    mongoColl     = os.Getenv("MONGODB_COLLECTION")
    mongoServer   = os.Getenv("MONGODB_SERVER")
    timeout       = 1 * time.Second
)

func getMongoCollection() (*mongo.Client, *mongo.Collection, error) {
    uri := fmt.Sprintf("mongodb://%s:%s", mongoServer, mongoPort)
    clientOpts := options.Client().ApplyURI(uri).SetAuth(options.Credential{
        Username: mongoUser,
        Password: mongoPassword,
    })
    client, err := mongo.Connect(context.TODO(), clientOpts)
    if err != nil {
        return nil, nil, err
    }
    collection := client.Database("DataIngestionDb").Collection("Data_Collection")
    return client, collection, nil
}

func collectData(dataSource string) (int, map[string]interface{}) {
    client := http.Client{Timeout: timeout}
    resp, err := client.Get(dataSource)
    if err != nil {
        fmt.Println("Request error:", err)
        return http.StatusRequestTimeout, nil
    }
    defer resp.Body.Close()

    var data map[string]interface{}
    json.NewDecoder(resp.Body).Decode(data)
    fmt.Println(data)

    return http.StatusOK, data
}

func transformData(input map[string]interface{}, source string) (int, map[string]interface{}) {
    output := map[string]interface{}{
        "data":       input,
        "ingested_at": time.Now().UTC(),
        "source":     source,
    }
    return http.StatusOK, output
}

func storeData(data map[string]interface{}) int {
    client, collection, err := getMongoCollection()
    if err != nil {
        fmt.Println("Mongo connection error:", err)
        return http.StatusInternalServerError
    }
    defer client.Disconnect(context.TODO())
    res, err := collection.InsertOne(context.TODO(), data)
    if err != nil {
        fmt.Println("Insert error:", err)
        return http.StatusInternalServerError
    }
    fmt.Println("Inserted ID:", res.InsertedID)
    return http.StatusOK
}

func fetchInsertedData() (int, map[string]interface{}) {
    client, collection, err := getMongoCollection()
    if err != nil {
        fmt.Println("Mongo connection error:", err)
        return http.StatusInternalServerError, nil
    }
    defer client.Disconnect(context.TODO())
    var result map[string]interface{}
    err = collection.FindOne(context.TODO(), bson.M{}, options.FindOne().SetSort(bson.D{{"ingested_at", -1}})).Decode(&result)
    if err != nil {
        fmt.Println("Fetch error:", err)
        return http.StatusInternalServerError, nil
    }
    return http.StatusOK, result
}



