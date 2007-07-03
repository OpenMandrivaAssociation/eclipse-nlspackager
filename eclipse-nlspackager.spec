%define gcj_support	1

%define eclipse_name	eclipse
%define eclipse_base	%{_datadir}/%{eclipse_name}


Name:		eclipse-nlspackager
Version:	0.1.4
Release:        %mkrel 2.2
Epoch:          0
Summary:	Eclipse NLS package generator
Group:		Development/Java
License:	Eclipse Public License
URL:		http://wiki.eclipse.org/index.php/Linux_Distributions_Project

Source0:	%{name}-src-%{version}.zip

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:		eclipse-platform
BuildRequires:		eclipse-pde
BuildRequires:		java-devel >= 1.4.2

Requires:		eclipse-rcp

%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif

%description
Language pack zips from eclipse.org are grouped by many different
languages together. However, it is unlikely for a user to use all
the languages that are included in the package. Instead of making
users download whole big chunk of language packs for just one language,
nlspackager breaks down the packages into a single feature/plugin per
one language.

%prep
%setup -q -c -n NLSPackager


%build
cp -r %{eclipse_base} SDK
SDK=$(cd SDK > /dev/null && pwd)

# Eclipse may try to write to the home directory.
mkdir home
homedir=$(cd home > /dev/null && pwd)

pushd nlspackager
	mkdir build
	# This can go away when package build handles plugins (not just features)
	echo "<project default=\"main\"><target name=\"main\"></target></project>" \
	> build/assemble.org.eclipse.linuxtools.nlspackager.all.xml
	echo "<project default=\"main\"><target name=\"main\"></target></project>" \
	> build/package.org.eclipse.linuxtools.nlspackager.all.xml

	# Build the langpackager plugin
	eclipse	\
	-application org.eclipse.ant.core.antRunner	\
	-Duser.home=$homedir				\
	-Dtype=plugin					\
	-Did=org.eclipse.linuxtools.nlspackager		\
	-DsourceDirectory=$(pwd)			\
	-DbaseLocation=$SDK				\
	-Dbuilder=%{eclipse_base}/plugins/org.eclipse.pde.build/templates/package-build	\
	-f %{eclipse_base}/plugins/org.eclipse.pde.build/scripts/build.xml


	pushd build/plugins/org.eclipse.linuxtools.nlspackager

		eclipse \
			-application org.eclipse.ant.core.antRunner	\
			-Duser.home=$homedir				\
			-DbaseLocation=$SDK				\
			-f build.xml build.update.jar

		mv org.eclipse.linuxtools.nlspackager_%{version}.jar $SDK/plugins
	popd
	
popd

%install
rm -rf $RPM_BUILD_ROOT
install -D -d -m 755 \
	$RPM_BUILD_ROOT%{eclipse_base}/plugins/ \
	$RPM_BUILD_ROOT%{eclipse_base}/features/org.eclipse.linuxtools.nlspackager_%{version}

install -p SDK/plugins/org.eclipse.linuxtools.nlspackager_%{version}.jar \
	$RPM_BUILD_ROOT%{eclipse_base}/plugins/

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

%files
%defattr(0644,root,root,0755)
%doc nlspackager/LICENSE nlspackager/ChangeLog
%{eclipse_base}/plugins/org.eclipse.linuxtools.nlspackager_%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

