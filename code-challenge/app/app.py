#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Enable CORS for all routes
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Routes

@app.route('/')
def home():
    return ''

@app.route('/heroes')
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [
        {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
        for hero in heroes
    ]
    return jsonify(heroes_data)

@app.route('/heroes/<int:hero_id>')
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        hero_data = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [
                {"id": power.id, "name": power.name, "description": power.description}
                for power in hero.hero_powers
            ]
        }
        return jsonify(hero_data)
    else:
        response = {"error": "Hero not found"}
        return jsonify(response), 404

@app.route('/powers')
def get_powers():
    powers = Power.query.all()
    powers_data = [
        {"id": power.id, "name": power.name, "description": power.description}
        for power in powers
    ]
    return jsonify(powers_data)

@app.route('/powers/<int:power_id>')
def get_power(power_id):
    power = Power.query.get(power_id)
    if power:
        power_data = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        return jsonify(power_data)
    else:
        response = {"error": "Power not found"}
        return jsonify(response), 404

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power:
        try:
            data = request.get_json()
            power.description = data['description']
            db.session.commit()
            updated_power = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            return jsonify(updated_power)
        except Exception as e:
            response = {"errors": [str(e)]}
            return jsonify(response), 400
    else:
        response = {"error": "Power not found"}
        return jsonify(response), 404

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.get_json()
        new_hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        db.session.add(new_hero_power)
        db.session.commit()
        return get_hero(data['hero_id'])  # Return hero data after creating the hero power
    except Exception as e:
        response = {"errors": [str(e)]}
        return jsonify(response), 400

if __name__ == '__main__':
    app.run(port=5555)
