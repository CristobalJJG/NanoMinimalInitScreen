Name:           fedora-power-menu
Version:        0.1.0
Release:        2%{?dist}
Summary:        GTK power and session menu for Fedora
License:        MIT
URL:            https://example.invalid/fedora-power-menu
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita

%description
A small GTK 4 application that provides confirmed actions to power off,
reboot, or end the current Fedora session.

%prep
%autosetup -p1

%build
# Python source requires no compilation.

%install
install -D -m 0755 power_menu.py %{buildroot}%{_bindir}/fedora-power-menu
install -D -m 0644 com.example.FedoraPowerMenu.desktop \
  %{buildroot}%{_datadir}/applications/com.example.FedoraPowerMenu.desktop
install -D -m 0644 com.example.FedoraPowerMenu.desktop \
  %{buildroot}%{_datadir}/fedora-power-menu/com.example.FedoraPowerMenu.desktop
install -D -m 0644 com.example.FedoraPowerMenu.appdata.xml \
  %{buildroot}%{_metainfodir}/com.example.FedoraPowerMenu.appdata.xml

%files
%{_bindir}/fedora-power-menu
%{_datadir}/applications/com.example.FedoraPowerMenu.desktop
%{_datadir}/fedora-power-menu/com.example.FedoraPowerMenu.desktop
%{_metainfodir}/com.example.FedoraPowerMenu.appdata.xml

%changelog
* Thu Jan 01 2026 Dashboard Maintainer <maintainer@example.invalid> - 0.1.0-1
- Initial Fedora GTK 4 power menu.
