# Lists copied from gcc.spec
# Current as of 13.2.1 (lines 66, 86, and 76, respectively).
# Note that asan and ubsan are available on all Fedora primary architectures;
# tsan is missing on i686 only.
%ifarch %{ix86} %{x86_64} ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} %{aarch64}
%global arch_has_asan 1
%endif
%ifarch %{ix86} %{x86_64} ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} %{aarch64}
%global arch_has_ubsan 1
%endif
%ifarch %{x86_64} ppc64 ppc64le %{aarch64} s390x
%global arch_has_tsan 1
%endif

# By default, enable sanitizers whenever they are available on the architecture.
%bcond asan 0
%bcond ubsan 0
%bcond tsan 0

Name:           wlcs
Version:        1.7.0
Release:        1
Summary:        Wayland Conformance Test Suite
License:        GPL-3.0-only AND (LGPL-2.0-only OR LGPL-3.0-only)
URL:            https://github.com/MirServer/wlcs
Source:         https://github.com/MirServer/wlcs/archive/v%{version}/wlcs-%{version}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  cmake(GTest)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-scanner)

BuildSystem:	cmake
BuildOption:	-DWLCS_BUILD_ASAN=%{?with_asan:ON}%{?!with_asan:OFF}
BuildOption:	-DWLCS_BUILD_TSAN=%{?with_tsan:ON}%{?!with_tsan:OFF}
BuildOption:	-DWLCS_BUILD_UBSAN=%{?with_ubsan:ON}%{?!with_ubsan:OFF}

%if %{with asan}
BuildRequires:  asan-devel
%endif
%if %{with ubsan}
BuildRequires:  ubsan-devel
%endif
%if %{with tsan}
BuildRequires:  tsan-devel
%endif

%description
wlcs aspires to be a protocol-conformance-verifying test suite usable by
Wayland compositor implementors.

It is growing out of porting the existing Weston test suite to be run in Mir’s
test suite, but it is designed to be usable by any compositor.

wlcs relies on compositors providing an integration module, providing wlcs with
API hooks to start a compositor, connect a client, move a window, and so on.

This makes both writing and debugging tests easier - the tests are (generally)
in the same address space as the compositor, so there is a consistent global
clock available, it’s easier to poke around in compositor internals, and
standard debugging tools can follow control flow from the test client to the
compositor and back again.

%package        devel
Summary:        Development files for wlcs
Requires:       wlcs%{?_isa} = %{version}-%{release}

%description    devel
wlcs aspires to be a protocol-conformance-verifying test suite usable by
Wayland compositor implementors.

The wlcs-devel package contains libraries and header files for developing
Wayland compositor tests that use wlcs.

%prep -a
# -Werror makes sense for upstream CI, but is too strict for packaging
sed -r -i 's/-Werror //' CMakeLists.txt

%files
%license COPYING.*
%doc README.rst
%{_libexecdir}/wlcs/

%files devel
%doc README.rst
%doc example/
%{_includedir}/wlcs/
%{_libdir}/pkgconfig/wlcs.pc
