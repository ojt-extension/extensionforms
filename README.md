This is a project dedicated to CvSU - DIT Extension Programs. 

This project is made with Python (Django) and PostgreSQL. 



## Aya - psql commands for tables
## Isa-isahin mo -- create table then create index

-- Create tblImpactAssessment table
CREATE TABLE "tblImpactAssessment" (
    assessment_id SERIAL PRIMARY KEY,
    department_id INTEGER NOT NULL REFERENCES "tblDepartment"(department_id) ON DELETE CASCADE,
    curricular_offering_id INTEGER NOT NULL REFERENCES "tblCurricularOffering"(curricular_offering_id) ON DELETE CASCADE,
    extension_ppa_ia_id INTEGER NOT NULL REFERENCES "tblExtensionPPA"(extension_ppa_id) ON DELETE CASCADE,
    proponent_ias VARCHAR(255) NOT NULL,
    date_conducted DATE NOT NULL,
    remarks TEXT
);

-- Create indexes for foreign keys
CREATE INDEX idx_impact_assessment_department ON "tblImpactAssessment"(department_id);
CREATE INDEX idx_impact_assessment_curricular ON "tblImpactAssessment"(curricular_offering_id);
CREATE INDEX idx_impact_assessment_extension_ppa ON "tblImpactAssessment"(extension_ppa_ia_id);

-- Create tblAwards table
CREATE TABLE "tblAwards" (
    award_id SERIAL PRIMARY KEY,
    department_id INTEGER NOT NULL REFERENCES "tblDepartment"(department_id) ON DELETE CASCADE,
    person_received_award VARCHAR(255) NOT NULL,
    award_title VARCHAR(500) NOT NULL,
    award_donor VARCHAR(255) NOT NULL,
    level_of_award VARCHAR(50) NOT NULL CHECK (level_of_award IN ('LOCAL', 'REGIONAL', 'NATIONAL', 'INTERNATIONAL')),
    date_received DATE NOT NULL,
    remarks TEXT
);

-- Create index for foreign key
CREATE INDEX idx_awards_department ON "tblAwards"(department_id);

-- Create tblOtherActivities table
CREATE TABLE "tblOtherActivities" (
    activity_id SERIAL PRIMARY KEY,
    date_conducted DATE NOT NULL,
    activity_title VARCHAR(500) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('TRAINING', 'SEMINAR', 'WORKSHOP', 'CONFERENCE', 'OUTREACH', 'OTHER')),
    participants VARCHAR(255) NOT NULL,
    purpose TEXT NOT NULL,
    amount_spent DECIMAL(10, 2),
    source_of_funds VARCHAR(255) NOT NULL,
    remarks TEXT
);

-- Add foreign key relationships to media_features_supportingdocument table
-- First, check if columns already exist
ALTER TABLE media_features_supportingdocument 
ADD COLUMN IF NOT EXISTS ordinance_id INTEGER REFERENCES "tblOrdinance"(ordinance_id) ON DELETE CASCADE;

ALTER TABLE media_features_supportingdocument 
ADD COLUMN IF NOT EXISTS impact_assessment_id INTEGER REFERENCES "tblImpactAssessment"(assessment_id) ON DELETE CASCADE;

ALTER TABLE media_features_supportingdocument 
ADD COLUMN IF NOT EXISTS award_id INTEGER REFERENCES "tblAwards"(award_id) ON DELETE CASCADE;

ALTER TABLE media_features_supportingdocument 
ADD COLUMN IF NOT EXISTS other_activity_id INTEGER REFERENCES "tblOtherActivities"(activity_id) ON DELETE CASCADE;

-- Create indexes for the new foreign keys
CREATE INDEX IF NOT EXISTS idx_supporting_doc_ordinance ON media_features_supportingdocument(ordinance_id);
CREATE INDEX IF NOT EXISTS idx_supporting_doc_impact_assessment ON media_features_supportingdocument(impact_assessment_id);
CREATE INDEX IF NOT EXISTS idx_supporting_doc_award ON media_features_supportingdocument(award_id);
CREATE INDEX IF NOT EXISTS idx_supporting_doc_other_activity ON media_features_supportingdocument(other_activity_id);

-- Verify the tables were created
\dt tbl*;
