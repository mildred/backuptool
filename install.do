: ${DESTDIR:=}
: ${PREFIX:=/usr}
: ${BINDIR:=$PREFIX/bin}
: ${LIBDIR:=$PREFIX/lib/backuptool}

install -d $DESTDIR$BINDIR $DESTDIR$LIBDIR
install -m755 backuptool.py $DESTDIR$LIBDIR/backuptool.py
for py in config.py; do
  install -m644 $py $DESTDIR$LIBDIR/$py
done
ln -sf $LIBDIR/backuptool.py $DESTDIR$BINDIR/backuptool

