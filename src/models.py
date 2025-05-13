from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, Text, DateTime, func, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    date_added: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_login: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    fav_planets: Mapped[List["FavPlanets"]] = relationship(
        "FavPlanet", back_populates="user")
    fav_people: Mapped[List["FavPeople"]] = relationship(
        "FavPerson", back_populates="user")
    fav_vehicles: Mapped[List["FavVehicles"]] = relationship(
        "FavVehicle", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "name": self.name,
            "lastname": self.lastname,
            "date_added": self.date_added,
            "last_login": self.last_login
        }


class Person(db.Model):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specie: Mapped[str] = mapped_column(String(50), nullable=True)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[int] = mapped_column(Integer, nullable=True)
    genre: Mapped[str] = mapped_column(String(20), nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    born_planet_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"), unique=True, nullable=True)

    vehicle: Mapped["Vehicle"] = relationship(
        "Vehicle",
        foreign_keys=[vehicle_id],
        back_populates="person",
        uselist=False
    )

    born_planet: Mapped["Planet"] = relationship(
        "Planet", back_populates="people")
    favs: Mapped["FavPeople"] = relationship(
        "FavPeople", back_populates="person")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "specie": self.specie,
            "height": self.height,
            "weight": self.weight,
            "genre": self.genre,
            "image_url": self.image_url,
            "description": self.description,
            "born_panet_id": self.born_planet_id,
            "vehicle_id": self.vehicle_id
        }


class Planet(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    diameter: Mapped[int] = mapped_column(Integer, nullable=True)
    weather: Mapped[str] = mapped_column(String(50), nullable=True)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    personajes: Mapped["Person"] = relationship(
        "Person", back_populates="born_planet")
    favoritos: Mapped["FavPlanets"] = relationship(
        "FavPlanet", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "weather": self.weather,
            "population": self.population,
            "image_url": self.image_url,
            "description": self.description
        }


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=True)
    length: Mapped[float] = mapped_column(Float, nullable=True)
    max_vel: Mapped[int] = mapped_column(Integer, nullable=True)
    crew: Mapped[int] = mapped_column(Integer, nullable=True)
    passengers: Mapped[int] = mapped_column(Integer, nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"), nullable=True)

    personaje: Mapped["Person"] = relationship(
        "Person",
        back_populates="vehicle",
        uselist=False,
        remote_side="Person.vehicle_id",
        primaryjoin="Vehicle.id == Person.vehicle_id"
    )
    favs: Mapped["FavVehicles"] = relationship(
        "FavVehicle", back_populates="vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "length": self.length,
            "max_vel": self.max_vel,
            "crew": self.crew,
            "passengers": self.passengers,
            "image_url": self.image_url,
            "description": self.description,
            "person_id": self.person_id
        }


class FavPeople(db.Model):
    __tablename__ = "fav_people"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"), nullable=False)
    date_added: Mapped[datetime] = mapped_column(
        DateTime, default=func.now())

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.planet_id,
            "date_added": self.date_added
        }

    user = relationship("User", back_populates="fav_people")
    person = relationship("Person", back_populates="favs")


class FavPlanets(db.Model):
    __tablename__ = "fav_planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=False)
    date_added: Mapped[datetime] = mapped_column(
        DateTime, default=func.now())

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "date_added": self.date_added
        }

    user = relationship("User", back_populates="fav_planets")
    planet = relationship("Planet", back_populates="favs")


class FavVehicles(db.Model):
    __tablename__ = "fav_vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"), nullable=False)
    date_added: Mapped[datetime] = mapped_column(
        DateTime, default=func.now())

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id,
            "date_added": self.date_added
        }

    user = relationship("User", back_populates="fav_vehicles")
    vehicle = relationship("Vehicle", back_populates="favs")
