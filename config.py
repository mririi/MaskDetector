from os import environ as env
import multiprocessing

PORT = 8081
DEBUG_MODE = 1

# Gunicorn config
bind = ":" + str(PORT)
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2 * multiprocessing.cpu_count()
