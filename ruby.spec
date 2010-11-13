# Package Maintainer: Increment phusion_release to match latest release available
%define phusion_release	2010.02
%define rubyver         1.8.7
%define rubyxver        1.8

%{!?ruby_vendorlib:     %global ruby_vendorlib  %{_prefix}/lib/ruby}
%{!?ruby_vendorarch:    %global ruby_vendorarch %{_libdir}/ruby}
%{!?ruby_sitelib:       %global ruby_sitelib    %{ruby_vendorlib}/site_ruby}
%{!?ruby_sitearch:      %global ruby_sitearch   %{ruby_vendorarch}/site_ruby}


Summary: Ruby Enterprise Edition (Release %{phusion_release})
Name: ruby-ee
Vendor: Phusion.nl
Version: 1.8.7
Release: 5.frameos
License: GPL 
Group: Development/Languages 
URL: http://www.rubyenterpriseedition.com/
Source0: ruby-enterprise-%{version}-%{phusion_release}.tar.gz
BuildRoot: %{_tmppath}/ruby-%{version}-%{phusion_release}-root-%(%{__id_u} -n)
BuildRequires:	readline readline-devel ncurses ncurses-devel gdbm gdbm-devel glibc-devel autoconf gcc unzip openssl-devel db4-devel byacc
BuildRequires: ruby
BuildRequires: gcc-c++
BuildRequires: make
Provides: ruby(abi) = 1.8
Provides: ruby-irb
Provides: ruby-rdoc
Provides: ruby-libs
Provides: ruby-devel
Obsoletes: ruby
Obsoletes: ruby-libs
Obsoletes: ruby-irb
Obsoletes: ruby-rdoc
Obsoletes: ruby-devel

%description 
Ruby Enterprise Edition is a server-oriented friendly branch of Ruby which includes various enhancements:
* A copy-on-write friendly garbage collector. Phusion Passenger uses this, in combination with a technique called preforking, to reduce Ruby on Rails applications' memory usage by 33% on average.
* An improved memory allocator called tcmalloc, which improves performance quite a bit.
* The ability to tweak garbage collector settings for maximum server performance, and the ability to inspect the garbage collector's state. (RailsBench GC patch)
* The ability to dump stack traces for all running threads (caller_for_all_threads), making it easier for one to debug multithreaded Ruby web applications.

%prep 
%setup -q -n ruby-enterprise-%{version}-%{phusion_release}

%build 
# work around bug in "installer"
#mkdir -p $RPM_BUILD_ROOT/usr/lib/ruby/gems/1.8/gems
## run installer
#./installer -c --enable-shared --auto $RPM_BUILD_ROOT --dont-install-useful-gems --no-dev-docs --destdir $RPM_BUILD_ROOT
#

cd source
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -g -02"
export CFLAGS
patch -p1 -R < ../fast-threading.patch
%configure \
  --with-default-kcode=none \
  --enable-shared \
  --enable-pthread \
  --disable-rpath \
  --with-readline-include=%{_includedir}/readline5 \
  --with-readline-lib=%{_libdir}/readline5 \
  --with-sitedir='%{ruby_sitelib}' \
  --with-sitearchdir='%{ruby_sitearch}' \
  --with-vendordir='%{ruby_vendorlib}' \
  --with-vendorarchdir='%{ruby_vendorarch}'

make

%install
cd source
make DESTDIR=$RPM_BUILD_ROOT \
  install
cp *.h $RPM_BUILD_ROOT/%{ruby_vendorarch}/%{rubyxver}/

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
/usr/bin/*
/usr/lib64/*
/usr/share/man/man1/*
%{ruby_vendorarch}/%{rubyxver}/*.h

%doc source/ChangeLog
%doc source/COPYING
%doc source/LEGAL
%doc source/LGPL
%doc source/NEWS
%doc source/README
%doc source/README.EXT
%doc source/ToDo

%changelog 
* Thu Nov 05 2010 Sergio Rubio <rubiojr@frameos.org> ruby-1.8.7-5.frameos
- do not use installer script
- define some ruby macros

* Thu Nov 05 2010 Sergio Rubio <rubiojr@frameos.org> ruby-1.8.7-4.frameos
- Obsoletes ruby-devel
- Provides ruby-devel

* Thu Nov 04 2010 Sergio Rubio <rubiojr@frameos.org> ruby-1.8.7-3.frameos
- Obsoletes ruby-irb ruby-rdoc
- Build requires make gcc-c++

* Thu Nov 03 2010 Sergio Rubio <rubiojr@frameos.org> ruby-1.8.7-2.frameos
- Obsoletes ruby-libs

* Tue Jun 15 2010 Sergio Rubio <rubiojr@frameos.org>
- Updated to 2010.02
- Install to /usr
- Replace RHEL/CentOS ruby package
- Remove rubygems

* Mon Apr 19 2010 End Point Corporation <hosting@endpoint.com>
- Updated for release 2010.01
- Updated rubygems to 1.3.6

* Wed Dec 02 2009 Adam Vollrath <adam@endpoint.com>
- Updated for release 2009.10

* Wed Oct 07 2009 Adam Vollrath and Richard Templet <hosting@endpoint.com>
- Updated for release 20090928

* Wed Jun 10 2009 Adam Vollrath <adam@endpoint.com>
- Updated for release 20090610

* Tue Jun 02 2009 Adam Vollrath <adam@endpoint.com>
- Added check for existing /usr/local/bin/gem
- Added LICENSE and other important document files

* Mon Jun 01 2009 Adam Vollrath <adam@endpoint.com>
- Refactored to use Phusion's installer instead of building from source
- Changed prefix to just /usr/local
- Added check for existing /usr/local/bin/ruby
- Split rubygems into a subpackage

* Sat May 30 2009 Adam Vollrath <adam@endpoint.com>
- Changed Release number convention
- Added tcmalloc support and `make test`

* Tue May 26 2009 Adam Vollrath <adam@endpoint.com>
- Updated for 1.8.6-20090520
- Several small improvements to spec file

* Fri Dec 13 2008 Tim C. Harper <tim.harper@leadmediapartners.com>
- first build of REE package
