# Apply the complete configuration
kubectl apply -f complete-agent-deployment.yaml

# Verify the deployment
kubectl get all -n agent-system

# Check the pods
kubectl get pods -n agent-system

# Monitor the deployment
kubectl describe deployment agent-api -n agent-system