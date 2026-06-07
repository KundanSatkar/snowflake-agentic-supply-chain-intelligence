-- =====================================================
-- OpsPilot AI: Snowflake Database and Schema Setup
-- =====================================================

CREATE DATABASE IF NOT EXISTS OPSPILOT_AI;

USE DATABASE OPSPILOT_AI;

CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS STAGING;
CREATE SCHEMA IF NOT EXISTS MARTS;
CREATE SCHEMA IF NOT EXISTS AI_FEATURES;

-- =====================================================
-- Purpose of each schema
-- RAW        : Original source data loaded from CSV files
-- STAGING    : Cleaned and standardized tables
-- MARTS      : Business-ready analytics tables
-- AI_FEATURES: ML and AI-ready feature tables
-- =====================================================