# TODO:
# - user for running daemon + fix perms to config files to be readable
#   only for daemon user
# - add deps to frontend

%include        /usr/lib/rpm/macros.perl
Summary:	Log Jabber conversations to a peer-visible database
Name:		bandersnatch
%define	_rc	RC1
Version:	0.4
Release:	0.%{_rc}.1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.funkypenguin.co.za/filestore2/download/5/%{name}-%{version}.%{_rc}.tar.gz
# Source0-md5:	e49075fce771f7c1ad7ff485eef76231
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.funkypenguin.co.za/taxonomy/term/5
BuildRequires:	rpm-perlprov
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tool to log Jabber instant messaging traffic. Is designed for a
corporate intranet environment in where the administrators can be
monitor the use/abuse of their Jabber servers.

%package frontend
Summary:	bandersnatch web frontend
Group:		Applications/WWW

%description frontend
bandersnatch web frontend.

%prep
%setup -q -n %{name}-%{version}.%{_rc}

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{rc.d/init.d,sysconfig,%{name}},%{_datadir}/%{name}-frontend}
install -d $RPM_BUILD_ROOT%{_sbindir}

cp -a frontend/* $RPM_BUILD_ROOT%{_datadir}/%{name}-frontend

install %{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}1
install %{name}2.pl $RPM_BUILD_ROOT%{_sbindir}/%{name}2
install config.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.xml

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

install frontend/includes/config.inc.php $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}-frontend.cfg
ln -sf %{_sysconfdir}/%{name}/%{name}-frontend.cfg \
	$RPM_BUILD_ROOT%{_datadir}/%{name}-frontend/includes/config.inc.php

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -r /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} server."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc *.sql doc/*
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.xml
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%files frontend
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%{_datadir}/%{name}-frontend
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}*.cfg
