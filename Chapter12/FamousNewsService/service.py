import mongoengine

from models import (
    CommandNewsModel,
    Base,
    QueryNewsModel,
)

from sqlalchemy import Sequence

from nameko.events import EventDispatcher
from nameko.rpc import rpc
from nameko.events import event_handler
from nameko_sqlalchemy import DatabaseSession


class Command:
    name = 'command_famous'
    dispatch = EventDispatcher()
    db = DatabaseSession(Base)

    @rpc
    def add_news(self, data):
        try:
            version = 1
            if data.get('version'):
                version = (data.get('version') + 1)
            if data.get('id'):
                id = data.get('id')
            else:
                id = self.db.execute(Sequence('news_id_seq'))
            news = CommandNewsModel(
                id=id,
                version=version,
                title=data['title'],
                content=data['content'],
                author=data['author'],
                published_at=data.get('published_at'),
                tags=data['tags'],
            )
            self.db.add(news)
            self.db.commit()
            data['id'] = news.id
            data['version'] = news.version
            self.dispatch('replicate_db_event', data)
            return data
        except Exception as e:
            self.db.rollback()
            return e


class Query:
    name = 'query_famous'

    @event_handler('command_famous', 'replicate_db_event')
    def normalize_db(self, data):
        try:
            news = QueryNewsModel.objects.get(
                id=data['id']
            )
            news.update(
                version=data.get('version', news.version),
                title=data.get('title', news.title),
                content=data.get('content', news.content),
                author=data.get('author', news.author),
                published_at=data.get('published_at', news.published_at),
                tags=data.get('tags', news.tags),
            )
            news.reload()
        except mongoengine.DoesNotExist:
            QueryNewsModel(
                id=data['id'],
                version=data['version'],
                title=data.get('title'),
                content=data.get('content'),
                author=data.get('author'),
                tags=data.get('tags'),
            ).save()
        except Exception as e:
            return e

    @rpc
    def get_news(self, id):
        try:
            news = QueryNewsModel.objects.get(id=id)
            return news.to_json()
        except mongoengine.DoesNotExist as e:
            return e
        except Exception as e:
            return e

    @rpc
    def get_all_news(self, num_page, limit):
        try:
            if not num_page:
                num_page = 1
            offset = (num_page - 1) * limit
            news = QueryNewsModel.objects.skip(offset).limit(limit)
            return news.to_json()
        except Exception as e:
            return e
