Summary:	Portable MPI Model Implementation
Summary(pl.UTF-8):	Przenośna implementacja standardu MPI
Name:		mpich
Version:	3.1.3
Release:	3
License:	BSD-like
Group:		Development/Libraries
Source0:	http://www.mpich.org/static/downloads/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	93cb17f91ac758cbf9174ecb03563778
Patch0:		%{name}-sh.patch
Patch1:		%{name}-opalink.patch
Patch2:		x32-misdetected-as-i386.patch
URL:		http://www.mpich.org/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.12.3
BuildRequires:	ftb-devel
BuildRequires:	gcc-fortran
BuildRequires:	hwloc-devel >= 1.9.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	openpa-devel
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
Group:		Development
Requires:	%{name} = %{version}-%{release}
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I confdb
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-hwloc-prefix=system \
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
%attr(755,root,root) %{_libdir}/libmpicxx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmpicxx.so.12
%attr(755,root,root) %{_libdir}/libmpifort.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmpifort.so.12
%{_mandir}/man1/hydra_nameserver.1*
%{_mandir}/man1/hydra_persist.1*
%{_mandir}/man1/hydra_pmi_proxy.1*
%{_mandir}/man1/mpiexec.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mpic++
%attr(755,root,root) %{_bindir}/mpicc
%attr(755,root,root) %{_bindir}/mpicxx
%attr(755,root,root) %{_bindir}/mpif77
%attr(755,root,root) %{_bindir}/mpif90
%attr(755,root,root) %{_bindir}/mpifort
%attr(755,root,root) %{_libdir}/libmpi.so
%attr(755,root,root) %{_libdir}/libmpicxx.so
%attr(755,root,root) %{_libdir}/libmpifort.so
%attr(755,root,root) %{_libdir}/libfmpich.so
%attr(755,root,root) %{_libdir}/libmpich.so
%attr(755,root,root) %{_libdir}/libmpichcxx.so
%attr(755,root,root) %{_libdir}/libmpichf90.so
%attr(755,root,root) %{_libdir}/libmpl.so
%{_libdir}/libmpi.la
%{_libdir}/libmpicxx.la
%{_libdir}/libmpifort.la
%{_includedir}/mpi*.h
%{_includedir}/mpi*.mod
%{_pkgconfigdir}/mpich.pc
%{_mandir}/man1/mpicc.1*
%{_mandir}/man1/mpicxx.1*
%{_mandir}/man1/mpif77.1*
%{_mandir}/man1/mpifort.1*
%{_mandir}/man3/MPIX_*.3*
%{_mandir}/man3/MPI_*.3*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libmpi.a
%{_libdir}/libmpicxx.a
%{_libdir}/libmpifort.a
