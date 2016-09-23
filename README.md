# oldurl

A bot who helps the society in shaming the bad people who's posting old links.

Originally used in an IRC environment, now cleaned up a bit and used for Slack.

## Environment variables

Make sure to provide the needed environment variables:

* `MONGO_DB`: Database to use in MongoDB
* `MONGO_USERNAME`: Username to use in MongoDB
* `MONGO_PASSWORD`: Password to use in MongoDB
* `SLACK_TOKEN`: Slack token to use (only used in `slack.py`)

## Import old data

`logparse.py` can be used to scan log files (with eggdrop like format) for URLs
to import in the database.


## Credits

* [Zn4rK](https://github.com/zn4rk)
* [pixnion](https://github.com/pixnion) for the old mIRC .BAT implementation (!)
