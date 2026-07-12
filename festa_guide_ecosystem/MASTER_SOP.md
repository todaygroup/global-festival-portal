# MASTER SOP: Single Source of Truth (SSoT) Supply Chain

## 1. Objective
To ensure that every piece of information from the global data lake to the final user interface is verified, consistent, and devoid of any synthetic data.

## 2. The Data Pipeline Architecture (L1 $\rightarrow$ L4)

### L1: Raw Acquisition (The Discovery Layer)
- **Process**: Autonomous agents crawl official tourism boards, government gazettes, and regional archives across 200+ countries.
- **Input**: HTML, PDF, JSON, CSV, API endpoints.
- **Standard**: "Capture everything." All raw formats are stored in the `data_lake/` with original timestamps and source URLs.

### L2: Validation & Refining (The Truth Layer)
- **Process**: The 'Truth Engine' evaluates L1 data against the **Zero Mock Policy**.
- **Criterion**:
    - **Existence Check**: Does the festival actually happen at this location?
    - **Cross-Referencing**: Must be verified by at least 2 independent official sources.
    - **Format Alignment**: Map raw data to the Global Festival Schema (GFS).
- **Output**: 'Verified' raw records.

### L3: Multi-modal Enrichment (The Context Layer)
- **Process**: Enrich verified records with multi-modal assets.
- **Tasks**:
    - **Visuals**: Fetch official imagery and map the POI coordinates.
    - **Temporal**: Map the Lifecycle (Planning $\rightarrow$ Report).
    - **Semantic**: AI-driven translation and categorization into festivals types.
- **Output**: Rich POI entities.

### L4: Service Delivery (The Presentation Layer)
- **Process**: Deployment to the Production Database and Frontend.
- **Mechanism**: 
    - Cache-first delivery for high-traffic POIs.
    - API-driven updates to ensure the UI always reflects the latest L3 state.

## 3. Quality Gate Checklists

| Stage | Check Point | Failure Action |
| :--- | :--- | :--- |
| **L1 $\rightarrow$ L2** | Source URL validity check | Discard record |
| **L2 $\rightarrow$ L3** | Coordinate accuracy ($\pm 1 \text{km}$) | Flag for manual review |
| **L3 $\rightarrow$ L4** | Integrity of official links | Mark as 'Link Broken' |

## 4. Emergency Rollback Procedure
In case of data corruption:
1. Freeze L4 delivery.
2. Identify the corrupted L2 batch.
3. Purge corrupted records from Master DB.
4. Re-run L2 $\rightarrow$ L3 for affected records.
5. Resume L4 delivery.
