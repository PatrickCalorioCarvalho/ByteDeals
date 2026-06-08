import aio_pika

from core.config.settings import settings

class RabbitPublisher:
    async def publish(self, routing_key: str, event):

        connection = await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASS
        )

        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            "bytedeals.events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        await exchange.publish(
            aio_pika.Message(
                body=event.model_dump_json().encode()
            ),
            routing_key=routing_key
        )

        await connection.close()