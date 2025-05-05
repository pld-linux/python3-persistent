#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	persistent
Summary:	Automatic persistence for Python objects
Summary(pl.UTF-8):	Automatyczne trwałe obiekty w Pythonie
Name:		python3-%{module}
Version:	6.1
Release:	1
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/persistent/
Source0:	https://files.pythonhosted.org/packages/source/p/persistent/%{module}-%{version}.tar.gz
# Source0-md5:	48ec39a6620f1f838d09b5a42014f4db
Patch0:		missing-header.patch
URL:		https://www.zope.dev/
BuildRequires:	python3-cffi >= 1.17
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-manuel
BuildRequires:	python3-zope.deferredimport
BuildRequires:	python3-zope.interface
BuildRequires:	python3-zope.testrunner
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a generic persistence implementation for Python.
It forms the core protocol for making objects interact "transparently"
with a database such as the ZODB.

%description -l pl.UTF-8
Ten pakiet zawiera ogólną implementację trwałych danych dla Pythona.
Tworzy główny protokół, pozwalający obiektom w sposób przezroczysty
współpracować z bazą danych taką jak ZODB.

%package devel
Summary:	Header files for C extensions using persisteny module
Summary(pl.UTF-8):	Pliki nagłówkowe dla rozszerzeń w C korzystających z modułu persistent
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python3-devel >= 1:3.8

%description devel
Header files for C extensions using persisteny module.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla rozszerzeń w C korzystających z modułu
persistent.

%package apidocs
Summary:	API documentation for Python persistent module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona persistent
Group:		Documentation

%description apidocs
API documentation for Python persistent module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona persistent.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
zope-testrunner-3 --test-path=src -v
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/persistent/*.[ch]
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/persistent/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%dir %{py3_sitedir}/persistent
%{py3_sitedir}/persistent/*.py
%attr(755,root,root) %{py3_sitedir}/persistent/*.so
%{py3_sitedir}/persistent/__pycache__
%{py3_sitedir}/persistent-%{version}-py*.egg-info

%files devel
%defattr(644,root,root,755)
%{py3_incdir}/persistent

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,api,*.html,*.js}
%endif
