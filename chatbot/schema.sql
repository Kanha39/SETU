-- Shared schema for the PAIMANA MVP.
-- Run this ONCE against the shared MySQL database before either service starts.
-- Do NOT let Hibernate/JPA auto-generate these two tables (ddl-auto=update) --
-- the chatbot service writes to them with raw SQL and expects these exact
-- column names and types.

CREATE TABLE IF NOT EXISTS user_submitted_projects (
    id                    BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id            VARCHAR(36)  NOT NULL UNIQUE,
    user_id               INT          NOT NULL,
    project_data          JSON         NOT NULL,
    predicted_overrun     DOUBLE       NULL,
    predicted_delay_days  DOUBLE       NULL,
    cost_risk_tier        VARCHAR(16)  NULL,
    time_risk_tier        VARCHAR(16)  NULL,
    overall_risk_tier     VARCHAR(16)  NULL,
    created_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS chat_messages (
    id             BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT          NOT NULL,
    session_id     VARCHAR(36)  NOT NULL,
    project_code   VARCHAR(64)  NULL,
    user_message   TEXT         NOT NULL,
    bot_response   TEXT         NOT NULL,
    created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session_id (session_id),
    INDEX idx_session_created (session_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- NOTE: the `projects` table (the migrated dataset CSV) is created
-- automatically by migrate_csv_to_mysql.py via pandas.to_sql(), because its
-- column set depends on whatever is in merged_projects.csv. Run that script
-- once, after this schema, to populate it.