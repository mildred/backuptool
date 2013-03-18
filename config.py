import os

from getpass import getuser
from socket import getfqdn

confdir="/etc/backup"

minute = 60
hour = 60 * minute
day = 24 * hour
week = 7 * day

defaultconf = {
  "env": None,
  "waitnewbackup": day,
  "waitfailedretry": minute,
  "waitwarnfailed": 3 * day,
  "backuphost": None,
  "contactemail": "%s@%s" % (getuser(), getfqdn()),
  "backupdir": "/etc/bakup.d",
  #"cmd_index": "xargs bup index",
  #"cmd_run": "bup save -n $BACKUP_NAME",
}

def get(name):
  fname = os.path.join(confdir, name)
  try:
    with open(fname, "r") as f:
      content = f.read().strip()
      if len(content) == 0:
        return None
      elif name in defaultconf and isinstance(defaultconf[name], int):
        num = content[0:-1]
        unit = content[-1]
        if unit == "s": return int(num)
        if unit == "m": return int(num) * minute
        if unit == "h": return int(num) * hour
        if unit == "d": return int(num) * day
        if unit == "w": return int(num) * week
        return int(content)
      else:
        return content
  except IOError:
    if name in defaultconf:
      return defaultconf[name]
    else:
      return None
