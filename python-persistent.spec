# TODO:
# - check test failures: FAIL: test_ring_impl (persistent.tests.test_picklecache.PickleCacheTests)
# - fix docs: Could not import extension repoze.sphinx.autointerface (exception: No module named 'repoze')
# - delete/packages /usr/lib64/python*/site-packages/persistent/tests/
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	persistent
%define		pypi_name	%{module}

Summary:	Automatic persistence for Python objects
Summary(pl.UTF-8):	Automytczne trwałe obiekty w Pythonie
Name:		python-%{module}
Version:	4.6.4
Release:	2
License:	ZPL 2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/persistent/
Source0:	https://files.pythonhosted.org/packages/source/p/persistent/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	6878fd3a3008fb5b7da7a374155fd6c2
URL:		http://www.zope.org/Products/ZODB
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%package -n python3-%{module}
Summary:	Automatic persistence for Python objects
Summary(pl.UTF-8):	Automytczne trwałe obiekty w Pythonie
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst CHANGES.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%{py_sitedir}/%{module}/*.[ch]
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%dir %{py_incdir}/persistent/
%{py_incdir}/persistent/cPersistence.h
%{py_incdir}/persistent/ring.h
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst CHANGES.rst
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/*.[ch]
%attr(755,root,root) %{py3_sitedir}/%{module}/*.so
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%dir %{py3_incdir}/persistent/
%{py3_incdir}/persistent/cPersistence.h
%{py3_incdir}/persistent/ring.h
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
