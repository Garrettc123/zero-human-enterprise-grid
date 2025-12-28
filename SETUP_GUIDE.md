# 🚀 MEGA AUTONOMOUS SYNC - Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Basic understanding of command line

## Step 1: Install Dependencies

```bash
# Navigate to the repository directory
cd zero-human-enterprise-grid

# Install all required packages
pip install -r requirements.txt
```

## Step 2: Configure Environment Variables

```bash
# Copy the example configuration
cp .env.example .env

# Edit the .env file with your credentials
# nano .env    # or use your preferred editor
```

### Essential Configuration

At minimum, configure:

**Cloud Providers** (if using):
```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

GCP_PROJECT_ID=your_project
AZURE_SUBSCRIPTION_ID=your_subscription
```

**Databases** (if using):
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

MONGODB_URI=mongodb://localhost:27017
```

**Sync Intervals** (optional - defaults provided):
```env
SYNC_INTERVAL_CLOUD=60
SYNC_INTERVAL_DATABASE=30
SYNC_INTERVAL_STORAGE=30
```

## Step 3: Run the Orchestrator

### Basic Usage

```bash
python run_mega_sync.py
```

This will start all 9 sync systems running in parallel.

### Expected Output

```
2024-01-15 10:30:45 - root - INFO - Starting Mega Autonomous Sync System...
2024-01-15 10:30:46 - root - INFO - ################################################################################
2024-01-15 10:30:46 - root - INFO - #                                                                              #
2024-01-15 10:30:46 - root - INFO - #          MEGA AUTONOMOUS ORCHESTRATOR STARTING                              #
2024-01-15 10:30:46 - root - INFO - #                                                                              #
2024-01-15 10:30:46 - root - INFO - ################################################################################

2024-01-15 10:30:47 - root - INFO - Initializing all sync systems...
2024-01-15 10:30:47 - root - INFO - Registered provider: AWS
2024-01-15 10:30:47 - root - INFO - Registered provider: GCP
... (more registrations)
```

## Step 4: Monitor the System

The system will display real-time sync cycles:

```
[Cycle 1] Deploying to 5 clouds...
✓ AWS: 3 files
✓ GCP: 3 files
✓ Azure: 3 files
✓ Render: 3 files
✓ Vercel: 3 files

[Cycle 1] Syncing 4 database pairs...
✓ PostgreSQL Primary -> PostgreSQL Backup: 100 records
✓ PostgreSQL Primary -> MongoDB: 100 records
✓ PostgreSQL Primary -> DynamoDB: 100 records
✓ PostgreSQL Primary -> Elasticsearch: 100 records
```

## Troubleshooting

### Issue: "No such file or directory: 'requirements.txt'"

**Solution**: Make sure you're in the correct directory

```bash
# Check current directory
pwd
# Should end with: .../ai-sales-engine

# If not, navigate to it
cd path/to/zero-human-enterprise-grid
```

### Issue: "Cannot stat '.env.example': No such file"

**Solution**: The .env.example file should have been deployed. If not:

```bash
# Create a basic .env file
cat > .env << 'EOF'
API_PORT=8000
LOG_LEVEL=INFO
SYNC_INTERVAL_CLOUD=60
SYNC_INTERVAL_DATABASE=30
EOF
```

### Issue: "ModuleNotFoundError: No module named 'sync_engine'"

**Solution**: Make sure all files are in the correct directory

```bash
# List files to verify
ls -la *.py
# Should show: sync_engine.py, database_sync.py, etc.

# If missing, they need to be deployed
```

### Issue: Connection errors to databases/services

**Expected Behavior**: The system will attempt to connect but will log connection errors if services are not running. This is normal for local development.

```bash
# To use with real services, configure them in .env
# The system is designed to handle unreachable services gracefully
```

## Configuration Reference

See `.env.example` for all 50+ configuration options including:

- **Cloud Providers**: AWS, GCP, Azure, Render, Vercel
- **Databases**: PostgreSQL, MongoDB, DynamoDB, Elasticsearch
- **Storage**: S3, GCS, Azure Blob, MinIO
- **Caching**: Redis, Memcached
- **Message Queues**: Kafka, RabbitMQ, SQS
- **Search**: Elasticsearch, Algolia, Meilisearch
- **ML Platforms**: MLflow, SageMaker, Vertex AI
- **Monitoring**: Prometheus, Grafana, CloudWatch
- **Performance**: Sync intervals, batch sizes, timeouts

## Next Steps

1. ✅ Successfully installed and running? Great!
2. ✅ Check the logs for any sync activity
3. ✅ Configure additional systems in `.env`
4. ✅ Read [API_REFERENCE.md](API_REFERENCE.md) to integrate with your app
5. ✅ Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design details

## Performance Tips

- **Adjust Sync Intervals**: Change `SYNC_INTERVAL_*` values in `.env`
  - Lower values = more frequent syncs (more resource usage)
  - Higher values = less frequent syncs (lower latency)

- **Batch Sizes**: Modify `BATCH_SIZE_*` for optimal throughput
  - Larger batches = better throughput but higher memory
  - Smaller batches = lower memory but lower throughput

- **Parallel Execution**: All systems run in parallel
  - Total cycle time ≈ longest individual cycle (60s by default)
  - No sequential bottlenecks

## Production Deployment

For production, consider:

1. **Environment Management**: Use secure credential storage
2. **Monitoring**: Enable Prometheus/Grafana integration
3. **Logging**: Configure centralized logging
4. **Error Handling**: Review and customize error handlers
5. **Scaling**: Adjust batch sizes and intervals for your load
6. **High Availability**: Run multiple replicas behind load balancer

## Getting Help

If you encounter issues:

1. Check the error message in the logs
2. Verify `.env` configuration
3. Ensure all dependencies are installed: `pip list`
4. Review this guide for similar issues
5. Check [API_REFERENCE.md](API_REFERENCE.md) and [ARCHITECTURE.md](ARCHITECTURE.md)

---

**You're all set! Run `python run_mega_sync.py` to start syncing.** 🚀
