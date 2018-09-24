#!/bin/bash

export DEBEMAIL=james@openastroproject.org
export DEBFULLNAME="James Fidell"

version=`cat version`

srcdir=libasicamera-$version
debdir=debian
debsrc=$debdir/source
quiltconf=$HOME/.quiltrc-dpkg

mkdir $srcdir
cd $srcdir
tar zxf ../libasicamera-$version.tar.gz
chmod -x demo/*.*
chmod -x demo/Makefile
dh_make -y -l -f ../libasicamera-$version.tar.gz

cp ../debfiles/control $debdir
cp ../debfiles/copyright $debdir
cp ../debfiles/changelog $debdir
cp ../debfiles/docs $debdir
cp ../debfiles/watch $debdir
cp ../debfiles/libasicamera.dirs $debdir
cp ../debfiles/libasicamera.links $debdir
cp ../debfiles/libasicamera.install $debdir
cp ../debfiles/libasicamera.symbols $debdir
cp ../debfiles/libasicamera.doc-base $debdir
cp ../debfiles/libasicamera-dev.dirs $debdir
cp ../debfiles/libasicamera-dev.install $debdir
cp ../debfiles/libasicamera-dev.examples $debdir

echo 9 >> $debdir/compat

sed -e '/^.*[ |]configure./a\
        ldconfig\
	udevadm control --reload-rules' < $debdir/postinst.ex > $debdir/postinst
chmod +x $debdir/postinst
sed -e '/^.*[ |]remove./a\
        ldconfig\
	udevadm control --reload-rules' < $debdir/postrm.ex > $debdir/postrm
chmod +x $debdir/postrm
echo "3.0 (quilt)" > $debsrc/format

sed -e "s/DEBVERSION/$version/g" < ../debfiles/rules.overrides >> $debdir/rules

rm $debdir/README.Debian
rm $debdir/README.source
rm $debdir/libasicamera-docs.docs
rm $debdir/libasicamera1.*
rm $debdir/*.[Ee][Xx]


export QUILT_PATCHES="debian/patches"
export QUILT_PATCH_OPTS="--reject-format=unified"
export QUILT_DIFF_ARGS="-p ab --no-timestamps --no-index --color=auto"
export QUILT_REFRESH_ARGS="-p ab --no-timestamps --no-index"
mkdir -p $QUILT_PATCHES

for p in `ls -1 ../debfiles/patches`
do
  quilt --quiltrc=$quiltconf new $p
  for f in `egrep '^\+\+\+' ../debfiles/patches/$p | awk '{ print $2; }'`
  do
    quilt --quiltrc=$quiltconf add $f
  done
pwd
  patch -p0 < ../debfiles/patches/$p
  quilt --quiltrc=$quiltconf refresh
done

dpkg-buildpackage -us -uc

echo "Now run:"
echo
echo "    lintian -i -I --show-overrides libasicamera_$version-1_amd64.changes"
