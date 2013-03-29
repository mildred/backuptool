#!.../dopsh
# kate: hl sh;

if ! has sendmail; then
  fail "Please install sendmail"
fi

redo install

export DOPS_MYCONF

do-provision bup

install -d /etc/backup
install -d /etc/backup.d

for c in backuphost cmd_index cmd_post cmd_pre cmd_run contactemail env test; do
  redo "conf/$c.conf"
  if [ -e "conf/$c.conf" ]; then
    install -m644 "conf/$c.conf" "/etc/backup/$c"
  fi
done

if has systemctl; then
  redo-exec systemctl enable backuptool.service
  redo-exec systemctl restart backuptool.service
else
  fail "Not available on systems without systemd"
fi

