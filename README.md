# Newsbot
Automated and personalized news delivery for your community.

## What does it do

Currently, it reads collects news for the following sites.

* [Phantasy Star Online 2](https://pso2.com/news)
* [Final Fantasy XIV](https://na.finalfantasyxiv.com/lodestone/news/)
* [Pokemon Go Hub](https://pokemongohub.net/)
* [Reddit](https://reddit.com)
* [YouTube](https://youtube.com)
* [Instagram](https://instagram.com)
* [Twitter](https://twitter.com)
* [Twitch](https://twitch.tv)
* RSS Feeds
* Atom Feeds
* [Json Feeds](https://jsonfeed.org/)

The results that are collected are then sent to the following platforms.

* [Discord - Webhooks](https://discord.com/)

## Deployment

This application was made to be deployed to a Docker host.  If you want to run it on metal, call the app.py file.  

Use the docker image to deploy the application.

[Docker Hub](https://hub.docker.com/r/jtom38/newsbot)

You can see an example of how to deploy the bot with the docker-compose.yml file.

### Local Build

If you want to build the program from source.

```bash
git clone https://github.com/jtom38/newsbot.git
git fetch --all --tags
git checkout tags/versionNumber
make docker-build
# Add your variables to .env
vi .env

# This will use the docker-compose.yml file in the project to run the application.
make docker-run
```

## Settings

The application settings are currently stored in the .env file.  Use the template and apply the webhook links for the sites that you want to use.

## Outputs

### Discord Webhooks

If you want to have a single source post to multiple webhooks, you can do that.  On the line where you enter your webhook seperate each one with a space character.  The program will split them up and post updates to both webhooks.

## Sources

### Phantasy Star Online 2

This source pulls information directly from the website pso2.com and collects the news for you.

For the configuration of this source, see the Example Template.

### Pokemon Go Hub

This source monitors the RSS feed and collects the news posts for you.
This will collect all information that has been posted on the RSS feed and send it.

For the configuration of this source, see the Example Template.

### Final Fantasy XIV

This source pulls information directly from the main site.
With this source you able to define what type of news is posted to your server.

For the configuration of this source, see the Example Template.

### Reddit

Each subreddit is defined by its own number value.
Currently, 10 different subreddits can be monitored.  
Each subreddit will need its own entry with the correct values.

For the configuration of this source, see the Example Template.

### YouTube

You can now get updates when you defined YouTube channel posts an update!
At this time you can only monitor 10 feeds.

For the configuration of this source, see the Example Template.

### Instagram

Instagram can monitor a users posts or a tag as long as they are public.  
You can currently monitor up to 10 of each.
This source will pull information from the web site directly so no API keys are required.

For the configuration of this source, see the Example Template.

### Twitter

In order to use the Twitter source you will need to sign up for a Twitter Developer Account.  
Once you have that, give the secrets to NewsBot to pull information for you.
This program will not act as a user when it comes to OAuth.
NewsBot is only going to use the keys to pull information that is public on other users or tags.
It will not pull your personal Twitter Feed.

For the configuration of this source, see the Example Template.

### Twitch

In order to use the Twitch source you will need to sign up for a [Twitch Developer Account](https://dev.twitch.tv/login).

1. Sign up for a developer account
2. Register a new Application.
3. OAuth Redirect URL: `https://localhost`
4. Category: Other
5. Once its created take the `Client ID` and `Client Secret` and place them in the NewsBot configuration.

For the configuration of this source, see the Example Template

## Example Template

```ini
# Pokemon Go Hub Example
NEWSBOT_POGO_ENABLED=true
NEWSBOT_POGO_HOOK=https://discordapp.com/api/webhooks/...

# Phantasy Star Online 2 Example
NEWSBOT_PSO2_ENABLED=true
NEWSBOT_PSO2_HOOK=https://discordapp.com/api/webhooks/...

# Final Fantasy XIV Example
NEWSBOT_FFXIV_ALL=False
NEWSBOT_FFXIV_TOPICS=True
NEWSBOT_FFXIV_NOTICES=False
NEWSBOT_FFXIV_MAINTENANCE=False
NEWSBOT_FFXIV_UPDATES=False
NEWSBOT_FFXIV_STATUS=False
NEWSBOT_FFXIV_HOOK=https://discordapp.com/api/webhooks/...

# Reddit Examples
NEWSBOT_REDDIT_SUB_0=aww
NEWSBOT_REDDIT_HOOK_0=https://discordapp.com/api/webhooks/...
NEWSBOT_REDDIT_SUB_1=corgi
NEWSBOT_REDDIT_HOOK_1=https://discordapp.com/api/webhooks/...

# YouTube Examples
NEWSBOT_YOUTUBE_URL_0=https://www.youtube.com/user/gamegrumps
NEWSBOT_YOUTUBE_HOOK_0=https://discordapp.com/api/webhooks/...
NEWSBOT_YOUTUBE_NAME_0=GameGrumps

# Instagram Examples
NEWSBOT_INSTAGRAM_USER_NAME_0=madmax_fluffyroad
NEWSBOT_INSTAGRAM_USER_HOOK_0=https://discordapp.com/api/webhooks/...
NEWSBOT_INSTAGRAM_TAG_NAME_0=corgi
NEWSBOT_INSTAGRAM_TAG_HOOK_0=https://discordapp.com/api/webhooks/...

# Twitter Examples
# Twitter Developer Secrets
NEWSBOT_TWITTER_API_KEY=
NEWSBOT_TWITTER_API_KEY_SECRET=

# User/Hashtag Examples
NEWSBOT_TWITTER_USER_NAME_0=dodo
NEWSBOT_TWITTER_USER_HOOK_0=https://discordapp.com/api/webhooks/...
NEWSBOT_TWITTER_TAG_NAME_0=corgi
NEWSBOT_TWITTER_TAG_HOOK_0=https://discordapp.com/api/webhooks/...

# Twitch Examples
# Twitch Developer Secrets
NEWSBOT_TWITCH_CLIENT_ID=
NEWSBOT_TWITCH_CLIENT_SECRET=

# Twitch Settings
NEWSBOT_TWITCH_MONITOR_CLIPS=True
NEWSBOT_TWITCH_MONITOR_VOD=True

# Twitch User Examples
NEWSBOT_TWITCH_USER_NAME_0=nintendo
NEWSBOT_TWITCH_HOOK_0=https://discordapp.com/api/webhooks/...

NEWSBOT_RSS_NAME_1=omgubuntu
NEWSBOT_RSS_LINK_1=https://www.omgubuntu.co.uk
NEWSBOT_RSS_HOOK_1=https://discordapp.com/api/webhooks/...
```

## Known Issues

### Discord Webhook Video Embed

At this time Discord webhooks do not support playing video links inside Discord.  This is a requested feature but it has not had any movement.  Because of this, if a video post is found it will let you know to "Watch the video online!"

[Feature Request](https://support.discord.com/hc/en-us/community/posts/360037387352-Videos-in-Rich-Embeds)

## Change Log

### 0.7.0

| Type    | Notes |
| ---     | --- |
| Note    |  Instagram has been disabled for this release. Due to changes on the UI Selenium is unable to pull up user/tag pages directly now |
| Added   | [Generic RSS Reader](https://github.com/jtom38/newsbot/issues/45) | |
| Added   | [Dynamic Site Icon Pull](https://github.com/jtom38/newsbot/issues/46)
| Updated | [Logs can be stored in the DB](https://github.com/jtom38/newsbot/issues/42)
| Closed  | [Add support for Steam News]()
| Updated | Cleaned up how Newsbot reads all the env values.
| Updated | Optimized the Twitter source to check if the url has been seen already and skips it if it has.
| Updated | Did some cleanup on the sources and moved code reuse to its own class.
| Updated | The Dockerfile now has logic to force a build a fail to make sure that selenium should always work.

### 0.6.0

| Type | Notes |
| ---    | --- |
| Added  | [Add Cache Layer](https://github.com/jtom38/newsbot/issues/40)
| Added  | [Add Twitch Clip Support](https://github.com/jtom38/newsbot/issues/39)
| Added  | [Add Twitch VoD Support](https://github.com/jtom38/newsbot/issues/38)
| Added  | [Reddit Album Support](https://github.com/jtom38/newsbot/issues/36)
| Fixed  | [Discord Webhooks looping with multiple webhooks](https://github.com/jtom38/newsbot/issues/37)
| Update | Reddit and YouTube sources will use the cache to store some values to avoid extra calls that are not required.

### 0.5.1

| Type | Notes |
| ---    | --- |
| Update | Corrected a problem with the Reddit source that would crash the thread when it pulled Author information from a subreddit that did not have a custom CSS.  

### 0.5.0

| Type | Notes |
| ---    | --- |
| Added  | Twitter Support was added.  To enable Twitter you will need to provide it with the Twitter Developer API keys |
| Update | Discord Template was updated. |
| Update | Database changes to enable storing the posters information. |
