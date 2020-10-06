# newsbot
Automated news delivery

## What does it do

Currently, it reads collects news for the following sites.

* [Phantasy Star Online 2](https://pso2.com/news)
* [Final Fantasy XIV](https://na.finalfantasyxiv.com/lodestone/news/)
* [Pokemon Go Hub](https://pokemongohub.net/)
* [Reddit](https://reddit.com)
* [YouTube](https://youtube.com)
* [Instagram](https://instagram.com)

The results that are collected are then sent to the following platforms.

* [Discord - Webhooks](https://discord.com/)

## Deployment

This application was made to be deployed to a Docker host.  If you want to run it on metal, call the app.py file.  

Use the docker image to deploy the application.

https://hub.docker.com/r/jtom38/newsbot

You can see an example of how to deploy the bot with the docker-compose.yml file.

## Settings

The application settings are currently stored in the .env file.  Use the template and apply the webhook links for the sites that you want to use.

### Discord Webhooks

If you want to have a single source post to multiple webhooks, you can do that.  On the line where you enter your webhook seperate each one with a space character.  The program will split them up and post updates to both webhooks.

### Reddit

Each subreddit is defined by its own number value.

```ini
NEWSBOT_REDDIT_SUB_0=aww
NEWSBOT_REDDIT_HOOK_0=https://discordapp.com/api/webhooks/...
NEWSBOT_REDDIT_SUB_1=python
NEWSBOT_REDDIT_HOOK_1=https://discordapp.com/api/webhooks/...
```

Currently, 10 different subreddits can be monitored.  Each subreddit will need its own entry with the correct values.

### YouTube

You can now get updates when you defined YouTube channel posts an update!  
Here is the entries that are required to support a single feed.  
At this time you can only monitor 10 feeds.

```ini
NEWSBOT_YOUTUBE_URL_0=https://www.youtube.com/user/gamegrumps
NEWSBOT_YOUTUBE_HOOK_0=https://discordapp.com/api/webhooks/...
NEWSBOT_YOUTUBE_NAME_0=GameGrumps
```

### Instagram

Instagram can monitor a users posts or a tag as long as they are public.  You can currently monitor up to 10 of each.

```ini
NEWSBOT_INSTAGRAM_USER_NAME_0=play_pso2
NEWSBOT_INSTAGRAM_USER_HOOK_0=https://discordapp.com/api/webhooks/...

NEWSBOT_INSTAGRAM_TAG_NAME_0=corgi
NEWSBOT_INSTAGRAM_TAG_HOOK_0=https://discordapp.com/api/webhooks/...
```

[Configuration Template](https://github.com/jtom38/newsbot/blob/master/env.template)

## Known Issues

### Discord Webhook Video Embed

At this time Discord webhooks do not support playing video links inside Discord.  This is a requested feature but it has not had any movement.  Because of this, if a video post is found it will let you know to "Watch the video online!"

[Feature Request](https://support.discord.com/hc/en-us/community/posts/360037387352-Videos-in-Rich-Embeds)
