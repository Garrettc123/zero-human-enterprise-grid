# REST API Reference - Mega Autonomous Sync

## Base URL

```
http://localhost:8000/api/v1
```

## Status Endpoints

### Get Full Orchestration Status

```http
GET /orchestration/status
```

**Response**:
```json
{
  "uptime_seconds": 3600,
  "cloud_sync": {
    "running": true,
    "providers": ["AWS", "GCP", "Azure", "Render", "Vercel"],
    "total_syncs": 60
  },
  "database_sync": {
    "running": true,
    "databases": ["PostgreSQL Primary", "PostgreSQL Backup", "MongoDB", "DynamoDB", "Elasticsearch"],
    "sync_pairs": 4,
    "total_syncs": 120
  },
  "monitoring": {
    "running": true,
    "total_checks": 360
  }
}
```

### Get Cloud Sync Status

```http
GET /cloud/status
```

**Response**:
```json
{
  "running": true,
  "providers": ["AWS", "GCP", "Azure", "Render", "Vercel"],
  "total_syncs": 60
}
```

### Get Database Sync Status

```http
GET /database/status
```

**Response**:
```json
{
  "running": true,
  "databases": ["PostgreSQL Primary", "PostgreSQL Backup", "MongoDB", "DynamoDB", "Elasticsearch"],
  "sync_pairs": 4,
  "total_syncs": 120
}
```

### Get Storage Sync Status

```http
GET /storage/status
```

**Response**:
```json
{
  "running": true,
  "storage_providers": ["S3", "GCS", "Azure Blob", "MinIO"],
  "total_files_synced": 300
}
```

### Get Cache Sync Status

```http
GET /cache/status
```

**Response**:
```json
{
  "running": true,
  "cache_providers": ["Redis Primary", "Redis Replica"],
  "total_syncs": 180
}
```

### Get Message Sync Status

```http
GET /messages/status
```

**Response**:
```json
{
  "running": true,
  "message_queues": ["Kafka", "RabbitMQ", "SQS"],
  "total_messages_processed": 240
}
```

### Get Search Sync Status

```http
GET /search/status
```

**Response**:
```json
{
  "running": true,
  "search_engines": ["Elasticsearch", "Algolia", "Meilisearch"],
  "total_documents_indexed": 480
}
```

### Get ML Sync Status

```http
GET /ml/status
```

**Response**:
```json
{
  "running": true,
  "ml_platforms": ["MLflow", "SageMaker", "Vertex AI"],
  "total_models_synced": 60
}
```

### Get GraphQL Sync Status

```http
GET /graphql/status
```

**Response**:
```json
{
  "running": true,
  "graphql_endpoints": ["Production", "Backup"],
  "total_syncs": 120
}
```

### Get Monitoring Health

```http
GET /monitoring/health
```

**Response**:
```json
{
  "running": true,
  "total_checks": 360,
  "last_check": "2024-01-15T10:35:45.123456"
}
```

## Control Endpoints

### Start All Syncs

```http
POST /orchestration/start
```

**Response**:
```json
{
  "status": "started",
  "systems": 9,
  "endpoints": 27,
  "timestamp": "2024-01-15T10:36:00.000000"
}
```

### Stop All Syncs

```http
POST /orchestration/stop
```

**Response**:
```json
{
  "status": "stopped",
  "uptime_seconds": 3600,
  "systems_stopped": 9,
  "timestamp": "2024-01-15T10:40:00.000000"
}
```

### Restart Cloud Sync

```http
POST /cloud/restart
```

**Response**:
```json
{
  "system": "cloud_sync",
  "status": "restarted",
  "providers": 5,
  "timestamp": "2024-01-15T10:36:05.000000"
}
```

### Restart Database Sync

```http
POST /database/restart
```

**Response**:
```json
{
  "system": "database_sync",
  "status": "restarted",
  "databases": 5,
  "sync_pairs": 4,
  "timestamp": "2024-01-15T10:36:10.000000"
}
```

### Restart Storage Sync

```http
POST /storage/restart
```

### Restart Cache Sync

```http
POST /cache/restart
```

### Restart Message Sync

```http
POST /messages/restart
```

### Restart Search Sync

```http
POST /search/restart
```

### Restart ML Sync

```http
POST /ml/restart
```

### Restart GraphQL Sync

```http
POST /graphql/restart
```

## Usage Examples

### Check Overall Health

```bash
curl http://localhost:8000/api/v1/orchestration/status
```

### Check Specific System Status

```bash
curl http://localhost:8000/api/v1/database/status
curl http://localhost:8000/api/v1/cloud/status
curl http://localhost:8000/api/v1/search/status
```

### Restart a System

```bash
curl -X POST http://localhost:8000/api/v1/cloud/restart
curl -X POST http://localhost:8000/api/v1/database/restart
```

### Stop All Systems

```bash
curl -X POST http://localhost:8000/api/v1/orchestration/stop
```

## Error Responses

### 400 Bad Request

```json
{
  "error": "Invalid request",
  "message": "Missing required parameters"
}
```

### 404 Not Found

```json
{
  "error": "Not found",
  "message": "System not found: invalid_system"
}
```

### 500 Internal Error

```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

## Rate Limiting

- No rate limiting currently configured
- Recommended: 100 requests/minute per IP

## Authentication

- Currently: No authentication required
- Recommended for production: API key or JWT

## CORS

- All origins allowed (modify in production)
- Methods: GET, POST, OPTIONS

## Webhooks

### Register Webhook

```http
POST /webhooks/register
Content-Type: application/json

{
  "event_type": "sync_complete",
  "url": "https://your-endpoint.com/webhook"
}
```

### Webhook Events

- `deployment_complete`
- `sync_complete`
- `error_occurred`
- `health_degraded`

---

For setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

For architecture details, see [ARCHITECTURE.md](ARCHITECTURE.md)
