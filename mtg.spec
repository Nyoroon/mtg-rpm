%define debug_package %{nil}

Name:		mtg
Version:	0.15
Release:	2%{?dist}
Summary:	MtProto proxy for Telegram writen on Go
License:	MIT
URL:		https://github.com/9seconds/%{name}

Source0:	%{url}/archive/%{version}.tar.gz
Source1:	mtg.service
Source2:	mtg.default

BuildRequires:	golang >= 1.11
BuildRequires:	systemd
%{?systemd_requires}


%description
MtProto proxy for Telegram writen on Go

%prep
%setup -q
cat > version.go <<EOF
package main
const version = "%{version} ($(go version)) [$(date -Ru)]"
EOF

%build
%make_build

%install
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
