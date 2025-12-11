# Default target
.PHONY: run test

# Run the app in dev/prod mode
run:
	@echo "Starting app with dev/prod environment..."
	@export $$(cat .env | xargs) && uvicorn app.main:app --reload

# Run tests in test mode
test:
	@echo "Running tests with test environment..."
	@export $$(cat .env.test | xargs) && pytest -v --disable-warnings