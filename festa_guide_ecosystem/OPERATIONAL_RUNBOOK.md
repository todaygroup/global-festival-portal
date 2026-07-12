# OPERATIONAL RUNBOOK: Infrastructure & Stability Guide

## 1. Infrastructure Architecture
To support millions of records and multi-modal POI data, the system utilizes a Hybrid-Storage architecture:
- **Metadata**: PostgreSQL with PostGIS for high-performance geospatial queries.
- **Rich Assets**: S3-compatible object storage for high-res images, videos, and PDF reports.
- **Search/Discovery**: Elasticsearch / Meilisearch for sub-second global search across 200+ countries.
- **Caching**: Redis for frequent POI lookups and session management.

## 2. Performance Tuning (The Scale-Up Path)
- **Geospatial Indexing**: Implementation of H3 (Uber's Hexagonal Hierarchical Spatial Index) to optimize map clustering and spatial aggregation.
- **API Gateway**: Rate limiting and request queuing to prevent DDoS during peak festival seasons.
- **CDN Strategy**: Edge-caching of multi-modal assets to reduce latency for global users.

## 3. Maintenance & Health Checks
The **Ops-Swarm** (Maintenance Agents) performs the following on a schedule:
- **Daily**: Link-checker agent verifies the validity of all `official_url` fields.
- **Weekly**: Data-freshness agent identifies festivals with upcoming dates and flags them for update.
- **Monthly**: Infrastructure stress-test and database vacuuming/optimization.

## 4. Disaster Recovery (DR)
- **Backups**: Daily snapshot of PostgreSQL and incremental backups of S3 assets.
- **Recovery Point Objective (RPO)**: 24 hours.
- **Recovery Time Objective (RTO)**: 4 hours.
- **Procedure**: Automated Terraform scripts for rapid environment replication in a different cloud region.
