
# AgentOS: Enterprise-Grade Agent Infrastructure Platform


[![Join our Discord](https://img.shields.io/badge/Discord-Join%20our%20server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/agora-999382051935506503) [![Subscribe on YouTube](https://img.shields.io/badge/YouTube-Subscribe-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@kyegomez3242) [![Connect on LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kye-g-38759a207/) [![Follow on X.com](https://img.shields.io/badge/X.com-Follow-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://x.com/kyegomezb)


[![GitHub stars](https://img.shields.io/github/stars/The-Swarm-Corporation/Legal-Swarm-Template?style=social)](https://github.com/The-Swarm-Corporation/Legal-Swarm-Template)
[![Swarms Framework](https://img.shields.io/badge/Built%20with-Swarms-blue)](https://github.com/kyegomez/swarms)


[![GitHub stars](https://img.shields.io/github/stars/The-Swarm-Corporation/agentos?style=social)](https://github.com/The-Swarm-Corporation/agentos)
[![PyPI version](https://badge.fury.io/py/agentos.svg)](https://badge.fury.io/py/agentos)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Documentation Status](https://readthedocs.org/projects/agentos/badge/?version=latest)](https://agentos.readthedocs.io/en/latest/?badge=latest)

AgentOS is an enterprise-ready infrastructure platform designed for deploying, managing, and scaling AI agents in production environments. It provides secure sandboxed environments, robust monitoring, and scalable architecture for reliable agent operations.

## 🚀 Key Features

- Secure containerized environment
- Integrated memory system
- Tool access management
- API endpoints for agent interaction
- Horizontal scaling support
- Production-grade security

## Prerequisites
- Docker 24.0+
- Docker Compose 2.0+
- Kubernetes 1.25+ (for orchestration)

## Environment Variables
Create a `.env` file with the following required variables:

```env
# Core Configuration
WORKSPACE_DIR=agent_workspace

# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
PINECONE_API_KEY=your_pinecone_key
GOOGLE_API_KEY=your_google_key
REPLICATE_API_TOKEN=your_replicate_token
STABILITY_API_KEY=your_stability_key
COHERE_API_KEY=your_cohere_key

# Optional Configuration
WORKERS=4
TIMEOUT=120
LOG_LEVEL=warning
MAX_REQUESTS=10000
```

## Quick Start

### Using Docker

1. Build the image:
```bash
docker build -t agent-api:latest .
```

2. Run the container:
```bash
docker run -d \
    --name agent-api \
    --env-file .env \
    -p 8000:8000 \
    -v $(pwd)/data:/agent_workspace/data \
    -v $(pwd)/logs:/agent_workspace/logs \
    --security-opt=no-new-privileges \
    --cap-drop=ALL \
    --read-only \
    agent-api:latest
```

### Using Docker Compose

1. Start the services:
```bash
docker compose up -d
```

2. View logs:
```bash
docker compose logs -f
```

3. Stop services:
```bash
docker compose down
```

## Kubernetes Deployment

1. Create required namespaces and secrets:
```bash
# Apply the complete configuration
kubectl apply -f complete-agent-deployment.yaml

# Verify the deployment
kubectl get all -n agent-system
```

2. Monitor the deployment:
```bash
kubectl get pods -n agent-system
kubectl describe deployment agent-api -n agent-system
```

## Security Configuration

### Docker Security Features
- Non-root user execution
- Read-only filesystem
- Dropped capabilities
- No privilege escalation
- Resource limitations
- Health checks

### Kubernetes Security Features
- Network policies
- Resource quotas
- Security contexts
- Service accounts
- Secret management

## Directory Structure
```
/
├── Dockerfile
├── docker-compose.yml
├── complete-agent-deployment.yaml
├── .env
├── data/
└── logs/
└── agent_api/
    └── main.py
```

## Monitoring

### Docker
```bash
# Container stats
docker stats agent-api

# Container logs
docker logs -f agent-api

# Container health
docker inspect agent-api
```

### Kubernetes
```bash
# Pod metrics
kubectl top pods -n agent-system

# Pod logs
kubectl logs -f deployment/agent-api -n agent-system

# Deployment status
kubectl get deployment agent-api -n agent-system -o wide
```

## Production Deployment Checklist

1. Environment Configuration
   - [ ] Set all required API keys
   - [ ] Configure resource limits
   - [ ] Set appropriate log levels

2. Security
   - [ ] Enable security features
   - [ ] Configure network policies
   - [ ] Set up secret management

3. Storage
   - [ ] Configure persistent volumes
   - [ ] Set up backup solutions
   - [ ] Configure log rotation

4. Monitoring
   - [ ] Set up health checks
   - [ ] Configure logging
   - [ ] Set up metrics collection

## API Endpoints

The service exposes the following endpoint:
- `http://localhost:8000/health` - Health check endpoint

## Troubleshooting

### Common Issues

1. Container fails to start:
```bash
# Check container logs
docker logs agent-api

# Check container status
docker inspect agent-api
```

2. Permission issues:
```bash
# Ensure volumes have correct permissions
chmod -R 770 data logs
```

3. Resource constraints:
```bash
# Check resource usage
docker stats agent-api
```

## Support

For issues and feature requests, please open an issue in the repository.

## License

[MIT License](LICENSE)