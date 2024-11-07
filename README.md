 curl http://127.0.0.1:8000/items/1


curl -X 'POST' \
  'http://127.0.0.1:8000/items/123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
        "name": "Sample Item",
        "description": "A sample item description",
        "price": 12.99,
        "quantity": 5
      }'


curl -X 'POST' \
  'http://127.0.0.1:8000/items/123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'api_key: your-expected-api-key' \
  -d '{
        "name": "Sample Item",
        "description": "A sample item description",
        "price": 12.99,
        "quantity": 5
      }'
