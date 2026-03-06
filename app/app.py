import redis
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Redis Cache
redis_client = redis.Redis.from_url(os.environ.get('REDIS_URL'))

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Example endpoint that caches result
@app.route("/visits")
def visits():
    count = redis_client.incr("visits_count")
    return jsonify({"visits": count})

@app.route("/health")
def health():
    return {"status": "UP"}, 200

@app.route("/")
def home():
    return "Hello Flask + Postgres + Redis inside Docker!"