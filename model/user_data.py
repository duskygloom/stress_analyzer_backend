from datetime import datetime, timedelta

from model.database import Database


def mean(l: list[float]) -> float:
    s = sum(l)
    if len(l) == 0:
        return 0
    return s / len(l)


class UserData:
    mood: float
    stress: float
    comment: str
    upload_time: datetime

    def __init__(self, mood: float, stress: float, comment: str) -> None:
        self.mood = mood
        self.stress = stress
        self.comment = comment
        self.upload_time = datetime.now()

    def __str__(self) -> str:
        return f"[{self.upload_time}] Mood: {self.mood} Stress: {self.stress} Comment: {self.comment}"

    def __repr__(self) -> str:
        return self.__str__()


def store_user_data(email: str, mood: float, stress: float, comment: str):
    with Database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "insert into user_data values (?, ?, ?, ?, ?)",
            (email, datetime.now().isoformat(), mood, stress, comment),
        )
        conn.commit()


def fetch_user_data(email: str, date_start: datetime, date_stop: datetime):
    with Database.get_connection() as conn:
        cursor = conn.cursor()
        # group mood and stress trend and daily participation
        cursor.execute(
            "select date(upload_time), avg(mood), avg(stress) "
            "from user_data "
            "where date(upload_time) >= ? and date(upload_time) <= ? and email = ?"
            "group by date(upload_time) "
            "order by date(upload_time)",
            (date_start.strftime("%Y-%m-%d"), date_stop.strftime("%Y-%m-%d"), email),
        )
        result = cursor.fetchall()
        data = {
            "daily": {},
        }
        dt = date_start
        while dt <= date_stop:
            data["daily"][dt.strftime("%Y-%m-%d")] = {
                "avg_mood": 0,
                "avg_stress": 0,
                "ai_mood": 3.0,
                "ai_stress": 3.0,
            }
            dt += timedelta(days=1)
        for r in result:
            k = r[0]
            if k in data["daily"]:
                data["daily"][k]["avg_mood"] = r[1]
                data["daily"][k]["avg_stress"] = r[2]
        return data


def fetch_admin_data(date_start: datetime, date_stop: datetime):
    with Database.get_connection() as conn:
        cursor = conn.cursor()
        # total participants, pilot duration
        cursor.execute(
            "select count(distinct email), min(date(upload_time)) from user_data"
        )
        result = cursor.fetchone()
        total_participants, pilot_start = result
        if pilot_start == None:
            pilot_duration = timedelta(seconds=0)
        else:
            pilot_duration = datetime.now() - datetime.fromisoformat(pilot_start)
        # group mood and stress trend and daily participation
        cursor.execute(
            "select date(upload_time), avg(mood), avg(stress), count(distinct email) "
            "from user_data "
            "where date(upload_time) >= ? and date(upload_time) <= ? "
            "group by date(upload_time) "
            "order by date(upload_time)",
            (date_start.strftime("%Y-%m-%d"), date_stop.strftime("%Y-%m-%d")),
        )
        result = cursor.fetchall()
        data = {
            "total_participants": total_participants,
            "pilot_duration": int(pilot_duration.total_seconds()),
            "daily": {},
        }
        dt = date_start
        while dt <= date_stop:
            data["daily"][dt.strftime("%Y-%m-%d")] = {
                "avg_mood": 0,
                "avg_stress": 0,
                "participation": 0,
            }
            dt += timedelta(days=1)
        for r in result:
            k = r[0]
            if k in data["daily"]:
                data["daily"][k]["avg_mood"] = r[1]
                data["daily"][k]["avg_stress"] = r[2]
                data["daily"][k]["participation"] = r[3]
        return data
