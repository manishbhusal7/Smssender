import json
import logging
import os
import asyncio
import redis2
import aiohttp.web as web
from dotenv import load_dotenv
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
import redis2

redis_url = "redis://localhost:6379/0"

# Convert the redis_url string to a bytes-like object
redis_url_bytes = redis_url.encode()

# Create the Redis connection pool using the from_url method
redis_pool = redis2.StrictRedis.from_url(
    redis_url, max_connections=10, decode_responses=True
)


# Use the redis_pool object to interact with Redis





class SMSHandler:
    def __init__(self, account_sid, auth_token, number, redis_pool):
        self.client = Client(account_sid, auth_token)
        self.redis_pool = redis_pool
        self.number = number

    async def handle_request(self, request):
        if request.method != 'POST':
            return web.Response(status=405)

        try:
            data = await request.json()
        except json.JSONDecodeError:
            return web.Response(status=400)

        if self.redis_pool.get(data['to']):
            response = {'message': 'SMS already sent to this phone number'}
            return web.json_response(response)

        try:
            message = await self.send_sms(data['to'], data['body'])
            response = {'message_id': message.sid}
            self.redis_pool.set(data['to'], 'sent', ex=3600)
            return web.json_response(response)
        except TwilioRestException as e:
            logging.error(str(e))
            return web.Response(status=500)

    async def send_sms(self, to, body):
        try:
            message = self.client.messages.create(
                body=body,
                from_=self.number,  # Replace with your Twilio phone number
                to=to
            )
            return message
        except TwilioRestException as e:
            logging.error(str(e))
            raise


async def start_server():
    load_dotenv()

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    number = os.getenv("TWILIO_NUMBER")
    redis_url = os.getenv('REDIS_URL')
    redis_password = os.getenv('REDIS_PASSWORD')
    try:
        redis_pool = redis2.StrictRedis.from_url(
            redis_url, decode_responses=True, max_connections=10, password=redis_password
        )
    except Exception as e:
        logging.error(str(e))
        raise e
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = SMSHandler(account_sid, auth_token, number, redis_pool)
    app = web.Application()
    

    app.add_routes([web.post('/sms', handler.handle_request)])

    port = int(os.getenv('PORT', 8081))
    logging.info(f'SMS server is listening on port {port}...')
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_server())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()