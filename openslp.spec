%define	name	openslp
%define	version	1.2.1

%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	libname_devel	%mklibname %{name} %{major} -d

Name:		%name
Version: 	%version
Release:	%mkrel 10
Summary:	OpenSLP implementation of Service Location Protocol V2 
License:	BSD-like
Group:		Networking/Other
URL:		http://www.openslp.org/
BuildRoot:	%{_tmppath}/%{name}-root
Source0:	http://prdownloads.sourceforge.net/openslp/%{name}-%{version}/%{name}-%{version}.tar.bz2
Patch0:		openslp-1.2.1-lsb.patch

%Description
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

%description -n %{libname}
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as defined
by RFC 2608 and RFC 2614.  This package include the daemon, libraries, header
files and documentation

This package contains the %libname runtime library.

%package -n %{libname_devel}
Summary:        Development tools for programs which will use the %{name} library
Group:          Development/C
Requires:       %{libname} = %version
Provides:       %{name}-devel = %version-%release
Provides:       lib%{name}-devel = %version-%release

%description -n %{libname_devel}
The %{name}-devel package includes the header files and static libraries
necessary for developing programs using the %{name} library.

If you are going to develop programs, you should install %{name}-devel.  
You'll also need to have the %{name} package installed.


%prep
%setup -q
%patch0 -p1
rm -rf `find -name CVS`

%build
autoreconf -fis
%serverbuild
%configure --localstatedir=/var
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
#fix doc
rm -rf installeddoc
mv %buildroot/%_prefix/doc/%{name}-%{version} installeddoc
rm -rf `find installeddoc -name CVS`

mkdir -p %buildroot/%_sysconfdir/sysconfig/daemons 
cat <<EOF  > %buildroot/%_sysconfdir/sysconfig/daemons/slpd
IDENT=slp
DESCRIPTIVE="SLP Service Agent"
ONBOOT="yes"
EOF
install -m 755 etc/slpd.all_init -D %buildroot/%_initrddir/slpd

%clean
rm -rf %buildroot

%post
%_post_service slpd

%preun 
%_preun_service slpd

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(644,root,root,755)
%doc doc/*
%config(noreplace) %_sysconfdir/slp.conf
%config(noreplace) %_sysconfdir/slp.reg
%config(noreplace) %_sysconfdir/slp.spi
%config(noreplace) %_sysconfdir/sysconfig/daemons/slpd
%defattr(755,root,root,755)
%config(noreplace) %_initrddir/slpd
%_sbindir/slpd
%_bindir/slptool

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING
%_libdir/*.so.*

%files -n %{libname_devel}
%defattr(-,root,root)
%doc ChangeLog COPYING
%_libdir/*a
%_libdir/*.so
%_includedir/*

