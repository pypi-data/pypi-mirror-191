from app_common.config.base import SLACK_BUGS_CHANNEL, IS_PROD
from app_common.providers.slack import SlackMessageBuilder


def post_error_on_slack(msg_type, message):
    prefix = IS_PROD and 'Production' or 'Staging'
    SlackMessageBuilder(f'{msg_type} on {prefix}').add_line(
        f'\n{message}'
    ).post(channel=SLACK_BUGS_CHANNEL)


def post_dict_on_slack(title, message_dict):
    if not isinstance(message_dict, dict):
        return
    builder = SlackMessageBuilder(f'{title}')
    for key, value in message_dict.items():
        builder.add_line(f'{key}:- {value}')
    builder.post(channel=SLACK_BUGS_CHANNEL)
