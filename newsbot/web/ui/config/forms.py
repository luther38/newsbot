from wtforms import Form, StringField
from wtforms import validators
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, URL

class DiscordWebhookAddForm(Form):
    server = StringField("server", validators=[DataRequired()])
    channel = StringField("channel", validators=[DataRequired()])
    url = StringField("url", validators=[URL()])
    pass

class YoutubeNew(Form):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    discordwebhook = StringField('discord', validators=[DataRequired()])
    enabled = BooleanField('enabled')
