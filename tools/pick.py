import os, pty, re, sys, time, select
pid, fd = pty.fork()
if pid == 0:
    os.execvp("zeus", ["zeus", "preview"])
buf = b""
def read(t=1.0):
    global buf
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.2)
        if r:
            try: buf += os.read(fd, 65536)
            except OSError: return False
    return True
while b"Which device" not in buf: read(1)
target = sys.argv[1]
for _ in range(80):
    tail = buf.decode("utf8", "ignore")[-400:]
    m = re.findall(r"❯ ([^\r\n\x1b]+)", tail)
    if m and m[-1].strip() == target: break
    os.write(fd, b"\x1b[B"); read(0.3)
os.write(fd, b"\r")
for _ in range(120):
    if not read(1): break
out = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", buf.decode("utf8", "ignore"))
print(out[out.find("Start building"):][:200]); print(out[out.find("expire"):])
