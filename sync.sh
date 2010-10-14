rsync -rtlz . root@rpm-builder:/home/rpmbuilder/ruby/
ssh root@rpm-builder "chown rpmbuilder -R /home/rpmbuilder/ruby/"
