#!.../dopsh
# kate: hl sh;

do-provision bup
for c in conf/*.do; do
  redo-ifchange ${c%.do}
done

do-getconf mail "$(whoami)@$(hostname -f)"

install -d /etc/backup
install -d /etc/backup.d

for c in conf/*.do; do
  c=${c%.do}
  if [ -e $c ]; then
    install -m644 $c /etc/backup/${c#conf/}
  fi
done

