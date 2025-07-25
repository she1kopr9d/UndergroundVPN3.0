import faststream.rabbit

import config

broker = faststream.rabbit.RabbitBroker(config.settings.rabbitmq_url)
