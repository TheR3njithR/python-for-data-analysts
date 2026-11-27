"""Is the saved Kite Connect token still valid?
Docs: access_token expires 6 AM next day."""
import json, sys
from datetime import datetime, time, timedelta


def expiry(login):
    six = datetime.combine(login.date(), time(6))
    return six if login < six else six + timedelta(1)


s = json.load(open("session.json"))
login = datetime.fromisoformat(s["login_time"])
now = datetime.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.now()
exp = expiry(login)
print(f"logged in: {login:%a %d %b %H:%M}  expires: {exp:%a %d %b %H:%M}")
print("token OK" if now < exp else "EXPIRED: log in again, save the new token")
