# Docker Deployment Guide

This guide explains how to deploy the Liturgia system using Docker and Docker Swarm.

## Table of Contents
- [Quick Start with Docker](#quick-start-with-docker)
- [Docker Swarm Deployment](#docker-swarm-deployment)
- [Configuration](#configuration)
- [Updating the Application](#updating-the-application)
- [Monitoring and Logs](#monitoring-and-logs)

## Quick Start with Docker

### Using Docker Compose (Development)

1. **Pull the image:**
```bash
docker pull ghcr.io/josemaeldon/liturgia:latest
```

2. **Run with docker-compose:**
```bash
docker-compose up -d
```

3. **Access the application:**
   - Open your browser to http://localhost:8001

### Using Docker Run (Simple deployment)

```bash
docker run -d \
  --name liturgia \
  -p 8001:8001 \
  -e SECRET_KEY=your-secret-key-here \
  -v liturgia-pdfs:/tmp/liturgia_pdfs \
  ghcr.io/josemaeldon/liturgia:latest
```

## Docker Swarm Deployment

### Prerequisites
- Docker Swarm initialized
- Access to the swarm manager node

### Initialize Docker Swarm (if not already done)

```bash
docker swarm init
```

### Deploy as a Stack

1. **Deploy the stack:**
```bash
docker stack deploy -c docker-compose.yml liturgia
```

2. **Verify deployment:**
```bash
docker stack services liturgia
docker service ls
```

3. **Check service status:**
```bash
docker service ps liturgia_liturgia
```

### Manual Service Creation

If you prefer not to use docker-compose.yml:

```bash
docker service create \
  --name liturgia \
  --replicas 3 \
  --publish 8001:8001 \
  --env SECRET_KEY=your-secret-key-here \
  --env FLASK_ENV=production \
  --mount type=volume,source=liturgia-pdfs,target=/tmp/liturgia_pdfs \
  --health-cmd "python -c 'import requests; requests.get(\"http://localhost:8001/\", timeout=5)'" \
  --health-interval 30s \
  --health-timeout 10s \
  --health-retries 3 \
  --update-parallelism 1 \
  --update-delay 10s \
  --update-failure-action rollback \
  --rollback-parallelism 1 \
  --rollback-delay 10s \
  --restart-condition on-failure \
  --restart-max-attempts 3 \
  ghcr.io/josemaeldon/liturgia:latest
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Flask secret key for sessions | - | Yes |
| `FLASK_ENV` | Flask environment | `production` | No |
| `FLASK_DEBUG` | Enable debug mode | `False` | No |
| `UPLOAD_FOLDER` | Path for PDF files | `/tmp/liturgia_pdfs` | No |

### Secrets Management

For production, use Docker secrets instead of environment variables:

1. **Create a secret:**
```bash
echo "your-super-secret-key" | docker secret create liturgia_secret_key -
```

2. **Update service to use secret:**
```bash
docker service update \
  --secret-add source=liturgia_secret_key,target=SECRET_KEY \
  liturgia_liturgia
```

### Volumes

The application uses a volume for temporary PDF files:
- **Volume name:** `liturgia-pdfs`
- **Mount point:** `/tmp/liturgia_pdfs`

## Updating the Application

### Rolling Update

```bash
# Pull the latest image
docker pull ghcr.io/josemaeldon/liturgia:latest

# Update the service
docker service update --image ghcr.io/josemaeldon/liturgia:latest liturgia_liturgia
```

### Using Stack Update

```bash
# Update the stack
docker stack deploy -c docker-compose.yml liturgia
```

### Rollback if Needed

```bash
docker service rollback liturgia_liturgia
```

## Monitoring and Logs

### View Service Logs

```bash
# All replicas
docker service logs liturgia_liturgia

# Follow logs
docker service logs -f liturgia_liturgia

# Last 100 lines
docker service logs --tail 100 liturgia_liturgia
```

### Check Service Health

```bash
# Service status
docker service ps liturgia_liturgia

# Detailed inspect
docker service inspect liturgia_liturgia
```

### Monitor Resource Usage

```bash
# CPU and memory usage
docker stats

# Service-specific stats
docker stats $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_liturgia")
```

## Scaling

### Scale Up/Down

```bash
# Scale to 5 replicas
docker service scale liturgia_liturgia=5

# Scale down to 2 replicas
docker service scale liturgia_liturgia=2
```

## Load Balancing

Docker Swarm automatically load balances requests across all healthy replicas. You can also use:

### With Traefik

The docker-compose.yml includes Traefik labels. To use:

1. Deploy Traefik in your swarm
2. Update the `Host` rule in docker-compose.yml
3. Deploy the stack

### With NGINX

Example NGINX configuration:

```nginx
upstream liturgia {
    server node1:8001;
    server node2:8001;
    server node3:8001;
}

server {
    listen 80;
    server_name liturgia.example.com;

    location / {
        proxy_pass http://liturgia;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Service not starting

```bash
# Check service logs
docker service logs liturgia_liturgia

# Check events
docker events --filter service=liturgia_liturgia

# Inspect service
docker service inspect liturgia_liturgia
```

### Health check failing

```bash
# Check container logs
docker logs $(docker ps -q --filter "label=com.docker.swarm.service.name=liturgia_liturgia" | head -1)

# Test health check manually
docker exec -it <container_id> python -c "import requests; print(requests.get('http://localhost:8001/').status_code)"
```

### Volume issues

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect liturgia-pdfs

# Remove volume (caution: this deletes data)
docker volume rm liturgia-pdfs
```

## Production Checklist

- [ ] Set a strong `SECRET_KEY`
- [ ] Use Docker secrets for sensitive data
- [ ] Configure proper backup for volumes
- [ ] Set up monitoring and alerting
- [ ] Configure log aggregation
- [ ] Use HTTPS with reverse proxy
- [ ] Implement rate limiting
- [ ] Configure firewall rules
- [ ] Set resource limits appropriately
- [ ] Test rollback procedures
- [ ] Document disaster recovery plan

## Support

For issues or questions:
- GitHub Issues: https://github.com/josemaeldon/liturgia/issues
- Documentation: https://github.com/josemaeldon/liturgia

## License

See LICENSE file in the repository.
