# Social Support AI System - Architecture Documentation

## System Overview

The Social Support AI System is a comprehensive, multi-agent orchestration platform designed to automate the evaluation of social support applications. The system processes various document types, extracts information, validates data across sources, and provides ML-powered eligibility decisions with explainability.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           User Interface Layer                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  Streamlit UI                    │  FastAPI REST API                       │
│  • Application Submission        │  • /ingest                              │
│  • Status Monitoring            │  • /status/{id}                         │
│  • Decision Display             │  • /decision/{id}                        │
│  • Chat Interface               │  • /chat/{id}                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Master Agent Orchestrator                            │
│  • Workflow Management                                                    │
│  • Agent Coordination                                                     │
│  • Error Handling & Recovery                                             │
│  • Progress Tracking                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Multi-Agent System                               │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────┤
│  Extraction     │   Validation    │   Eligibility   │   Recommender      │
│     Agent       │     Agent       │     Agent       │     Agent          │
│                 │                 │                 │                    │
│ • OCR Processing│ • Cross-check   │ • ML Model      │ • Economic         │
│ • PDF Parsing   │ • Conflict      │ • Feature       │   Enablement       │
│ • Excel Import  │   Resolution    │   Engineering   │ • Personalized     │
│ • Text Analysis │ • Data          │ • SHAP          │   Suggestions      │
│                 │   Reconciliation│   Explainability│ • Resource         │
│                 │                 │                 │   Linking          │
└─────────────────┴─────────────────┴─────────────────┴─────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Data & ML Layer                                  │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────┤
│  PostgreSQL     │   ChromaDB      │   ML Models     │   Feature Store    │
│   Database      │   Vector DB     │                 │                    │
│                 │                 │                 │                    │
│ • Applicants    │ • Document      │ • XGBoost       │ • Income Stability │
│ • Documents     │   Embeddings    │ • LightGBM      │ • Employment       │
│ • Decisions     │ • Semantic      │ • Random Forest │   Stability        │
│ • Audit Logs    │   Search        │ • SHAP Values   │ • Credit Scoring   │
└─────────────────┴─────────────────┴─────────────────┴─────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Infrastructure Layer                              │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────┤
│   Ollama        │   Tesseract     │   File Storage  │   Logging &        │
│   Local LLM     │   OCR Engine    │                 │   Monitoring       │
│                 │                 │                 │                    │
│ • Llama2 Models │ • Image Text    │ • Upload        │ • Structured       │
│ • Embeddings    │   Extraction    │   Management    │   Logging          │
│ • Text          │ • Multi-format  │ • Security      │ • Audit Trails     │
│   Generation    │   Support       │   Controls      │ • Performance      │
└─────────────────┴─────────────────┴─────────────────┴─────────────────────┘
```

## Agent Architecture Details

### Master Agent (Orchestrator)

The Master Agent implements the ReAct (Reasoning and Acting) pattern with the following responsibilities:

- **Workflow Orchestration**: Manages the execution sequence of all agents
- **State Management**: Tracks workflow progress and maintains execution state
- **Error Handling**: Implements fail-fast and graceful degradation strategies
- **Result Aggregation**: Combines outputs from all agents into coherent responses
- **Monitoring**: Tracks performance metrics and execution times

**Workflow Steps:**
1. **Extraction**: Process documents and extract structured information
2. **Validation**: Cross-check information across sources and resolve conflicts
3. **Eligibility**: Run ML models and generate decisions with explanations
4. **Recommendation**: Generate personalized economic enablement suggestions

### Extraction Agent

**Capabilities:**
- Multi-format document processing (PDF, images, Excel, text)
- OCR for image-based documents using Tesseract
- Table extraction from PDFs and Excel files
- Structured data extraction with confidence scoring
- Pattern recognition for common document types

**Processing Pipeline:**
```
Document Input → Format Detection → Content Extraction → 
Structured Parsing → Confidence Scoring → Output Consolidation
```

### Validation Agent

**Capabilities:**
- Cross-document information validation
- Conflict detection and resolution
- Priority-based data reconciliation
- Confidence scoring for validation results
- Audit trail for all validation decisions

**Validation Fields:**
- Personal Information (name, DOB, contact details)
- Financial Information (income, employment, debt)
- Address Information (residence, verification)
- Employment Information (status, duration, employer)

**Priority Rules:**
- Government ID > Application Form > Supporting Documents
- Bank Statements > Pay Stubs > Self-reported Income
- Utility Bills > Application Form > Supporting Documents

### Eligibility Agent

**Capabilities:**
- Feature engineering from application data
- ML model training and inference
- SHAP-based explainability
- Confidence scoring and uncertainty quantification
- Model versioning and performance tracking

**Feature Engineering:**
- **Basic Features**: Monthly income, employment length, family size
- **Derived Features**: Income stability, employment stability, debt-to-income ratio
- **Calculated Features**: Credit score estimation, balance consistency
- **Normalized Features**: Scaled and standardized for ML models

**ML Models:**
- **Baseline**: Logistic Regression for interpretability
- **Production**: XGBoost/LightGBM for performance
- **Ensemble**: Multiple models for robustness
- **Explainability**: SHAP values for feature importance

### Recommender Agent

**Capabilities:**
- Personalized recommendation generation
- Economic enablement strategy suggestions
- Resource linking and referral
- Progress tracking and follow-up suggestions
- Motivational support and guidance

**Recommendation Categories:**
- **Credit Improvement**: Secured cards, payment history, credit monitoring
- **Debt Reduction**: Snowball method, consolidation, negotiation
- **Employment**: Certifications, career advancement, skill development
- **Financial Education**: Workshops, counseling, budgeting tools

## Data Flow Architecture

### 1. Application Ingestion Flow

```
User Submission → File Upload → Document Storage → 
Extraction Agent → Structured Data → Validation Agent → 
Conflict Resolution → Eligibility Agent → Decision Generation → 
Recommendation Agent → Response Assembly → User Notification
```

### 2. Document Processing Flow

```
Document Upload → Format Detection → Content Extraction → 
OCR/Text Processing → Pattern Recognition → Structured Output → 
Confidence Scoring → Quality Validation → Storage
```

### 3. Decision Generation Flow

```
Validated Data → Feature Engineering → Model Inference → 
SHAP Analysis → Confidence Calculation → Decision Logic → 
Explanation Generation → Recommendation Creation → Response
```

## Security Architecture

### Data Protection
- **PII Masking**: Automatic identification and masking of sensitive information
- **Encryption**: Database encryption at rest and in transit
- **Access Control**: Role-based access control (RBAC) implementation
- **Audit Logging**: Comprehensive audit trail for all operations

### File Security
- **Upload Validation**: File type, size, and content validation
- **Virus Scanning**: Malware detection for uploaded files
- **Secure Storage**: Encrypted file storage with access controls
- **Cleanup**: Automatic removal of temporary files

### API Security
- **Authentication**: JWT-based authentication system
- **Rate Limiting**: API rate limiting to prevent abuse
- **Input Validation**: Comprehensive input sanitization
- **CORS Configuration**: Controlled cross-origin resource sharing

## Scalability Architecture

### Horizontal Scaling
- **Stateless Design**: All agents are stateless for easy scaling
- **Load Balancing**: Multiple instances can be deployed behind load balancers
- **Database Sharding**: Horizontal partitioning for large datasets
- **Microservices**: Independent deployment of different components

### Performance Optimization
- **Async Processing**: Non-blocking I/O operations throughout
- **Caching**: Redis-based caching for frequently accessed data
- **Connection Pooling**: Database connection optimization
- **Background Tasks**: Celery-based task queue for heavy operations

## Monitoring & Observability

### Logging Strategy
- **Structured Logging**: JSON-formatted logs for easy parsing
- **Log Levels**: Configurable logging levels per component
- **Centralized Logging**: Centralized log aggregation and analysis
- **Audit Trails**: Complete audit trail for compliance

### Metrics Collection
- **Performance Metrics**: Response times, throughput, error rates
- **Business Metrics**: Application volumes, decision distributions
- **System Metrics**: CPU, memory, disk usage
- **Custom Metrics**: Agent-specific performance indicators

### Health Checks
- **Liveness Probes**: Basic system availability checks
- **Readiness Probes**: System readiness for traffic
- **Dependency Checks**: Database, external service health
- **Custom Health Checks**: Business logic health validation

## Deployment Architecture

### Container Strategy
- **Docker Containers**: Containerized deployment for consistency
- **Multi-stage Builds**: Optimized container images
- **Health Checks**: Built-in health monitoring
- **Resource Limits**: CPU and memory constraints

### Orchestration
- **Kubernetes**: Container orchestration for production
- **Helm Charts**: Kubernetes deployment templates
- **Service Mesh**: Istio for service-to-service communication
- **Auto-scaling**: Horizontal pod autoscaling

### Environment Management
- **Configuration**: Environment-specific configuration files
- **Secrets Management**: Secure handling of sensitive data
- **Feature Flags**: Runtime feature toggling
- **Blue-Green Deployment**: Zero-downtime deployment strategy

## Integration Points

### External Systems
- **Document Management**: Integration with document management systems
- **CRM Systems**: Customer relationship management integration
- **Payment Systems**: Payment processing integration
- **Reporting Tools**: Business intelligence and reporting

### APIs and Services
- **Credit Bureaus**: Credit score and history retrieval
- **Government APIs**: Identity verification services
- **Financial APIs**: Bank account verification
- **Employment APIs**: Employment verification services

## Future Enhancements

### Advanced AI Capabilities
- **Multi-modal AI**: Processing of video and audio content
- **Advanced NLP**: More sophisticated text understanding
- **Computer Vision**: Enhanced image and document analysis
- **Predictive Analytics**: Advanced forecasting and trend analysis

### Integration Capabilities
- **API Gateway**: Centralized API management
- **Event Streaming**: Real-time event processing
- **Microservices**: Further service decomposition
- **Cloud Native**: Full cloud-native architecture

### Compliance and Governance
- **GDPR Compliance**: Enhanced data privacy controls
- **SOC 2 Certification**: Security and compliance certification
- **Regulatory Reporting**: Automated compliance reporting
- **Data Governance**: Enhanced data quality and lineage tracking 