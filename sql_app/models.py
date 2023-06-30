from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from .database import Base

class User(Base):
  __tablename__ = 'users'

  # primary_key は主キー、indexは検索しやすくなるため
  user_id = Column(Integer, primary_key=True, index=True)
  # unique は一意であるかどうか
  username = Column(String, unique=True, index=True)

class Room(Base):
  __tablename__ = 'rooms'
  
  room_id = Column(Integer, primary_key=True, index=True)
  room_name = Column(String, unique=True, index=True)
  capacity = Column(Integer)

class Booking(Base):
  __tablename__ = 'bookings'
  
  booking_id = Column(Integer, primary_key=True, index=True)
  # ForeignKey は紐付け。ondeleteはuser_idがなくなった時の対応。SET NULLはnullにセットするという意味。 nullableはnullを許容するかどうか
  user_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=False, index=True)
  room_id = Column(Integer, ForeignKey('rooms.room_id', ondelete='SET NULL'), nullable=False, index=True)
  booked_num = Column(Integer)
  start_datetime = Column(DateTime, nullable=False)
  end_datetime = Column(DateTime, nullable=False)
