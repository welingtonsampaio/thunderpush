# This file contains default settings for this project.
# If you want to customize this settings, use command line arguments
# to do so, instead of modifying this file.

# Although Thunderpush server supports multiple server clients,
# at the moment we make it single-client.

# Port to which the server will be bound.
PORT = 8080

# Host to which the server will be binded.
HOST = ''

# Debug mode? Tornado will restart the server whenever any project file
# change. Very useful for development.
DEBUG = False

# This sets the logging level to DEBUG.
VERBOSE = False

# MONGO informations
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'thunderpush_db'
MONGO_TABLE = 'auth'
MONGO_PUBLIC = 'public_key'
MONGO_SECRET = 'secret_key'