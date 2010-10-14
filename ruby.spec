# Package Maintainer: Increment phusion_release to match latest release available
%define phusion_release	2010.02

Summary: Ruby Enterprise Edition (Release %{phusion_release})
Name: ruby
Vendor: Phusion.nl
Version: 1.8.7
Release: 1frameos
License: GPL 
Group: Development/Languages 
URL: http://www.rubyenterpriseedition.com/
Source0: ruby-enterprise-%{version}-%{phusion_release}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{phusion_release}-root-%(%{__id_u} -n)
BuildRequires:	readline readline-devel ncurses ncurses-devel gdbm gdbm-devel glibc-devel autoconf gcc unzip openssl-devel db4-devel byacc
BuildRequires: ruby
Provides: ruby(abi) = 1.8
Provides: ruby-irb
Provides: ruby-rdoc
Provides: ruby-libs
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
mkdir -p $RPM_BUILD_ROOT/usr/lib/ruby/gems/1.8/gems
# run installer
./installer -c --enable-shared --auto /usr --dont-install-useful-gems --no-dev-docs --destdir $RPM_BUILD_ROOT

%install
# no-op

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
/usr/bin/*
/usr/lib/*
/usr/share/man/man1/*
%doc source/ChangeLog
%doc source/COPYING
%doc source/LEGAL
%doc source/LGPL
%doc source/NEWS
%doc source/README
%doc source/README.EXT
%doc source/ToDo
# rubygems
%exclude /usr/bin/gem
%exclude /usr/lib/ruby/gems
%exclude /usr/lib/ruby/site_ruby/1.8/rubygems*
%exclude /usr/lib/ruby/site_ruby/1.8/ubygems.rb
%exclude /usr/lib/ruby/site_ruby/1.8/rbconfig

%changelog 
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
