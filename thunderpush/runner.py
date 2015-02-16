from thunderpush.sortingstation import SortingStation, StationMongo
from thunderpush.handler import ThunderSocketHandler
from thunderpush import api, __version__
from thunderpush import settings

from sockjs.tornado import SockJSRouter

import sys
import tornado.ioloop
import argparse
import logging

logger = logging.getLogger()


def run_app():
    # configure logging level
    if settings.VERBOSE:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


    ThunderRouter = SockJSRouter(ThunderSocketHandler, "/connect")

    # api urls
    urls = [
        (r"/api/1\.0\.0/(?P<apikey>.+)/users/",
            api.UserCountHandler),
        (r"/api/1\.0\.0/(?P<apikey>.+)/users/(?P<user>.+)/",
            api.UserHandler),
        (r"/api/1\.0\.0/(?P<apikey>.+)/channels/(?P<channel>.+)/",
            api.ChannelHandler),
        (r"/api/1\.0\.0/(?P<apikey>.+)/events/(?P<event>.+)/",
            api.EventHandler),
    ]

    # include sockjs urls
    urls += ThunderRouter.urls

    application = tornado.web.Application(urls, settings.DEBUG)

    ss = SortingStation()
    sr = StationMongo(settings.MONGO_HOST, settings.MONGO_PORT, settings.MONGO_DB, settings.MONGO_TABLE, settings.MONGO_PUBLIC, settings.MONGO_SECRET)

    # Single-client only at the moment.
    # ss.create_messenger(settings.APIKEY, settings.APISECRET)

    logger.info("Starting Thunderpush server at %s:%d",
        settings.HOST, settings.PORT)

    application.listen(settings.PORT, settings.HOST)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.info("Shutting down...")


def update_settings(args):
    args = vars(args)

    for optname in ["PORT", "HOST", "VERBOSE", "DEBUG", "MONGO_HOST", "MONGO_PORT", "MONGO_DB", "MONGO_TABLE", "MONGO_PUBLIC", "MONGO_SECRET"]:
        value = args.get(optname, None)

        if not value is None:
            setattr(settings, optname, value)


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--port',
        default=settings.PORT,
        help='binds server to custom port',
        action="store", type=int, dest="PORT")

    parser.add_argument('-H', '--host',
        default=settings.HOST,
        help='binds server to custom address',
        action="store", type=str, dest="HOST")

    parser.add_argument('-v', '--verbose',
        default=settings.VERBOSE,
        help='verbose mode',
        action="store_true", dest="VERBOSE")

    parser.add_argument('-d', '--debug',
        default=settings.DEBUG,
        help='debug mode (useful for development)',
        action="store_true", dest="DEBUG")

    parser.add_argument('-mh', '--mongo-host',
        default=settings.MONGO_HOST,
        help='Hostname of Mongo database',
        action="store", dest="MONGO_HOST")

    parser.add_argument('-mp', '--mongo-port',
        default=settings.MONGO_PORT,
        help='Port to Mongo connection',
        action="store", dest="MONGO_PORT")

    parser.add_argument('-md', '--mongo-db',
        default=settings.MONGO_DB,
        help='Database Mongo collection',
        action="store", dest="MONGO_DB")

    parser.add_argument('-mt', '--mongo-table',
        default=settings.MONGO_TABLE,
        help='DB Mongo number',
        action="store", dest="MONGO_TABLE")

    parser.add_argument('-mpk', '--mongo-public',
        default=settings.MONGO_PUBLIC,
        help='Public field in Mongo collection',
        action="store", dest="MONGO_PUBLIC")

    parser.add_argument('-msk', '--mongo-secret',
        default=settings.MONGO_SECRET,
        help='Secret field in Mongo collection',
        action="store", dest="MONGO_SECRET")

    parser.add_argument('-V', '--version', 
        action='version', version=__version__)

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    update_settings(args)
    run_app()

if __name__ == "__main__":
    main()
