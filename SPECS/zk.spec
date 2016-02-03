# TODO:
# - how to add to the trusted service of the firewall?

%define __os_install_post \ /usr/lib/rpm/brp-compress \ %{!?__debug_package:/usr/lib/rpm/brp-strip %{__strip}} \ /usr/lib/rpm/brp-strip-static-archive %{__strip} \ /usr/lib/rpm/brp-strip-comment-note %{__strip} %{__objdump} \ %{nil}
%define org cn
#%define workdir %{_var}/lib/zookeeper
%define workdir /cn/runtime/zookeeper
%define start_script_path /usr/lib/systemd/system/zookeeper.service

Name:           %{org}-zookeeper
Version:        %{ver}
Release:        %{rel}
Summary:        Apache Zookeeper
Source:         zookeeper-%{version}.tar.gz
Source1:        zookeeper.service.in
Source2:        zookeeper.sysconfig.in
URL:            https://zookeeper.apache.org/
Group:          Development/Tools/Building
License:        Apache License, Version 2.0
BuildRoot:      %{_tmppath}/build-%{name}-%{version}
Requires:       /usr/sbin/groupadd, /usr/sbin/useradd, systemd, java-headless >= 1:1.8.0
BuildArch:      noarch

%description
ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.

%prep
%setup -q -c

%build

%install
rm -rf "%{buildroot}"
%__install -d "%{buildroot}%{workdir}"
cp -Rp zookeeper-%{version}/* "%{buildroot}%{workdir}"

%__install -D -m0755 "%{SOURCE1}" "%{buildroot}%{start_script_path}"

%__install -D -m0600 "%{SOURCE2}" "%{buildroot}/etc/sysconfig/zookeeper"
%__sed -i 's,@@PKG_ROOT@@,%{workdir},g' "%{buildroot}%{start_script_path}"

%pre
/usr/sbin/groupadd -r zookeeper &>/dev/null || :
/usr/sbin/useradd -g zookeeper -s /bin/false -r -c "Zookeeper Server" \
        -d "%{workdir}" zookeeper &>/dev/null || :

%post
/usr/bin/systemctl daemon-reload

%preun
if [ "$1" = 0 ] ; then
    # if this is uninstallation as opposed to upgrade, delete the service
    /usr/bin/systemctl stop zookeeper > /dev/null 2>&1
    /usr/bin/systemctl disable zookeeper
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
    /usr/bin/systemctl restart zookeeper > /dev/null 2>&1
fi
exit 0

%clean
%__rm -rf "%{buildroot}"

%files
%defattr(-,zookeeper,zookeeper)
%attr(0755,zookeeper,zookeeper) %{workdir}
%config(noreplace) %{start_script_path}
%config(noreplace) /etc/sysconfig/zookeeper

%changelog
* Tue Feb 2 2016 brian_wong@condenast.com
- Initial version
