%define		_enable_debug_packages	0
Summary:	HP Command Line Smart Storage Administrator
Name:		hpssacli
Version:	1.50
Release:	4.0
License:	not distributable (HP Software License Agreement)
Group:		Applications
# These downloads are available for customers according to the terms in the HP
# Software License Agreement. Certain software may require a valid warranty,
# current support contract with HP, or a license fee.
Source0:	ftp://ftp.hp.com/pub/softlib2/software1/pubsw-linux/p1865889733/v83803/%{name}-%{version}-%{release}.i386.rpm
# NoSource0-md5:	ab21e9fd6649bf7e4b99a1818de74c48
NoSource:	0
Source1:	ftp://ftp.hp.com/pub/softlib2/software1/pubsw-linux/p215599048/v83802/%{name}-%{version}-%{release}.x86_64.rpm
# NoSource1-md5:	23f144bdeac050313adf6773379d19ff
NoSource:	1
URL:		http://h20566.www2.hp.com/portal/site/hpsc/template.PAGE/public/psi/swdDetails/?swItem=MTX_1463d8b5d39d411c8f264163a7
# hpacucli dlopens libemsdm.so, libqlsdm.so at runtime
Suggests:	fibreutils
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep libstdc++.so.6

%description
The HP Smart Storage Administrator CLI (HP SSACLI) is a
commandline-based disk configuration program that helps you configure,
manage, diagnose, and monitor HP ProLiant Smart Array Controllers and
now other storage devices as well, such as host bus a

Supported Controllers:
- Smart Array P410i Controller
- Smart Array P411 Controller
- Smart Array P212 Controller
- Smart Array P712m Controller
- Smart Array B110i SATA RAID
- Smart Array P812 Controller
- Smart Array P220i Controller
- Smart Array P222 Controller
- Smart Array P420 Controller
- Smart Array P420i Controller
- Smart Array P421 Controller
- Smart Array P822 Controller
- Smart Array P721m Controller
- Dynamic Smart Array B320i RAID
- Dynamic Smart Array B120i RAID
- Smart Array P430 Controller
- Smart Array P431 Controller
- Smart Array P731m Controller

%prep
%setup -qcT
%ifarch %{ix86}
rpm2cpio %{SOURCE0} | cpio -dimu
%else
rpm2cpio %{SOURCE1} | cpio -dimu
%endif

mv opt/hp/%{name}/bld/* .
mv %{name}-%{version}-%{release}.*.txt %{name}.txt

mv usr/man .
gzip -d man/*/*.gz

# fix man paths
%{__sed} -i -e '
	s#/opt/hp/%{name}/bld/%{name}-VERSION.PLATFORM.txt#%{_docdir}/%{name}-%{version}/%{name}.txt#
' man/man8/*

cat <<'EOF' > wrapper.sh
#!/bin/sh
PROGRAM=${0##*/}
if [ $(uname -m) = "ia64" ]; then
	exec prctl --unaligned=silent %{_libdir}/$PROGRAM "$@"
else
	exec %{_libdir}/$PROGRAM "$@"
fi
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir},%{_mandir}/man8}
install -p hpssacli hpssascripting $RPM_BUILD_ROOT%{_libdir}
install -p wrapper.sh $RPM_BUILD_ROOT%{_sbindir}/%{name}
ln $RPM_BUILD_ROOT%{_sbindir}/{%{name},hpssascripting}

cp -p man/man8/* $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{name}.txt %{name}.license
%attr(755,root,root) %{_libdir}/hpssacli
%attr(755,root,root) %{_libdir}/hpssascripting
%attr(755,root,root) %{_sbindir}/hpssacli
%attr(755,root,root) %{_sbindir}/hpssascripting
%{_mandir}/man8/hpssacli.8*
