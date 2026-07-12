from sqlalchemy import Column, DateTime, Float, Integer, String

from database.database import Base


class Weather(Base):

    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)

    city = Column(String)
    country = Column(String)

    latitude = Column(Float)

    longitude = Column(Float)

    temperature = Column(Float)

    feels_like = Column(Float)

    temp_min = Column(Float)

    temp_max = Column(Float)

    humidity = Column(Integer)

    pressure = Column(Integer)

    wind_speed = Column(Float)

    wind_degree = Column(Float)

    clouds = Column(Integer)

    weather = Column(String)

    description = Column(String)

    visibility = Column(Integer)

    sunrise = Column(DateTime)

    sunset = Column(DateTime)

    timestamp = Column(DateTime)

    temperature_level = Column(String)

    humidity_level = Column(String)

    day = Column(String)

    hour = Column(Integer)
