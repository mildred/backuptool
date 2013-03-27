: ${DESTDIR:=}
: ${PREFIX:=/usr}
: ${BINDIR:=$PREFIX/bin}
: ${LIBDIR:=$PREFIX/lib}

export BINDIR
redo backuptool.service

install -d $DESTDIR$BINDIR $DESTDIR$LIBDIR/backuptool
install -m755 backuptool.py $DESTDIR$LIBDIR/backuptool/backuptool.py
for py in config.py; do
  install -m644 $py $DESTDIR$LIBDIR/backuptool/$py
done
ln -sf $LIBDIR/backuptool/backuptool.py $DESTDIR$BINDIR/backuptool
install -m644 backuptool.service $DESTDIR$LIBDIR/systemd/system/backuptool.service
