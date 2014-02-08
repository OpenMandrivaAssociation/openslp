%define	name	openslp
%define	version	1.2.1

%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	libname_devel	%mklibname %{name} %{major} -d

Name:		%name
Version: 	%version
Release:	14
Summary:	OpenSLP implementation of Service Location Protocol V2 
License:	BSD-like
Group:		Networking/Other
URL:		http://www.openslp.org/
BuildRoot:	%{_tmppath}/%{name}-root
Source0:	http://prdownloads.sourceforge.net/openslp/%{name}-%{version}/%{name}-%{version}.tar.bz2
Patch0:		openslp-1.2.1-lsb.patch
Patch1:		openslp-1.2.1-CVE-2012-3609.patch

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
%patch1 -p1
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



%changelog
* Mon Aug 27 2012 Danila Leontiev <danila.leontiev@rosalab.ru> 1.2.1-13
- Fix CVE-2012-3609

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-12mdv2011.0
+ Revision: 666965
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-11mdv2011.0
+ Revision: 607022
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-10mdv2010.1
+ Revision: 521155
- rebuilt for 2010.1

* Thu Aug 13 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.2.1-9mdv2010.0
+ Revision: 416036
- Updated initscript to be LSB-compliant.

* Sat Jun 28 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-8mdv2009.0
+ Revision: 229844
- fix build
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-6mdv2008.1
+ Revision: 179111
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Jun 22 2007 Andreas Hasenack <andreas@mandriva.com> 1.2.1-5mdv2008.0
+ Revision: 43264
- rebuild with new serverbuild macro (-fstack-protector)

* Wed May 02 2007 Adam Williamson <awilliamson@mandriva.org> 1.2.1-4mdv2008.0
+ Revision: 20361
- rebuild for new era, drop useless Requires


* Fri Nov 18 2005 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-3mdk
- rebuilt against openssl-0.9.8a

* Thu Nov 17 2005 Laurent MONTEL <lmontel@mandriva.com> 1.2.1-2mdk
- Rebuild

* Thu Oct 06 2005 Austin Acton <austin@mandriva.org> 1.2.1-1mdk
- New release 1.2.1
- fix source URL

* Wed Mar 23 2005 Olivier Blin <oblin@mandrakesoft.com> 1.0.11-6mdk
- from Vincent Danen <vdanen@mandrakesoft.com>:
  o security fix based on SUSE's audit

* Wed Nov 19 2003 Stefan van der Eijk <stefan@eijk.nu> 1.0.11-5mdk
- rebuild 4 reupload (alpha)

* Tue Jul 15 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.11-4mdk
- Fix log directory

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.11-3mdk
- Rebuild

* Thu Jun 26 2003 Till Kamppeter <till@mandrakesoft.com> 1.0.11-2mdk
- Let the SLP library not require the daemon package, once, the daemon
  can run on a remote machine and second, a program (as CUPS) can be linked
  against libslp, but most users have the SLP functionality turned off. So
  they do not want to get a new daemon pulled in and started by urpmi.
- Added a "Requires:" to tell that openslp needs libslp (one can see this
  necessity by applying "rpm -qR" to openslp.
- Removed "Packager:" tag.

* Wed Jun 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.0.11-1mdk
- 1.0.11
- use %%mklibname macro
- rm -rf $RPM_BUILD_ROOT in %%install
- cosmetics
- fix docs and permissions
- macroize

* Fri Jan 10 2003 Yves Duret <yves@zarb.org> 1.0.10-1mdk
- first mandrake version

* Wed Feb 06 2002 alain.richard@equation.fr
Adapted to enable build under redhat 7.x (uses BuildRoot macro,
	install instead of installtool for non libraries objects,
	protected rm -r for install & clean)

* Wed Jun 13 2001 matt@caldera.com
Removed server stuff.  We want on binary rpm again

* Mon Jul 17 2000 mpeterson@calderasystems.com
Added lisa stuff

* Fri Jul 07 2000 david.mccormack@ottawa.com
Made it work with the new autoconf/automake scripts.

* Thu Apr 27 2000 mpeterson
started

