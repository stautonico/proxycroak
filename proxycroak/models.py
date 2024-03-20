from typing import List
import datetime

from flask_login import UserMixin
from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from proxycroak.database import db


class Set(db.Model):
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    legalities: Mapped[str] = mapped_column(String(128), nullable=True)  # json
    name: Mapped[str] = mapped_column(String(256), nullable=True)
    printedTotal: Mapped[int] = mapped_column(Integer)
    ptcgoCode: Mapped[str] = mapped_column(String(64), nullable=True)
    alternatePtcgoCode: Mapped[str] = mapped_column(String(64), nullable=True)
    releaseDate: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    series: Mapped[str] = mapped_column(String(128), nullable=True)
    total: Mapped[int] = mapped_column(Integer)
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    cards: Mapped[List["Card"]] = relationship(back_populates="set")


class Card(db.Model):
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    abilities: Mapped[str] = mapped_column(String(2048), nullable=True)  # json
    artist: Mapped[str] = mapped_column(String(128), nullable=True)
    ancientTrait: Mapped[str] = mapped_column(String(256), nullable=True)  # json
    attacks: Mapped[str] = mapped_column(String(2048), nullable=True)  # json
    convertedRetreatCost: Mapped[int] = mapped_column(Integer, nullable=True)
    evolvesFrom: Mapped[str] = mapped_column(String(128), nullable=True)
    flavorText: Mapped[str] = mapped_column(String(1024), nullable=True)
    hp: Mapped[str] = mapped_column(String(64), nullable=True)
    image: Mapped[str] = mapped_column(String(128), nullable=True)
    regulationMark: Mapped[str] = mapped_column(String(8), nullable=True)
    legalities: Mapped[str] = mapped_column(String(512), nullable=True)  # json
    name: Mapped[str] = mapped_column(String(128), nullable=True)
    nationalPokedexNumbers: Mapped[str] = mapped_column(String(128), nullable=True)
    number: Mapped[str] = mapped_column(String(8), nullable=True)
    rarity: Mapped[str] = mapped_column(String(64), nullable=True)
    resistances: Mapped[str] = mapped_column(String(1024), nullable=True)  # json
    retreatCost: Mapped[str] = mapped_column(String(1024), nullable=True)  # json/unnecessary?
    rules: Mapped[str] = mapped_column(String(1024), nullable=True)  # json
    subtypes: Mapped[str] = mapped_column(String(512), nullable=True)  # json
    supertype: Mapped[str] = mapped_column(String(512), nullable=True)  # json
    types: Mapped[str] = mapped_column(String(256), nullable=True)  # json
    weaknesses: Mapped[str] = mapped_column(String(1024), nullable=True)  # json
    set_id: Mapped[int] = mapped_column(ForeignKey("set.id"))
    set: Mapped["Set"] = relationship(back_populates="cards")


class UnreleasedSet(db.Model):
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=True)
    ptcgoCode: Mapped[str] = mapped_column(String(64), nullable=True)
    alternatePtcgoCode: Mapped[str] = mapped_column(String(64), nullable=True)
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    cards: Mapped[List["UnreleasedCard"]] = relationship(back_populates="set")


class UnreleasedCard(db.Model):
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    image: Mapped[str] = mapped_column(String(128), nullable=True)
    name: Mapped[str] = mapped_column(String(128), nullable=True)
    number: Mapped[str] = mapped_column(String(8), nullable=True)
    set_id: Mapped[int] = mapped_column(ForeignKey("unreleased_set.id"))
    set: Mapped["UnreleasedSet"] = relationship(back_populates="cards")


class SharedDecklist(db.Model):
    id: Mapped[str] = mapped_column(String(8), primary_key=True)
    decklist: Mapped[str] = mapped_column(String(4192))
    expires: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    password_reset_token: Mapped[str] = mapped_column(String(64), nullable=True, unique=True)
    password_reset_expires: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    account_activation_token: Mapped[str] = mapped_column(String(64), nullable=True, unique=True)
    account_activation_expires: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    account_activated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    account_activated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def get_id(self):
        return f"{self.id}"

    def __str__(self):
        return f"User(username={self.username})"

    def __repr__(self):
        return self.__str__()
