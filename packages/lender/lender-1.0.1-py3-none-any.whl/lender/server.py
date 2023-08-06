#!/usr/bin/env python3
# coding=utf-8
import argparse

import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options

from lender.handlers import config
from lender.handlers import database
from lender.handlers import fileserver
from lender import application


def get_args_parser():
    parser = argparse.ArgumentParser(description="lender command line interface.")
    parser.add_argument("-c", "--config", default='config.ini', help="配置文件路径")
    parser.add_argument("-p", "--port", default=80, type=int, help="配置文件路径")
    return parser.parse_args()

def main():
    args = get_args_parser()
    print(args)
    config.Parse(args.config)

    handler = []
    handler.extend(database.Handle(config.Get_database()))
    handler.extend(fileserver.Handle(config.Get_fileupload()))
    print(handler)
    application.Serving(int(args.port), handler)


    # http_server = tornado.httpserver.HTTPServer(application)
    # http_server.listen(options.port)

    print("Development server is running at http://127.0.0.1:%s" % args.port)
    print("Quit the server with Control-C")

    # tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()