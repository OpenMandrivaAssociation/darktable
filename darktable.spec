# Keep libraries private
%if %{_use_internal_dependency_generator}
%define __noautoprov '(.*)\\.so(.*)'
%define __noautoreq 'libdarktable\\.so(.*)'
%endif

# Workaround for https://bugs.llvm.org/show_bug.cgi?id=50981
%global optflags %{optflags} -g0

Summary:	Utility to organize and develop raw images
Name:		darktable
Version:	4.0.0
Release:	1
Group:		Graphics
License:	GPLv3+
Url:		http://www.darktable.org
Source0:	https://github.com/darktable-org/darktable/releases/download/release-%{version}/%{name}-%{version}.tar.xz
Source100:	%{name}.rpmlintrc
# https://github.com/darktable-org/darktable/issues/2093
#Patch0:		fix-aarch64.patch
# Needed or build failed with: 
# builddir/build/BUILD/darktable-3.6.1/src/common/darktable.h:576:3: error: unexpected OpenMP clause 'nontemporal' in directive '#pragma omp simd'
# for_each_channel(k,aligned(in,out:16) dt_omp_nontemporal(out)) out[k] = in[k];
Patch1:		darktable-3.6.0-fix-openmp-version.patch
Patch2:		darktable-3.8.0-clang.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	gettext-devel
#BuildRequires:	gomp-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(colord-gtk)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	pkgconfig(flickcurl)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gnome-keyring-1)
BuildRequires:	pkgconfig(GraphicsMagick)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libavif)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(lensfun)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libgphoto2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pugixml-devel
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libssh)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(osmgpsmap-1.0)
BuildRequires:	cups-devel
BuildRequires:  gmic-devel
BuildRequires:	po4a
# For OpenCL
BuildRequires:	llvm
BuildRequires:	llvm-devel
BuildRequires:	clang
BuildRequires:	lld
BuildRequires:	spirv-llvm-translator

BuildRequires:  lldb
# Dirty fix
BuildRequires:	%{_lib}gpuruntime
BuildRequires:	llvm-static-devel
BuildRequires:	%{_lib}LLVMDemangle-static-devel
BuildRequires:	%{_lib}LLVMSupport-static-devel
BuildRequires:	%{_lib}mlir
BuildRequires:	llvm-bolt

%description
Darktable is an open source photography workflow application and RAW developer.
A virtual lighttable and darkroom for photographers. It manages your digital
negatives in a database, lets you view them through a zoomable lighttable
and enables you to develop raw images and enhance them.

%files -f %{name}.lang
#doc doc/README doc/AUTHORS doc/LICENSE doc/TRANSLATORS
%{_bindir}/%{name}*
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/darktable.appdata.xml
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}*
%{_mandir}/man1/%{name}*
%{_mandir}/*
%config %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

#----------------------------------------------------------------------------

%prep
%autosetup -p1
%cmake \
	-DCMAKE_LIBRARY_PATH:PATH=%{_libdir} \
	-DDONT_INSTALL_GCONF_SCHEMAS:BOOLEAN=ON \
	-DCMAKE_BUILD_TYPE:STRING=Release \
	-DBINARY_PACKAGE_BUILD=1 \
	-DPROJECT_VERSION:STRING="%{version}" \
	-DINSTALL_IOP_EXPERIMENTAL:BOOLEAN=ON \
	-G Ninja

%build
%ninja_build -C build

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%ninja_install -C build

#to find libdarktable.so
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf << EOF
%{_libdir}/%{name}
EOF

%find_lang %{name}

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
rm -rf %{buildroot}%{_datadir}/doc/%{name}
