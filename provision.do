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

for c in conf/*.do; do
  c="${c%.do}"
  redo "$c"
  if [ -e $c ]; then
    install -m644 "$c" "/etc/backup/${c#conf/}"
  fi
done

if has systemctl; then
  redo-exec systemctl enable backuptool.service
  redo-exec systemctl restart backuptool.service
else
  fail "Not available on systems without systemd"
fi

