%define oname	slp

%define	major	1
%define	libname	%mklibname %{oname} %{major}
%define	devname	%mklibname %{oname} -d

Name:		openslp
Version: 	2.0.0
Release:	5
Summary:	OpenSLP implementation of Service Location Protocol V2
License:	BSD-like
Group:		Networking/Other
URL:		http://www.openslp.org/
Source0:	http://prdownloads.sourceforge.net/openslp/%{name}-%{version}.tar.gz
Patch0:		openslp-1.2.1-lsb.patch

%description
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as defined
by RFC 2608 and RFC 2614.  This package include the daemon, libraries, header
files and documentation

%package -n %{libname}
Summary:        OpenSLP implementation of Service Location Protocol V2
Group:          System/Libraries
Obsoletes:	%{_lib}openslp1 < 2.0.0-2

%description -n %{libname}
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as defined
by RFC 2608 and RFC 2614.  This package include the daemon, libraries, header
files and documentation

This package contains the %{libname} runtime library.

%package -n %{devname}
Summary:        Development tools for programs which will use the %{name} library
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       lib%{name}-devel = %{version}-%{release}
Provides:	lib%{oname}-devel = %{version}-%{release}
Obsoletes:	%{_lib}openslp1-devel < 2.0.0-2

%description -n %{devname}
The %{name}-devel package includes the header files and static libraries
necessary for developing programs using the %{name} library.

If you are going to develop programs, you should install %{name}-devel.
You'll also need to have the %{name} package installed.

%prep
%setup -q
%patch0 -p1

%build
autoreconf -fis
%serverbuild
%configure2_5x \
	--disable-static
%make

%install
%makeinstall_std

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/daemons
cat <<EOF  > %{buildroot}/%{_sysconfdir}/sysconfig/daemons/slpd
IDENT=slp
DESCRIPTIVE="SLP Service Agent"
ONBOOT="yes"
EOF

install -m 755 etc/slpd.all_init -D %{buildroot}/%{_initrddir}/slpd

#we don't want these
find %{buildroot} -name "*.la" -delete

%post
%_post_service slpd

%preun
%_preun_service slpd

%files
%doc doc/*
%config(noreplace) %{_sysconfdir}/slp.conf
%config(noreplace) %{_sysconfdir}/slp.reg
%config(noreplace) %{_sysconfdir}/slp.spi
%config(noreplace) %{_sysconfdir}/sysconfig/daemons/slpd
%config(noreplace) %{_initrddir}/slpd
%{_sbindir}/slpd
%{_bindir}/slptool

%files -n %{libname}
%doc AUTHORS COPYING
%{_libdir}/lib%{oname}.so.%{major}
%{_libdir}/lib%{oname}.so.%{major}.*

%files -n %{devname}
%doc ChangeLog COPYING
%{_libdir}/lib%{oname}.so
%{_includedir}/%{oname}.h


