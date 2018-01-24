package main

import (
	"flag"
	"log"
	"os"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"

	raven "github.com/getsentry/raven-go"
)

const (
	createUsersQueue = "CREATE_USER"
	updateUsersQueue = "UPDATE_USER"
	deleteUsersQueue = "DELETE_USER"
	portAddr         = ":50051"
)

func init() {
	raven.SetDSN("change by keep")
}

func main() {
	var numWorkers int
	cache := Cache{Enable: true}
	flag.StringVar(&cache.Address, "redis_address", os.Getenv("APP_RD_ADDRESS"), "Redis Address")
	flag.StringVar(&cache.Auth, "redis_auth", os.Getenv("APP_RD_AUTH"), "Redis Auth")
	flag.StringVar(&cache.DB, "redis_db_name", os.Getenv("APP_RD_DBNAME"), "Redis DB name")
	flag.IntVar(&cache.MaxIdle, "redis_max_idle", 100, "Redis Max Idle")
	flag.IntVar(&cache.MaxActive, "redis_max_active", 100, "Redis Max Active")
	flag.IntVar(&cache.IdleTimeoutSecs, "redis_timeout", 60, "Redis timeout in seconds")
	flag.IntVar(&numWorkers, "num_workers", 10, "Number of workers to consume queue")
	flag.Parse()
	cache.Pool = cache.NewCachePool()

	connectionString := os.Getenv("DATABASE_URL")

	db, err := sqlx.Open("postgres", connectionString)
	if err != nil {
		log.Fatal(err)
	}

	go UsersToDB(numWorkers, db, cache, createUsersQueue)
	go UsersToDB(numWorkers, db, cache, updateUsersQueue)
	go UsersToDB(numWorkers, db, cache, deleteUsersQueue)

	a := App{}
	a.Initialize(cache, db)
	go a.runGRPCServer(portAddr)
	a.initializeRoutes()
	a.Run(":3000")
}
