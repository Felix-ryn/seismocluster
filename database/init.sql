-- SeismoCluster Database Schema
-- Tables are created empty; data is populated by ETL and training pipelines.

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- ── Tables ───────────────────────────────────────────────────

CREATE TABLE public.raw_earthquakes (
    id character varying NOT NULL,
    "time" timestamp without time zone,
    latitude double precision,
    longitude double precision,
    depth double precision,
    magnitude double precision,
    mag_type character varying,
    nst integer,
    gap double precision,
    dmin double precision,
    rms double precision,
    net character varying,
    place text,
    type character varying,
    horizontal_error double precision,
    depth_error double precision,
    mag_error double precision,
    mag_nst integer,
    status character varying,
    location_source character varying,
    mag_source character varying,
    updated timestamp without time zone
);

CREATE TABLE public.processed_earthquakes (
    id character varying NOT NULL,
    "time" timestamp without time zone,
    latitude double precision,
    longitude double precision,
    depth double precision,
    magnitude double precision,
    year integer,
    month integer,
    day integer,
    latitude_scaled double precision,
    longitude_scaled double precision,
    depth_scaled double precision,
    magnitude_scaled double precision
);

CREATE TABLE public.cluster_summary (
    cluster_label integer NOT NULL,
    total_earthquakes integer,
    avg_magnitude double precision,
    avg_depth double precision
);

CREATE TABLE public.earthquake_clusters (
    id character varying NOT NULL,
    cluster_label integer,
    is_noise boolean,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_anomaly boolean DEFAULT false,
    hierarchy_label integer
);

-- ── Primary Keys ─────────────────────────────────────────────

ALTER TABLE ONLY public.raw_earthquakes
    ADD CONSTRAINT raw_earthquakes_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.processed_earthquakes
    ADD CONSTRAINT processed_earthquakes_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.cluster_summary
    ADD CONSTRAINT cluster_summary_pkey PRIMARY KEY (cluster_label);

ALTER TABLE ONLY public.earthquake_clusters
    ADD CONSTRAINT earthquake_clusters_pkey PRIMARY KEY (id);

-- ── Indexes ──────────────────────────────────────────────────

CREATE INDEX idx_location ON public.raw_earthquakes USING btree (latitude, longitude);
CREATE INDEX idx_time ON public.raw_earthquakes USING btree ("time");
CREATE INDEX idx_cluster ON public.earthquake_clusters USING btree (cluster_label);

-- ── Foreign Keys ─────────────────────────────────────────────

ALTER TABLE ONLY public.processed_earthquakes
    ADD CONSTRAINT fk_processed_raw FOREIGN KEY (id) REFERENCES public.raw_earthquakes(id) ON DELETE CASCADE;

ALTER TABLE ONLY public.earthquake_clusters
    ADD CONSTRAINT fk_cluster_processed FOREIGN KEY (id) REFERENCES public.processed_earthquakes(id) ON DELETE CASCADE;

ALTER TABLE ONLY public.earthquake_clusters
    ADD CONSTRAINT fk_cluster_summary FOREIGN KEY (cluster_label) REFERENCES public.cluster_summary(cluster_label);
