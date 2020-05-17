%define debug_package %{nil}

Name:           libasicamera
Version:        1.14.1227
Release:        0
Summary:        ZWO ASI camera SDK
License:        expat
URL:            http://astronomy-imaging-camera.com/
Prefix:         %{_prefix}
Provides:       libasicamera = %{version}-%{release}
Obsoletes:      libasicamera < 1.14.1227
Requires:       libusbx
Source:         libasicamera-%{version}.tar.gz
Patch0:         pkg-config.patch
Patch1:         udev-rules.patch

%description
libASICamera is a user-space driver for ZWO ASI astronomy cameras.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libasicamera-devel = %{version}-%{release}
Obsoletes:      libasicamera-devel < 1.14.1227

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libasicamera2.pc.in > libasicamera2.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/demo
mkdir -p %{buildroot}/etc/udev/rules.d

case %{_arch} in
  i386)
    cp lib/x86/libASICamera*.so.%{version} %{buildroot}%{_libdir}
    cp lib/x86/libASICamera*.a %{buildroot}%{_libdir}
    ;;
  x86_64)
    cp lib/x64/libASICamera*.so.%{version} %{buildroot}%{_libdir}
    cp lib/x64/libASICamera*.a %{buildroot}%{_libdir}
    ;;
  *)
    echo "unknown target architecture %{_arch}"
    exit 1
    ;;
esac

ln -sf %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.1
cp include/*.h %{buildroot}%{_includedir}
cp *.pc %{buildroot}%{_libdir}/pkgconfig
cp doc/* %{buildroot}%{_docdir}/%{name}-%{version}
cp license.txt %{buildroot}%{_docdir}/%{name}-%{version}
cp lib/README.txt %{buildroot}%{_docdir}/%{name}-%{version}
cp demo/Makefile %{buildroot}%{_docdir}/%{name}-%{version}/demo
cp demo/*.* %{buildroot}%{_docdir}/%{name}-%{version}/demo
cp 70-asi-cameras.rules %{buildroot}/etc/udev/rules.d

%post
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%postun
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%files
%{_libdir}/*.so.*
%{_docdir}/%{name}-%{version}/*.txt
%{_sysconfdir}/udev/rules.d/*.rules

%files devel
%{_includedir}/ASICamera*.h
%{_libdir}/pkgconfig/%{name}*.pc
%{_libdir}/*.a
%{_docdir}/%{name}-%{version}/*.pdf
%{_docdir}/%{name}-%{version}/demo/Makefile
%{_docdir}/%{name}-%{version}/demo/*.*

%changelog
* Sun May 17 2020 James Fidell <james@openastroproject.org> - 1.14.1227-0
- Initial RPM release

