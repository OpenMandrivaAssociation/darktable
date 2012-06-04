%define _cmake_skip_rpath -DCMAKE_SKIP_RPATH:BOOL=OFF

Name:		darktable
Version:	1.0.4
Release:	%mkrel 1
Summary:	Utility to organize and develop raw images
Group:		Graphics
License:	GPLv3+
URL:		http://darktable.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	cmake
BuildRequires:	zlib-devel
BuildRequires:	sqlite3-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(librsvg-2.0) >= 2.26
BuildRequires:	libGConf2-devel
BuildRequires:	gtk2-devel
BuildRequires:	cairo-devel
BuildRequires:	libglade2.0-devel
BuildRequires:	lcms2-devel
BuildRequires:	libexiv-devel
BuildRequires:	lensfun-devel
BuildRequires:	GConf2
BuildRequires:	OpenEXR-devel >= 1.6
BuildRequires:	gphoto2-devel >= 2.4.5
BuildRequires:	curl-devel >= 7.18.0
BuildRequires:	flickcurl-devel
BuildRequires:	dbus-glib-devel >= 0.80
BuildRequires:	libgnome-keyring-devel >= 2.28.0
BuildRequires:	gnome-doc-utils
BuildRequires:	fop
BuildRequires:	desktop-file-utils

%description
Darktable is an open source photography workflow application and RAW developer.
A virtual lighttable and darkroom for photographers. It manages your digital
negatives in a database, lets you view them through a zoomable lighttable
and enables you to develop raw images and enhance them.

%package plugins-experimental
Summary:	Darktable plugins that are unstable, unfinished or likely-to-change-soon
Requires:	%{name} = %{version}-%{release}

%description plugins-experimental
Darktable is an open source photography workflow application and RAW developer.
A virtual lighttable and darkroom for photographers. It manages your digital
negatives in a database, lets you view them through a zoomable lighttable
and enables you to develop raw images and enhance them.

This package contains plugins being under development. They can be unstable
or broken, use at your own risk.

%prep
%setup -q

%build
%cmake \
	-DCMAKE_LIBRARY_PATH:PATH=%{_libdir} \
	-DDONT_INSTALL_GCONF_SCHEMAS:BOOLEAN=ON \
	-DCMAKE_BUILD_TYPE:STRING=Release \
	-DBINARY_PACKAGE_BUILD=1 \
	-DPROJECT_VERSION:STRING="%{name}-%{version}-%{release}" \
	-DINSTALL_IOP_EXPERIMENTAL:BOOLEAN=ON

%make

%install
rm -rf %{buildroot}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%makeinstall_std -C build

find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang %{name}
desktop-file-validate %{buildroot}/%{_datadir}/applications/darktable.desktop
rm -rf %{buildroot}%{_datadir}/doc/darktable

%files -f %{name}.lang
%doc doc/README doc/AUTHORS doc/LICENSE doc/TRANSLATORS
%{_bindir}/darktable*
%{_libdir}/darktable
%{_datadir}/applications/darktable.desktop
%{_datadir}/darktable
%{_iconsbasedir}/*/apps/darktable.*
%{_datadir}/man/man1/darktable.1.*

#files plugins-experimental
