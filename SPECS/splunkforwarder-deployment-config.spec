%{!?SPLUNKVERSION:%global SPLUNKVERSION 6.6.0}
%{!?SPLUNKPKG:%global SPLUNKPKG splunkforwarder}
%{!?SPLUNKUSER:%global SPLUNKUSER splunk}
%global name %{SPLUNKPKG}-deployment-config
%global release 28
%global splunk_home /opt/%{SPLUNKPKG}
%global splunk_app_path %{splunk_home}/etc/apps/zzRPM-%{SPLUNKPKG}-deployment-config

%{!?DEPLOYMENTPORT:%global DEPLOYMENTPORT 8089}
%{!?vendor: %global vendor None}

Summary: Build custom Splunk deployment rpm
Name: %{name}
Version: %{SPLUNKVERSION}
Release: %{release}
License: none
# Groups: See /usr/share/doc/rpm*/GROUPS file.
Group: Applications/System
Source0: deploymentclient.conf.in
Source1: README.md
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-root
Requires: %{SPLUNKPKG} >= %{SPLUNKVERSION}

Vendor: %{vendor}
Packager: %{?_packager:%{_packager}}%{!?_packager:%{_vendor}}

%description
Custom Splunk deployment client configuration

%prep
cp %{SOURCE0} .
cp %{SOURCE1} .

#Test that custom macros are defined
%if !0%{?CLIENTNAME:1} || !0%{?DEPLOYMENTSERVER:1}
%{error: You must define CLIENTNAME and DEPLOYMENTSERVER.
        See the --define option of the rpmbuild command.
}
exit 1
%endif

%build

%install

mkdir -p %{buildroot}%{splunk_app_path}/{default,local}
sed -e 's/CLIENTNAME/%{CLIENTNAME}/' \
    -e 's/DEPLOYMENTSERVER/%{DEPLOYMENTSERVER}/' \
    -e 's/DEPLOYMENTPORT/%{DEPLOYMENTPORT}/' \
    deploymentclient.conf.in > %{buildroot}%{splunk_app_path}/default/deploymentclient.conf

%pre
if [ "$(pgrep splunkd)" ]; then
    %{splunk_home}/bin/splunk stop
fi

%posttrans
%{splunk_home}/bin/splunk enable boot-start -user %{SPLUNKUSER}
/bin/chown -R ${SPLUNKUSER}: %{splunk_home}
%{splunk_home}/bin/splunk start --accept-license --no-prompt --answer-yes

# Hack to fix upgrades
# When a Splunk RPM is removed a postuninstall script stops splunkd. This
# occurs after the splunk-deploy-client starts splunkd. This stanza will
# restart splunk after the upgrade process is complete
#if [ -z "$(pgrep splunkd)" ] && [ -x %{splunk_home}/bin/splunk ]; then
#    (sleep 300; %{splunk_home}/bin/splunk start) &
#fi

%clean
rm -rf %{buildroot}

%files
%{splunk_app_path}
%doc README.md

%changelog
* Fri Jul 14 2017 Daniel Deighton <ddeighton-github@aplura.com>
- Use individual source files rather than a tgz.
- Update default version to 6.6.0.
- Update doc to README.md

* Fri Nov 14 2014 Daniel Deighton <ddeighton-github@aplura.com>
- Add SPLUNKUSER option; default to "splunk"
- Remove macro references in changelog, since they cause problems with newer versions of RPMBUILD

* Wed Nov  5 2014 Daniel Deighton <ddeighton-github@aplura.com>
- Use all caps for configurable variables
- Update README file

* Thu Oct 30 2014 Daniel Deighton <ddeighton-github@aplura.com>
- Update to use splunkforwarder 6.1.0 as default

* Wed Oct 23 2013 Daniel Deighton <ddeighton-github@aplura.com>
- Update to use splunkforwarder 6.0

* Mon Sep 30 2013 Daniel Deighton <ddeighton-github@aplura.com>
- Update to use splunkforwarder 5.0.5

* Tue Jul  9 2013 Daniel Deighton <ddeighton-github@aplura.com>
- Update to use splunkforwarder 5.0.2
- Move mkdir command to install section

* Fri Jan 18 2013 Daniel Deighton <ddeighton-github@aplura.com>
- Upgrade to use splunkforwarder 5.0.1

* Mon Jul 20 2012 Daniel Deighton <ddeighton-github@aplura.com>
- Use splunk or splunkforwarder in name macro, rather than including it in the release macro.
- Disable post install hack; using posttrans now.
- Base etc/apps subdir on splunkpkg macro

* Mon Jun 18 2012 Daniel Deighton <ddeighton-github@aplura.com>
- Use posttrans instead of post script to restart splunk

* Mon Dec 19 2011 Daniel Deighton <ddeighton-github@aplura.com>
- Added "hack" to start
* Fri Dec 16 2011 Daniel Deighton <ddeighton-github@aplura.com>
- Use splunkpkg macro to allow use of splunk or splunkforwarder
- Set default values for splunkpkg, splunkversion, DEPLOYMENTPORT
- Moved sources into tarball
- included a README

* Fri Dec  2 2011 Daniel Deighton <ddeighton-github@aplura.com>
- Move Variable test code to prep section
- Add BuildRoot line. Needed to build on RHEL5

* Thu Dec  1 2011 Daniel Deighton <ddeighton-github@aplura.com>
- Fix: Put deploymentclient.conf into default subdir.

* Wed Nov 30 2011 Daniel Deighton <ddeighton-github@aplura.com>
- Initial release.
