-- =========================================
-- Enable extensions
-- =========================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- =========================================
-- Enum Types
-- =========================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'visibilityenum') THEN
        CREATE TYPE visibilityenum AS ENUM ('public', 'personal', 'private', 'secure');
    END IF;
END$$;

-- =========================================
-- Journals Table
-- =========================================
CREATE TABLE IF NOT EXISTS journals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(50) NOT NULL,
    profile_id VARCHAR(50),
    s3_key VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    content_summary TEXT,
    visibility visibilityenum DEFAULT 'personal',
    canonical_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ingestion_source VARCHAR(50),
    encryption_meta JSON,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================
-- Journal Metadata Table
-- =========================================
CREATE TABLE IF NOT EXISTS journal_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    journal_id UUID NOT NULL REFERENCES journals(id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tags TEXT[],
    mood VARCHAR(50),
    feelings JSON,
    location JSON,
    device_info JSON,
    ingestion_source VARCHAR(50),
    embeddings VECTOR(384),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================
-- Recommendations Table
-- =========================================
CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(50) NOT NULL,
    journal_id UUID REFERENCES journals(id),
    product_id VARCHAR(50),
    category VARCHAR(100),
    recommendation_text TEXT,
    source VARCHAR(50),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================
-- Insights Table
-- =========================================
CREATE TABLE IF NOT EXISTS insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(50) NOT NULL,
    journal_id UUID REFERENCES journals(id),
    insight_type VARCHAR(50),
    value TEXT,
    source VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================
-- Notifications Table
-- =========================================
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(50) NOT NULL,
    type VARCHAR(50),
    message TEXT,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================
-- User Features Table
-- =========================================
CREATE TABLE IF NOT EXISTS user_features (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(50) NOT NULL,
    feature_name VARCHAR(100),
    feature_value TEXT,
    source VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================
-- Indexes
-- =========================================
CREATE INDEX IF NOT EXISTS idx_journals_user_id ON journals(user_id);
CREATE INDEX IF NOT EXISTS idx_journal_metadata_journal_id ON journal_metadata(journal_id);
CREATE INDEX IF NOT EXISTS idx_journal_metadata_embeddings 
    ON journal_metadata USING ivfflat (embeddings vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_recommendations_user_id ON recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_insights_user_id ON insights(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_user_features_user_id ON user_features(user_id);
