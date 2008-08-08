Summary: C Library for Amazon S3 Access
Name: libs3
Version: 0.4
Release: 1
License: GPL
Group: Development/Tools
URL: http://sourceforge.net/projects/reallibs3
Source0: libs3-0.4.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
# Want to include curl dependencies, but older Fedora Core uses curl-devel,
# and newer Fedora Core uses libcurl-devel ... have to figure out how to
# handle this problem, but for now, just don't check for any curl libraries
# Buildrequires: curl-devel
Buildrequires: libxml2-devel
Buildrequires: openssl-devel
Buildrequires: make
# Requires: libcurl
Requires: libxml2
Requires: openssl

%define debug_package %{nil}

%description
This library provides an API for using Amazon's S3 service (see
http://s3.amazonaws.com).  Its design goals are:

 - To provide a simple and straightforward API for accessing all of S3's
   functionality
 - To not require the developer using libs3 to need to know anything about:
     - HTTP
     - XML
     - SSL
   In other words, this API is meant to stand on its own, without requiring
   any implicit knowledge of how S3 services are accessed using HTTP
   protocols.
 - To be usable from multithreaded code
 - To be usable by code which wants to process multiple S3 requests
   simultaneously from a single thread
 - To be usable in the simple, straightforward way using sequentialized
   blocking requests

%prep
%setup -q

%build
BUILD=$RPM_BUILD_ROOT/build make exported

%install
BUILD=$RPM_BUILD_ROOT/build DESTDIR=$RPM_BUILD_ROOT/usr make install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/bin/*
/usr/include/*
/usr/lib/*

%changelog
* Tue Aug 05 2008  <bryan@ischo,com> Bryan Ischo
- Initial build.
