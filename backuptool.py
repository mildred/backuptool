#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from subprocess import Popen, PIPE, STDOUT
from email.mime.text import MIMEText
from time import sleep, time, clock
from getpass import getuser
from socket import getfqdn
import signal
import shlex

import config

class Terminate(Exception): pass

def handle_term(sig, frame):
  raise Terminate()

signal.signal(signal.SIGTERM, handle_term)

def run(cmd, output, stdin=None, cmdname=None, extract_output=False):
  env = config.get("env")
  if env != None:
    for e in env.split("\n"):
      var, val = e.partition("=")
      if os.getenv(var) != val:
        output.append(e)
      os.environ[var]=val
  if not cmdname:
    cmdname = shlex.split(cmd)[0]
  output.append("Running %s: %s" % (cmdname, cmd))
  p = Popen(cmd,
    stdin=(None if stdin == None else PIPE),
    stdout=PIPE,
    stderr=(PIPE if extract_output else STDOUT))
  p.communicate(stdin)
  out = p.stderr if extract_output else p.stdout
  output.extend(["  "+l for l in out.split("\n")])
  output.append("Running %s: exit code %d" % (cmdname, p.returncode))
  if extract_output:
    return p.returncode == 0, p.stdout
  else:
    return p.returncode == 0

def run_command(cmdname, output, stdin=None, extract_output=False):
  cmd = config.get("cmd_%s" % cmdname)
  if cmd:
    return run(cmd, output, stdin, cmdname=cmdname, extract_output=extract_output)
  else:
    output.append("Running %s: (no command)" % cmdname)
    return True

def run_backup(output):
  ok = True
  ok = ok and run_command("pre", output)
  backupdir = config.get("backupdir")
  for element in os.listdir(backupdir):
    elemdir = os.path.join(backupdir, element)
    if element not in [".", ".."] and os.path.isdir(elemdir):
      os.environ["BACKUP_DIR"]  = elemdir
      os.environ["BACKUP_NAME"] = element
      output.append ("Backup %s" % element)
      status, output = run(os.path.join(elemdir, "backup"), extract_output=True)
      ok = ok and status
      if status:
        ok = ok and run_command("index", output, stdin = output)
        ok = ok and run_command("run", output)
      output.append ("Backup for %s finished" % element)
  ok = ok and run_command("run_all", output)
  ok = ok and run_command("post", output)
  return ok

def send_email(subject, body):
  msg = MIMEText(body)
  msg["From"] = "%s@%s" % (getuser(), getfqdn())
  msg["To"] = config.get("contactemail")
  msg["Subject"] = subject
  p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
  p.communicate(msg.as_string())

def warn_failed_too_long(errors):
  send_email("Too long since last backup", errors)

def notice_backup_ok(output):
  send_email("Backup successfull", output)

def ping(host, output):
  if host == None: return True
  t1 = clock()
  ping = Popen(
    ["ping", "-c", "1", host],
    stdout = PIPE,
    stderr = PIPE
  )
  out, err = ping.communicate()
  t2 = clock()
  t = t2 - t1
  if ping.returncode == 0:
    output.append("Ping %s: ok (%.3f %s)" % (host, t / 1000 if t < 1 else t, "ms" if t < 1 else "s"))
    return True
  else:
    output.append("Ping %s: failed: %s" % (host, err.strip()))
    return False

def ping_and_run_backup():
  pinghost = config.get("backuphost")
  output = []

  if not ping(pinghost, output): return False, output
  if not run_backup(output):     return False, output
  return ping(pinghost, output), output

def run_backup_sleep_and_warn(last_ok_backup):
  ok, output = ping_and_run_backup()
  output = "\n".join(output)
  if ok:
    oktime = time()
    notice_backup_ok(output)
    sleep(config.get("waitnewbackup"))
    return oktime
  else:
    sleep(config.get("waitfailedretry"))
    now = time()
    waitwarnfailed = config.get("waitwarnfailed")
    if last_ok_backup + waitwarnfailed < now:
      warn_failed_too_long(output)
      # pretend last ok backup is such as the next warning will be in
      # waitnewbackup time
      return now - waitwarnfailed + config.get("waitnewbackup")
    else:
      return last_ok_backup

try:
  # Attempt backup right away
  last_ok_backup = time() - config.get("waitnewbackup")
  while True:
    last_ok_backup = run_backup_sleep_and_warn(last_ok_backup)
except Terminate:
  print "Terminateed"
