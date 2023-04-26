# SMS Server
The SMS server is a simple Python and aiohttp application that sends SMS messages through the Twilio API. It also uses Redis to prevent multiple SMS messages from being sent to the same phone number within a specified period.


Requirements:

* Python 3.7 or higher
* Twilio account with API credentials and a phone number
* Redis server

## Dependencies
* aiohttp
* redis2
* python-dotenv
* twilio

## You can install the dependencies using pip:
```bash
pip install -r "/home/manish/Documents/SMS Server/requirement.txt"
```

## Configuration
Create a .env file in the root directory of the project.
Add the following environment variables to the .env file:

```bash
TWILIO_ACCOUNT_SID=<your_twilio_account_sid>
TWILIO_AUTH_TOKEN=<your_twilio_auth_token>
TWILIO_NUMBER=<your_twilio_phone_number>
REDIS_URL=<your_redis_url>
REDIS_PASSWORD=<your_redis_password>
```
Replace `<your_twilio_account_sid>`, `<your_twilio_auth_token>`, `<your_twilio_phone_number>`, `<your_redis_url>`, and `<your_redis_password>` with the appropriate values from your Twilio account and Redis server.

Running the Server
Run the server with the following command:
```bash
python app.py
```
By default, the server will listen on port 8081. You can change the port by setting the `PORT` environment variable in your `.env` file.

## API Endpoint
The server exposes one API endpoint:
* POST /sms

## Request
The request body should contain a JSON object with the following properties:

* `to`: The recipient's phone number in E.164 format (e.g., "+1234567890").
* `body`: The text of the SMS message.

## Response
On success, the server will return a JSON object containing the Twilio message SID:
```json
{
  "message_id": "<twilio_message_sid>"
}
````
If an SMS has already been sent to the specified phone number, the server will return a JSON object with an informative message:
```json
{
  "message": "SMS message has already been sent to this phone number."
}
```
In case of an error, the server will return an appropriate HTTP status code.
                                                               
## Testing the API with cURL
You can test the API using a cURL command as follows:
```bash
curl -X POST \
  http://localhost:8081/sms \
  -H 'Content-Type: application/json' \
  -d '{
    "to": "+1234567890",
    "body": "Hello, this is a test SMS message!"
}'
```
 curl -X POST \
  http://localhost:5000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Task title",
    "description": "Task description",
    "dueDate": "2023-05-01"
  }'
Replace `http://localhost:8081 `with the appropriate URL if your server is running on a different host or port. Replace `+1234567890 `with the recipient's phone number and customize the body field as desired.