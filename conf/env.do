#!.../dopsh
# kate: hl sh;

do-getconf mountpoint /run/backup/mnt/
echo "BUP_DIR=$mountpoint" >$3
