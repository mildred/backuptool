#!.../dopsh
# kate: hl sh

if ! [ -e /usr/local/stow/bup ] && do-install --any -f /usr/bin/bup -p bup -f /usr/local/bin/bup; then
  :
else
  #yum groupinstall -y "Development Tools"
  do-install -p stow -p pandoc -p gcc
  do-install -p python -p python-devel -p fuse-python -p pyxattr -p pylibacl #-p perl-Time-HiRes
  do-git-clone git://github.com/bup/bup /usr/local/src/bup
  pushd /usr/local/src/bup
  git checkout -f master
  make CFLAGS="-Wno-error"
  make PREFIX=/usr/local/stow/bup install
  stow -d /usr/local/stow -R bup
  popd
fi

if ! has bup; then
  fail "Could not install bup"
fi





