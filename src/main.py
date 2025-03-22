# encoding: utf-8

import requests as req
import locale
from dialog import Dialog

#available_distros = ["debian", "arch", "fedora", "ubuntu", "gentoo", "nix", "mint", "endeavour", "cachy", "pop", "opensuse", "zorin",
		     #"nobara", "elementary", "antix", "freebsd", "kali", "garuda", "cent", "alpine", "tails", "qubes", "puppy", "arco", "slackware", "openbsd"]

#available_distros.sort()

# Yeah I know, that hierarchy makes no sense
# Nice idea ; TODO : JSON instead
distro_mirror = {
	"fedora": "https://download.fedoraproject.org/pub/fedora/linux/releases/41/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-41-1.4.iso",
	"slackware": "https://mirrors.slackware.com/slackware/slackware-iso/slackware64-15.0-iso/slackware64-15.0-install-dvd.iso",
	"tails": "https://download.tails.net/tails/stable/tails-amd64-6.13/tails-amd64-6.13.img",
	"freebsd": "https://download.freebsd.org/releases/amd64/amd64/ISO-IMAGES/14.2/FreeBSD-14.2-RELEASE-amd64-dvd1.iso",
	"zorin": "https://free.download.zorinos.com/17/Zorin-OS-17.2-Core-64-bit.iso",
	"debian": "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.10.0-amd64-netinst.iso",
	"mint": {
		"cinnamon": "https://mirrors.layeronline.com/linuxmint/stable/22.1/linuxmint-22.1-cinnamon-64bit.iso",
		"xfce": "https://mirrors.layeronline.com/linuxmint/stable/22.1/linuxmint-22.1-xfce-64bit.iso",
		"mate": "https://mirrors.layeronline.com/linuxmint/stable/22.1/linuxmint-22.1-mate-64bit.iso"
	},
	"alpine": "https://dl-cdn.alpinelinux.org/alpine/v3.21/releases/x86_64/alpine-standard-3.21.3-x86_64.iso",
	"antix": {
		"sysVinit": "https://sourceforge.net/projects/antix-linux/files/Final/antiX-23.2/antiX-23.2_x64-full.iso/download",
		"runit": "https://sourceforge.net/projects/antix-linux/files/Final/antiX-23.2/runit-antiX-23.2/antiX-23.2-runit_x64-full.iso/download"
	},
	"opensuse": "https://download.opensuse.org/tumbleweed/iso/openSUSE-Tumbleweed-DVD-x86_64-Current.iso",
	"puppy": "https://distro.ibiblio.org/puppylinux/puppy-bookwormpup/BookwormPup64/10.0.10/BookwormPup64_10.0.10.iso",
	"elementary": "https://fra1.dl.elementary.io/download/MTc0MjY2MTg4Nw==/elementaryos-8.0-stable.20250314rc.iso",
	"qubes": "https://mirrors.edge.kernel.org/qubes/iso/Qubes-R4.2.4-x86_64.iso",
	"cent": "https://mirrors.centos.org/mirrorlist?path=/10-stream/BaseOS/x86_64/iso/CentOS-Stream-10-latest-x86_64-dvd1.iso&redirect=1&protocol=https",
	"nix": {
		"gnome": "https://channels.nixos.org/nixos-24.11/latest-nixos-gnome-x86_64-linux.iso",
		"plasma": "https://channels.nixos.org/nixos-24.11/latest-nixos-plasma6-x86_64-linux.iso",
		"minimal": "https://channels.nixos.org/nixos-24.11/latest-nixos-minimal-x86_64-linux.iso"
	},
	"openbsd": "https://cdn.openbsd.org/pub/OpenBSD/7.6/amd64/install76.img",
	"pop": {
		"nvidia": "https://iso.pop-os.org/22.04/amd64/nvidia/51/pop-os_22.04_amd64_nvidia_51.iso",
		"amd/intel": "https://iso.pop-os.org/22.04/amd64/intel/51/pop-os_22.04_amd64_intel_51.iso"
	},
	#"nobara": { # I am NOT doing all dat
	#	"official-amd": "",
	#	"gnome-amd": "",
	#	"plasma-amd": "",
	#	"official-nvidia": "",
	#	"gnome-nvidia": "",
	#	"plasma-nvidia": ""
	#},
	"gentoo": "https://distfiles.gentoo.org/releases/amd64/autobuilds/20250315T023326Z/install-amd64-minimal-20250315T023326Z.iso",
	"artix": {
		"runit": "https://download.artixlinux.org/iso/artix-base-runit-20250310-x86_64.iso",
		"dinit": "https://download.artixlinux.org/iso/artix-base-dinit-20250310-x86_64.iso",
		"s6": "https://iso.artixlinux.org/iso/artix-base-s6-20250310-x86_64.iso",
		"openrc": "https://iso.artixlinux.org/iso/artix-base-openrc-20250310-x86_64.iso"
	},
	"arcolinux": {
		"arconet-xfce": "https://sourceforge.net/projects/arconetpro/files/arconet/arconet-v25.03.05-x86_64.iso/download",
		"arcopro-tty": "https://sourceforge.net/projects/arconetpro/files/arcopro/arcopro-v25.03.05-x86_64.iso/download",
		"arcoplasma-plasma": "https://sourceforge.net/projects/arconetpro/files/arcoplasma/arcoplasma-v25.03.05-x86_64.iso/download"
	},
	"arch": {
		"vanilla": "https://geo.mirror.pkgbuild.com/iso/2025.03.01/archlinux-2025.03.01-x86_64.iso",
		"alpine": "https://dl-cdn.alpinelinux.org/alpine/v3.21/releases/x86_64/alpine-standard-3.21.3-x86_64.iso",
		"archbang": "https://netix.dl.sourceforge.net/project/archbang/ArchBang/archbang-1603-x86_64.iso?viasf=1",
		"archcraft": "https://kumisystems.dl.sourceforge.net/project/archcraft/v25.01/archcraft-2025.01.03-x86_64.iso?viasf=1",
		"cachy": "https://cdn77.cachyos.org/ISO/desktop/250202/cachyos-desktop-linux-250202.iso",
		"endeavour": "https://mirrors.gigenet.com/endeavouros/iso/EndeavourOS_Mercury-2025.02.08.iso" 
	},
	"ubuntu": {
		"vanilla": "https://ubuntu.com/download/desktop/thank-you?version=24.04.2&architecture=amd64&lts=true",
		"lubuntu": "https://cdimage.ubuntu.com/lubuntu/releases/noble/release/lubuntu-24.04.2-desktop-amd64.iso",
		"kubuntu": "https://cdimage.ubuntu.com/kubuntu/releases/24.10/release/kubuntu-24.10-desktop-amd64.iso",
		"xubuntu": "https://mirror.us.leaseweb.net/ubuntu-cdimage/xubuntu/releases/24.04/release/xubuntu-24.04.2-desktop-amd64.iso",
		"server": "https://ubuntu.com/download/server/thank-you?version=24.04.2&architecture=amd64&lts=true"
	},
	"garuda": "https://iso.builds.garudalinux.org/iso/latest/garuda/mokka/latest.iso?r2=1"
}

def install_file(url, destination):
	with req.get(url, stream=True) as response:
		response.raise_for_status()
		with open(f"{destination}.iso", "wb") as file:
			for chunk in response.iter_content(chunk_size=8192):
				file.write(chunk)

distro_mirror = dict(sorted(distro_mirror.items()))

locale.setlocale(locale.LC_ALL, '')

menu = Dialog(dialog="dialog", autowidgetsize=True)

menu.set_background_title("ISO-Installer")

code, tags = menu.checklist("Select with <space>",
			    choices = [(distro, "", False) for distro in distro_mirror],
			    title = "Choose distribution(s) to install")

chosen_flavor = None

if code == menu.OK and tags:
	for distro in tags:
		if isinstance(distro_mirror[distro], dict):
			flavors = distro_mirror[distro]
			code, chosen_flavor = menu.checklist("Select with <space>",
				choices = [(flavor, "", False) for flavor in flavors],
				title = f"Choose a flavor to install for {distro}")

	if chosen_flavor:
		chosen_flavor = chosen_flavor[0]
		choice = distro_mirror[distro][chosen_flavor]
		menu.msgbox(f"You have chosen : {chosen_flavor} for {distro}")
		menu.msgbox(f"Installing {chosen_flavor}...")
		menu.msgbox(choice)
		
		file_name = f"{distro}-{chosen_flavor}"
		install_file(choice, file_name)
	else:
		menu.msgbox(f"You have chosen : {tags}")
else:
		menu.msgbox("You have not chosen any distribution.")


