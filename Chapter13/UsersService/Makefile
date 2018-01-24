.PHONY: install
install:
	@go get

.PHONY: test
test: 
	@go test -v

.PHONY: vendor
test: 
	@go get github.com/kardianos/govendor
	@govendor init
	@govendor add +external
	@govendor add github.com/viniciusfeitosa/BookProject/UsersService/user_data

.PHONY: run
run:
	@go run main.go app.go cache.go models.go workers.go