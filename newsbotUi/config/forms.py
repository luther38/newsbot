
from wtforms import Form, StringField
from wtforms import validators
from wtforms.validators import DataRequired, URL


class DiscordWebhookAddForm(Form):
    server = StringField('server', validators=[DataRequired()])
    channel = StringField('channel', validators=[DataRequired()])
    url = StringField('url', validators=[URL()])
    pass

class DiscordNew():
    pass