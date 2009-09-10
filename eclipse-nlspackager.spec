# Disable repacking of jars, since it takes forever for all the little jars,
# and we don't need multilib anyway:
%define __jar_repack %{nil}

%define gcj_support	0

%define eclipse_name	eclipse
%define eclipse_data	%{_datadir}/%{eclipse_name}
%define oname   eclipse-nls

%define snapshot 20080807snap

Name:		eclipse-nlspackager
Version: 0.2.0
Release: 0.5.%{snapshot}.%mkrel 2
Epoch:          0
Summary:	Eclipse NLS package generator
Group:		Development/Java
License:	Eclipse Public License
URL:		http://wiki.eclipse.org/index.php/Linux_Distributions_Project

Source0: org.eclipse.nls-%{snapshot}-fetched-src.tar.bz2
Source1: fetch-babel.sh

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:  noarch

BuildRequires:		eclipse-platform
BuildRequires:		eclipse-pde
BuildRequires:		java-devel >= 1.4.2

Requires:		eclipse-rcp

%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif

%description
Babel language packs include translations for the Eclipse platform and other
Eclipse-related packages.

%define lang_meta_pkg() \
%package %1 \
Summary:    Eclipse/Babel language pack for %2 \
Group:      Development/Java \
# provides %{eclipse_data}/dropins \
Requires:   eclipse-platform >= 3.4.0-18 \
Obsoletes:  eclipse-sdk-nlspackager-%1 < 3.2.1-4 \
\
%description %1 \
This language pack for %2 contains user-contributed translations of the \
strings in all Eclipse projects. Please see the http://babel.eclipse.org/ \
Babel project web pages for a full how-to-use explanation of these \
translations as well as how you can contribute to \
the translations of this and future versions of Eclipse. \
Note that English text will be displayed if Babel doesn't \
have a translation for a given string. \
\
%files %1 \
%defattr(-,root,root,-) \
%{eclipse_data}/dropins/babel-%1

# Note that no licence %%doc files are listed under %%files.  Upstream does
# not provide a single distribution archive for eclipse-nls, but rather an
# update site which serves up 400 plugin jars for each language.  These
# jars are collected into a tarball by fetch-babel.sh.  Each jar does
# include HTML files with licence information, and these jars are placed
# in the dropins/babel-* directory above.

%lang_meta_pkg cs Czech
%lang_meta_pkg hu Hungarian
%lang_meta_pkg pl Polish
%lang_meta_pkg ru Russian
%lang_meta_pkg ar Arabic
# NB 'he' is 'iw' as far as Java is concerned.  fetch-babel.sh knows about it
%lang_meta_pkg he Hebrew
%lang_meta_pkg da Danish
%lang_meta_pkg de German
%lang_meta_pkg el Greek
%lang_meta_pkg es Spanish
%lang_meta_pkg fi Finnish
%lang_meta_pkg fr French
%lang_meta_pkg it Italian
%lang_meta_pkg ja Japanese
%lang_meta_pkg ko Korean
%lang_meta_pkg nl Dutch
%lang_meta_pkg no Norwegian
%lang_meta_pkg pt Portuguese
%lang_meta_pkg pt_BR Portuguese (Brazilian)
%lang_meta_pkg sv Swedish
%lang_meta_pkg tr Turkish
%lang_meta_pkg zh Chinese (Simplified)
%lang_meta_pkg zh_TW Chinese (Traditional)
##########################################
# Currently less than 10% coverage
%lang_meta_pkg uk Ukrainian
%lang_meta_pkg ro Romanian
%lang_meta_pkg bg Bulgarian
##########################################
##########################################
# Currently 0% coverage
#Hindi
#Klingon
#Spanish-Catalonian
#English
##########################################

%prep
%setup -q -n %{oname}

%build
# nothing to do

%install
rm -rf $RPM_BUILD_ROOT

for loc in ?? ??_??; do
   mkdir -p $RPM_BUILD_ROOT%{eclipse_data}/dropins/babel-${loc}/eclipse
   cp -R ${loc}/features ${loc}/plugins $RPM_BUILD_ROOT%{eclipse_data}/dropins/babel-${loc}/eclipse
done

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif
