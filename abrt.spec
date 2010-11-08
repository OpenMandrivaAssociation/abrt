%define lib_major 0
%define lib_name %mklibname %{name} %{lib_major}
%define lib_name_devel %mklibname %{name} -d

%define _disable_ld_no_undefined 0


Summary: Automatic bug detection and reporting tool
Name: abrt
Version: 1.1.13
Release: %mkrel 3
License: GPLv2+
Group: System/Base
URL: https://fedorahosted.org/abrt/
Source: https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.gz
Source1: abrt.init
Source2: 00abrt.sh
Source3: 00abrt.csh
Source4: abrt-debuginfo-install
# (fc) 1.0.8-1mdv fix format security error
# (misc) sent upstream https://fedorahosted.org/abrt/attachment/ticket/120
Patch0: abrt-1.1.0-format_security.patch
# (fc) 1.0.8-1mdv fix build with rpm 4.6
Patch1: abrt-1.0.8-rpm46.patch
# (fc) 1.0.8-1mdv disable package signature check
Patch2: abrt_disable_gpgcheck.diff
# (fc) 1.0.8-1mdv use mdv bugzilla
Patch3: abrt-mdvbugzilla.patch
# (pt) 1.0.8-3mdv generate stacktrace twice to get missing -debug packages
Patch5: abrt-1.1.13-debug.patch
# (fc) 1.1.0-1mdv parse mandriva-release
Patch6: abrt-1.1.13-mandriva-release.patch
# (fc) 1.1.0-1mdv disable nspluginwrapper-i386 (Mdv bug #59237)
Patch7: abrt-1.1.13-nspluginwrapper.patch
# (fc) 1.1.0-1mdv fix for non UTF-8 locale
Patch8: abrt-1.1.1-nonutf8-locale.patch
Patch9: polkit.patch
BuildRequires: dbus-devel
BuildRequires: gtk2-devel
BuildRequires: curl-devel
BuildRequires: rpm-devel >= 4.6
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
BuildRequires: bison
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: %{lib_name} >= %{version}-%{release}
Requires(pre): rpm-helper
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(postun): rpm-helper
Obsoletes: plugin-catcut < 1.1.13

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
Requires: %{lib_name} = %{version}-%{release}
Requires: abrt = %{version}-%{release}
Obsoletes: %{_lib}abrt0-devel

%description -n %{lib_name_devel}
Development libraries and headers for %{name}.

%package gui
Summary: %{name}'s gui
Group: Graphical desktop/Other
Requires: %{name} = %{version}-%{release}
Requires: dbus-python, pygtk2.0, pygtk2.0-libglade
Requires: python-gobject
Requires: gnome-python-desktop

%description gui
GTK+ wizard for convenient bug reporting.

%package addon-ccpp
Summary: %{name}'s C/C++ addon
Group: System/Libraries
Requires: elfutils
Requires: %{name} = %{version}-%{release}

%description addon-ccpp
This package contains hook for C/C++ crashed programs and %{name}'s C/C++
analyzer plugin.

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

%package plugin-logger
Summary: %{name}'s logger reporter plugin
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description plugin-logger
The simple reporter plugin which writes a report to a specified file.

%package plugin-mailx
Summary: %{name}'s mailx reporter plugin
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
Requires: mailx

%description plugin-mailx
The simple reporter plugin which sends a report via mailx to a specified
email address.

%package plugin-runapp
Summary: %{name}'s runapp plugin
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description plugin-runapp
Plugin to run external programs.

%package plugin-sosreport
Summary: %{name}'s sosreport plugin
Group: System/Libraries
Requires: sos
Requires: %{name} = %{version}-%{release}

%description plugin-sosreport
Plugin to include an sosreport in an abrt report.

%package plugin-bugzilla
Summary: %{name}'s bugzilla plugin
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

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
Requires: %{name} = %{version}-%{release}
Obsoletes: plugin-ticketuploader < 1.1.13
Provides: plugin-ticketuploader = %{version}-%{release}

%description plugin-reportuploader
Plugin to report bugs into anonymous FTP site associated with ticketing system.

%package plugin-filetransfer
Summary: %{name}'s File Transfer plugin
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description plugin-filetransfer
Plugin to uploading files to a server.

%package addon-python
Summary: %{name}'s addon for catching and analyzing Python exceptions
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description addon-python
This package contains python hook and python analyzer plugin for handling
uncaught exception in python programs.

%package cli
Summary: %{name}'s command line interface
Group: Graphical desktop/Other
Requires: %{name} = %{version}-%{release}
Requires: %{name}-addon-kerneloops
Requires: %{name}-addon-ccpp, %{name}-addon-python
Requires: %{name}-plugin-bugzilla, %{name}-plugin-logger, %{name}-plugin-runapp

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
Requires: %{name} = %{version}-%{release}
Requires: %{name}-addon-kerneloops
Requires: %{name}-addon-ccpp, %{name}-addon-python
# Default config of addon-ccpp requires gdb
Requires: gdb >= 7.0-3
Requires: %{name}-gui
Requires: %{name}-plugin-logger, %{name}-plugin-bugzilla, %{name}-plugin-runapp
#Obsoletes: bug-buddy
#Provides: bug-buddy

%description desktop
Virtual package to make easy default installation on desktop environments.

%prep
%setup -q
%patch0 -p1 -b .format_security
%patch1 -p1 -b .rpm46
%patch2 -p1 -b .disable_signature_check
%patch3 -p0 -b .mdvbugzilla
%patch5 -p0 -b .debug
%patch6 -p0 -b .mandriva-release
%patch7 -p0 -b .nspluginwrapper
%patch8 -p1 -b .nonutf8-locale
%patch9 -p1 -b .polkit

%build
%configure2_5x
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %{name}

#rm -rf %{buildroot}/%{_libdir}/lib*.la
#rm -rf %{buildroot}/%{_libdir}/%{name}/lib*.la
# remove all .la and .a files
find %{buildroot} -name '*.la' -or -name '*.a' | xargs rm -f
mkdir -p %{buildroot}/%{_initrddir}
install -m 755 %SOURCE1 %{buildroot}/%{_initrddir}/abrtd
mkdir -p %{buildroot}/var/cache/%{name}
mkdir -p %{buildroot}/var/cache/%{name}-di
mkdir -p %{buildroot}/var/run/%{name}
# remove fedora gpg key
rm -f %{buildroot}%{_sysconfdir}/abrt/gpg_keys
touch %{buildroot}%{_sysconfdir}/abrt/gpg_keys

# install ulimit disabler
mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
install -m755 %SOURCE2 %SOURCE3 %{buildroot}%{_sysconfdir}/profile.d/

desktop-file-install \
        --dir %{buildroot}%{_sysconfdir}/xdg/autostart \
        src/Applet/%{name}-applet.desktop

# replace with our own version
cat %{SOURCE4} > %{buildroot}/usr/bin/%{name}-debuginfo-install

#remove RH specific plugins
rm -f %{buildroot}%{_libdir}/%{name}/{RHTSupport.glade,libRHTSupport.so}
rm -f %{buildroot}%{_sysconfdir}/%{name}/plugins/RHTSupport.conf


%clean
rm -rf %{buildroot}

%pre
%_pre_useradd %{name} %{_sysconfdir}/%{name} /bin/nologin
%_pre_groupadd %{name} %{name}

%post
%_post_service %{name}d

%preun
%_preun_service %{name}d

%postun
%_postun_userdel %{name}
%_postun_groupdel %{name} %{name}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING
%{_sbindir}/%{name}d
%{_bindir}/%{name}-debuginfo-install
%{_bindir}/%{name}-backtrace
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/gpg_keys
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/dbus-%{name}.conf
%{_initrddir}/%{name}d
%dir %attr(0755, %{name}, %{name}) %{_localstatedir}/cache/%{name}
%dir /var/run/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
%dir %{_libdir}/%{name}
%{_mandir}/man1/%{name}-backtrace.1.*
%{_mandir}/man8/abrtd.8.*
%{_mandir}/man5/%{name}.conf.5.*
#%{_mandir}/man5/pyhook.conf.5.*
%{_mandir}/man7/%{name}-plugins.7.*
%{_datadir}/polkit-1/actions/org.fedoraproject.abrt.policy
%{_datadir}/dbus-1/system-services/com.redhat.abrt.service
%config(noreplace) %{_sysconfdir}/%{name}/plugins/SQLite3.conf
%{_libdir}/%{name}/libSQLite3.so*
%{_mandir}/man7/%{name}-SQLite3.7.*

%files -n %{lib_name}
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*

%files -n %{lib_name_devel}
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/%{name}.pc

%files gui
%defattr(-,root,root,-)
%{_bindir}/%{name}-gui
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_bindir}/%{name}-applet
%{_sysconfdir}/xdg/autostart/%{name}-applet.desktop

%files addon-ccpp
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/CCpp.conf
%dir %{_localstatedir}/cache/%{name}-di
%{_libdir}/%{name}/libCCpp.so*
%{_libexecdir}/abrt-hook-ccpp
%{_sysconfdir}/profile.d/00abrt.*

%files addon-kerneloops
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/Kerneloops.conf
%{_bindir}/dumpoops
%{_libdir}/%{name}/libKerneloops.so*
%{_libdir}/%{name}/libKerneloopsScanner.so*
%{_mandir}/man7/%{name}-KerneloopsScanner.7.*
%{_libdir}/%{name}/libKerneloopsReporter.so*
%{_libdir}/%{name}/KerneloopsReporter.glade
%{_mandir}/man7/%{name}-KerneloopsReporter.7.*

%files plugin-logger
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/Logger.conf
%{_libdir}/%{name}/libLogger.so*
%{_libdir}/%{name}/Logger.glade
%{_mandir}/man7/%{name}-Logger.7.*

%files plugin-mailx
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/Mailx.conf
%{_libdir}/%{name}/libMailx.so*
%{_libdir}/%{name}/Mailx.glade
%{_mandir}/man7/%{name}-Mailx.7.*

%files plugin-runapp
%defattr(-,root,root,-)
%{_libdir}/%{name}/libRunApp.so*
%{_mandir}/man7/%{name}-RunApp.7.*

%files plugin-sosreport
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/SOSreport.conf
%{_libdir}/%{name}/libSOSreport.so*


%files plugin-bugzilla
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/Bugzilla.conf
%{_libdir}/%{name}/libBugzilla.so*
%{_libdir}/%{name}/Bugzilla.glade
%{_mandir}/man7/%{name}-Bugzilla.7.*

##%files plugin-catcut
#%defattr(-,root,root,-)
#%config(noreplace) %{_sysconfdir}/%{name}/plugins/Catcut.conf
#%{_libdir}/%{name}/libCatcut.so*
#%{_libdir}/%{name}/Catcut.GTKBuilder
#%{_mandir}/man7/%{name}-Catcut.7.*

%files plugin-reportuploader
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/ReportUploader.conf
%{_bindir}/%{name}-handle-upload
%{_libdir}/%{name}/libReportUploader.so*
%{_libdir}/%{name}/ReportUploader.glade
%{_mandir}/man7/%{name}-ReportUploader.7.*

%files plugin-filetransfer
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/FileTransfer.conf
%{_libdir}/%{name}/libFileTransfer.so*
%{_mandir}/man7/%{name}-FileTransfer.7.*

%files addon-python
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/Python.conf
#%attr(4755, abrt, abrt) %{_libexecdir}/abrt-hook-python
%{_libdir}/%{name}/libPython.so*
%{py_puresitedir}/*.py*
%{py_puresitedir}/*.pth


%files cli
%defattr(-,root,root,-)
%{_bindir}/abrt-cli
%{_mandir}/man1/abrt-cli.1.*
%{_sysconfdir}/bash_completion.d/abrt-cli.bash

%files desktop
%defattr(-,root,root,-)

