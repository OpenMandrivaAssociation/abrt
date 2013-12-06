# (blino) FIXME: switch back to 1 when systemd is installable
%define with_systemd 1

%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}

%define lib_name_devel %mklibname %{name} -d
%define lib_report_devel %mklibname report -d

Summary:	Automatic bug detection and reporting tool
Name:		abrt
Version:	2.0.10
Release:	5
License:	GPLv2+
Group:		System/Libraries
URL:		https://fedorahosted.org/abrt/
Source0:	https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.gz
Source1:	abrt.init
Source2:	00abrt.sh
Source3:	00abrt.csh
Source4:	abrt-debuginfo-install
Source5:	abrt-ccpp.init
Source6:	abrt-oops.init
Patch0:		abrt-2.0.8-format_security.patch
# (fc) disable package signature check
Patch2:		abrt_disable_gpgcheck.diff
# (pt) generate stacktrace twice to get missing -debug packages
#Patch5: abrt-1.1.14-debug.patch
# (fc) disable nspluginwrapper-i386 (Mdv bug #59237)
Patch7:		abrt-2.0.2-nspluginwrapper.patch
Patch8:		abrt-2.0.8-nonutf8-locale.patch
Patch10:	abrt-2.0.8-link-against-libreport.patch
# (proyvind): port to rpm5 api
Patch11:	abrt-2.0.8-rpm5.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	dbus-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	curl-devel
BuildRequires:	rpm-devel
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	desktop-file-utils
#BuildRequires: nss-devel
BuildRequires:	libnotify-devel
BuildRequires:	xmlrpc-c-devel
BuildRequires:	xmlrpc-c
#BuildRequires: file-devel
BuildRequires:	python-devel
BuildRequires:	gettext
BuildRequires:	polkit-1-devel
BuildRequires:	libzip-devel, libtar-devel, bzip2-devel, zlib-devel
BuildRequires:	intltool
BuildRequires:	pkgconfig(btparser) => 0.16
BuildRequires:	pkgconfig(libreport) => 2.0.9
BuildRequires:	pkgconfig(libreport-gtk) => 2.0.9
BuildRequires:	gnome-common
BuildRequires:	bison
BuildRequires:	asciidoc
BuildRequires:	docbook-style-xsl
BuildRequires:	xmlto
BuildRequires:	libgnome-keyring-devel
BuildRequires:	gettext-devel
%if %{?with_systemd}
BuildRequires:	systemd-units
%endif
Requires:	%{lib_name} >= %{version}-%{release}
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Obsoletes:	abrt-plugin-catcut < 1.1.13
Obsoletes:	abrt-plugin-sqlite3 < 1.1.18
# required for transition from 1.1.13, can be removed after some time
Obsoletes:	abrt-plugin-runapp < 1.1.18
Obsoletes:	abrt-plugin-filetransfer < 1.1.18
Obsoletes:	abrt-plugin-sosreport < 1.1.18
BuildConflicts:	%{mklibname abrt 0} %{mklibname abrt -d} abrt

%description
%{name} is a tool to help users to detect defects in applications and
to create a bug report with all informations needed by maintainer to fix it.
It uses plugin system to extend its functionality.

%package -n %{lib_name}
Summary:	Libraries for %{name}
Group:		System/Libraries

%description -n %{lib_name}
Libraries for %{name}.

%package -n %{lib_name_devel}
Summary:	Development libraries for %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Requires:	abrt = %{version}-%{release}

%description -n %{lib_name_devel}
Development libraries and headers for %{name}.

%package gui
Summary:	%{name}'s gui
Group:		Graphical desktop/Other
Requires:	%{name} = %{version}-%{release}
Requires:	python-dbus
Requires:	pygtk2.0
Requires:	pygtk2.0-libglade
Requires:	python-gobject
##Requires: gnome-python-desktop
Requires:	libreport-gtk

%description gui
GTK+ wizard for convenient bug reporting.

%package addon-ccpp
Summary:	%{name}'s C/C++ addon
Group:		System/Libraries
Requires:	elfutils
Requires:	%{name} = %{version}-%{release}

%description addon-ccpp
This package contains hook for C/C++ crashed programs and %{name}'s C/C++
analyzer plugin.

%package addon-kerneloops
Summary:	%{name}'s kerneloops addon
Group:		System/Libraries
Requires:	curl
Requires:	%{name} = %{version}-%{release}
#Obsoletes: kerneloops

%description addon-kerneloops
This package contains plugin for collecting kernel crash information
and reporter plugin which sends this information to specified server,
usually to kerneloops.org.

%package addon-vmcore
Summary:	%{name}'s vmcore addon
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	abrt-addon-kerneloops

%description addon-vmcore
This package contains plugin for collecting kernel crash information from
vmcore files.

%package addon-python
Summary:	%{name}'s addon for catching and analyzing Python exceptions
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description addon-python
This package contains python hook and python analyzer plugin for handling
uncaught exception in python programs.

%package cli
Summary:	%{name}'s command line interface
Group:		Graphical desktop/Other
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-addon-kerneloops
Requires:	%{name}-addon-ccpp
Requires:	%{name}-addon-python

%description cli
This package contains simple command line client for controlling abrt 
daemon over the sockets.

%package desktop
Summary:	Virtual package that installs all necessary packages
Group:		Graphical desktop/Other
# This package gets installed when anything requests bug-buddy -
# happens when users upgrade Fn to Fn+1;
# or if user just wants "typical desktop installation".
# Installing abrt-desktop should result in the abrt which works without
# any tweaking in abrt.conf (IOW: all plugins mentioned there must be installed)
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-addon-kerneloops
Requires:	%{name}-addon-vmcore
Requires:	%{name}-addon-ccpp
Requires:	%{name}-addon-python
# Default config of addon-ccpp requires gdb
Requires:	gdb >= 7.0-3
Requires:	%{name}-gui
#Obsoletes: bug-buddy
#Provides: bug-buddy

%description desktop
Virtual package to make easy default installation on desktop environments.

%if 0
%package retrace-server
Summary:	%{name}'s retrace server using HTTP protocol
Group:		Graphical desktop/Other
Requires:	abrt-addon-ccpp
Requires:	gdb >= 7.0-3
Requires:	apache-mod_wsgi
Requires:	apache-mod_ssl
Requires:	python-webob
Requires:	mock
Requires:	xz
Requires:	elfutils
Requires:	createrepo
Requires(preun):	/sbin/install-info
Requires(post):	/sbin/install-info

%description retrace-server
The retrace server provides a coredump analysis and backtrace
generation service over a network using HTTP protocol.
%endif

%package addon-xorg
Summary:	%{name}'s Xorg addon
Group:		System/Libraries
Requires:	curl
Requires:	%{name} = %{version}-%{release}

%description addon-xorg
This package contains plugin for collecting Xorg crash information 
from Xorg log.

%prep

%setup -q
%apply_patches
# (tv)) disable -Werror:
perl -pi -e 's!-Werror!-Wno-deprecated!' configure{.ac,} */*/Makefile*

%build
NOCONFIGURE=yes gnome-autogen.sh
%define Werror_cflags %nil

%configure2_5x \
%if !%{with_systemd}
    --without-systemdsystemunitdir \
%endif
%if %{with_systemd}
    --with-systemdsystemunitdir=/lib/systemd/system \
%endif
    --disable-rpath \
    --enable-gtk3

%make

%install

%makeinstall_std
%find_lang %{name}

# remove all .la and .a files
find %{buildroot} -name '*.la' -or -name '*.a' | xargs rm -f
%if !%{with_systemd}
mkdir -p %{buildroot}/%{_initrddir}
install -m 755 %SOURCE1 %{buildroot}/%{_initrddir}/%{name}d
install -m 755 %SOURCE5 %{buildroot}/%{_initrddir}/%{name}-ccpp
install -m 755 %SOURCE6 %{buildroot}/%{_initrddir}/%{name}-oops
sed -i 's!@libexec@!%_libdir!' %{buildroot}/%{_initrddir}/%{name}-ccpp
%endif
mkdir -p %{buildroot}/var/cache/%{name}-di
mkdir -p %{buildroot}/var/run/%{name}
mkdir -p %{buildroot}/var/spool/%{name}
mkdir -p %{buildroot}/var/spool/%{name}-retrace
mkdir -p %{buildroot}/var/cache/%{name}-retrace
mkdir -p %{buildroot}/var/log/%{name}-retrace
mkdir -p %{buildroot}/var/spool/%{name}-upload

# remove fedora gpg key
rm -f %{buildroot}%{_sysconfdir}/abrt/gpg_keys
touch %{buildroot}%{_sysconfdir}/abrt/gpg_keys

touch %buildroot/var/run/abrt/abrt.socket
touch %buildroot/var/run/abrtd.pid

# install ulimit disabler
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
install -m0644 %SOURCE2 %SOURCE3 %{buildroot}%{_sysconfdir}/profile.d/

desktop-file-install \
        --dir %{buildroot}%{_sysconfdir}/xdg/autostart \
        src/applet/%{name}-applet.desktop

# replace with our own version
cat %{SOURCE4} > %{buildroot}/usr/bin/%{name}-debuginfo-install

#remove RH specific plugins
rm -f %{buildroot}%{_libdir}/%{name}/{RHTSupport.glade,libRHTSupport.so}
rm -f %{buildroot}%{_sysconfdir}/%{name}/plugins/RHTSupport.conf
rm -f %{buildroot}%{_sysconfdir}/%{name}/events.d/rhtsupport_events.conf
rm -f %{buildroot}%{_sysconfdir}/%{name}/events/report_RHTSupport.xml
rm -f %{buildroot}%{_bindir}/%{name}-action-rhtsupport

# After everything is installed, remove info dir
rm -f %{buildroot}%{_infodir}/dir

%pre
%_pre_useradd %{name} %{_sysconfdir}/%{name} /bin/nologin
%_pre_groupadd %{name} %{name}

%post
if [ $1 -eq 1 ]; then
%if %{with systemd}
    # Enable (but don't start) the units by default
    /bin/systemctl enable abrtd.service >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add abrtd
%endif
fi

%post addon-ccpp
# this is required for transition from 1.1.x to 2.x
# because /cache/abrt-di/* was created under root with root:root
# so 2.x fails when it tries to extract debuginfo there..
chown -R abrt:abrt %{_localstatedir}/cache/abrt-di
if [ $1 -eq 1 ]; then
%if %{with systemd}
    # Enable (but don't start) the units by default
    /bin/systemctl enable abrt-ccpp.service >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add abrt-ccpp
%endif
fi

%post addon-kerneloops
if [ $1 -eq 1 ]; then
%if %{with systemd}
    # Enable (but don't start) the units by default
    /bin/systemctl enable abrt-oops.service >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add abrt-oops
%endif
fi

%post addon-vmcore
if [ $1 -eq 1 ]; then
%if %{with systemd}
    # Enable (but don't start) the units by default
    /bin/systemctl enable abrt-vmcore.service >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add abrt-vmcore
%endif
fi

%preun
if [ "$1" -eq "0" ] ; then
%if %{with systemd}
    /bin/systemctl --no-reload disable abrtd.service > /dev/null 2>&1 || :
    /bin/systemctl stop abrtd.service >/dev/null 2>&1 || :
%else
    service abrtd stop >/dev/null 2>&1
    /sbin/chkconfig --del abrtd
%endif
fi

%preun addon-ccpp
if [ "$1" -eq "0" ] ; then
%if %{with systemd}
    /bin/systemctl --no-reload disable abrt-ccpp.service >/dev/null 2>&1 || :
    /bin/systemctl stop abrt-ccpp.service >/dev/null 2>&1 || :
%else
    service abrt-ccpp stop >/dev/null 2>&1
    /sbin/chkconfig --del abrt-ccpp
%endif
fi

%preun addon-kerneloops
if [ "$1" -eq "0" ] ; then
%if %{with systemd}
    /bin/systemctl --no-reload abrt-oops.service >/dev/null 2>&1 || :
    /bin/systemctl stop abrt-oops.service >/dev/null 2>&1 || :
%else
    service abrt-oops stop >/dev/null 2>&1
    /sbin/chkconfig --del abrt-oops
%endif
fi

%preun addon-vmcore
if [ "$1" -eq "0" ] ; then
%if %{with systemd}
    /bin/systemctl --no-reload abrt-vmcore.service >/dev/null 2>&1 || :
    /bin/systemctl stop abrt-vmcore.service >/dev/null 2>&1 || :
%else
    service abrt-vmcore stop >/dev/null 2>&1
    /sbin/chkconfig --del abrt-vmcore
%endif
fi

%postun
%_postun_userdel %{name}
%_postun_groupdel %{name} %{name}
%if %{with systemd}
if [ $1 -ge 1 ] ; then
# On upgrade, reload init system configuration if we changed unit files
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif

%if %{with systemd}
%postun addon-kerneloops
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun addon-vmcore
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun addon-ccpp
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

%post gui
# update icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gui
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
service abrtd condrestart >/dev/null 2>&1 || :

%posttrans addon-ccpp
service abrt-ccpp condrestart >/dev/null 2>&1 || :

%posttrans addon-kerneloops
service abrt-oops condrestart >/dev/null 2>&1 || :

%posttrans addon-vmcore
service abrt-vmcore condrestart >/dev/null 2>&1 || :

%posttrans gui
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%if 0
%post retrace-server
/sbin/install-info %{_infodir}/abrt-retrace-server %{_infodir}/dir 2> /dev/null || :
/usr/sbin/usermod -G mock apache 2> /dev/null || :

%preun retrace-server
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/abrt-retrace-server %{_infodir}/dir 2> /dev/null || :
fi
%endif

%files -f %{name}.lang
%doc README COPYING
%if %{with systemd}
/lib/systemd/system/abrtd.service
%else
%{_initrddir}/abrtd
%endif
%{_sbindir}/%{name}d
%{_sbindir}/%{name}-server
%{_sbindir}/abrt-dbus
%{_bindir}/%{name}-debuginfo-install
%{_bindir}/abrt-action-generate-core-backtrace
%{_bindir}/abrt-dedup-client
%{_bindir}/%{name}-handle-upload
%{_bindir}/%{name}-action-save-package-data
%{_bindir}/%{name}-retrace-client
%{_bindir}/abrt-watch-log
%{_libexecdir}/abrt-handle-event
%config(noreplace) %{_sysconfdir}/%{name}/abrt.conf
%config(noreplace) %{_sysconfdir}/%{name}/abrt-action-save-package-data.conf
%config(noreplace) %{_sysconfdir}/%{name}/gpg_keys
%config(noreplace) %{_sysconfdir}/libreport/events.d/abrt_event.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/dbus-abrt.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/smart_event.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/smolt_event.conf
%{_sysconfdir}/libreport/events.d/ccpp_retrace_event.conf
%{_sysconfdir}/libreport/events/analyze_RetraceServer.xml
%ghost %attr(0666, -, -) %{_localstatedir}/run/%{name}/abrt.socket
%ghost %attr(0644, -, -) %{_localstatedir}/run/%{name}d.pid
#%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/cache/%{name}
%dir /var/run/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
%{_mandir}/man1/abrt-handle-upload.1.*
%{_mandir}/man1/abrt-server.1.*
%{_mandir}/man1/abrt-action-save-package-data.1.*
%{_mandir}/man1/abrt-retrace-client.1.*
%{_mandir}/man1/abrt-cli.1.*
%{_mandir}/man8/abrtd.8.*
%{_mandir}/man8/abrt-dbus.8.*
%{_mandir}/man5/abrt.conf.5.*
%{_mandir}/man5/abrt-action-save-package-data.conf.5.*
%{_datadir}/dbus-1/system-services/org.freedesktop.problems.service
%{_datadir}/polkit-1/actions/abrt_polkit.policy

%files -n %{lib_name}
%{_libdir}/libabrt*.so.*

%files -n %{lib_name_devel}
%{_includedir}/abrt/*
%{_libdir}/libabrt*.so
#FIXME: this should go to libreportgtk-devel package
%{_libdir}/pkgconfig/%{name}.pc

%files gui
%{_bindir}/%{name}-gui
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_bindir}/%{name}-applet
%{_sysconfdir}/xdg/autostart/%{name}-applet.desktop

%files addon-ccpp
%config(noreplace) %{_sysconfdir}/%{name}/plugins/CCpp.conf
%{_sysconfdir}/libreport/events.d/ccpp_event.conf
%{_sysconfdir}/libreport/events.d/gconf_event.conf
%{_sysconfdir}/libreport/events.d/vimrc_event.conf
%{_sysconfdir}/libreport/events/analyze_LocalGDB.xml
%{_sysconfdir}/libreport/events/collect_xsession_errors.xml
%{_sysconfdir}/libreport/events/collect_Smolt.xml
%{_sysconfdir}/libreport/events/collect_GConf.xml
%{_sysconfdir}/libreport/events/collect_vimrc_user.xml
%{_sysconfdir}/libreport/events/collect_vimrc_system.xml
%dir %attr(0775, abrt, abrt) %{_localstatedir}/cache/abrt-di
%if %{with systemd}
/lib/systemd/system/abrt-ccpp.service
%else
%{_initrddir}/abrt-ccpp
%endif
%{_libdir}/abrt-hook-ccpp
%{_sysconfdir}/profile.d/00abrt.*
%{_bindir}/abrt-action-analyze-c
%{_bindir}/abrt-action-trim-files
%{_bindir}/abrt-action-analyze-core
%{_bindir}/abrt-action-list-dsos
%attr(2755, abrt, abrt) %{_bindir}/abrt-action-install-debuginfo
%attr(4755, abrt, abrt) %{_libexecdir}/abrt-action-install-debuginfo-to-abrt-cache
%{_bindir}/abrt-action-generate-backtrace
%{_bindir}/abrt-action-analyze-backtrace
%{_sbindir}/abrt-install-ccpp-hook
%{_mandir}/man*/abrt-action-analyze-c.*
%{_mandir}/man*/abrt-action-trim-files.*
%{_mandir}/man*/abrt-action-generate-backtrace.*
%{_mandir}/man*/abrt-action-generate-core-backtrace.*
%{_mandir}/man*/abrt-action-analyze-backtrace.*
%{_mandir}/man*/abrt-action-list-dsos.*
%{_mandir}/man1/abrt-install-ccpp-hook.*

%files addon-kerneloops
%config(noreplace) %{_sysconfdir}/libreport/events.d/koops_event.conf
%if %{with systemd}
/lib/systemd/system/abrt-oops.service
%else
%{_initrddir}/abrt-oops
%endif
%{_bindir}/abrt-dump-oops
%{_bindir}/abrt-action-analyze-oops
%{_mandir}/man1/abrt-action-analyze-oops.1*

%files addon-vmcore
%config(noreplace) %{_sysconfdir}/libreport/events.d/vmcore_event.conf
%{_sysconfdir}/libreport/events/analyze_VMcore.xml
%if %{with systemd}
/lib/systemd/system/abrt-vmcore.service
%else
%{_initrddir}/abrt-vmcore
%endif
%{_sbindir}/abrt-harvest-vmcore
%{_bindir}/abrt-action-analyze-vmcore
%{_mandir}/man1/abrt-action-analyze-vmcore.1*

%files cli
%{_bindir}/abrt-cli

%files addon-python
%dir %{_sysconfdir}/%{name}/plugins
%config(noreplace) %{_sysconfdir}/%{name}/plugins/python.conf
%{_sysconfdir}/libreport/events.d/python_event.conf
%{_bindir}/abrt-action-analyze-python
%{_mandir}/man1/abrt-action-analyze-python.1*
%{py_puresitedir}/abrt*.py*
%{py_puresitedir}/*.pth

%files addon-xorg
%config(noreplace) %{_sysconfdir}/libreport/events.d/xorg_event.conf
%if %{with systemd}
%{_unitdir}/abrt-xorg.service
%else
%{_initrddir}/abrt-xorg
%endif
%{_bindir}/abrt-dump-xorg

%files desktop

%if 0
%files retrace-server
%config(noreplace) %{_sysconfdir}/%{name}/retrace.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/retrace_httpd.conf
%config(noreplace) %{_sysconfdir}/yum.repos.d/retrace.repo
%dir %attr(0775, apache, abrt) %{_localstatedir}/spool/abrt-retrace
%dir %attr(0755, abrt, abrt) %{_localstatedir}/cache/abrt-retrace
%dir %attr(0755, abrt, abrt) %{_localstatedir}/log/abrt-retrace
%caps(cap_setuid=ep) %{_bindir}/abrt-retrace-worker
%{_bindir}/abrt-retrace-cleanup
%{_bindir}/abrt-retrace-reposync
%{_bindir}/coredump2packages
%{py_puresitedir}/retrace.py*
%{_datadir}/abrt-retrace/*.py*
%{_datadir}/abrt-retrace/*.wsgi
%{_datadir}/abrt-retrace/plugins/*.py*
%{_infodir}/abrt-retrace-server*
%endif


%changelog
* Tue May 01 2012 Guilherme Moro <guilherme@mandriva.com> 2.0.10-0
+ Revision: 794841
- Updated to version 2.0.10

* Mon Mar 12 2012 Oden Eriksson <oeriksson@mandriva.com> 2.0.8-3
+ Revision: 784394
- drop the abrt1-to-abrt2 stuff

* Mon Mar 12 2012 Oden Eriksson <oeriksson@mandriva.com> 2.0.8-2
+ Revision: 784346
- fix deps
- fix build
- fix deps
- standardize the spec file so it becomes more readable for non kde people
- merged systemd changes from fedora
- various fixes
- add the source as well (wtf?)
- rebuild

  + Alexander Khrukin <akhrukin@mandriva.org>
    - btparser-devel instead of pkgconfig(btparser)
    - btparser install deps fix
    - BR:libreport =>2.0.9
    - BR:pkgconfig(libreport-gtk) pkgconfig(libreport)
    - BR:pkgconfig(btparser) instead of btparser-devel
    - files section fixes
    - version update 2.0.8

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - string format fix (P0)
    - regenerate patches
    - link against libreport (P8)

* Sun Dec 11 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.2-2
+ Revision: 740273
- heh, when was this built last time really?
- fix the deps in xmlto
- attempt to fix the build (#2)
- attempt to fix the build (#1)
- various fixes
- rebuild against rpm5.4

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add asciidoc, xmlto & libgnome-keyring-devel to buildrequires
    - syncronize %%install, %%files etc. with Mageia
    - new version (with some updated patches taken from Mageia)
    - rebuild against new rpm 5.4

* Wed Jul 06 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.1.14-11
+ Revision: 688938
- fix abrt's login shell to be /sbin/nologin rather than /bin/nologinj (#63658)

* Tue Apr 12 2011 Funda Wang <fwang@mandriva.org> 1.1.14-10
+ Revision: 652780
- build with libnotify 0.7
- add more br

* Sat Feb 26 2011 Eugeni Dodonov <eugeni@mandriva.com> 1.1.14-9
+ Revision: 640152
- Systemd-units is only needed for the build, not actually Required.

* Sun Jan 09 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.1.14-8mdv2011.0
+ Revision: 630720
- finally get rpm 5.3 linked abrt into main/release "#!"#!" :p

* Tue Jan 04 2011 Eugeni Dodonov <eugeni@mandriva.com> 1.1.14-7mdv2011.0
+ Revision: 628561
- Add support for systemd (based on fedora spec).
- Install systemd service.
  Disable periodic run of KerneloopsScanner by default (#61986).

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix issue with CheckHash() in rpm5 & fmode
    - try again rpm5 build in main/testing, hopefully not messing up main/release

* Wed Dec 15 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 1.1.14-5mdv2011.0
+ Revision: 621949
- AGAIN push the rpm in release because packages got deleted each time someone
  push abrt in main/testing because of rpm5

* Sun Dec 12 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.1.14-4mdv2011.0
+ Revision: 620608
- really apply rpm5 patch
- reenable rpm5 patch, make it conditional as well

* Thu Dec 09 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 1.1.14-3mdv2011.0
+ Revision: 616599
- Rebuild because of missing rpms

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - rpm5 support (P11)

* Tue Nov 30 2010 Funda Wang <fwang@mandriva.org> 1.1.14-1mdv2011.0
+ Revision: 603263
- new version 1.1.14
- fix linkage
- rediff format and debug patch
- drop merged polkit patch

* Mon Nov 08 2010 Funda Wang <fwang@mandriva.org> 1.1.13-3mdv2011.0
+ Revision: 595032
- add fedora patch on polkit to make it built

  + Jani Välimaa <wally@mandriva.org>
    - rebuild for python 2.7

* Tue Aug 10 2010 Emmanuel Andry <eandry@mandriva.org> 1.1.13-2mdv2011.0
+ Revision: 568329
- use versioned obsoletes/provides
- set disable_ld_no_undefined to 0

* Tue Aug 10 2010 Emmanuel Andry <eandry@mandriva.org> 1.1.13-1mdv2011.0
+ Revision: 568324
- New version 1.1.13
- rediff p2, p3, p5, p6, p7
- drop catcut plugin
- update files list

* Wed May 12 2010 Frederic Crozat <fcrozat@mandriva.com> 1.1.1-1mdv2010.1
+ Revision: 544618
- Release 1.1.1
- Update patches 0, 2
- Update patches 3 to teach him Mdv specific bugzilla (still in progress)
- Remove patches 4 (no longer needed)
- Patch6: parse /etc/mandriva-release and teach abrt about Cooker
- Patch7: skip nspluginwrapper-i386 (Mdv bug #59237)
- Patch8: ensure all translations are in UTF-8 (caused dbus to exit in abrtd)

  + Emmanuel Andry <eandry@mandriva.org>
    - fix devel name

  + Pascal Terjan <pterjan@mandriva.org>
    - Install missing -debug packages

* Wed Mar 03 2010 Frederic Crozat <fcrozat@mandriva.com> 1.0.8-2mdv2010.1
+ Revision: 513937
- Update gio patch and apply it
- enforce gnome-python-desktop dependency for keyring support

* Mon Mar 01 2010 Frederic Crozat <fcrozat@mandriva.com> 1.0.8-1mdv2010.1
+ Revision: 513060
- import abrt


