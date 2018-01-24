.PHONY: help

status:
		docker-compose ps

stop:
		docker stop $(shell docker ps -aq)

clean:
		docker stop $(shell docker ps -aq)
		docker rm $(shell docker ps -aq)

destroy:
		docker stop $(shell docker ps -aq)
		docker rm $(shell docker ps -aq)
		docker rmi -f $(shell docker images -q)

up:
		docker stop $(shell docker ps -aq)
		docker-compose -f docker-compose.yml up --build -d
		sleep 5
		docker-compose ps
		docker-compose exec users_service go run db/dbmigrate.go
		docker-compose exec famous_news_service python dbmigrate.py
		docker-compose exec politics_news_service python dbmigrate.py
		docker-compose exec sports_news_service python dbmigrate.py

up-tests:
		docker stop $(shell docker ps -aq)
		docker rm $(shell docker ps -aq)
		docker-compose -f docker-compose.yml -f docker-compose.test.yml up --build -d
		sleep 5
		docker-compose ps
		docker-compose exec users_service go run db/dbmigrate.go
		docker-compose exec famous_news_service python dbmigrate.py
		docker-compose exec politics_news_service python dbmigrate.py
		docker-compose exec sports_news_service python dbmigrate.py

run-tests:
		go run ${PWD}/TestRobot/main.go
		docker exec -it $(shell docker ps -q --filter "name=orcherstrator_news_service_1") python tests.py
		docker exec -it $(shell docker ps -q --filter "name=orcherstrator_news_service_1") python tests_integration.py

migrate:
		docker-compose exec users_service go run db/dbmigrate.go
		docker-compose exec famous_news_service python dbmigrate.py
		docker-compose exec politics_news_service python dbmigrate.py
		docker-compose exec sports_news_service python dbmigrate.py
