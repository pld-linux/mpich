#
# Conditional build:
%bcond_with	blcr	# blcr application checkpointing support (no support for recent kernels)
#
Summary:	Portable MPI Model Implementation
Summary(pl.UTF-8):	Przenośna implementacja standardu MPI
Name:		mpich
Version:	3.1.4
Release:	1
License:	BSD-like
Group:		Development/Libraries
Source0:	https://www.mpich.org/static/downloads/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2ab544607986486562e076b83937bba2
Patch0:		%{name}-sh.patch
Patch1:		x32-misdetected-as-i386.patch
URL:		https://www.mpich.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.12.3
%{?with_blcr:BuildRequires:	blcr-devel}
BuildRequires:	ftb-devel
BuildRequires:	gcc-fortran
BuildRequires:	hwloc-devel >= 1.9.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	openpa-devel
BuildRequires:	rpmbuild(macros) >= 1.750
Requires:	hwloc-libs >= 1.9.0
Provides:	mpi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MPICH is a high-performance and widely portable implementation of the
MPI-3.0 standard from the Argonne National Laboratory. This release
has all MPI 3.0 functions and features required by the standard with
the exception of support for the "external32" portable I/O format and
user-defined data representations for I/O.

This package contains MPICH shared libraries and runtime utilities,
including Hydra PM.

%description -l pl.UTF-8
MPICH to wysoko wydajna i przenośna implementacja standardu MPI-3.0
pochodząca z Argonne National Laboratory. To wydanie zawiera całą
funkcjonalność i możliwości MPI 3.0 wymagane przez standard z
wyjątkiem obsługi przenośnego formatu we-wy "external32" oraz
definiowanych przez użytkownika reprezentacji danych dla we/wy.

Ten pakiet zawiera biblioteki współdzielone MPICH oraz narzędzia
uruchomieniowe, w tym Hydra PM.

%package devel
Summary:	MPICH header files and development tools
Summary(pl.UTF-8):	Pliki nagłówkowe oraz narzędzia programistyczne MPICH
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openpa-devel
Provides:	mpi-devel

%description devel
MPICH header files and development tools.

%description devel
Pliki nagłówkowe oraz narzędzia programistyczne MPICH.

%package static
Summary:	MPICH static libraries
Summary(pl.UTF-8):	Biblioteki statyczne MPICH
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	mpi-static

%description static
MPICH static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne MPICH.

%package c++
Summary:	MPICH C++ library
Summary(pl.UTF-8):	Biblioteka MPICH dla C++
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	mpi-c++

%description c++
MPICH C++ library.

%description c++ -l pl.UTF-8
Biblioteka MPICH dla C++.

%package c++-devel
Summary:	MPICH C++ development package
Summary(pl.UTF-8):	Pakiet programistyczny MPICH dla C++
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel
Provides:	mpi-c++-devel

%description c++-devel
MPICH C++ development package.

%description c++-devel -l pl.UTF-8
Pakiet programistyczny MPICH dla C++.

%package c++-static
Summary:	MPICH C++ static library
Summary(pl.UTF-8):	Biblioteka statyczna MPICH dla C++
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}
Provides:	mpi-c++-static

%description c++-static
MPICH C++ static library.

%description c++-static -l pl.UTF-8
Biblioteka statyczna MPICH dla C++.

%package fortran
Summary:	MPICH Fortran library
Summary(pl.UTF-8):	Biblioteka MPICH dla Fortranu
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	mpi-fortran

%description fortran
MPICH Fortran library.

%description fortran -l pl.UTF-8
Biblioteka MPICH dla Fortranu.

%package fortran-devel
Summary:	MPICH Fortran development package
Summary(pl.UTF-8):	Pakiet programistyczny MPICH dla Fortranu
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-fortran = %{version}-%{release}
Requires:	gcc-fortran
Provides:	mpi-fortran-devel

%description fortran-devel
MPICH Fortran development package.

%description fortran-devel -l pl.UTF-8
Pakiet programistyczny MPICH dla Fortranu.

%package fortran-static
Summary:	MPICH Fortran static library
Summary(pl.UTF-8):	Biblioteka statyczna MPICH dla Fortranu
Group:		Development/Libraries
Requires:	%{name}-fortran-devel = %{version}-%{release}
Provides:	mpi-fortran-static

%description fortran-static
MPICH Fortran static library.

%description fortran-static -l pl.UTF-8
Biblioteka statyczna MPICH dla Fortranu.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%{__libtoolize}
%{__aclocal} -I confdb
%{__autoconf}
%{__autoheader}
%{__automake}
%define	gfortran_version	%(gfortran -dumpversion)
%if "%{_ver_ge '%{gfortran_version}' '10.0'}" == "1"
FFLAGS="%{rpmcflags} -fallow-argument-mismatch"
FCFLAGS="%{rpmcflags} -fallow-argument-mismatch"
%endif
%configure \
	--disable-silent-rules \
	%{?with_blcr:--enable-checkpointing} \
	--with-hwloc-prefix=system \
	%{!?with_blcr:--with-hydra-ckpointlib=none} \
	--with-openpa-prefix=system

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__rm} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/{cpi,cpi.o,examples.sln}

# see openpa.spec
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libopa.so

# PDFs packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/mpich

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%post	fortran -p /sbin/ldconfig
%postun	fortran -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES COPYRIGHT README README.envvar RELEASE_NOTES doc/{installguide/install.pdf,logging/logging.pdf,userguide/user.pdf}
%attr(755,root,root) %{_bindir}/hydra_nameserver
%attr(755,root,root) %{_bindir}/hydra_persist
%attr(755,root,root) %{_bindir}/hydra_pmi_proxy
%attr(755,root,root) %{_bindir}/mpichversion
%attr(755,root,root) %{_bindir}/mpiexec
%attr(755,root,root) %{_bindir}/mpiexec.hydra
%attr(755,root,root) %{_bindir}/mpirun
%attr(755,root,root) %{_bindir}/mpivars
%attr(755,root,root) %{_bindir}/parkill
%attr(755,root,root) %{_libdir}/libmpi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmpi.so.12
%{_mandir}/man1/hydra_nameserver.1*
%{_mandir}/man1/hydra_persist.1*
%{_mandir}/man1/hydra_pmi_proxy.1*
%{_mandir}/man1/mpiexec.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mpicc
%attr(755,root,root) %{_libdir}/libmpi.so
%attr(755,root,root) %{_libdir}/libmpich.so
%attr(755,root,root) %{_libdir}/libmpl.so
%{_libdir}/libmpi.la
%{_includedir}/mpi.h
%{_includedir}/mpio.h
%{_pkgconfigdir}/mpich.pc
%{_mandir}/man1/mpicc.1*
%{_mandir}/man3/MPIX_*.3*
%{_mandir}/man3/MPI_*.3*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libmpi.a

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmpicxx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmpicxx.so.12

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mpic++
%attr(755,root,root) %{_bindir}/mpicxx
%attr(755,root,root) %{_libdir}/libmpicxx.so
%attr(755,root,root) %{_libdir}/libmpichcxx.so
%{_libdir}/libmpicxx.la
%{_includedir}/mpicxx.h
%{_mandir}/man1/mpicxx.1*

%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libmpicxx.a

%files fortran
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmpifort.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmpifort.so.12

%files fortran-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mpif77
%attr(755,root,root) %{_bindir}/mpif90
%attr(755,root,root) %{_bindir}/mpifort
%attr(755,root,root) %{_libdir}/libmpifort.so
%attr(755,root,root) %{_libdir}/libfmpich.so
%attr(755,root,root) %{_libdir}/libmpichf90.so
%{_libdir}/libmpifort.la
%{_includedir}/mpif.h
%{_includedir}/mpiof.h
%{_includedir}/mpi*.mod
%{_mandir}/man1/mpif77.1*
%{_mandir}/man1/mpifort.1*

%files fortran-static
%defattr(644,root,root,755)
%{_libdir}/libmpifort.a
