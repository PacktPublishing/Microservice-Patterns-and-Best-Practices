package main

import (
	"encoding/json"
	redigo "github.com/garyburd/redigo/redis"
	"github.com/jmoiron/sqlx"
	"log"
	"sync"
)

// Worker is the struct with worker configuration values
type Worker struct {
	cache Cache
	db    *sqlx.DB
	id    int
	queue string
}

// UsersToDB create workers to consume de queues
func UsersToDB(numWorkers int, db *sqlx.DB, cache Cache, queue string) {
	var wg sync.WaitGroup
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func(id int, db *sqlx.DB, cache Cache, queue string) {
			worker := newWorker(i, db, cache, queue)
			worker.process(i)
			defer wg.Done()
		}(i, db, cache, queue)
	}
	wg.Wait()
}

func newWorker(id int, db *sqlx.DB, cache Cache, queue string) Worker {
	return Worker{cache: cache, db: db, id: id, queue: queue}
}

func (w Worker) process(id int) {
	for {
		conn := w.cache.Pool.Get()
		var channel string
		var uuid int
		if reply, err := redigo.Values(conn.Do("BLPOP", w.queue, 30+id)); err == nil {

			if _, err := redigo.Scan(reply, &channel, &uuid); err != nil {
				w.cache.enqueueValue(w.queue, uuid)
				continue
			}

			values, err := redigo.String(conn.Do("GET", uuid))
			if err != nil {
				w.cache.enqueueValue(w.queue, uuid)
				continue
			}

			user := User{}
			if err := json.Unmarshal([]byte(values), &user); err != nil {
				w.cache.enqueueValue(w.queue, uuid)
				continue
			}

			log.Println(user)
			if err := user.create(w.db); err != nil {
				w.cache.enqueueValue(w.queue, uuid)
				continue
			}

		} else if err != redigo.ErrNil {
			log.Fatal(err)
		}
		conn.Close()
	}
}
