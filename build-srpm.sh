BASEDIR=~/rpmbuilder
cp ruby-enterprise*.tar.gz $BASEDIR/SOURCES/
cp ruby.spec $BASEDIR/SPECS/
rpmbuild -bs $BASEDIR/SPECS/ruby.spec
