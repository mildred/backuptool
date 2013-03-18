#!.../dopsh
# kate: hl sh

set -x

do-install -p stow

if do-install --any -f /usr/bin/bup -p bup -f /usr/local/bin/bup; then
  :
elif has yum; then
  yum groupinstall -y "Development Tools"
  yum install -y python python-devel fuse-python pyxattr pylibacl perl-Time-HiRes
  do-git-clone git://github.com/bup/bup /usr/local/src/bup
  ( cd /usr/local/src/bup
    git checkout -f master
    make CFLAGS="-werror -Wno-error"
    #make test
    make PREFIX=/usr/local/stow/bup install
    stow -d /usr/local/stow -R bup
    #make DESTDIR=$PWD/root install
    #rm -f bup-*.rpm
    #fpm -s dir -t rpm -C root -n bup -v 0.24b .
    #rpm -ivh bup-*.rpm
  )
fi

if ! has bup; then
  fail "Could not install bup"
fi





