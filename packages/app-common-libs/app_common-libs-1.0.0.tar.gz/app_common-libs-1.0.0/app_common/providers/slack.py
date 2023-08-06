import os

from slack.web.client import WebClient

client = WebClient(token=os.environ.get('slack_api_token'))


class _SlackAttachmentBuilder:
    def __init__(self, parent_builder):
        self.parent_builder = parent_builder
        self.title = ''
        self.media_url = None

    def add_title(self, title):
        self.title = title
        return self

    def add_media_url(self, media_url):
        self.media_url = media_url
        return self

    def end(self):
        media_attachment = {
            'title': self.title,
            'image_url': self.media_url,
        }
        self.parent_builder.attachments.append(media_attachment)
        return self.parent_builder


class _SlackRedirectionButtonBuilder:
    def __init__(self, parent_builder):
        self.parent_builder = parent_builder
        self.title = ''
        self.actions = []

    def add_title(self, title):
        self.title = title
        return self

    def add_redirection_url(self, button_title, redirection_url):
        self.actions.append(
            {
                'type': 'button',
                'text': button_title,
                'url': redirection_url
            }
        )

        return self

    def end(self):
        button_attachment = {
            'fallback': self.title,
            'actions': self.actions
        }
        self.parent_builder.attachments.append(button_attachment)
        return self.parent_builder


class _SlackHeadingBuilder:
    def __init__(self, parent_builder):
        self.parent_builder = parent_builder
        self.title = ''
        self.messages = []

    def add_title(self, title):
        self.title = title
        return self

    def add_line(self, message):
        self.messages.append(str(message))
        return self

    def add_spaces(self, points=1):
        self.messages.append('\n' * points)
        return self

    def end(self):
        heading = {
            'pretext': self.title,
            'text': '\n'.join(self.messages),
            'mrkdwn_in': ['title', 'text', 'pretext']
        }
        self.parent_builder.attachments.append(heading)
        return self.parent_builder


class SlackMessageBuilder:
    def __init__(self, message):
        self.messages = [message]
        self.attachments = []

    def add_heading(self):
        return _SlackHeadingBuilder(self)

    def add_attachment(self):
        return _SlackAttachmentBuilder(self)

    def add_redirection_button(self):
        return _SlackRedirectionButtonBuilder(self)

    def add_line(self, message):
        self.messages.append(str(message))
        return self

    def add_lines(self, lines):
        for message in lines:
            self.messages.append(str(message))
        return self

    def add_spaces(self, points=1):
        self.messages.append('\n' * points)
        return self

    def build(self):
        return '\n'.join(self.messages)

    def post(self, channel='payment-error-dev', username='Mobilads'):
        """
        Post provide message on provided slack channel
        """
        message = self.build()
        print(f'SlackBuilder post message:-{message}')
        client.chat_postMessage(
            username=username,
            channel=channel,
            text=message,
            attachments=self.attachments,
        )
