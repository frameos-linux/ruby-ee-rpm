CHROOT=centos-5.5-x86_64
CHROOT_DIR=/var/lib/mock/$CHROOT/root
MOCK_CMD="/usr/bin/mock --disable-plugin ccache"

rm -rf tmp rpms
mkdir tmp
mkdir -p rpms/SRPMS

$MOCK_CMD --init -r  $CHROOT
$MOCK_CMD -r $CHROOT --rebuild ruby-1.8*.src.rpm

cp $CHROOT_DIR/builddir/build/RPMS/*.rpm rpms
cp $CHROOT_DIR/builddir/build/SRPMS/*.rpm rpms/SRPMS/
rm -rf tmp
