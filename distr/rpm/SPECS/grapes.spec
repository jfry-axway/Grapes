# Avoid unnecessary debug-information (native code)
%define		debug_package %{nil}

# Avoid jar repack (brp-java-repack-jars)
#%define __jar_repack 0

# Avoid CentOS 5/6 extras processes on contents (especially brp-java-repack-jars)
%define __os_install_post %{nil}

%ifos darwin
%define __portsed sed -i "" -e
%else
%define __portsed sed -i
%endif

#
# app_ver is application version provided by build script from Maven Artifact version
# ex: 1.0.0, 2.0.1-8, 3.5.0-1
#

%define app_ver    %{APP_VERSION}

#
# RPM release, to be updated when app_ver/app_rel don't change but spec file has been updated
#
%define rpm_rel    2



Name: grapes
Version: %{app_ver}
Release: %{rpm_rel}
Summary: Grapes v%{APP_VERSION}
Group: CI/grapes
URL: http://www.grapes-project.org/
Vendor: Grapes-Project-OSS
Packager: Grapes-Project-OSS
License: ASLv2
BuildArch:  noarch

%define ciapp             		  grapes
%define ciappusername     		  grapesusr
%define ciappuserid       		  1350
%define ciappgroupid      		  1350

%define ciappdir          /opt/%{ciapp}
%define ciappbindir       %{ciappdir}/bin
%define ciappconfdir      %{ciappdir}/conf
%define ciapplibdir       %{ciappdir}/lib
%define ciappexec         %{ciappbindir}/server.sh
%define ciappdatadir      %{_var}/lib/%{ciapp}
%define ciapplogdir       %{_var}/log/%{ciapp}
%define ciapptmpdir       /tmp/%{ciapp}

%define cimongouser       admin
%define cimongopassword   admin
%define cimongoport   	  12441
%define cimongodb   	  grapes

%define _systemdir        /lib/systemd/system
%define _initrddir        %{_sysconfdir}/init.d

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

Requires: java = 1:1.6.0
Requires: mongodb
Requires: ciprovisioning-all

Source0: %{APP_FILE}
Source1: initd.skel
Source2: sysconfig.skel
Source3: jmxremote.access.skel
Source4: jmxremote.password.skel
Source5: server.sh.skel
Source6: limits.conf.skel
Source7: systemd.skel
Source8: server-conf.yml.skel
Source9: logrotate.skel

%description
Grapes v%{APP_VERSION}

%prep

%build

%install
# Prep the install location.
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/security/limits.d
mkdir -p %{buildroot}%{_systemdir}

mkdir -p %{buildroot}%{ciappdir}
mkdir -p %{buildroot}%{ciappbindir}
mkdir -p %{buildroot}%{ciappconfdir}
mkdir -p %{buildroot}%{ciapplibdir}
mkdir -p %{buildroot}%{ciapplogdir}
mkdir -p %{buildroot}%{ciappdatadir}
mkdir -p %{buildroot}%{ciappdatadir}/repository
mkdir -p %{buildroot}%{ciapptmpdir}

# copy jar
cp %{SOURCE0} %{buildroot}%{ciapplibdir}/server.jar

# init.d
cp  %{SOURCE1} %{buildroot}%{_initrddir}/%{ciapp}
sed -i 's|@@SKEL_APP@@|%{ciapp}|g' %{buildroot}%{_initrddir}/%{ciapp}
sed -i 's|@@SKEL_USER@@|%{ciappusername}|g' %{buildroot}%{_initrddir}/%{ciapp}
sed -i 's|@@SKEL_VERSION@@|version %{version} release %{release}|g' %{buildroot}%{_initrddir}/%{ciapp}
sed -i 's|@@SKEL_EXEC@@|%{ciappexec}|g' %{buildroot}%{_initrddir}/%{ciapp}

# sysconfig
cp  %{SOURCE2}  %{buildroot}%{_sysconfdir}/sysconfig/%{ciapp}
sed -i 's|@@SKEL_APP@@|%{ciapp}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{ciapp}
sed -i 's|@@SKEL_APPDIR@@|%{ciappdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{ciapp}
sed -i 's|@@SKEL_DATADIR@@|%{ciappdatadir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{ciapp}
sed -i 's|@@SKEL_LOGDIR@@|%{ciapplogdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{ciapp}
sed -i 's|@@SKEL_USER@@|%{ciappusername}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{ciapp}
sed -i 's|@@SKEL_CONFDIR@@|%{ciappconfdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{ciapp}
sed -i 's|@@SKEL_TMPDIR@@|%{ciapptmpdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{ciapp}

# JMX (including JMX Remote)
cp %{SOURCE3}  %{buildroot}%{ciappconfdir}
cp %{SOURCE4}  %{buildroot}%{ciappconfdir}

# Start/Stop script
cp %{SOURCE5} %{buildroot}%{ciappbindir}/server.sh
sed -i 's|@@SKEL_APP@@|%{ciapp}|g' %{buildroot}%{ciappbindir}/server.sh
sed -i 's|@@SKEL_LOGDIR@@|%{ciapplogdir}|g' %{buildroot}%{ciappbindir}/server.sh

# Setup user limits
cp %{SOURCE6} %{buildroot}%{_sysconfdir}/security/limits.d/%{ciapp}.conf
sed -i 's|@@SKEL_USER@@|%{ciappusername}|g' %{buildroot}%{_sysconfdir}/security/limits.d/%{ciapp}.conf

# Setup Systemd
cp %{SOURCE7} %{buildroot}%{_systemdir}/%{ciapp}.service
sed -i 's|@@SKEL_APP@@|%{ciapp}|g' %{buildroot}%{_systemdir}/%{ciapp}.service
sed -i 's|@@SKEL_EXEC@@|%{ciappexec}|g' %{buildroot}%{_systemdir}/%{ciapp}.service

# Setup application configuration
cp %{SOURCE8} %{buildroot}%{ciappconfdir}/server-conf.yml
sed -i 's|@@SKEL_APP@@|%{ciapp}|g' %{buildroot}%{ciappconfdir}/server-conf.yml
sed -i 's|@@SKEL_LOGDIR@@|%{ciapplogdir}|g' %{buildroot}%{ciappconfdir}/server-conf.yml
sed -i 's|@@DATABASE_PORT@@|%{cimongoport}|g' %{buildroot}%{ciappconfdir}/server-conf.yml
sed -i 's|@@DATABASE_USER@@|%{cimongouser}|g' %{buildroot}%{ciappconfdir}/server-conf.yml
sed -i 's|@@DATABASE_PASSWORD@@|%{cimongopassword}|g' %{buildroot}%{ciappconfdir}/server-conf.yml
sed -i 's|@@DATABASE_NAME@@|%{cimongodb}|g' %{buildroot}%{ciappconfdir}/server-conf.yml

# Install logrotate
cp %{SOURCE9} %{buildroot}%{_sysconfdir}/logrotate.d/%{ciapp}
sed -i 's|@@SKEL_LOGDIR@@|%{ciapplogdir}|g' %{buildroot}%{_sysconfdir}/logrotate.d/%{ciapp}

# ensure shell scripts are executable
chmod 755 %{buildroot}%{ciappbindir}/*.sh

%clean
rm -rf %{buildroot}

%pre
service mongodb restart

%if 0%{?suse_version} > 1140
%service_add_pre %{ciapp}.service
%endif
# First install time, add user and group
if [ "$1" == "1" ]; then
  %{_sbindir}/groupadd -r -g %{ciappgroupid} %{ciappusername} 2>/dev/null || :
  %{_sbindir}/useradd -s /sbin/nologin -c "%{ciapp} user" -g %{ciappusername} -r -d %{ciappdatadir} -u %{ciappuserid} %{ciappusername} 2>/dev/null || :
else
# Update time, stop service if running
  if [ "$1" == "2" ]; then
    if [ -f %{_var}/run/%{ciapp}.pid ]; then
      %{_initrddir}/%{ciapp} stop
      touch %{ciapplogdir}/rpm-update-stop
    fi
  fi
fi

%post
%if 0%{?suse_version} > 1140
%service_add_post %{ciapp}.service
%endif

# First install time, register service, generate random passwords and start application
if [ "$1" == "1" ]; then
  # register app as service
  systemctl enable %{ciapp}.service >/dev/null 2>&1

  %if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
    chkconfig %{ciapp} on
  %endif

  # Generated random password for RO and RW accounts
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@SKEL_RO_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{ciapp}
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@SKEL_RW_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{ciapp}

  # start application at first install (uncomment next line this behaviour not expected)
  # %{_initrddir}/%{ciapp} start
else
  # Update time, restart application if it was running
  if [ "$1" == "2" ]; then
    if [ -f %{ciapplogdir}/rpm-update-stop ]; then
      # restart application after update (comment next line this behaviour not expected)
      %{_initrddir}/%{ciapp} start
      rm -f %{ciapplogdir}/rpm-update-stop
    fi
  fi
fi

# Configure mongo
if [ "$1" == "1" ]; then

# set mongodb listen port and restart it
sed -i 's|#port = 27017|port = %{cimongoport}|g' %{_sysconfdir}/mongodb.conf
service mongodb restart
sleep 10

# add grapes user & db
cat << EOF1 | mongo --port %{cimongoport}
use %{cimongodb}
db.addUser("%{cimongouser}","%{cimongopassword}");
EOF1
fi

# Ensure that installation is sucessfull even if the mongo credentials are not stored
exit 0

%preun
%if 0%{?suse_version} > 1140
%service_del_preun %{ciapp}.service
%endif
if [ "$1" == "0" ]; then
  # Uninstall time, stop service and cleanup

  # stop service
  %{_initrddir}/%{ciapp} stop

  # unregister app from services
  systemctl disable %{ciapp}.service >/dev/null 2>&1

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
  chkconfig %{ciapp} off
%endif
fi

%postun
%if 0%{?suse_version} > 1140
%service_del_postun %{ciapp}.service
%endif


%files
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/%{ciapp}
%attr(0644,root,root) %{_systemdir}/%{ciapp}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{ciapp}
%config %{_sysconfdir}/logrotate.d/%{ciapp}
%config %{_sysconfdir}/security/limits.d/%{ciapp}.conf
%{ciappdir}/bin
%{ciappdir}/conf
%{ciappdir}/lib
%attr(0755,%{ciappusername},%{ciappusername}) %dir %{ciappdatadir}
%attr(0755,%{ciappusername},%{ciappusername}) %dir %{ciapplogdir}
%attr(0755,%{ciappusername},%{ciappusername}) %dir %{ciappdatadir}/repository
%attr(0755,%{ciappusername},%{ciappusername}) %dir %{ciapptmpdir}

%changelog
* Tue Apr 8 2014 jdcoffre@gmail.com 1.1.0-2
- Use open source binaries

* Tue Mar 11 2014 jdcoffre@gmail.com 1.1.0-1.1.1
- Use Grapes 1.1.0

* Wed Feb 5 2014 jdcoffre@gmail.com 1.0.0-1.1.2
- [BRS-1146] Fix package collocation with cidepmngr

* Mon Feb 3 2014 jdcoffre@gmail.com 1.0.0-1.1.1
- Use Grapes 1.0.0

* Thu Jan 16 2014 drautureau@gmail.com 1.0.0-1.rc3.2
- Fix typo.

* Tue Nov 5 2013 jdcoffre@gmail.com 1.0.0-1.rc3.1
- Initial RPM