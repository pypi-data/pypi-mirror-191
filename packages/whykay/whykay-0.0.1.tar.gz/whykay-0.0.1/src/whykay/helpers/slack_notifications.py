import config
import os

from prefect_slack import SlackWebhook
from prefect_slack.messages import send_incoming_webhook_message
from prefect import flow, get_run_logger, task

webhook_url = config.SLACK_WEBHOOK

def post_to_slack(message: str):
    if config.SLACK_NOTIFICATIONS:
        send_incoming_webhook_message(
            slack_webhook=SlackWebhook(
                url=webhook_url
            ),
            text= message
        )
    else:
        logger = get_run_logger()
        logger.info(message)
