package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()

    r.POST("/v1/data_ingestion", func(c *gin.Context) {
        dataSource := "https://jsonplaceholder.typicode.com/posts/1"
        status, collected := collectData(dataSource)
        if status != http.StatusOK {
            c.JSON(http.StatusInternalServerError, gin.H{"message": "Unable to collect data"})
            return
        }
        status, transformed := transformData(collected, dataSource)
        if status != http.StatusOK {
            c.JSON(http.StatusInternalServerError, gin.H{"message": "Error transforming data"})
            return
        }
        status = storeData(transformed)
        if status != http.StatusOK {
            c.JSON(http.StatusInternalServerError, gin.H{"message": "Error storing data"})
            return
        }
        c.JSON(http.StatusOK, gin.H{"message": "Data Ingestion Successful"})
    })

    r.GET("/v1/retrieve_data", func(c *gin.Context) {
        status, data := fetchInsertedData()
        if status != http.StatusOK {
            c.JSON(http.StatusInternalServerError, gin.H{"message": "Error fetching data"})
            return
        }
        c.JSON(http.StatusOK, gin.H{"message": "Data Retrieved successfully", "data": data})
    })

    r.Run(":8080")
}
