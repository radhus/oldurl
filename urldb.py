import os
import sys
import mongoengine
from mongoengine import Document, StringField, DateTimeField


class URL(Document):
    url = StringField(required=True,
                      unique=True,
                      primary_key=True)
    nick = StringField(required=True)
    date = DateTimeField(required=True)

    def __str__(self):
        return "[%s] <%s> %s" % (str(self.date),
                                 str(self.nick),
                                 str(self.url))


def lookup_url(url):
    urls = URL.objects(url=url)
    if urls:
        return urls.first()


def connect():
    envs = {"db": "MONGO_DB",
            "username": "MONGO_USERNAME",
            "password": "MONGO_PASSWORD"}
    for key, env in envs.items():
        if env not in os.environ:
            print("Provide ", env, " in the environment!")
            sys.exit(1)
        envs[key] = os.environ[env]
    mongoengine.connect(envs["db"],
                        username=envs["username"],
                        password=envs["password"])
