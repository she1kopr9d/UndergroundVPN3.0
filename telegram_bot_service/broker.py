import faststream.rabbit

import config


broker_obj = faststream.rabbit.RabbitBroker(config.settings.rabbitmq_url)
