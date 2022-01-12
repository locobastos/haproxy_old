%define haproxy_user    haproxy
%define haproxy_group   %{haproxy_user}
%define haproxy_homedir %{_localstatedir}/lib/haproxy
%define haproxy_confdir %{_sysconfdir}/haproxy
%define haproxy_datadir %{_datadir}/haproxy

%global _hardened_build 1
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:             haproxy
Version:          2.4.9
Release:          1%{?dist}

Summary:          HAProxy reverse proxy for high availability environments

Vendor:           HAProxy Technologies, LLC
License:          GPLv2+
URL:              http://www.haproxy.org/
Packager:         Bastien MARTIN (https://github.com/locobastos/haproxy)

Source0:          http://www.haproxy.org/download/2.4/src/haproxy-%{version}.tar.gz
Source1:          %{name}.service
Source2:          %{name}.cfg
Source3:          %{name}.logrotate
Source4:          %{name}.sysconfig
Source5:          halog.1

BuildRequires:    epel-rpm-macros
BuildRequires:    openssl-devel
BuildRequires:    pcre2-devel
BuildRequires:    systemd-devel
BuildRequires:    systemd-units
BuildRequires:    zlib-devel

Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
HAProxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
 - route HTTP requests depending on statically assigned cookies
 - spread load among several servers while assuring server persistence
   through the use of HTTP cookies
 - switch to backup servers in the event a main one fails
 - accept connections to special ports dedicated to service monitoring
 - stop accepting connections without breaking existing ones
 - add, modify, and delete HTTP headers in both directions
 - block requests matching particular patterns
 - report detailed status to authenticated users from a URI
   intercepted from the application

%prep
%setup -q


%build
regparm_opts=
%ifarch %ix86 x86_64
regparm_opts="USE_REGPARM=1"
%endif

%{__make} %{?_smp_mflags} CPU="generic" TARGET="linux-glibc" USE_OPENSSL=1 USE_PCRE2=1 USE_ZLIB=1 USE_LUA=1 USE_CRYPT_H=1 USE_SYSTEMD=1 USE_LINUX_TPROXY=1 USE_GETADDRINFO=1 ${regparm_opts} ADDINC="%{optflags}" ADDLIB="%{__global_ldflags}" EXTRA_OBJS="" LUA_INC=%{_lua_bin} LUA_LIB=%{_lua_bin}

%{__make} admin/halog/halog

pushd admin/iprange
%{__make} iprange OPTIMIZE="%{optflags} %{build_ldflags}"
popd

%install
%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix} TARGET="linux-glibc"
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{haproxy_confdir}/%{name}.cfg
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -D -m 0644 %{SOURCE5} %{buildroot}%{_mandir}/man1/halog.1
%{__install} -d -m 0755 %{buildroot}%{haproxy_homedir}
%{__install} -d -m 0755 %{buildroot}%{haproxy_datadir}
%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -p -m 0755 ./admin/halog/halog %{buildroot}%{_bindir}/halog
%{__install} -p -m 0755 ./admin/iprange/iprange %{buildroot}%{_bindir}/iprange
%{__install} -p -m 0644 ./examples/errorfiles/* %{buildroot}%{haproxy_datadir}

for httpfile in $(find ./examples/errorfiles/ -type f)
do
    %{__install} -p -m 0644 $httpfile %{buildroot}%{haproxy_datadir}
done

%{__rm} -rf ./examples/errorfiles/

find ./examples/* -type f ! -name "*.cfg" -exec %{__rm} -f "{}" \;

for textfile in $(find ./ -type f -name '*.txt')
do
    %{__mv} $textfile $textfile.old
    iconv --from-code ISO8859-1 --to-code UTF-8 --output $textfile $textfile.old
    %{__rm} -f $textfile.old
done

%pre
getent group %{haproxy_group} >/dev/null || groupadd -r %{haproxy_group}
getent passwd %{haproxy_user} >/dev/null || useradd -r -g %{haproxy_user} -d %{haproxy_homedir} -s /sbin/nologin -c "haproxy" %{haproxy_user}
exit 0

%post
%systemd_post %{name}.service
echo ""
echo ""
echo -e "\e[1;31m ==============================================================================\e[0m"
echo -e "\e[1;31m  WARNING: This HAProxy RPM is not an official one. \e[0m"
echo ""
echo -e "\e[1;31m  To report bug fully related to HAProxy, please use their GitHub page:\e[0m"
echo -e "\e[1;31m        https://github.com/haproxy/haproxy/issues\e[0m"
echo ""
echo -e "\e[1;31m  To report bug related to this RPM itself or the files inside "SOURCES" folder,\e[0m"
echo -e "\e[1;31m  please use my GitHub page: https://github.com/locobastos/haproxy/issues\e[0m"
echo -e "\e[1;31m ==============================================================================\e[0m"
echo ""
echo ""


%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,-)
%doc doc/* examples/*
%doc CHANGELOG README ROADMAP VERSION
%license LICENSE
%dir %{haproxy_homedir}
%dir %{haproxy_confdir}
%dir %{haproxy_datadir}
%{haproxy_datadir}/*
%config(noreplace) %{haproxy_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_sbindir}/%{name}
%{_bindir}/halog
%{_bindir}/iprange
%{_mandir}/man1/*
%attr(-,%{haproxy_user},%{haproxy_group}) %dir %{haproxy_homedir}
