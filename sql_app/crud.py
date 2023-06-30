from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

# sqlalchemyはpythonの書き方でデータベースの操作を行うことができる。

# ユーザー一覧取得
# skip = どこから取得するのか。 limit = 何件取得するのか
def get_users(db: Session, skip: int = 0, limit: int = 100):
  # どこのデータベースの何件目から何件分をすべて返す。
  return db.query(models.User).offset(skip).limit(limit).all()

# 会議室一覧取得
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Room).offset(skip).limit(limit).all()

# 予約一覧取得
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Booking).offset(skip).limit(limit).all()

# ユーザー登録
# fastapi側から userを受け取る
def create_user(db: Session, user: schemas.User):
  # db用のインスタンスを作成
  db_user = models.User(username = user.username)
  # db側に作成したインスタンスを追加
  db.add(db_user)
  # db側にコミットする（反映させる）
  db.commit()
  # dbをリフレッシュする。反映させる。
  db.refresh(db_user)
  return db_user

# 会議室登録
def create_room(db: Session, room: schemas.Room):
  db_room = models.Room(room_name = room.room_name, capacity = room.capacity)
  db.add(db_room)
  db.commit()
  db.refresh(db_room)
  return db_room

# 予約登録
def create_booking(db: Session, booking: schemas.Booking):
  db_booked = db.query(models.Booking).\
    filter(models.Booking.room_id == booking.room_id).\
    filter(models.Booking.end_datetime > booking.start_datetime).\
    filter(models.Booking.start_datetime < booking.end_datetime).\
    all()
  
  if len(db_booked) == 0:
    db_booking = models.Booking(
      user_id = booking.user_id,
      room_id = booking.room_id,
      booked_num = booking.booked_num,
      start_datetime = booking.start_datetime,
      end_datetime = booking.end_datetime,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
  else:
    raise HTTPException(status_code=404, detail="Already booked")

