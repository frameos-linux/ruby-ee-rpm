# Package Maintainer: Increment phusion_release to match latest release available
%define phusion_release	2011.03
%define rubyver		1.8.7
%define rubyxver	1.8

%define _prefix         /opt/ruby-ee
%{!?ruby_prefix:        %global ruby_prefix     /opt/ruby-ee}
%{!?ruby_vendorlib:     %global ruby_vendorlib  %{ruby_prefix}/lib/ruby}
%{!?ruby_vendorarch:    %global ruby_vendorarch %{ruby_vendorlib}}
%{!?ruby_sitelib:       %global ruby_sitelib    %{ruby_vendorlib}/site_ruby}
%{!?ruby_sitearch:      %global ruby_sitearch   %{ruby_vendorarch}/site_ruby}


Summary: Ruby Enterprise Edition (Release %{phusion_release})
Name: ruby-ee
Vendor: Phusion.nl
Version: 1.8.7
Release: 9.%{phusion_release}%{?dist}
License: GPL 
Group: Development/Languages 
URL: http://www.rubyenterpriseedition.com/
Source0: http://rubyenterpriseedition.googlecode.com/files/ruby-enterprise-%{version}-%{phusion_release}.tar.gz
Source1: ruby-ee.sh
Source2: ruby-ee.conf
BuildRoot: %{_tmppath}/ruby-%{version}-%{phusion_release}-root-%(%{__id_u} -n)
BuildRequires:	readline readline-devel ncurses ncurses-devel gdbm gdbm-devel glibc-devel autoconf gcc unzip openssl-devel db4-devel byacc
BuildRequires: ruby
BuildRequires: gcc-c++
BuildRequires: make
Provides: ruby(abi) = 1.8

%description 
Ruby Enterprise Edition is a server-oriented friendly branch of Ruby which includes various enhancements:
* A copy-on-write friendly garbage collector. Phusion Passenger uses this, in combination with a technique called preforking, to reduce Ruby on Rails applications' memory usage by 33% on average.
* An improved memory allocator called tcmalloc, which improves performance quite a bit.
* The ability to tweak garbage collector settings for maximum server performance, and the ability to inspect the garbage collector's state. (RailsBench GC patch)
* The ability to dump stack traces for all running threads (caller_for_all_threads), making it easier for one to debug multithreaded Ruby web applications.

%prep 
%setup -q -n ruby-enterprise-%{version}-%{phusion_release}

%build 
cd source
%{__patch} -p1 -R < ../fast-threading.patch
%configure \
  --prefix=%{ruby_prefix} \
  --exec-prefix=%{ruby_prefix} \
  --with-default-kcode=none \
  --enable-shared \
  --enable-pthread \
  --disable-rpath \
  --program-suffix='-ree' \
  --with-readline-include=%{_includedir}/readline5 \
  --with-readline-lib=%{_libdir}/readline5 \
  --with-sitedir='%{ruby_sitelib}' \
  --with-sitearchdir='%{ruby_sitearch}' \
  --with-vendordir='%{ruby_vendorlib}' \
  --with-vendorarchdir='%{ruby_vendorarch}'

%{__make} %{?_smp_mflags} CFLAGS="%{optflags} -fPIC -fno-strict-aliasing -g -D__LINUX__ -D_GNU_SOURCE -D_LARGEFILE64_SOURCE"

%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/
%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d/
cd source
%{__make} DESTDIR=$RPM_BUILD_ROOT install 
%{__cp} *.h $RPM_BUILD_ROOT/%{ruby_vendorarch}/%{rubyxver}/
%{__install} -m 0755 %{SOURCE1} %{buildroot}/%{_sysconfdir}/profile.d/
%{__cp} %{SOURCE2} %{buildroot}/%{_sysconfdir}/ld.so.conf.d/


%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig

%files 
%defattr(-,root,root)
/usr/share/man/man1/*
%{ruby_prefix}/*
%{_sysconfdir}/profile.d/ruby-ee.sh
%{_sysconfdir}/ld.so.conf.d/ruby-ee.conf

%doc source/ChangeLog
%doc source/COPYING
%doc source/LEGAL
%doc source/LGPL
%doc source/NEWS
%doc source/README
%doc source/README.EXT
%doc source/ToDo

%changelog
* Wed Jul 27 2011 Sergio Rubio <rubiojr@frameos.org> - 1.8.7-9.2011.03
- ruby-ee installs to /opt now and is parallel instalable with system ruby

* Mon Apr 11 2011 Sergio Rubio <rubiojr@frameos.org> - 1.8.7-8.2011.03.frameos
- Back to ruby-ee

* Fri Apr 01 2011 Sergio Rubio <rubiojr@frameos.org> - 1.8.7-7.2011.03.frameos
- obsoletes ruby-ee

* Thu Feb 24 2011 Sergio Rubio <rubiojr@frameos.org> ruby-1.8.7-6.2011.03.frameos
- updated to upstream 2011.03

* Thu Nov 05 2010 Sergio Rubio <rubiojr@frameos.org> ruby-1.8.7-5.frameos
- do not use installer script
- define some ruby macros
- tcmalloc no longer used
- renamed to ruby-ee

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
