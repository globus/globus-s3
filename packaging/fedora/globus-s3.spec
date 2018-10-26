Summary: C Library and Tools for Amazon S3 Access
Name: globus-s3
%global _name %(tr - _ <<< %{name})
%if %{?suse_version}%{!?suse_version:0} >= 1315
%global license LGPL-3.0
%else
%global license LGPL
%endif
%global soname 1
Version:	1.4
Release:	1%{?dist}
License: %{license}
Group: Networking/Utilities
URL: http://github.com/globus/globus-s3
Source0: %{_name}-%{version}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	pkgconfig

%if %{?fedora}%{!?fedora:0} >= 19 || %{?rhel}%{!?rhel:0} >= 7
BuildRequires:  automake >= 1.11
BuildRequires:  autoconf >= 2.60
BuildRequires:  libtool >= 2.2
%endif

%if %{?rhel}%{!?rhel:0} == 5
Buildrequires: curl-devel
%else
Buildrequires: libcurl-devel
%endif

BuildRequires: libxml2-devel

%if %{?suse_version}%{!?suse_version:0} >= 1315
BuildRequires:  openssl
BuildRequires:  libopenssl-devel
%else
BuildRequires:  openssl
BuildRequires:  openssl-devel
%endif

%if %{?rhel}%{!?rhel:0} == 5
Requires: curl
%else
%if %{?suse_version}%{!?suse_version:0} > 0
Requires: libcurl4
%else
Requires: libcurl
%endif
%endif

Requires: libxml2

%if %{?suse_version}%{!?suse_version:0} >= 1315
%global mainpkg lib%{_name}-%{soname}
%global nmainpkg -n %{mainpkg}
%else
%global mainpkg %{name}
%endif

%description
This package is a modified version of libs3 which adds support for
accessing the Ceph Rados Gateway Admin endpoint to access user information.

%if %{?nmainpkg:1}%{!?nmainpkg:0} != 0
%package %{nmainpkg}
Summary:        Library for %{name}
Group:          System Environment/Libraries
%description %{nmainpkg}
This package is a modified version of libs3 which adds support for
accessing the Ceph Rados Gateway Admin endpoint to access user information.
This package includes the development header files and libraries.
%endif

%package devel
Summary: Headers and documentation for %{name}
Group: Development/Libraries
Requires: %{mainpkg} = %{version}-%{release}

%description devel
This package is a modified version of libs3 which adds support for
accessing the Ceph Rados Gateway Admin endpoint to access user information.
This package includes the development header files and libraries.
%prep

%setup -q -n %{_name}-%{version}

%build
%if %{?fedora}%{!?fedora:0} >= 19 || %{?rhel}%{!?rhel:0} >= 7
# Remove files that should be replaced during bootstrap
rm -rf autom4te.cache

autoreconf -if
%endif

%configure \
           --disable-static \
           --docdir=%{_docdir}/%{name}-%{version} \
           --includedir=%{_includedir}/globus/%{name} \
           --datadir=%{_datadir}/globus \
           --libexecdir=%{_datadir}/globus

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libtool archives (.la files)
find $RPM_BUILD_ROOT%{_libdir} -name 'lib*.la' -exec rm -v '{}' \;

# Remove the s3 executable which is not needed
rm -f $RPM_BUILD_ROOT%{_bindir}/s3

%clean
rm -rf $RPM_BUILD_ROOT

%post %{?nmainpkg} -p /sbin/ldconfig

%postun %{?nmainpkg} -p /sbin/ldconfig

%files %{?nmainpkg}
%defattr(-,root,root,-)
%{_libdir}/libglobus_s3.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/globus
%dir %{_includedir}/globus/%{name}
%{_includedir}/globus/%{name}/*.h
%{_libdir}/libglobus_s3.so
%{_libdir}/pkgconfig/globus-s3.pc

%changelog
* Thu Nov 01 2018 Globus Toolkit <support@globus.org> - 1.4-1 
- Make anonymous requests when credentials aren't available (closes #2)
- Add GLOBUS_LIBS3_DEBUG_FILE env var to capture curl debug

* Fri Jun 22 2018 Globus Toolkit <support@globus.org> - 1.3-1
- add GLOBUS_S3_GOOGLE_CLOUD env to disable encoding-type query param

* Tue Apr 10 2018 Globus Toolkit <support@globus.org> - 1.2-1
- recognize SSE-KMS encryption

* Tue Mar 13 2018 Globus Toolkit <support@globus.org> - 1.1-2
- fix versioning in build files
- pull in 4.1 upstream changes
- adds support for V4 signatures

* Wed Apr 19 2017 Globus Toolkit <support@globus.org> - 0.4-1
- Don't set expires header when S3PutProperties.expires == 0

* Thu Oct 13 2016 Globus Toolkit <support@globus.org> - 0.3-5
- SLES 12 packaging updates

* Thu May 12 2016 Globus Toolkit <support@globus.org> - 0.3-1
- Handle '+' -> ' ' conversion in url encoding

* Thu May 12 2016 Globus Toolkit <support@globus.org> - 0.2-1
- Set encoding-type=url in bucket list operation

* Thu May 05 2016 Globus Toolkit <support@globus.org> - 0.1-1
- Address xml parsing error for prefixes

* Tue Feb 23 2016 Globus Toolkit <support@globus.org> - 0.0-3
- Adjust some dependencies for SLES 11SP3

* Tue Feb 23 2016 Globus Toolkit <support@globus.org> - 0.0-2
- Adjust some dependencies for older centos

* Fri Feb 19 2016  <bester@mcs.anl.gov> Joseph Bester - 0.0-1
- Based on Bryan Ischo's libs3 with radosgw modifications

* Sat Aug 09 2008  <bryan@ischo,com> Bryan Ischo
- Split into regular and devel packages.

* Tue Aug 05 2008  <bryan@ischo,com> Bryan Ischo
- Initial build.
