"""Local test inbox on localhost:8025: saves each email to outbox/, sends nothing anywhere."""
import time
from pathlib import Path
from aiosmtpd.controller import Controller
OUT = Path(__file__).resolve().parent.parent / "outbox"
class Save:
    async def handle_DATA(self, server, session, envelope):
        f = OUT / f"mail_{len(list(OUT.glob('*.eml'))) + 1}.eml"; f.write_bytes(envelope.content)
        print(f"inbox: mail for {envelope.rcpt_tos[0]} -> {f.name}", flush=True)
        return "250 OK"
Controller(Save(), hostname="localhost", port=8025).start()
print("test inbox on localhost:8025", flush=True)
while True: time.sleep(3600)
