#!/bin/bash
set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Log file setup
LOG_DIR="/var/log/install"
LOG_FILE="${LOG_DIR}/install-$(date +%Y%m%d-%H%M%S).log"

# Create log directory if it doesn't exist
sudo mkdir -p "${LOG_DIR}"
sudo chmod 755 "${LOG_DIR}"

# Function to log messages
log() {
    local level=$1
    shift
    local message=$*
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}" | sudo tee -a "${LOG_FILE}"
    
    case ${level} in
        ERROR)
            echo -e "${RED}${message}${NC}" >&2
            ;;
        WARNING)
            echo -e "${YELLOW}${message}${NC}"
            ;;
        INFO)
            echo -e "${GREEN}${message}${NC}"
            ;;
    esac
}

# Function to check system requirements
check_requirements() {
    log "INFO" "Checking system requirements..."
    
    # Check OS
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [[ "${ID}" != "ubuntu" ]]; then
            log "ERROR" "This script requires Ubuntu. Current OS: ${ID}"
            exit 1
        fi
    else
        log "ERROR" "Could not determine OS"
        exit 1
    fi

    # Check memory
    total_mem=$(free -m | awk '/^Mem:/{print $2}')
    if [ "${total_mem}" -lt 2048 ]; then
        log "ERROR" "Insufficient memory. Required: 2GB, Available: ${total_mem}MB"
        exit 1
    fi

    # Check CPU cores
    cpu_cores=$(nproc)
    if [ "${cpu_cores}" -lt 2 ]; then
        log "ERROR" "Insufficient CPU cores. Required: 2, Available: ${cpu_cores}"
        exit 1
    fi

    # Check disk space
    free_space=$(df -m / | awk 'NR==2 {print $4}')
    if [ "${free_space}" -lt 20480 ]; then
        log "ERROR" "Insufficient disk space. Required: 20GB, Available: ${free_space}MB"
        exit 1
    fi

    log "INFO" "System requirements check passed"
}

# Function to install dependencies
install_dependencies() {
    log "INFO" "Installing dependencies..."
    
    sudo apt-get update
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        software-properties-common
}

# Function to install Docker
install_docker() {
    log "INFO" "Installing Docker..."
    
    # Remove old versions
    sudo apt-get remove -y docker docker-engine docker.io containerd runc || true
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Add Docker repository
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker packages
    sudo apt-get update
    sudo apt-get install -y \
        docker-ce \
        docker-ce-cli \
        containerd.io \
        docker-compose-plugin
    
    # Configure Docker daemon
    sudo mkdir -p /etc/docker
    cat <<EOF | sudo tee /etc/docker/daemon.json
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "100m",
        "max-file": "3"
    },
    "default-ulimits": {
        "nofile": {
            "Name": "nofile",
            "Hard": 64000,
            "Soft": 64000
        }
    },
    "live-restore": true,
    "iptables": true,
    "userland-proxy": false
}
EOF

    # Start Docker service
    sudo systemctl enable docker
    sudo systemctl start docker
    
    # Add user to docker group
    sudo usermod -aG docker "${USER}"
    
    # Verify Docker installation
    if ! docker --version; then
        log "ERROR" "Docker installation failed"
        exit 1
    fi
}

# Function to install Kubernetes
install_kubernetes() {
    log "INFO" "Installing Kubernetes..."
    
    # Add Kubernetes GPG key
    curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /usr/share/keyrings/kubernetes-archive-keyring.gpg
    
    # Add Kubernetes repository
    echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
    
    # Install Kubernetes packages
    sudo apt-get update
    sudo apt-get install -y \
        kubelet \
        kubeadm \
        kubectl
    
    # Hold packages at current version
    sudo apt-mark hold kubelet kubeadm kubectl
    
    # Configure system settings for Kubernetes
    cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF
    sudo sysctl --system
    
    # Disable swap
    sudo swapoff -a
    sudo sed -i '/swap/d' /etc/fstab
    
    # Configure containerd
    sudo mkdir -p /etc/containerd
    containerd config default | sudo tee /etc/containerd/config.toml
    sudo systemctl restart containerd
    
    # Initialize Kubernetes cluster
    if [[ "${INSTALL_TYPE:-}" == "master" ]]; then
        log "INFO" "Initializing Kubernetes master node..."
        sudo kubeadm init --pod-network-cidr=10.244.0.0/16
        
        # Configure kubectl for current user
        mkdir -p "${HOME}/.kube"
        sudo cp -i /etc/kubernetes/admin.conf "${HOME}/.kube/config"
        sudo chown "$(id -u):$(id -g)" "${HOME}/.kube/config"
        
        # Install network plugin (Calico)
        kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
    fi
}

# Function to verify installation
verify_installation() {
    log "INFO" "Verifying installation..."
    
    # Check Docker
    if ! docker run hello-world; then
        log "ERROR" "Docker verification failed"
        exit 1
    fi
    
    # Check Kubernetes
    if ! kubectl version --client; then
        log "ERROR" "Kubernetes client verification failed"
        exit 1
    fi
    
    if [[ "${INSTALL_TYPE:-}" == "master" ]]; then
        # Wait for node to be ready
        timeout=300
        while [[ $timeout -gt 0 ]]; do
            if kubectl get nodes | grep -q "Ready"; then
                log "INFO" "Node is ready"
                break
            fi
            sleep 5
            ((timeout-=5))
        done
        
        if [[ $timeout -le 0 ]]; then
            log "ERROR" "Node failed to become ready"
            exit 1
        fi
    fi
    
    log "INFO" "Installation verified successfully"
}

# Main installation function
main() {
    log "INFO" "Starting installation..."
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --master)
                INSTALL_TYPE="master"
                shift
                ;;
            --worker)
                INSTALL_TYPE="worker"
                shift
                ;;
            *)
                log "ERROR" "Unknown argument: $1"
                exit 1
                ;;
        esac
    done
    
    if [[ -z "${INSTALL_TYPE:-}" ]]; then
        log "ERROR" "Must specify --master or --worker"
        exit 1
    fi
    
    # Run installation steps
    check_requirements
    install_dependencies
    install_docker
    install_kubernetes
    verify_installation
    
    log "INFO" "Installation completed successfully"
    
    if [[ "${INSTALL_TYPE}" == "master" ]]; then
        log "INFO" "Kubernetes master node is ready"
        kubectl get nodes
    else
        log "INFO" "Kubernetes worker node is ready"
    fi
}

# Execute main function with command line arguments
main "$@"


# chmod +x install-docker-k8s.sh
# ./install-docker-k8s.sh --master
# ./install-docker-k8s.sh --worker