
# Skills and Knowledge Assessment

## System Requirements

### Windows

- Windows 10/11
- WSL 2
- Docker Desktop for Windows
- 4GB RAM minimum (8GB recommended)
- Virtualization enabled in BIOS

### Linux

- Any modern Linux distribution (Ubuntu 20.04+, Debian 11+, Fedora 35+, etc.)
- Docker Engine
- Docker Compose
- 2GB RAM minimum (4GB recommended)

## Usage

Docker is required, see Docker Installation

### Windows
WSL 2 and Hyper-V is required

1. Launch Docker Desktop
2. At the first launch, build docker from project directory:
	```
	docker compose up --build
	```

### Linux

1. Launch docker services if you haven't already done so:
	```
	sudo systemctl start docker
	sudo systemctl enable docker
	```

2. At the first launch, build docker from project directory:
	```
	docker compose up --build
	```

### Common usage

- Running program:
       ```
       docker compose start
       ```

- Stopping the program while saving containers:
        ```
        docker compose stop
        ```

- Full stop with container removal:
	    ```
	    docker compose down
	    ```

	- Complete cleaning, including volumes:
		    ```
		    docker compose down -v
		    ```

- Running after a full stop:
        ```
        docker compose up
        ```
	- Rebuilding docker:
		    ```
		    docker compose down -v --build
		    ```

- View container logs:
        ```
        docker compose logs
        ```

# Docker Installation

## Windows

1. Install Docker Desktop for Windows:
	- Manual Installation:
		- Go to the official website: <https://www.docker.com/products/docker-desktop>
		- Download Docker Desktop Installer for Windows
		- Run the installer and follow the instructions

	- PowerShell Installation:
		```
		$dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
		$installerPath = "$env:TEMP\DockerDesktopInstaller.exe"
		Invoke-WebRequest -Uri $dockerUrl -OutFile $installerPath
		Start-Process -Wait $installerPath -ArgumentList "install --quiet"
		Remove-Item $installerPath
		```

2. Enable the WSL 2 and Hyper-V. To do this, open PowerShell from the administrator and run:
	```
	dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
	dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
	Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
	```

3. Reboot system
4. After reboot:
	- Launch Docker Desktop
	- Wait for full initialization
	- Check the installation. Open PowerShell and run:
		```
		docker --version
		```
	- If the installation went well, see Usage

## Linux

### Installation

#### Ubuntu/Debian

1. System Preparation:
	```
	sudo apt update
	sudo apt upgrade -y
	```

2. Install Prerequisites:
	```
	sudo apt install -y \
   		 apt-transport-https \
    		ca-certificates \
    		curl \
    		gnupg \
    		lsb-release \
    		software-properties-common
	```

3. Add Docker Repository:
	```
	sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
	```

#### Arch Linux

1. System Preparation:

	```
	sudo pacman -Syu
	```

2. Install Docker:
	```
	sudo pacman -S docker docker-compose
	```

3. Start and enable Docker service:
	```
	sudo systemctl start docker
	sudo systemctl enable docker
	```

#### Fedora

1. System Preparation:

	```
	sudo dnf update -y
	```

2. Add Docker Repository:
	```
	sudo dnf -y install dnf-plugins-core
	sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
	```

3. Install Docker:
	```
	sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
	```

4. Start and enable Docker service:
	```
	sudo systemctl start docker
	sudo systemctl enable docker
	```

#### CentOS/RHEL

1. System Preparation:

	```
	sudo yum update -y
	```

2. Add Docker Repository:
	```
	sudo yum install -y yum-utils
	sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
	```

3. Install Docker:
	```
	sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
	```

4. Start and enable Docker service:
	```
	sudo systemctl start docker
	sudo systemctl enable docker
	```

### Post-Installation

1. Add User to Docker Group:
	```
	sudo usermod -aG docker $USER
	newgrp docker
	```

2. Verify Installation:
	```
	docker --version
	sudo systemctl status docker
	```

	If the installation went well, see Usage
>>>>>>> Stashed changes
