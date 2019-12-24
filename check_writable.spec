%define version          2.0.1
%define release          0
%define sourcename       check_writable
%define packagename      nagios-plugins-check-writables
%define nagiospluginsdir %{_libdir}/nagios/plugins

# No binaries in this package
%define debug_package    %{nil}

Summary:       Nagios plugin that checks if one or more directories are writable
Name:          %{packagename}
Version:       %{version}
Obsoletes:     check_writable
Release:       %{release}%{?dist}
License:       GPLv3+
Packager:      Matteo Corti <matteo@corti.li>
Group:         Applications/System
BuildRoot:     %{_tmppath}/%{packagename}-%{version}-%{release}-root-%(%{__id_u} -n)
URL:           https://github.com/matteocorti/check_writable
Source:        https://github.com/matteocorti/%{sourcename}/releases/download/v%{version}/%{sourcename}-%{version}.tar.gz

# Fedora build requirement (not needed for EPEL{4,5})
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More)
BuildRequires: perl(Readonly)

Requires:      nagios-plugins
Requires:      hddtemp
# Yum security plugin RPM:
#    Fedora             : yum-plugin-security (virtual provides yum-security)
#    Red Hat Enterprise : yum-security
# Requires:  yum-security

%description
check_writable is a Nagios plugin that checks if one or more
directories are writable by:

- checking that the supplied directory is indeed a directory
- checking if the the filesystem permissions are OK
- creating a temporary file
- writing random data to the temporary file (and reading it back)

It return a critical status if one of the tests fails

%prep
%setup -q -n %{sourcename}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor \
    INSTALLSCRIPT=%{nagiospluginsdir} \
    INSTALLVENDORSCRIPT=%{nagiospluginsdir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name "*.pod" -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS Changes NEWS README TODO COPYING COPYRIGHT
%{nagiospluginsdir}/%{sourcename}
%{_mandir}/man1/%{sourcename}.1*

%changelog
* Tue Dec 24 2019 Matteo Corit <matteo@corti.li> - 2.0.1
- Fixed the spec file

