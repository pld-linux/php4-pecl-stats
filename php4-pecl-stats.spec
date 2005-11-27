%define		_modname	stats
%define		_status		stable
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - extension with routines for statistical computation
Summary(pl):	%{_modname} - rozszerzenie z funkcjami do wykonywania obliczeñ statystycznych
Name:		php4-pecl-%{_modname}
Version:	1.0.0
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	aaab90d3b8c2da8db07c09305a8feebc
URL:		http://pecl.php.net/package/stats/
BuildRequires:	php4-devel >= 3:4.3.0
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Extension that provides few dozens routines for statistical
computation, such as stats_absolute_deviation(), stats_covariance(),
harmonic_mean() and others.

In PECL status of this extension is: %{_status}.

%description -l pl
To rozszerzenie dostarcza wiele ró¿nych funkcji do wykonywania
obliczeñ statystycznych, takich jak stats_absolute_deviation(),
stats_covariance(), harmonic_mean() i inne.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,TODO}
%doc %{_modname}-%{version}/tests
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
