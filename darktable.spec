%define _cmake_skip_rpath -DCMAKE_SKIP_RPATH:BOOL=OFF

Name:		darktable
Version:	1.1
Release:	1
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
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	gtk2-devel
BuildRequires:	cairo-devel
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	lcms2-devel
BuildRequires:	libexiv-devel
BuildRequires:	lensfun-devel
BuildRequires:	GConf2
BuildRequires:	OpenEXR-devel >= 1.6
BuildRequires:	pkgconfig(libgphoto2)
BuildRequires:	curl-devel >= 7.18.0
BuildRequires:	flickcurl-devel
BuildRequires:	dbus-glib-devel >= 0.80
BuildRequires:	libgnome-keyring-devel >= 2.28.0
BuildRequires:	gnome-doc-utils
BuildRequires:	fop
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	gomp-devel

%description
Darktable is an open source photography workflow application and RAW developer.
A virtual lighttable and darkroom for photographers. It manages your digital
negatives in a database, lets you view them through a zoomable lighttable
and enables you to develop raw images and enhance them.

%prep
%setup -q

%build
%cmake \
	-DCMAKE_LIBRARY_PATH:PATH=%{_libdir} \
	-DDONT_INSTALL_GCONF_SCHEMAS:BOOLEAN=ON \
	-DCMAKE_BUILD_TYPE:STRING=Release \
	-DBINARY_PACKAGE_BUILD=1 \
	-DPROJECT_VERSION:STRING="%{name}-%{EVRD}" \
	-DINSTALL_IOP_EXPERIMENTAL:BOOLEAN=ON

%make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%makeinstall_std -C build

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

%changelog
* Mon Jun 04 2012 Dmitry Mikhirev <dmikhirev@mandriva.org> 1.0.4-1mdv2012.0
+ Revision: 802462
- update to 1.0.4

* Tue May 29 2012 Andrey Bondrov <abondrov@mandriva.org> 1.0.3-1
+ Revision: 801072
- New version 1.0.3, don't package broken gconf schemas file

* Sat Dec 24 2011 Dmitry Mikhirev <dmikhirev@mandriva.org> 0.9.3-3
+ Revision: 745070
- file list fixed
- remove unneeded patch
- fix rpath
- BR fixed

* Thu Nov 10 2011 Andrey Smirnov <asmirnov@mandriva.org> 0.9.3-2
+ Revision: 729615
- Patch for proper rpath setting added
- imported package darktable

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added patch3 for new glib2 deprecated function errors

