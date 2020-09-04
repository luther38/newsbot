# newsbot
Automated news delivery

## What does it do

Currently, it reads collects news for the following sites.

* [Phantasy Star Online 2](https://pso2.com/news)
* [Final Fantasy XIV](https://na.finalfantasyxiv.com/lodestone/news/)
* [Pokemon Go Hub](https://pokemongohub.net/)
* [Reddit](https://reddit.com)

The results that are collected are then sent to the following platforms.

* [Discord - Webhooks](https://discord.com/new)

## Deploy

Use the docker image to deploy the application.

https://hub.docker.com/r/jtom38/newsbot

You can see an example of how to deploy the bot with the docker-compose.yml file.

## Settings

The application settings are currently stored in the .env file.  Use the template and apply the webhook links for the sites that you want to use.

To send to discord for a site, add the webhook url to the HOOK variable.  You can also send to more then one webhook.  With each variable, add a space between them and the program will convert it to two different webhooks.

Each subreddit is defined by its own number value.

`NEWSBOT_REDDIT_SUB_0 = aww`
`NEWSBOT_REDDIT_HOOK_0 = webHookUrl`
`NEWSBOT_REDDIT_SUB_1 = python`
`NEWSBOT_REDDIT_HOOK_1 = webHookUrl`

Currently, 10 different subreddits can be monitored.  Each subreddit will need its own entry with the correct values.

[Configuration Template](https://github.com/jtom38/newsbot/blob/master/env.template)

## Tools

* Python 3
* Beautiful Soup
* Requests
