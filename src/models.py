# Importa la clase SQLAlchemy desde la extensión flask_sqlalchemy para interactuar con la base de datos
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    usuario_favorito = relationship('Favorito', backref='user', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "usuario_favorito": list(map(lambda item: item.serialize),self.usuario_favorito)
            # do not serialize the password, its a security breach
        }

class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    mass = db.Column(db.String(120), unique=True, nullable=False)
    hair_color = db.Column(db.String(120), unique=True, nullable=False)
    skin_color = db.Column(db.String(120), unique=True, nullable=False)
    eye_color = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Personajes %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
        }


class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    diameter = db.Column(db.String(120), unique=True, nullable=False)
    rotation_period = db.Column(db.String(120), unique=True, nullable=False)
    orbital_period = db.Column(db.String(120), unique=True, nullable=False)
    gravity = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(120), unique=True, nullable=False)
    terrain = db.Column(db.String(120), unique=True, nullable=False)
    surface_water = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Planetas %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
        }

class Vehiculos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    model = db.Column(db.String(120), unique=True, nullable=False)
    vehicle_class = db.Column(db.String(120), unique=True, nullable=False)
    manufacturer = db.Column(db.String(120), unique=True, nullable=False)
    cost_in_credits = db.Column(db.String(120), unique=True, nullable=False)
    length = db.Column(db.String(120), unique=True, nullable=False)
    crew = db.Column(db.String(120), unique=True, nullable=False)
    passengers = db.Column(db.String(120), unique=True, nullable=False)
    max_atmosphering_speed = db.Column(db.String(120), unique=True, nullable=False)
    cargo_capacity = db.Column(db.String(120), unique=True, nullable=False)
    consumables = db.Column(db.String(120), unique=True, nullable=False)
    films = db.Column(db.String(120), unique=True, nullable=False)
    pilots = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Vehiculos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "films": self.films,
            "pilots": self.pilots,
        }

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

    personajes_id = db.Column(db.Integer, db.ForeignKey('personajes.id')) 
    personajes = db.relationship(Personajes) 

    vehiculos_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id')) 
    vehiculos = db.relationship(Vehiculos)  

    planetas_id = db.Column(db.Integer, db.ForeignKey('planetas.id')) 
    planetas = db.relationship(Planetas)  

    def __repr__(self):
        return '<Favorito %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.user_id,
            # "usuario" : self.user,
            "personajes_id": None if self.personajes is None else self.personajes.serialize(),
            # "personajes" : self.personajes,
            "vehiculos_id": None if self.vehiculos is None else self.vehiculos.serialize(),
            # "vehiculos" : self.vehiculos,
            "planetas_id": None if self.planetas is None else self.planetas.serialize(),
            # "planetas" : self.planetas,
        }