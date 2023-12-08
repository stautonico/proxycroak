from typing import List
import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from proxycroak.database import db


class Set(db.Model):
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    legalities: Mapped[str] = mapped_column(String(128), nullable=True)  # json
    name: Mapped[str] = mapped_column(String(256), nullable=True)
    printedTotal: Mapped[int] = mapped_column(Integer)
    ptcgoCode: Mapped[str] = mapped_column(String(64), nullable=True)
    releaseDate: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    series: Mapped[str] = mapped_column(String(128), nullable=True)
    total: Mapped[int] = mapped_column(Integer)
    updatedAt: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    cards: Mapped[List["Card"]] = relationship(back_populates="set")


class Card(db.Model):
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    abilities: Mapped[str] = mapped_column(String(512), nullable=True)  # json
    artist: Mapped[str] = mapped_column(String(128), nullable=True)
    ancientTrait: Mapped[str] = mapped_column(String(256), nullable=True)  # json
    attacks: Mapped[str] = mapped_column(String(512), nullable=True)  # json
    convertedRetreatCost: Mapped[int] = mapped_column(Integer, nullable=True)
    evolvesFrom: Mapped[str] = mapped_column(String(128), nullable=True)
    flavorText: Mapped[str] = mapped_column(String(128), nullable=True)
    hp: Mapped[str] = mapped_column(String(64), nullable=True)
    image: Mapped[str] = mapped_column(String(128), nullable=True)
    regulationMark: Mapped[str] = mapped_column(String(8), nullable=True)
    legalities: Mapped[str] = mapped_column(String(128), nullable=True)  # json
    name: Mapped[str] = mapped_column(String(128), nullable=True)
    nationalPokedexNumbers: Mapped[str] = mapped_column(String(128), nullable=True)
    number: Mapped[str] = mapped_column(String(8), nullable=True)
    rarity: Mapped[str] = mapped_column(String(64), nullable=True)
    resistances: Mapped[str] = mapped_column(String(512), nullable=True)  # json
    retreatCost: Mapped[str] = mapped_column(String(512), nullable=True)  # json/unnecessary?
    rules: Mapped[str] = mapped_column(String(512), nullable=True)  # json
    subtypes: Mapped[str] = mapped_column(String(512), nullable=True)  # json
    supertype: Mapped[str] = mapped_column(String(512), nullable=True)  # json
    types: Mapped[str] = mapped_column(String(256), nullable=True)  # json
    weaknesses: Mapped[str] = mapped_column(String(256), nullable=True)  # json
    set_id: Mapped[int] = mapped_column(ForeignKey("set.id"))
    set: Mapped["Set"] = relationship(back_populates="cards")


class SharedDecklist(db.Model):
    id: Mapped[str] = mapped_column(String(8), primary_key=True)
    decklist: Mapped[str] = mapped_column(String(4192))
    expires: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
