#!/usr/bin/python3
"""Initialization of the API package"""
from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False
