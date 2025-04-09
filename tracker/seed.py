import random
from datetime import datetime, timedelta
import storage


def seed_database(_conn, clients: int, n_entries: int, days: int):
    cursor = _conn.cursor()
    projects = []
    for i in range(clients):
        projects.append(f'Client_{i + 1}')

    now = datetime.now()

    for project in projects:
        for _ in range(n_entries):
            days_back = random.randint(0, days)
            start_hour = random.randint(8, 15)
            start_minute = random.choice([0, 15, 30, 45])
            duration_hours = random.uniform(1, 4)

            clock_in = now - timedelta(days=days_back, hours=(24 - start_hour), minutes=start_minute)
            clock_out = clock_in + timedelta(hours=duration_hours)

            cursor.execute(
                "INSERT INTO sessions (project_name, clock_in, clock_out) VALUES (?, ?, ?)",
                (project, clock_in, clock_out)
            )

    _conn.commit()
    print("Database seeded with test data.")


if __name__ == "__main__":
    conn = storage.get_connection()
    storage.init_db()
    seed_database(conn, clients=6, n_entries=20, days=360)
