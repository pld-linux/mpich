Summary:	Portable MPI Model Implementation
Summary(pl.UTF-8):	Przenośna implementacja standardu MPI
Name:		mpich
Version:	1.2.7p1
Release:	4
License:	Open source (MPICH), BSD-like (MPI-2-C++)
Group:		Development/Libraries
Source0:	ftp://ftp.mcs.anl.gov/pub/mpi/%{name}-%{version}.tar.bz2
# Source0-md5:	4fc0f20bddfbd5061a11047cf2d17d31
Patch0:		%{name}-fuckssh.patch
Patch1:		%{name}-opt.patch
Patch2:		http://squishy.monkeysoft.net/mpich/%{name}-1.2.5-oM.patch
Patch3:		mpich-c++.patch
URL:		http://www-unix.mcs.anl.gov/mpi/
BuildRequires:	gcc-g77
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
Provides:	mpi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MPICH is an open-source, portable implementation of the
Message-Passing Interface Standard. It contains a complete
implementation of version 1.2 of the MPI Standard and also significant
parts of MPI-2, particularly in the area of parallel I/O.

%description -l pl.UTF-8
MPICH jest wolnodostępną implementacją standardu MPI (Message-Passing
Interface). Zawiera pełną implementację wersji MPI 1.2 oraz znaczne
części wersji MPI-2, szczególnie w zakresie równoległej komunikacji.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

sed -i -e 's|RCPCOMMAND-rcp|RCPCOMMAND-scp|' mpid/ch_p4/mpirun.ch_p4.in

%build
RSHCOMMAND=/usr/bin/ssh ; export RSHCOMMAND
RCPCOMMAND=/usr/bin/scp ; export RCPCOMMAND
# note: can't run autoconf - we must patch configure not only configure.in
# also, don't change it to %%configure - it won't work
# no configure options for sysconfdir and messagecat_dir :/
sysconfdir=%{_sysconfdir} \
messagecat_dir=%{_libdir} \
./configure \
	--prefix=%{_prefix} \
	--exec_prefix=%{_prefix} \
	--includedir=%{_includedir} \
	--sharedlib=%{_libdir} \
	--libdir=%{_libdir} \
	--datadir=%{_datadir}/%{name} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--mandir=%{_mandir} \
	--docdir=%{_docdir} \
	-opt="%{rpmcflags} -fPIC -DPIC" \
	-fc=gfortran

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

# really awful
DESTDIR=$RPM_BUILD_ROOT ; export DESTDIR
%{__make} -j1 install

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv -f $RPM_BUILD_ROOT%{_prefix}/examples/* \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

(cd $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
rm -f mpirun MPI-2-C++/mpirun
ln -sf %{_bindir}/mpirun mpirun
ln -sf %{_bindir}/mpirun MPI-2-C++/mpirun
)

# argh... where came that 4 from???
for f in $RPM_BUILD_ROOT%{_mandir}/man4/*.4 ; do
	mv -f "$f" $RPM_BUILD_ROOT%{_mandir}/man3/`basename "$f" .4`.3
done

for f in HISTORY LICENSE README TODO ; do
	mv -f MPI-2-C++/$f $f.MPI-2-C++
done

rm -rf $RPM_BUILD_ROOT%{_prefix}/{doc,logfiles,www}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/*.ps* COPYRIGHT README KnownBugs
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/lib*.so*
%{_libdir}/lib*.a
%{_libdir}/mpe_prof.o
%{_sysconfdir}/mpichversion.c
%{_sysconfdir}/mpichconf.h.dat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mpi*.conf
%{_includedir}/*.h
%{_includedir}/mpi2c++
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_datadir}/mpich
%{_examplesdir}/%{name}-%{version}
