conn = new Mongo();
db = conn.getDB("DataIngestionDb");
//use DataIngestionService
//db.createCollection("Data_Collection"); 
db.createUser({
    user: "admin",
    pwd: "admin",
    roles: [
      {
        role: "readWrite",
        db: "DataIngestionDb"
      }
    ]
  });
