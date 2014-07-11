%define	major	1
%define	libname	%mklibname slp %{major}
%define	devname	%mklibname slp -d

Summary:	OpenSLP implementation of Service Location Protocol V2 
Name:		openslp
Version:	1.2.1
Release:	20
License:	BSD-like
Group:		Networking/Other
Url:		http://www.openslp.org/
Source0:	http://prdownloads.sourceforge.net/openslp/%{name}-%{version}/%{name}-%{version}.tar.bz2
Patch0:		openslp-1.2.1-lsb.patch
Patch1:		openslp-1.2.1-CVE-2012-3609.patch

%description
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as defined 
by RFC 2608 and RFC 2614.  This package include the daemon, libraries, header 
files and documentation

%package -n %{libname}
Summary:	OpenSLP implementation of Service Location Protocol V2
Group:		System/Libraries
Obsoletes:	%{_lib}openslp1 < 1.2.1-14

%description -n %{libname}
This package contains the runtime library for %{name}.

%package -n %{devname}
Summary:	Development tools for programs which will use the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}openslp1-devel < 1.2.1-14

%description -n %{devname}
This package includes the development files for %{name}.

%prep
%setup -q
%apply_patches
rm -rf `find -name CVS`
autoreconf -fis

%build
%serverbuild
%configure2_5x \
	--disable-static \
	--localstatedir=/var
%make

%install
%makeinstall_std
#fix doc
rm -rf installeddoc
mv %{buildroot}%{_prefix}/doc/%{name}-%{version} installeddoc
rm -rf `find installeddoc -name CVS`

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/daemons 
cat <<EOF  > %{buildroot}%{_sysconfdir}/sysconfig/daemons/slpd
IDENT=slp
DESCRIPTIVE="SLP Service Agent"
ONBOOT="yes"
EOF
install -m 755 etc/slpd.all_init -D %{buildroot}%{_initrddir}/slpd

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
%{_libdir}/libslp.so.%{major}*

%files -n %{devname}
%doc ChangeLog COPYING
%{_libdir}/*.so
%{_includedir}/*

