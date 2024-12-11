<div align="center">

# Skills and Knowledge Assessment

A Docker-based assessment system

[![Docker][Docker-badge]][Docker-url]
[![Docker-Install][Docker-Install-badge]][Docker-Install-url]
[![Todo][Todo-badge]][Todo-url]
[![Notes][Notes-badge]][Notes-url]
[![License][License-badge]][License-url]
[![Authors][Authors-badge]][Authors-url]

</div>

## System Requirements

<details>
<summary>Windows</summary>

- Windows 10/11
- WSL 2
- Docker Desktop for Windows
- 4GB RAM minimum (8GB recommended)
- Virtualization enabled in BIOS
</details>

<details>
<summary>Linux</summary>

- Any modern Linux distribution (Ubuntu 20.04+, Debian 11+, Fedora 35+, etc.)
- Docker Engine
- Docker Compose
- 2GB RAM minimum (4GB recommended)
</details>

## Usage

### Linux Setup
> Docker is required, see [Docker Installation](DOCKER_INSTALL.md)

1. Start Docker services:
   ```bash
   # Start Docker daemon
   sudo systemctl start docker
   
   # Enable Docker to start on boot
   sudo systemctl enable docker
   ```

2. Build the project:
   ```bash
   # Build and start containers (first run will take several minutes)
   docker compose up --build
   ```

3. Set up environment:
   ```bash
   # Generate environment variables from template
   docker compose exec web python manage.py setenv
   
   # Create unique secret key for security
   docker compose exec web python manage.py keygen
   
   # Apply changes by restarting containers
   docker compose restart
   ```

4. Access the application:
   - 🌐 [Main Interface](http://127.0.0.1:8000/)
   - ⚙️ [Admin Panel](http://127.0.0.1:8000/admin)

### Windows Setup
> Docker is required, see [Docker Installation](DOCKER_INSTALL.md)

1. Launch Docker Desktop
   > Ensure WSL 2 and Hyper-V are enabled

2. Follow the same steps as Linux setup:
   ```bash
   # Build and start containers (first run will take several minutes)
   docker compose up --build
   
   # Generate environment variables from template
   docker compose exec web python manage.py setenv
   
   # Create unique secret key for security
   docker compose exec web python manage.py keygen
   
   # Apply changes by restarting containers
   docker compose restart
   ```

3. Access the application:
   - 🌐 [Main Interface](http://127.0.0.1:8000/)
   - ⚙️ [Admin Panel](http://127.0.0.1:8000/admin)

> **Note**: First build may take several minutes depending on your internet connection and system performance

## Common Commands

### Container Management

```bash
# Start containers
docker compose start

# Stop containers (preserve data)
docker compose stop

# Restart containers
docker compose restart

# Stop and remove containers
docker compose down

# Full cleanup (including volumes)
docker compose down -v

# Start containers after a full stop
docker compose up

# Rebuild and start
docker compose up --build
```

### Development Commands

```bash
# Database migrations
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# View logs
docker compose logs

# Environment setup
docker compose exec web python manage.py setenv
docker compose exec web python manage.py setenv --debug  # Debug mode (debug runserver is used as an automatic startup server)

# Generate secret key
docker compose exec web python manage.py keygen
docker compose exec web python manage.py keygen --force  # Force regenerate
```

### Server Management

```bash
# Run release server
docker compose exec web python manage.py runrelease

# Custom config (must be located in ska/management/release/)
docker compose exec web python manage.py runrelease --config custom.conf.py

# Debug server
docker compose exec web python manage.py runserver
```

## Troubleshooting

<details>
<summary>Docker Service Won't Start</summary>

### Symptoms
- Docker service fails to start
- `docker` commands return connection errors

### Solution
Check service status and logs:
```bash
# View service status
sudo systemctl status docker

# Check detailed logs
sudo journalctl -xu docker

# Restart service
sudo systemctl restart docker
```
</details>

<details>
<summary>Permission Denied Errors</summary>

### Symptoms
- "Permission denied" when running Docker commands
- Access denied to Docker socket

### Diagnosis
```bash
# Check Docker socket permissions
ls -l /var/run/docker.sock

# View current user groups
groups
```

### Solutions
1. Add user to Docker group (recommended):
   ```bash
   # Add current user to docker group
   sudo usermod -aG docker $USER
   
   # Activate changes
   newgrp docker
   ```

2. Temporary fix (not recommended):
   ```bash
   # Run command with sudo
   sudo docker [command]
   ```
</details>

<details>
<summary>Port Conflicts</summary>

### Symptoms
- "Port is already in use" error
- Container fails to start due to port binding issues

### Solutions
1. Find process using the port:
   ```bash
   # Replace PORT with the conflicting port number
   sudo lsof -i :PORT
   
   # Alternative using netstat
   sudo netstat -tulpn | grep PORT
   ```

2. Resolve the conflict:
   ```bash
   # Kill the process using the port
   sudo kill $(sudo lsof -t -i:PORT)
   
   # Or modify docker-compose.yml to use different ports
   ```
</details>

<details>
<summary>Environment File Issues</summary>

### Symptoms
- Cannot modify .env file
- "Permission denied" when running setenv command

### Solutions
1. Fix permissions:
   ```bash
   # Make .env file writable
   sudo chmod 666 .env
   
   # Or change ownership
   sudo chown $USER:$USER .env
   ```

2. Create new .env file:
   ```bash
   # Backup existing file
   cp .env .env.backup
   
   # Generate new environment file
   docker compose exec web python manage.py setenv
   ```
</details>

<details>
<summary>Common Runtime Issues</summary>

### Container Won't Start
```bash
# View container logs
docker compose logs

# Rebuild containers
docker compose up --build

# Full reset
docker compose down -v
docker compose up --build
```

### Database Connection Issues
```bash
# Check if database container is running
docker compose ps

# Reset database container
docker compose rm -f db
docker compose up -d db
```

### Memory Issues
```bash
# View container resource usage
docker stats

# Clear Docker system
docker system prune -a
docker volume prune
```
</details>

<!-- Badges -->
[Docker-badge]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/

[Docker-Install-badge]: https://img.shields.io/badge/DOCKER-Installation-2496ED?style=for-the-badge
[Docker-Install-url]: DOCKER_INSTALLATION.md

[Todo-badge]: https://img.shields.io/badge/TODO-Roadmap-red?style=for-the-badge
[Todo-url]: TODO.md

[Notes-badge]: https://img.shields.io/badge/NOTES-Documentation-yellow?style=for-the-badge
[Notes-url]: NOTES.md

[License-badge]: https://img.shields.io/badge/License-GPL%20v3-blue.svg?style=for-the-badge
[License-url]: LICENSE.md

[Authors-badge]: https://img.shields.io/badge/AUTHORS-Contributors-orange?style=for-the-badge
[Authors-url]: AUTHORS.md
