%define _prefix	/usr

Name:			hhexen
Summary:		Hacked Hexen is a Linux port of Raven Games old shooter, Hexen
License:		GPL
Group:			Games/Arcade
Version:		1.6.2
Release:		%mkrel 1
URL:			http://hhexen.sourceforge.net/
Source:			http://downloads.sourceforge.net/hhexen/%{name}-%{version}-src.tgz
Source1:		%{name}.png
Source90:		%{name}-rpmlintrc
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:	GL-devel
BuildRequires:	SDL-devel >= 1.2.4
BuildRequires:	SDL_mixer-devel >= 1.2.4
Requires:	TiMidity

%description
Hacked Hexen is a Linux port of Raven Game's old shooter, Hexen.

This is a new release of Dan's excellent Hacked Hexen, by the
authors of Hammer of Thyrion (Hexen II). We're applying fixes,
adding a few features, and ensuring it runs on most *nix operating
systems.

This package contains the OpenGL enabled binary.

This package is non-free because it requires non-free data. 

%package sdl
Summary:	Hacked Hexen is a Linux port of Raven Game's old shooter, Hexen
Group:		Games/Arcade

%description sdl
Hacked Hexen is a Linux port of Raven Game's old shooter, Hexen.

This is a new release of Dan's excellent Hacked Hexen, by the
authors of Hammer of Thyrion (Hexen II). We're applying fixes,
adding a few features, and ensuring it runs on most *nix operating
systems.

This package contains the sdl enabled binary.

%package demo
Summary:	Hacked Hexen is a Linux port of Raven Game's old shooter, Hexen
Group:		Games/Arcade
Requires:	%{name}

%description demo
Hacked Hexen is a Linux port of Raven Game's old shooter, Hexen.

This package contains the demo wad (a 4 level version from the
MacHexen shareware)
Those without the full retail version of Hexen can still play the
demo.


%prep
%setup -q -n %{name}-%{version}-src 

%build
# compile the OpenGL version (hhexen-gl)
%configure \
	--with-audio=sdlmixer
%__make %{?jobs:-j%{jobs}}

# compile the software version (hhexen-sdl)
%__make clean
%configure \
	--disable-gl \
	--with-audio=sdlmixer
%__make %{?jobs:-j%{jobs}}

%install
# wrapper startscript
%__install -dm 755 %{buildroot}%{_bindir}
for i in gl sdl; do
	%{__cat} > %{name}-$i.sh << EOF
#!/bin/bash
if [ ! -f \$HOME/.hhexen/version-%{version} ]; then
	mkdir -p \$HOME/.hhexen

	# if demo is installed create a link
	if [ -f %{_datadir}/games/%{name}/hexen.wad ]; then
		cd \$HOME/.hhexen
		ln -s %{_datadir}/games/%{name}/hexen.wad .
	fi
	touch version-%{version}
fi
cd \$HOME/.hhexen
%{_prefix}/games/%{name}-$i "\$@"
EOF

	%__install -m 755 %{name}-$i.sh \
		%{buildroot}%{_bindir}
done

# install the gamedata
%__install -dm 755 %{buildroot}/%{_datadir}/games/%{name}
%__install -m 644 hexen.wad \
	%{buildroot}%{_datadir}/games/%{name}

%__install -dm 755 %{buildroot}%{_prefix}/games/%{name}
%__install -dm 755 %{buildroot}%{_datadir}/pixmaps
for i in gl sdl; do
	# binaries
	%__install -m 755 %{name}-$i \
		%{buildroot}%{_prefix}/games

	# icon
	%__install -m 644 %{SOURCE1} \
		%{buildroot}%{_datadir}/pixmaps/%{name}-$i.png
done

# install menu entry
%__install -dm 755 %{buildroot}%{_datadir}/applications
%{__cat} > %{name}-gl.desktop << EOF
[Desktop Entry]
Name=Hacked Hexen (OpenGL)
GenericName=Hacked Hexen (OpenGL)
Comment=Hacked Hexen is a Linux port of Raven Game's old shooter, Hexen
Exec=%{name}-gl.sh
Icon=%{name}-gl
Terminal=false
Type=Application
#Encoding=UTF-8
EOF

%{__cat} > %{name}-sdl.desktop << EOF
[Desktop Entry]
Name=Hacked Hexen (SDL)
GenericName=Hacked Hexen (SDL)
Comment=Hacked Hexen is a Linux port of Raven Game's old shooter, Hexen
Exec=%{name}-sdl.sh
Icon=%{name}-sdl
Terminal=false
Type=Application
#Encoding=UTF-8
EOF

%__install -m 644 %{name}*.desktop \
	%{buildroot}%{_datadir}/applications

%clean
[ -d "%{buildroot}" -a "%{buildroot}" != "" ] && %__rm -rf "%{buildroot}"

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog LICENSE README-* RELEASE TODO WADFILES
%{_bindir}/%{name}-gl.sh
%{_prefix}/games/%{name}-gl
%{_datadir}/pixmaps/%{name}-gl.png
%{_datadir}/applications/%{name}-gl.desktop

%files sdl
%defattr(-,root,root)
%{_bindir}/%{name}-sdl.sh
%{_prefix}/games/%{name}-sdl
%{_datadir}/pixmaps/%{name}-sdl.png
%{_datadir}/applications/%{name}-sdl.desktop

%files demo
%defattr(-,root,root)
%doc README.demowad
%dir %{_datadir}/games/%{name}
