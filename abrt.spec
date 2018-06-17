# (blino) FIXME: switch back to 1 when systemd is installable
%define with_systemd 1
%define _disable_rebuild_configure 1
%define _disable_ld_no_undefined 1
%bcond_with python2


%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}

%define lib_name_devel %mklibname %{name} -d
%define lib_report_devel %mklibname report -d

Summary:	Automatic bug detection and reporting tool
Name:		abrt
Version:	2.10.10
Release:	1
License:	GPLv2+
Group:		System/Libraries
URL:		https://github.com/abrt/abrt
Source0:	https://github.com/abrt/abrt/archive/%{version}.tar.gz
Source1:	abrt.init
Source2:	00abrt.sh
Source3:	00abrt.csh
Source4:	abrt-debuginfo-install
Source5:	abrt-ccpp.init
Source6:	abrt-oops.init
Patch1:		abrt-2.10.10-compile.patch
# (fc) disable package signature check
Patch2:		abrt_disable_gpgcheck.diff
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	dbus-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas) >= 3.15.1
BuildRequires:	curl-devel
BuildRequires:	rpm-devel
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	desktop-file-utils
BuildRequires:	nss-devel
BuildRequires:	systemd
BuildRequires:	libnotify-devel
BuildRequires:	xmlrpc-c-devel
BuildRequires:	xmlrpc-c
#BuildRequires: file-devel
%if %{with python2}
BuildRequires:	pkgconfig(python)
%endif
BuildRequires:	pkgconfig(python3)
BuildRequires:	gettext
BuildRequires:	polkit-1-devel
BuildRequires:	libzip-devel, libtar-devel, bzip2-devel, zlib-devel
BuildRequires:	intltool
BuildRequires:	pkgconfig(satyr)
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
BuildRequires:	pkgconfig(libsystemd)
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
#BuildConflicts:	%{mklibname abrt 0} %{mklibname abrt -d} abrt

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
Requires:	python-gi
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

%package addon-upload-watch
Summary: %{name}'s upload addon
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description addon-upload-watch
This package contains hook for uploaded problems.

%package retrace-client
Summary: %{name}'s retrace client
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
Requires: xz
Requires: tar

%description retrace-client
This package contains the client application for Retrace server
which is able to analyze C/C++ crashes remotely.

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

%package addon-pstoreoops
Summary: %{name}'s pstore oops addon
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
Requires: abrt-addon-kerneloops
Obsoletes: abrt-addon-uefioops < 2.1.7

%description addon-pstoreoops
This package contains plugin for collecting kernel oopses from pstore storage.

%package plugin-bodhi
Summary: %{name}'s bodhi plugin
BuildRequires: json-c-devel
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
BuildRequires: libreport-web-devel
Obsoletes: libreport-plugin-bodhi > 0.0.1
Provides: libreport-plugin-bodhi

%description plugin-bodhi
Search for a new updates in bodhi server.

%package addon-python
Summary:	%{name}'s addon for catching and analyzing Python exceptions
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description addon-python
This package contains python hook and python analyzer plugin for handling
uncaught exception in python programs.

%package addon-python2
Summary:        %{name}'s addon for catching and analyzing Python exceptions
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}

%description addon-python2
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

%package dbus
Summary: ABRT DBus service
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
BuildRequires: polkit-1-devel

%description dbus
ABRT DBus service which provides org.freedesktop.problems API on dbus and
uses PolicyKit to authorize to access the problem data.

%package -n python-%{name}
Summary: ABRT Python API
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
Requires: python-gi
Requires: python-dbus
Requires: libreport-python
BuildRequires: python-nose
BuildRequires: python-sphinx

%description -n python-%{name}
High-level API for querying, creating and manipulating
problems handled by ABRT in Python.

%package -n python-%{name}-doc
Summary: ABRT Python API Documentation
Group: Documentation
BuildArch: noarch
BuildRequires: python-devel
Requires: %{name} = %{version}-%{release}
Requires: python-%{name} = %{version}-%{release}

%description -n python-%{name}-doc
Examples and documentation for ABRT Python API.

%if %{with python2}
%package -n python2-%{name}
Summary: ABRT Python 2 API
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
Requires: python-gobject
Requires: python2-dbus
Requires: libreport-python2
BuildRequires: python2-nose
BuildRequires: python2-sphinx
BuildRequires: libreport-python2

%description -n python2-%{name}
High-level API for querying, creating and manipulating
problems handled by ABRT in Python 2.

%package -n python2-%{name}-doc
Summary: ABRT Python API Documentation
Group: Documentation
BuildArch: noarch
BuildRequires: python2-devel
Requires: %{name} = %{version}-%{release}
Requires: python2-%{name} = %{version}-%{release}

%description -n python2-%{name}-doc
Examples and documentation for ABRT Python 2 API.
%endif

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

%package console-notification
Summary: ABRT console notification script
Group: System/Configuration/Other
Requires: %{name} = %{version}-%{release}
Requires: %{name}-cli = %{version}-%{release}

%description console-notification
A small script which prints a count of detected problems when someone logs in
to the shell

%prep

%autosetup -p1
# (tv)) disable -Werror:
perl -pi -e 's!-Werror!-Wno-deprecated!' configure{.ac,} */*/Makefile*
[ -e autogen.sh ] && ./autogen.sh

%build
%define Werror_cflags %nil
#autoreconf -fi
%if %{with python2}
export PYTHON=%__python2
%endif
export PYTHONDONTWRITEBYTECODE=True
%configure \
%if !%{with_systemd}
    --without-systemdsystemunitdir \
%endif
%if %{with_systemd}
    --with-systemdsystemunitdir=/lib/systemd/system \
%endif
    --disable-rpath \
    --enable-gtk3 \
%if ! %{with python2}
	--without-python2
%endif

%make \
%if %{with python2}
	PYTHON_CFLAGS="`python2-config --cflags`" PYTHON_LIBS="`python2-config --libs`"
%endif

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

# systemd units should go to the right place
mkdir -p %{buildroot}/lib
mv %{buildroot}%{_prefix}/lib/systemd %{buildroot}/lib

%pre
%_pre_useradd %{name} %{_sysconfdir}/%{name} /sbin/nologin
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
%license COPYING
%if %{with systemd}
/lib/systemd/system/abrtd.service
%{_tmpfilesdir}/abrt.conf
%else
%{_initrddir}/abrtd
%endif
%{_sbindir}/%{name}d
%{_sbindir}/%{name}-server
%{_sbindir}/%{name}-auto-reporting
%{_bindir}/%{name}-debuginfo-install
%{_bindir}/%{name}-handle-upload
%{_bindir}/abrt-action-notify
%{_mandir}/man1/abrt-action-notify.1.*
%{_bindir}/abrt-action-analyze-xorg
%{_bindir}/abrt-action-analyze-python
%{_bindir}/%{name}-action-save-package-data
%{_bindir}/abrt-watch-log
%{_libexecdir}/abrt-handle-event
%{_libexecdir}/abrt-action-ureport
%{_libexecdir}/abrt-action-generate-machine-id
%config(noreplace) %{_sysconfdir}/%{name}/abrt.conf
%{_datadir}/%{name}/conf.d/abrt.conf
%config(noreplace) %{_sysconfdir}/%{name}/abrt-action-save-package-data.conf
%{_datadir}/%{name}/conf.d/abrt-action-save-package-data.conf
%config(noreplace) %{_sysconfdir}/%{name}/gpg_keys.conf
%{_datadir}/%{name}/conf.d/gpg_keys.conf
%{_mandir}/man5/gpg_keys.conf.5.*
%config(noreplace) %{_sysconfdir}/libreport/events.d/abrt_event.conf
%{_mandir}/man5/abrt_event.conf.5.*
%config(noreplace) %{_sysconfdir}/libreport/events.d/smart_event.conf
%{_mandir}/man5/smart_event.conf.5.*
%ghost %attr(0666, -, -) %{_localstatedir}/run/%{name}/abrt.socket
%ghost %attr(0644, -, -) %{_localstatedir}/run/%{name}d.pid
#%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/cache/%{name}
%dir /var/run/%{name}
%dir %{_sysconfdir}/%{name}
%ghost %{_sysconfdir}/%{name}/gpg_keys
%dir %{_sysconfdir}/%{name}/plugins
%{_mandir}/man1/abrt-handle-upload.1.*
%{_mandir}/man1/abrt-server.1.*
%{_mandir}/man1/abrt-action-save-package-data.1.*
%{_mandir}/man1/abrt-watch-log.1.*
%{_mandir}/man1/abrt-action-analyze-python.1*
%{_mandir}/man1/abrt-action-analyze-xorg.1.*
%{_mandir}/man1/abrt-auto-reporting.1.*
%{_mandir}/man8/abrtd.8.*
%{_mandir}/man5/abrt.conf.5.*
%{_mandir}/man5/abrt-action-save-package-data.conf.5.*
%{_sysconfdir}/bash_completion.d/abrt.bash_completion
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.problems.daemon.conf
/lib/systemd/system/abrt-coredump-helper.service
/lib/systemd/system/abrt-journal-core.service
%{_bindir}/abrt
%{_bindir}/abrt-action-check-oops-for-alt-component
%{_bindir}/abrt-action-find-bodhi-update
%{_bindir}/abrt-dump-journal-core
%{_bindir}/abrt-dump-journal-xorg
%{_libexecdir}/abrt-action-save-container-data
%{_datadir}/abrt/conf.d/plugins/CCpp_Atomic.conf
%doc %{_docdir}/abrt/README.md
%{_datadir}/libreport/events/analyze_BodhiUpdates.xml
%{_sysconfdir}/libreport/events.d/abrt_dbus_event.conf
%{_sysconfdir}/libreport/events.d/bodhi_event.conf
%{_sysconfdir}/libreport/events.d/machine-id_event.conf
%{_sysconfdir}/libreport/events.d/sosreport_event.conf
/lib/systemd/catalog/abrt_ccpp.catalog
%{_sysconfdir}/libreport/plugins/catalog_ccpp_format.conf
%{_sysconfdir}/libreport/plugins/catalog_journal_ccpp_format.conf
/lib/systemd/catalog/abrt_koops.catalog
%{_sysconfdir}/libreport/plugins/catalog_koops_format.conf
/lib/systemd/catalog/abrt_python3.catalog
%{_sysconfdir}/libreport/plugins/catalog_python3_format.conf
/lib/systemd/catalog/abrt_vmcore.catalog
%{_sysconfdir}/libreport/plugins/catalog_vmcore_format.conf
/lib/systemd/catalog/abrt_xorg.catalog
%{_sysconfdir}/libreport/plugins/catalog_xorg_format.conf
%{_mandir}/man1/abrt-action-find-bodhi-update.1*
%{_mandir}/man1/abrt-dump-journal-core.1*
%{_mandir}/man1/abrt-dump-journal-xorg.1*
%{_mandir}/man1/abrt.1*
%{_datadir}/augeas/lenses/abrt.aug

%files -n %{lib_name}
%{_libdir}/libabrt*.so.*

%files -n %{lib_name_devel}
%{_includedir}/abrt/*
%{_libdir}/libabrt*.so
#FIXME: this should go to libreportgtk-devel package
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/abrt_gui.pc

%files gui
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/status/*
%{_datadir}/abrt/icons/hicolor/*/status/*
%{_datadir}/%{name}/ui/*
%{_bindir}/system-config-abrt
%{_bindir}/%{name}-applet
%{_sysconfdir}/xdg/autostart/%{name}-applet.desktop
%{_mandir}/man1/abrt-applet.1*
%{_mandir}/man1/system-config-abrt.1*

%files addon-ccpp
%config(noreplace) %{_sysconfdir}/%{name}/plugins/CCpp.conf
%config(noreplace) %{_sysconfdir}/abrt/plugins/CCpp_Atomic.conf
%{_datadir}/%{name}/conf.d/plugins/CCpp.conf
%{_sysconfdir}/libreport/events.d/ccpp_event.conf
%{_mandir}/man5/ccpp_event.conf.5.*
%{_sysconfdir}/libreport/events.d/gconf_event.conf
%{_mandir}/man5/gconf_event.conf.5.*
%{_sysconfdir}/libreport/events.d/vimrc_event.conf
%{_mandir}/man5/vimrc_event.conf.5.*
%{_datadir}/libreport/events/analyze_CCpp.xml
%{_datadir}/libreport/events/analyze_LocalGDB.xml
%{_datadir}/libreport/events/collect_xsession_errors.xml
%{_datadir}/libreport/events/collect_GConf.xml
%{_datadir}/libreport/events/collect_vimrc_user.xml
%{_datadir}/libreport/events/collect_vimrc_system.xml
%{_datadir}/libreport/events/post_report.xml
%dir %attr(0775, abrt, abrt) %{_localstatedir}/cache/abrt-di
%if %{with systemd}
/lib/systemd/system/abrt-ccpp.service
%else
%{_initrddir}/abrt-ccpp
%endif
%{_libexecdir}/abrt-hook-ccpp
%{_libexecdir}/abrt-gdb-exploitable
%attr(6755, abrt, abrt) %{_libexecdir}/abrt-action-install-debuginfo-to-abrt-cache
%{_sysconfdir}/profile.d/00abrt.*
%{_bindir}/abrt-action-analyze-c
%{_bindir}/abrt-action-trim-files
%{_bindir}/abrt-action-analyze-core
%{_bindir}/abrt-action-analyze-vulnerability
%{_bindir}/abrt-action-install-debuginfo
%{_bindir}/abrt-action-generate-backtrace
%{_bindir}/abrt-action-generate-core-backtrace
%{_bindir}/abrt-action-analyze-backtrace
%{_bindir}/abrt-action-list-dsos
%{_bindir}/abrt-action-perform-ccpp-analysis
%{_bindir}/abrt-action-analyze-ccpp-local
%{_sbindir}/abrt-install-ccpp-hook
%{_mandir}/man*/abrt-action-analyze-c.*
%{_mandir}/man*/abrt-action-trim-files.*
%{_mandir}/man*/abrt-action-generate-backtrace.*
%{_mandir}/man*/abrt-action-generate-core-backtrace.*
%{_mandir}/man*/abrt-action-analyze-backtrace.*
%{_mandir}/man*/abrt-action-list-dsos.*
%{_mandir}/man*/abrt-install-ccpp-hook.*
%{_mandir}/man*/abrt-action-install-debuginfo.*
%{_mandir}/man*/abrt-action-analyze-ccpp-local.*
%{_mandir}/man*/abrt-action-analyze-core.*
%{_mandir}/man*/abrt-action-analyze-vulnerability.*
%{_mandir}/man*/abrt-action-perform-ccpp-analysis.*
%{_mandir}/man5/abrt-CCpp.conf.5.*

%files addon-upload-watch
%defattr(-,root,root,-)
%{_sbindir}/abrt-upload-watch
%if %{with systemd}
%{_unitdir}/abrt-upload-watch.service
%else
%{_initrddir}/abrt-upload-watch
%endif
%{_mandir}/man*/abrt-upload-watch.*

%files retrace-client
%{_bindir}/abrt-retrace-client
%{_mandir}/man1/abrt-retrace-client.1.*
%config(noreplace) %{_sysconfdir}/libreport/events.d/ccpp_retrace_event.conf
%{_mandir}/man5/ccpp_retrace_event.conf.5.*
%{_datadir}/libreport/events/analyze_RetraceServer.xml

%files addon-kerneloops
%config(noreplace) %{_sysconfdir}/libreport/events.d/koops_event.conf
%{_datadir}/%{name}/conf.d/plugins/oops.conf
%{_mandir}/man5/koops_event.conf.5.*
%config(noreplace) %{_sysconfdir}/%{name}/plugins/oops.conf
%if %{with systemd}
/lib/systemd/system/abrt-oops.service
%else
%{_initrddir}/abrt-oops
%endif
%{_bindir}/abrt-dump-oops
%{_bindir}/abrt-dump-journal-oops
%{_bindir}/abrt-action-analyze-oops
%{_mandir}/man1/abrt-dump-oops.1*
%{_mandir}/man1/abrt-dump-journal-oops.1*
%{_mandir}/man1/abrt-action-analyze-oops.1*
%{_mandir}/man5/abrt-oops.conf.5*

%files addon-vmcore
%config(noreplace) %{_sysconfdir}/libreport/events.d/vmcore_event.conf
%{_mandir}/man5/vmcore_event.conf.5.*
%config(noreplace) %{_sysconfdir}/%{name}/plugins/vmcore.conf
%{_datadir}/%{name}/conf.d/plugins/vmcore.conf
%{_datadir}/libreport/events/analyze_VMcore.xml
%if %{with systemd}
/lib/systemd/system/abrt-vmcore.service
%else
%{_initrddir}/abrt-vmcore
%endif
%{_sbindir}/abrt-harvest-vmcore
%{_bindir}/abrt-action-analyze-vmcore
%{_bindir}/abrt-action-check-oops-for-hw-error
%{_mandir}/man1/abrt-harvest-vmcore.1*
%{_mandir}/man5/abrt-vmcore.conf.5*
%{_mandir}/man1/abrt-action-analyze-vmcore.1*
%{_mandir}/man1/abrt-action-check-oops-for-hw-error.1*

%files cli
%{_bindir}/abrt-cli
%{_mandir}/man1/abrt-cli.1.*
%{python_sitearch}/abrtcli


%files addon-pstoreoops
%defattr(-,root,root,-)
%if %{with systemd}
%{_unitdir}/abrt-pstoreoops.service
%else
%{_initrddir}/abrt-pstoreoops
%endif
%{_sbindir}/abrt-harvest-pstoreoops
%{_bindir}/abrt-merge-pstoreoops
%{_mandir}/man1/abrt-harvest-pstoreoops.1*
%{_mandir}/man1/abrt-merge-pstoreoops.1*

%files addon-python
%dir %{_sysconfdir}/%{name}/plugins
%config(noreplace) %{_sysconfdir}/%{name}/plugins/python3.conf
%{_datadir}/%{name}/conf.d/plugins/python3.conf
%{_sysconfdir}/libreport/events.d/python3_event.conf
%{_mandir}/man5/python3_event.conf.5.*
%{_mandir}/man5/abrt-python3.conf.5.*
%{py_platsitedir}/abrt*.py*
%{py_platsitedir}/*.pth

%if %{with python2}
%files addon-python2
%dir %{_sysconfdir}/%{name}/plugins
%config(noreplace) %{_sysconfdir}/%{name}/plugins/python.conf
%{_datadir}/%{name}/conf.d/plugins/python.conf
%{_sysconfdir}/libreport/events.d/python_event.conf
%{_mandir}/man5/python_event.conf.5.*
%{_mandir}/man5/abrt-python.conf.5.*
%{py2_platsitedir}/abrt*.py*
%{py2_platsitedir}/*.pth
%endif

%files addon-xorg
%config(noreplace) %{_sysconfdir}/libreport/events.d/xorg_event.conf
%config(noreplace) %{_sysconfdir}/%{name}/plugins/xorg.conf
%{_datadir}/%{name}/conf.d/plugins/xorg.conf
%if %{with systemd}
%{_unitdir}/abrt-xorg.service
%else
%{_initrddir}/abrt-xorg
%endif
%{_bindir}/abrt-dump-xorg
%{_mandir}/man1/abrt-dump-xorg.1*
%{_mandir}/man5/xorg_event.conf.5.*
%{_mandir}/man5/abrt-xorg.conf.5.*

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

%files plugin-bodhi
%defattr(-,root,root,-)
%{_bindir}/abrt-bodhi
%{_mandir}/man1/abrt-bodhi.1.*

%files dbus
%{_sbindir}/abrt-dbus
%{_sbindir}/abrt-configuration
%{_mandir}/man8/abrt-dbus.8.*
%{_mandir}/man8/abrt-configuration.8.*
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/dbus-abrt.conf
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.abrt.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.ccpp.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.oops.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.python.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.vmcore.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.xorg.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Problems2.Entry.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Problems2.Session.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Problems2.Task.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Problems2.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.problems.service
%{_datadir}/dbus-1/system-services/com.redhat.problems.configuration.service
%{_datadir}/polkit-1/actions/abrt_polkit.policy
%dir %{_defaultdocdir}/%{name}-dbus-%{version}/
%dir %{_defaultdocdir}/%{name}-dbus-%{version}/html/
%{_defaultdocdir}/%{name}-dbus-%{version}/html/*.html
%{_defaultdocdir}/%{name}-dbus-%{version}/html/*.css

%files -n python-%{name}
%{py_platsitedir}/problem/
%{py_platsitedir}/__pycache__/abrt*
%{_mandir}/man5/abrt-python3.*

%files -n python-%{name}-doc
%{py_puresitedir}/problem_examples

%if %{with python2}
%files -n python2-%{name}
%{py2_platsitedir}/problem/
%{_mandir}/man5/abrt-python.5.*

%files -n python2-%{name}-doc
%{py2_puresitedir}/problem_examples
%endif

%files console-notification
%config(noreplace) %{_sysconfdir}/profile.d/abrt-console-notification.sh
