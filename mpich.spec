Summary:	Portable MPI Model Implementation
Summary(pl):	Przeno¶na implementacja standardu MPI
Name:		mpich
Version:	1.2.6
Release:	2
License:	Open source (MPICH), BSD-like (MPI-2-C++)
Group:		Development/Libraries
Source0:	ftp://ftp.mcs.anl.gov/pub/mpi/%{name}-%{version}.tar.bz2
# Source0-md5:	4c4e2bc23b5f1b73b577bc630f782913
Patch0:		%{name}-fuckssh.patch
Patch1:		%{name}-opt.patch
Patch2:		http://squishy.monkeysoft.net/mpich/%{name}-1.2.5-oM.patch
URL:		http://www-unix.mcs.anl.gov/mpi/
BuildRequires:	gcc-g77
BuildRequires:	libstdc++-devel
Provides:	mpi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MPICH is an open-source, portable implementation of the
Message-Passing Interface Standard. It contains a complete
implementation of version 1.2 of the MPI Standard and also significant
parts of MPI-2, particularly in the area of parallel I/O.

%description -l pl
MPICH jest wolnodostêpn± implementacj± standardu MPI (Message-Passing
Interface). Zawiera pe³n± implementacjê wersji MPI 1.2 oraz znaczne
czê¶ci wersji MPI-2, szczególnie w zakresie równoleg³ej komunikacji.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
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
	-opt="%{rpmcflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

# really awful
DESTDIR=$RPM_BUILD_ROOT ; export DESTDIR
%{__make} install

# fix symlinks
(cd $RPM_BUILD_ROOT%{_libdir}
rm -f libfmpich.so libmpich.so libpmpich.so
ln -sf libfmpich.so.*.* libfmpich.so
ln -sf libmpich.so.*.* libmpich.so
ln -sf libpmpich.so.*.* libpmpich.so
)

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
