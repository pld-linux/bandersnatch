# TODO:
# - user for running daemon + fix perms to config files to be readable
#   only for daemon user
# - nobody MUST NOT own any file!
# - add deps to frontend

%include        /usr/lib/rpm/macros.perl
%define	_rc	RC1
Summary:	Log Jabber conversations to a peer-visible database
Summary(pl):	Logowanie rozmów przez Jabbera do bazy danych widocznej dla drugiej strony
Name:		bandersnatch
Version:	0.4
Release:	0.%{_rc}.1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.funkypenguin.co.za/filestore2/download/5/%{name}-%{version}.%{_rc}.tar.gz
# Source0-md5:	e49075fce771f7c1ad7ff485eef76231
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-utf8.patch
URL:		http://www.funkypenguin.co.za/taxonomy/term/5
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tool to log Jabber instant messaging traffic. Is designed for a
corporate intranet environment in where the administrators can be
monitor the use/abuse of their Jabber servers.

%description -l pl
Narzêdzie do logowania ruchu przez komunikatora Jabber. Zosta³o
zaprojektowane do u¿ywania w ¶rodowisku sieci korporacyjnych, gdzie
administratorzy mog± monitorowaæ u¿ywanie/nadu¿ywanie serwerów
Jabbera.

%package frontend
Summary:	bandersnatch web frontend
Summary(pl):	Interfejs WWW dla bandersnatcha
Group:		Applications/WWW
Requires:	php-pear-Auth
Requires:	php-pear-DB
Requires:	php-pear-HTML_Template_IT

%description frontend
bandersnatch web frontend.

%description frontend -l pl
Interfejs WWW dla bandersnatcha.

%prep
%setup -q -n %{name}-%{version}.%{_rc}
%patch0 -p1

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
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc *.sql doc/*
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,nobody) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.xml
# FIXME nobody user/group can't own files! -adapter.awk
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%files frontend
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%{_datadir}/%{name}-frontend
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}*.cfg
