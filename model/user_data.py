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


def fetch_user_data(email: str, time_start: datetime, time_stop: datetime):
    with Database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "select upload_time, mood, stress from user_data where email = ? "
            "and upload_time >= ? and upload_time <= ? "
            "order by upload_time",
            (
                email,
                (time_start - timedelta(days=1)).isoformat(),
                (time_stop + timedelta(days=1)).isoformat(),
            ),
        )
        result = cursor.fetchall()
        data = {}
        dt = time_start
        while dt <= time_stop:
            data[dt.strftime("%Y-%m-%d")] = ([], [])
            dt += timedelta(days=1)
        for r in result:
            k = datetime.fromisoformat(r[0]).strftime("%Y-%m-%d")
            if k in data:
                data[k][0].append(r[1])
                data[k][1].append(r[2])
        for k in data:
            data[k] = (mean(data[k][0]), mean(data[k][1]))
        return data
