# (blino) FIXME: switch back to 1 when systemd is installable
%define with_systemd 1

%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}

%define lib_name_devel %mklibname %{name} -d
%define lib_report_devel %mklibname report -d

Summary: Automatic bug detection and reporting tool
Name: abrt
Version: 2.0.8
Release: 2
License: GPLv2+
Group:   System/Libraries
URL: https://fedorahosted.org/abrt/
Source0: https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.gz
Source1: abrt.init
Source2: 00abrt.sh
Source3: 00abrt.csh
Source4: abrt-debuginfo-install
Source5: abrt-ccpp.init
Source6: abrt-oops.init
# (fc) disable package signature check
Patch2: abrt_disable_gpgcheck.diff
# (pt) generate stacktrace twice to get missing -debug packages
#Patch5: abrt-1.1.14-debug.patch
# (fc) disable nspluginwrapper-i386 (Mdv bug #59237)
Patch7: abrt-2.0.2-nspluginwrapper.patch
Patch8:	abrt-2.0.8-link-against-libreport.patch
# Fedora patches
BuildRequires: dbus-devel libdbus-glib-devel
BuildRequires: gtk2-devel
BuildRequires: curl-devel
BuildRequires: rpm-devel
BuildRequires: sqlite-devel > 3.0
BuildRequires: desktop-file-utils
#BuildRequires: nss-devel
BuildRequires: libnotify-devel
BuildRequires: xmlrpc-c-devel
BuildRequires: xmlrpc-c
#BuildRequires: file-devel
BuildRequires: python-devel
BuildRequires: gettext
BuildRequires: polkit-1-devel
BuildRequires: libzip-devel, libtar-devel, bzip2-devel, zlib-devel
BuildRequires: intltool
BuildRequires: pkgconfig(libreport)
BuildRequires: pkgconfig(libreport-gtk)
BuildRequires: gnome-common
BuildRequires: bison
BuildRequires: asciidoc
BuildRequires: docbook-style-xsl docbook5-style-xsl
BuildRequires: xmlto
BuildRequires: libgnome-keyring-devel
BuildRequires: gettext-devel
%if %{?with_systemd}
BuildRequires: systemd-units
%endif
BuildRequires: btparser-devel
#BuildRequires: libreport-devel
#BuildRequires: pkgconfig(libreport-gtk)
Requires: %{lib_name} >= %{version}-%{release}
Requires(pre): rpm-helper
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(postun): rpm-helper
Obsoletes: abrt-plugin-catcut < 1.1.13
Obsoletes: abrt-plugin-sqlite3 < 1.1.18
# required for transition from 1.1.13, can be removed after some time
Obsoletes: abrt-plugin-runapp < 1.1.18
Obsoletes: abrt-plugin-filetransfer < 1.1.18
Obsoletes: abrt-plugin-sosreport < 1.1.18

%description
%{name} is a tool to help users to detect defects in applications and
to create a bug report with all informations needed by maintainer to fix it.
It uses plugin system to extend its functionality.

%pre
%_pre_useradd %{name} %{_sysconfdir}/%{name} /bin/nologin
%_pre_groupadd %{name} %{name}

%post
%_post_service %{name}d
%if %{?with_systemd}
# Enable (but don't start) the units by default
  /bin/systemctl enable %{name}d.service >/dev/null 2>&1 || :
%endif

%posttrans
service abrtd condrestart >/dev/null 2>&1 || :

%preun
%_preun_service %{name}d
%if %{?with_systemd}
if [ "$1" -eq "0" ] ; then
  /bin/systemctl stop %{name}d.service >/dev/null 2>&1 || :
  /bin/systemctl disable %{name}d.service >/dev/null 2>&1 || :
fi
%endif

%postun
%_postun_userdel %{name}
%_postun_groupdel %{name} %{name}
%if %{?with_systemd}
if [ $1 -ge 1 ] ; then
# On upgrade, reload init system configuration if we changed unit files
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING
#systemd
%if %{?with_systemd}
%endif
%{_sbindir}/%{name}d
%{_sbindir}/%{name}-server
%{_sbindir}/abrt-dbus
%{_bindir}/%{name}-debuginfo-install
%{_bindir}/%{name}-handle-upload
%{_bindir}/%{name}-action-save-package-data
%{_bindir}/%{name}-retrace-client
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
%{_initrddir}/%{name}d
#%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/cache/%{name}
%dir /var/run/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
%{_mandir}/man1/abrt-handle-upload.1.*
%{_mandir}/man1/abrt-server.1.*
%{_mandir}/man1/abrt-action-save-package-data.1.*
%{_mandir}/man1/abrt-retrace-client.1.*
%{_mandir}/man8/abrtd.8.*
%{_mandir}/man8/abrt-dbus.8.*
%{_mandir}/man5/abrt.conf.5.*
%{_mandir}/man5/abrt-action-save-package-data.conf.5.*
%{_datadir}/dbus-1/system-services/com.redhat.%{name}.service

#--------------------------------------------------------------------

%package -n %{lib_name}
Summary: Libraries for %{name}
Group: System/Libraries

%description -n %{lib_name}
Libraries for %{name}.

%files -n %{lib_name}
%defattr(-,root,root,-)
%{_libdir}/libabrt*.so.*

#--------------------------------------------------------------------

%package -n %{lib_name_devel}
Summary: Development libraries for %{name}
Group: Development/C
Requires: %{lib_name} = %{version}-%{release}
Requires: abrt = %{version}-%{release}
Obsoletes: %{_lib}abrt0-devel

%description -n %{lib_name_devel}
Development libraries and headers for %{name}.

%files -n %{lib_name_devel}
%defattr(-,root,root,-)
%{_includedir}/abrt/*
%{_libdir}/libabrt*.so
#FIXME: this should go to libreportgtk-devel package
%{_libdir}/pkgconfig/%{name}.pc

#--------------------------------------------------------------------

%package gui
Summary: %{name}'s gui
Group: Graphical desktop/Other
Requires: %{name} = %{version}-%{release}
Requires: dbus-python, pygtk2.0, pygtk2.0-libglade
Requires: python-gobject
Requires: gnome-python-desktop
Requires: libreport-gtk

%description gui
GTK+ wizard for convenient bug reporting.

%files gui
%defattr(-,root,root,-)
%{_bindir}/%{name}-gui
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_bindir}/%{name}-applet
%{_sysconfdir}/xdg/autostart/%{name}-applet.desktop

#--------------------------------------------------------------------

%package addon-ccpp
Summary: %{name}'s C/C++ addon
Group: System/Libraries
Requires: elfutils
Requires: %{name} = %{version}-%{release}

%description addon-ccpp
This package contains hook for C/C++ crashed programs and %{name}'s C/C++
analyzer plugin.

%post addon-ccpp
chown -R abrt:abrt %{_localstatedir}/cache/abrt-di
#if [ $1 -eq 1 ]; then
/sbin/chkconfig --add abrt-ccpp
#fi

%if %{?with_systemd}
if [ "$1" -eq "0" ] ; then
    /bin/systemctl stop abrt-ccpp.service >/dev/null 2>&1 || :
    /bin/systemctl disable abrt-ccpp.service >/dev/null 2>&1 || :
fi
%endif

%posttrans addon-ccpp
service abrt-ccpp condrestart >/dev/null 2>&1 || :

%preun addon-ccpp
if [ "$1" -eq "0" ] ; then
  service abrt-ccpp stop >/dev/null 2>&1
  /sbin/chkconfig --del abrt-ccpp
fi

#systemd (not tested):
%if %{?with_systemd}
if [ "$1" -eq "0" ] ; then
    /bin/systemctl stop abrt-ccpp.service >/dev/null 2>&1 || :
    /bin/systemctl disable abrt-ccpp.service >/dev/null 2>&1 || :
fi
%endif

%files addon-ccpp
%defattr(-,root,root,-)
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
%{_initrddir}/abrt-ccpp
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
%{_mandir}/man*/abrt-action-analyze-backtrace.*
%{_mandir}/man*/abrt-action-list-dsos.*
%{_mandir}/man1/abrt-install-ccpp-hook.*

#--------------------------------------------------------------------

%package addon-kerneloops
Summary: %{name}'s kerneloops addon
Group: System/Libraries
Requires: curl
Requires: %{name} = %{version}-%{release}
#Obsoletes: kerneloops

%description addon-kerneloops
This package contains plugin for collecting kernel crash information
and reporter plugin which sends this information to specified server,
usually to kerneloops.org.

%post addon-kerneloops
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add abrt-oops
fi

%posttrans addon-kerneloops
service abrt-oops condrestart >/dev/null 2>&1 || :

%preun addon-kerneloops
if [ "$1" -eq "0" ] ; then
    service abrt-oops stop >/dev/null 2>&1
    /sbin/chkconfig --del abrt-oops
fi
#systemd (not tested):
%if %{?with_systemd}
if [ "$1" -eq "0" ] ; then
    /bin/systemctl stop abrt-oops.service >/dev/null 2>&1 || :
    /bin/systemctl disable abrt-oops.service >/dev/null 2>&1 || :
fi
%endif

%files addon-kerneloops
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/events.d/koops_event.conf
%{_initrddir}/abrt-oops
%{_bindir}/abrt-dump-oops
%{_bindir}/abrt-action-analyze-oops
%{_mandir}/man1/abrt-action-analyze-oops.1*

#--------------------------------------------------------------------

%package addon-vmcore
Summary: %{name}'s vmcore addon
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
Requires: abrt-addon-kerneloops

%description addon-vmcore
This package contains plugin for collecting kernel crash information from vmcore files.

%post addon-vmcore
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add abrt-oops
fi

%posttrans addon-vmcore
service abrt-oops condrestart >/dev/null 2>&1 || :

%preun addon-vmcore
if [ "$1" -eq "0" ] ; then
    service abrt-oops stop >/dev/null 2>&1
    /sbin/chkconfig --del abrt-oops
fi
#systemd (not tested):
%if %{?with_systemd}
if [ "$1" -eq "0" ] ; then
    /bin/systemctl stop abrt-oops.service >/dev/null 2>&1 || :
    /bin/systemctl disable abrt-oops.service >/dev/null 2>&1 || :
fi
%endif

%files addon-vmcore
%config(noreplace) %{_sysconfdir}/libreport/events.d/vmcore_event.conf
%{_sysconfdir}/libreport/events/analyze_VMcore.xml
%{_initrddir}/abrt-vmcore
%{_sbindir}/abrt-harvest-vmcore
%{_bindir}/abrt-action-analyze-vmcore

#--------------------------------------------------------------------

%package addon-python
Summary: %{name}'s addon for catching and analyzing Python exceptions
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description addon-python
This package contains python hook and python analyzer plugin for handling
uncaught exception in python programs.

%files addon-python
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/python.conf
%{_sysconfdir}/libreport/events.d/python_event.conf
%{_bindir}/abrt-action-analyze-python
%{_mandir}/man1/abrt-action-analyze-python.1*
%{py_puresitedir}/abrt*.py*
%{py_puresitedir}/*.pth

#--------------------------------------------------------------------

%package cli
Summary: %{name}'s command line interface
Group: Graphical desktop/Other
Requires: %{name} = %{version}-%{release}
Requires: %{name}-addon-kerneloops
Requires: %{name}-addon-ccpp, %{name}-addon-python

%description cli
This package contains simple command line client for controlling abrt 
daemon over the sockets.

%files cli
%defattr(-,root,root,-)
%{_bindir}/abrt-cli

#--------------------------------------------------------------------

%package desktop
Summary: Virtual package to install all necessary packages for usage from desktop environment
Group: Graphical desktop/Other
# This package gets installed when anything requests bug-buddy -
# happens when users upgrade Fn to Fn+1;
# or if user just wants "typical desktop installation".
# Installing abrt-desktop should result in the abrt which works without
# any tweaking in abrt.conf (IOW: all plugins mentioned there must be installed)
Requires: %{name} = %{version}-%{release}
Requires: %{name}-addon-kerneloops
Requires: %{name}-addon-vmcore
Requires: %{name}-addon-ccpp, %{name}-addon-python
# Default config of addon-ccpp requires gdb
Requires: gdb >= 7.0-3
Requires: %{name}-gui
#Obsoletes: bug-buddy
#Provides: bug-buddy

%description desktop
Virtual package to make easy default installation on desktop environments.

%files desktop
%defattr(-,root,root,-)

#--------------------------------------------------------------------
%if 0
%package retrace-server
Summary: %{name}'s retrace server using HTTP protocol
Group:   Graphical desktop/Other
Requires: abrt-addon-ccpp
Requires: gdb >= 7.0-3
Requires: apache-mod_wsgi, apache-mod_ssl, python-webob
Requires: mock, xz, elfutils, createrepo
Requires(preun): /sbin/install-info
Requires(post): /sbin/install-info

%post retrace-server
/sbin/install-info %{_infodir}/abrt-retrace-server %{_infodir}/dir 2> /dev/null || :
/usr/sbin/usermod -G mock apache 2> /dev/null || :

%preun retrace-server
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/abrt-retrace-server %{_infodir}/dir 2> /dev/null || :
fi

%description retrace-server
The retrace server provides a coredump analysis and backtrace
generation service over a network using HTTP protocol.

%files retrace-server
%defattr(-,root,root,-)
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
#--------------------------------------------------------------------

%prep
%setup -q
%apply_patches
# (tv)) disable -Werror:
perl -pi -e 's!-Werror!-Wno-deprecated!' configure{.ac,} */*/Makefile*





%build
NOCONFIGURE=yes gnome-autogen.sh

%configure2_5x \
%if !%{with_systemd}
	--without-systemdsystemunitdir \
%endif
	--disable-rpath
%make

%install
%makeinstall_std
%find_lang %{name}

# remove all .la and .a files
find %{buildroot} -name '*.la' -or -name '*.a' | xargs rm -f
mkdir -p %{buildroot}/%{_initrddir}
install -m 755 %SOURCE1 %{buildroot}/%{_initrddir}/%{name}d
install -m 755 %SOURCE5 %{buildroot}/%{_initrddir}/%{name}-ccpp
install -m 755 %SOURCE6 %{buildroot}/%{_initrddir}/%{name}-oops
mkdir -p %{buildroot}/var/cache/%{name}-di
mkdir -p %{buildroot}/var/run/%{name}
mkdir -p %{buildroot}/var/spool/%{name}
mkdir -p %{buildroot}/var/spool/%{name}-retrace
mkdir -p %{buildroot}/var/cache/%{name}-retrace
mkdir -p %{buildroot}/var/log/%{name}-retrace
mkdir -p %{buildroot}/var/spool/%{name}-upload

sed -i 's!@libexec@!%_libdir!' %{buildroot}/%{_initrddir}/%{name}-ccpp

# remove fedora gpg key
rm -f %{buildroot}%{_sysconfdir}/abrt/gpg_keys
touch %{buildroot}%{_sysconfdir}/abrt/gpg_keys

# install ulimit disabler
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
install -m755 %SOURCE2 %SOURCE3 %{buildroot}%{_sysconfdir}/profile.d/

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
