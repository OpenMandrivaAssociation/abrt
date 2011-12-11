%define with_systemd 1

%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}
%define libreport %mklibname report %{lib_major}
%define libreportgtk %mklibname report-gtk %{lib_major}

%define lib_name_devel %mklibname %{name} -d
%define lib_report_devel %mklibname report -d

Summary: Automatic bug detection and reporting tool
Name: abrt
Version: 2.0.2
Release: 2
License: GPLv2+
Group: System/Base
URL: https://fedorahosted.org/abrt/
Source: https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.gz
Source1: abrt.init
Source2: 00abrt.sh
Source3: 00abrt.csh
Source4: abrt-debuginfo-install
Source5: abrt-ccpp.init
Source6: abrt-oops.init
# (fc) 1.0.8-1mdv fix format security error
# (misc) sent upstream https://fedorahosted.org/abrt/attachment/ticket/120
Patch0: abrt-2.0.2-format_security.patch
# (fc) 1.0.8-1mdv disable package signature check
Patch2: abrt_disable_gpgcheck.diff
# (fc) 1.0.8-1mdv use mdv bugzilla
Patch3: abrt-mdvbugzilla.patch
# (pt) 1.0.8-3mdv generate stacktrace twice to get missing -debug packages
Patch5: abrt-1.1.14-debug.patch
# (fc) 1.1.0-1mdv parse mandriva-release
Patch6: abrt-1.1.13-mandriva-release.patch
# (fc) 1.1.0-1mdv disable nspluginwrapper-i386 (Mdv bug #59237)
Patch7: abrt-2.0.2-nspluginwrapper.patch
# (fc) 1.1.0-1mdv fix for non UTF-8 locale
Patch8: abrt-2.0.2-nonutf8-locale.patch
Patch10: abrt-2.0.2-link.patch
# (proyvind): port to rpm5 api
Patch11: abrt-2.0.2-rpm5.patch
Patch14: abrt-2.0.2-add-missing-locale-header.patch
BuildRequires: dbus-glib-devel
BuildRequires: gtk2-devel
BuildRequires: curl-devel
BuildRequires: rpm-devel >= 1:5.3
BuildRequires: sqlite-devel > 3.0
BuildRequires: desktop-file-utils
#BuildRequires: nss-devel
BuildRequires: libnotify-devel
BuildRequires: xmlrpc-c-devel
BuildRequires: xmlrpc-c
BuildRequires: file-devel
BuildRequires: python-devel
BuildRequires: gettext
BuildRequires: polkit-1-devel
BuildRequires: libzip-devel, libtar-devel, bzip2-devel, zlib-devel
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: bison
BuildRequires: asciidoc
BuildRequires: xmlto
BuildRequires: libgnome-keyring-devel
%if %{?with_systemd}
BuildRequires: systemd-units
%endif
Requires: %{lib_name} >= %{version}-%{release}
Requires(pre): rpm-helper
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(postun): rpm-helper
Obsoletes: plugin-catcut < 1.1.13
%rename abrt-plugin-runapp
%rename abrt-plugin-filetransfer
%rename abrt-plugin-sosreport

%description
%{name} is a tool to help users to detect defects in applications and
to create a bug report with all informations needed by maintainer to fix it.
It uses plugin system to extend its functionality.

%package -n %{lib_name}
Summary: Libraries for %{name}
Group: System/Libraries

%description -n %{lib_name}
Libraries for %{name}.

%package -n %{lib_name_devel}
Summary: Development libraries for %{name}
Group: Development/C
Requires: %{lib_name} >= %{version}-%{release}
Requires: abrt = %{version}-%{release}
Obsoletes: %{_lib}abrt0-devel

%description -n %{lib_name_devel}
Development libraries and headers for %{name}.

%package gui
Summary: %{name}'s gui
Group: Graphical desktop/Other
Requires: %{name} >= %{version}-%{release}
Requires: dbus-python, pygtk2.0, pygtk2.0-libglade
Requires: python-gobject
Requires: gnome-python-desktop

%description gui
GTK+ wizard for convenient bug reporting.

%package addon-ccpp
Summary: %{name}'s C/C++ addon
Group: System/Libraries
Requires: elfutils
Requires: %{name} >= %{version}-%{release}

%description addon-ccpp
This package contains hook for C/C++ crashed programs and %{name}'s C/C++
analyzer plugin.

%package addon-kerneloops
Summary: %{name}'s kerneloops addon
Group: System/Libraries
Requires: curl
Requires: %{name} >= %{version}-%{release}
#Obsoletes: kerneloops

%description addon-kerneloops
This package contains plugin for collecting kernel crash information
and reporter plugin which sends this information to specified server,
usually to kerneloops.org.

%package plugin-logger
Summary: %{name}'s logger reporter plugin
Group: System/Libraries
Requires: %{name} >= %{version}-%{release}

%description plugin-logger
The simple reporter plugin which writes a report to a specified file.

%package plugin-mailx
Summary: %{name}'s mailx reporter plugin
Group: System/Libraries
Requires: %{name} >= %{version}-%{release}
Requires: mailx

%description plugin-mailx
The simple reporter plugin which sends a report via mailx to a specified
email address.

%package plugin-bugzilla
Summary: %{name}'s bugzilla plugin
Group: System/Libraries
Requires: %{name} >= %{version}-%{release}

%description plugin-bugzilla
Plugin to report bugs into the bugzilla.

##%package plugin-catcut
#Summary: %{name}'s catcut plugin
#Group: System/Libraries
#Requires: %{name} = %{version}-%{release}

##%description plugin-catcut
#Plugin to report bugs into the catcut.

%package plugin-reportuploader
Summary: %{name}'s ticketuploader plugin
Group: System/Libraries
Requires: %{name} >= %{version}-%{release}
Obsoletes: plugin-ticketuploader < 1.1.13
Provides: plugin-ticketuploader = %{version}-%{release}

%description plugin-reportuploader
Plugin to report bugs into anonymous FTP site associated with ticketing system.

%package addon-python
Summary: %{name}'s addon for catching and analyzing Python exceptions
Group: System/Libraries
Requires: %{name} >= %{version}-%{release}

%description addon-python
This package contains python hook and python analyzer plugin for handling
uncaught exception in python programs.

%package cli
Summary: %{name}'s command line interface
Group: Graphical desktop/Other
Requires: %{name} >= %{version}-%{release}
Requires: %{name}-addon-kerneloops
Requires: %{name}-addon-ccpp, %{name}-addon-python
Requires: %{name}-plugin-bugzilla, %{name}-plugin-logger

%description cli
This package contains simple command line client for controlling abrt 
daemon over the sockets.

%package desktop
Summary: Virtual package to install all necessary packages for usage from desktop environment
Group: Graphical desktop/Other
# This package gets installed when anything requests bug-buddy -
# happens when users upgrade Fn to Fn+1;
# or if user just wants "typical desktop installation".
# Installing abrt-desktop should result in the abrt which works without
# any tweaking in abrt.conf (IOW: all plugins mentioned there must be installed)
Requires: %{name} >= %{version}-%{release}
Requires: %{name}-addon-kerneloops
Requires: %{name}-addon-ccpp, %{name}-addon-python
# Default config of addon-ccpp requires gdb
Requires: gdb >= 7.0-3
Requires: %{name}-gui
Requires: %{name}-plugin-logger, %{name}-plugin-bugzilla
#Obsoletes: bug-buddy
#Provides: bug-buddy

%description desktop
Virtual package to make easy default installation on desktop environments.

%package -n %{libreport}
Summary: Libraries for reporting crashes to different targets
Group:   System/Libraries

%description -n %{libreport}
Libraries providing API for reporting different problems in applications
to different bug targets like bugzilla, ftp, trac, etc...

%package -n %{lib_report_devel}
Summary: Development libraries and headers for libreport
Group:   System/Libraries

%description -n %lib_report_devel
Development libraries and headers for libreport.

%package -n python-libreport
Summary: Python bindings for report-libs
Group: System/Libraries

%description -n python-libreport
Python bindings for report-libs.

%package -n %{libreportgtk}
Summary: GTK frontend for libreport
Group:   System/Libraries

%description -n %{libreportgtk}
Applications for reporting bugs using libreport backend.

%package retrace-server
Summary: %{name}'s retrace server using HTTP protocol
Group:   Graphical desktop/Other
Requires: abrt-addon-ccpp
Requires: gdb >= 7.0-3
Requires: apache-mod_wsgi, apache-mod_ssl, python-webob
Requires: mock, xz, elfutils, createrepo
Requires(preun): /sbin/install-info
Requires(post): /sbin/install-info

%description retrace-server
The retrace server provides a coredump analysis and backtrace
generation service over a network using HTTP protocol.

%prep
%setup -q
%patch0 -p1 -b .format_security
%patch2 -p1 -b .disable_signature_check
#patch3 -p0 -b .mdvbugzilla
#patch6 -p0 -b .mandriva-release
%patch7 -p1 -b .nspluginwrapper
%patch8 -p1 -b .nonutf8-locale
%patch10 -p1 -b .link~
%patch11 -p1 -b .rpm5~
%patch14 -p1 -b .locale~

%build
NOCONFIGURE=yes gnome-autogen.sh
CFLAGS="-Wno-error=deprecated-declarations" \
%configure2_5x --disable-rpath
%make

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %{name}

#rm -rf %{buildroot}/%{_libdir}/lib*.la
#rm -rf %{buildroot}/%{_libdir}/%{name}/lib*.la
# remove all .la and .a files
find %{buildroot} -name '*.la' -or -name '*.a' | xargs rm -f
install -m755 %{SOURCE1} -D %{buildroot}/%{_initrddir}/abrtd
install -m755 %{SOURCE5} %{buildroot}/%{_initrddir}/abrt-ccpp
install -m755 %{SOURCE6} %{buildroot}/%{_initrddir}/abrt-oops

mkdir -p %{buildroot}/var/cache/%{name}
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
install -m755 %{SOURCE2} %{SOURCE3} %{buildroot}%{_sysconfdir}/profile.d/
install -m755 src/daemon/abrtd.service -D %{buildroot}/lib/systemd/system/%{name}d.service

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

touch %{buildroot}%{_localstatedir}/run/%{name}/abrt.socket
touch %{buildroot}%{_localstatedir}/run/%{name}d.pid

%pre
%_pre_useradd %{name} %{_sysconfdir}/%{name} /sbin/nologin
%_pre_groupadd %{name} %{name}

%post
%_post_service %{name}d
%if %{?with_systemd}
# Enable (but don't start) the units by default
  /bin/systemctl enable %{name}d.service >/dev/null 2>&1 || :
%endif


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

%post retrace-server
/sbin/install-info %{_infodir}/abrt-retrace-server %{_infodir}/dir 2> /dev/null || :
/usr/sbin/usermod -G mock apache 2> /dev/null || :

%preun retrace-server
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/abrt-retrace-server %{_infodir}/dir 2> /dev/null || :
fi

%files -f %{name}.lang
%doc README COPYING
#systemd
%if %{?with_systemd}
/lib/systemd/system/%{name}d.service
%endif
%{_sbindir}/%{name}d
%{_sbindir}/%{name}-server
%{_bindir}/%{name}-debuginfo-install
%{_bindir}/%{name}-action-analyze-core.py
%{_bindir}/%{name}-handle-upload
%{_bindir}/%{name}-handle-crashdump
%{_bindir}/%{name}-action-save-package-data
%{_bindir}/%{name}-retrace-client
%{_bindir}/bug-reporting-wizard
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/gpg_keys
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/dbus-%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}_event.conf
%ghost %attr(0666, -, -) %{_localstatedir}/run/%{name}/abrt.socket
%ghost %attr(0644, -, -) %{_localstatedir}/run/%{name}d.pid
%{_initrddir}/%{name}d
#%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/cache/%{name}
%dir /var/run/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
%dir %{_sysconfdir}/%{name}/events.d
%dir %{_sysconfdir}/%{name}/events
%{_mandir}/man8/%{name}d.8.*
%{_mandir}/man5/%{name}.conf.5.*
%{_mandir}/man5/%{name}_event.conf.5.*
%{_mandir}/man7/%{name}-plugins.7.*
%{_datadir}/dbus-1/system-services/com.redhat.%{name}.service

%files -n %{lib_name}
%{_libdir}/libabrt*.so.*
%{_libdir}/libbtparser.so.*

%files -n %{lib_name_devel}
%{_includedir}/abrt/*
%{_includedir}/btparser/*
%{_libdir}/libabrt*.so
%{_libdir}/libbtparser.so
#FIXME: this should go to libreportgtk-devel package
%{_libdir}/libreportgtk.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/btparser.pc

%files gui
%{_bindir}/%{name}-gui
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_bindir}/%{name}-applet
%{_sysconfdir}/xdg/autostart/%{name}-applet.desktop

%files addon-ccpp
%config(noreplace) %{_sysconfdir}/%{name}/plugins/CCpp.conf
%dir %attr(0775, abrt, abrt) %{_localstatedir}/cache/abrt-di
%{_initrddir}/abrt-ccpp
%{_libdir}/abrt-hook-ccpp
%{_sysconfdir}/profile.d/00abrt.*
%{_bindir}/abrt-action-analyze-c
%{_bindir}/abrt-action-trim-files
%attr(2755, abrt, abrt) %{_bindir}/abrt-action-install-debuginfo
%{_bindir}/abrt-action-install-debuginfo.py*
%{_bindir}/abrt-action-generate-backtrace
%{_bindir}/abrt-action-analyze-backtrace
%{_bindir}/abrt-action-list-dsos.py*
%{_sysconfdir}/%{name}/events.d/ccpp_events.conf
%{_sysconfdir}/%{name}/events/analyze_LocalGDB.xml
%{_sysconfdir}/%{name}/events/reanalyze_LocalGDB.xml
%{_sysconfdir}/%{name}/events/analyze_RetraceServer.xml
%{_sysconfdir}/%{name}/events/reanalyze_RetraceServer.xml
%{_mandir}/man*/abrt-action-trim-files.*
%{_mandir}/man*/abrt-action-generate-backtrace.*
%{_mandir}/man*/abrt-action-analyze-backtrace.*

%files addon-kerneloops
%config(noreplace) %{_sysconfdir}/%{name}/plugins/Kerneloops.conf
%config(noreplace) %{_sysconfdir}/%{name}/events.d/koops_events.conf
%{_sysconfdir}/%{name}/events/report_Kerneloops.xml
%{_initrddir}/abrt-oops
%{_mandir}/man7/abrt-KerneloopsReporter.7.*
%{_bindir}/abrt-dump-oops
%{_bindir}/abrt-action-analyze-oops
%{_bindir}/abrt-action-kerneloops

%files plugin-logger
%{_sysconfdir}/%{name}/events/report_Logger.conf
%{_bindir}/abrt-action-print
%{_mandir}/man7/%{name}-Logger.7.*
%{_mandir}/man*/%{name}-action-print.*

%files plugin-mailx
%{_sysconfdir}/%{name}/events/report_Mailx.xml
%{_sysconfdir}/%{name}/events.d/mailx_events.conf
%{_bindir}/abrt-action-mailx
%{_mandir}/man7/%{name}-Mailx.7.*
%{_mandir}/man*/%{name}-action-mailx.*

%files plugin-bugzilla
%config(noreplace) %{_sysconfdir}/%{name}/plugins/Bugzilla.conf
%{_sysconfdir}/%{name}/events/report_Bugzilla.xml
%config(noreplace) %{_sysconfdir}/%{name}/events/report_Bugzilla.conf
# FIXME: remove with the old gui
%{_mandir}/man7/abrt-Bugzilla.7.*
%{_bindir}/abrt-action-bugzilla

##%files plugin-catcut
#%config(noreplace) %{_sysconfdir}/%{name}/plugins/Catcut.conf
#%{_libdir}/%{name}/libCatcut.so*
#%{_libdir}/%{name}/Catcut.GTKBuilder
#%{_mandir}/man7/%{name}-Catcut.7.*

%files plugin-reportuploader
%config(noreplace) %{_sysconfdir}/%{name}/plugins/Upload.conf
%{_mandir}/man7/abrt-Upload.7.*
%{_bindir}/abrt-action-upload

%files addon-python
%config(noreplace) %{_sysconfdir}/%{name}/plugins/Python.conf
%{_bindir}/abrt-action-analyze-python
%{py_puresitedir}/abrt*.py*
%{py_puresitedir}/*.pth

%files cli
%{_bindir}/abrt-cli
%{_mandir}/man1/abrt-cli.1.*
%{_sysconfdir}/bash_completion.d/abrt-cli.bash

%files desktop

%files -n %{libreport}
%{_libdir}/libreport.so.%{lib_major}*

%files -n %{lib_report_devel}
%{_includedir}/report/*
%{_libdir}/libreport.so

%files -n %{libreportgtk}
%{_libdir}/libreportgtk.so.%{lib_major}*

%files -n python-libreport
%dir %{python_sitearch}/report
%{python_sitearch}/report/*

%files retrace-server
%config(noreplace) %{_sysconfdir}/%{name}/retrace.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/retrace_httpd.conf
%config(noreplace) %{_sysconfdir}/yum.repos.d/retrace.repo
%dir %attr(0775, apache, abrt) %{_localstatedir}/spool/abrt-retrace
%dir %attr(0755, abrt, abrt) %{_localstatedir}/cache/abrt-retrace
%dir %attr(0755, abrt, abrt) %{_localstatedir}/log/abrt-retrace
%{_bindir}/abrt-retrace-worker
%{_bindir}/abrt-retrace-cleanup
%{_bindir}/abrt-retrace-reposync
%{_bindir}/coredump2packages
%{py_puresitedir}/retrace.py*
%{_datadir}/abrt-retrace/*.py*
%{_datadir}/abrt-retrace/*.wsgi
%{_datadir}/abrt-retrace/plugins/*.py*
%{_infodir}/abrt-retrace-server*
