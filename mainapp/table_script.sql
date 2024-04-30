

CREATE TABLE Phonepe.state
(
    id SERIAL,
    state_name character varying,
    PRIMARY KEY (id)
);

CREATE TABLE Phonepe.year
(
    id SERIAL,
    year bigint NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Phonepe.users_device
(
    user_device_key character varying(256) NOT NULL,
    device_brand_name character varying(256),
    brand_count bigint,
    percentage double precision,
    no_of_users bigint,
    app_opening double precision,
    quarter bigint,
    state_key bigint,
    year_key bigint,
    CONSTRAINT user_device_pky PRIMARY KEY (user_device_key),
    CONSTRAINT state_fky FOREIGN KEY (state_key)
        REFERENCES Phonepe.state (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT year_fky FOREIGN KEY (year_key)
        REFERENCES Phonepe.year (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE Phonepe.users_location
(
    user_location_key character varying(256) NOT NULL,
    district_name character varying(256),
    users_count bigint,
    app_openig double precision,
    quarter bigint,
    state_key bigint,
    year_key bigint,
    CONSTRAINT user_location_pky PRIMARY KEY (user_location_key),
    CONSTRAINT state_fky FOREIGN KEY (state_key)
        REFERENCES Phonepe.state (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT year_fky FOREIGN KEY (year_key)
        REFERENCES Phonepe.year (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);


CREATE TABLE Phonepe.trans_location
(
    trans_location_id character varying NOT NULL,
    district_name character varying,
    total_transaction_count bigint,
    total_transaction_amount bigint,
    quarter bigint,
    state_key bigint,
    year_key bigint,
    CONSTRAINT trans_location_pky PRIMARY KEY (trans_location_id),
    CONSTRAINT state_key FOREIGN KEY (state_key)
        REFERENCES Phonepe.state (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT year_key FOREIGN KEY (year_key)
        REFERENCES Phonepe.year (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);


CREATE TABLE Phonepe.trans_method
(
    transaction_method_key character varying(256) NOT NULL,
    transaction_method character varying,
    transaction_count bigint,
    transaction_amount bigint,
    quarter bigint,
    state_key bigint,
    year_key bigint,
    CONSTRAINT trans_method_pky PRIMARY KEY (transaction_method_key),
    CONSTRAINT state_fky FOREIGN KEY (state_key)
        REFERENCES Phonepe.state (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT year_fky FOREIGN KEY (year_key)
        REFERENCES Phonepe.year (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);


CREATE TABLE Phonepe.pincode_table
(
    pin_code_key character varying(256) NOT NULL,
    pincode bigint,
    total_registered_user bigint,
    quarter bigint,
    state_key bigint,
    year_key bigint,
    CONSTRAINT pincode_pky PRIMARY KEY (pin_code_key),
    CONSTRAINT state_fky FOREIGN KEY (state_key)
        REFERENCES Phonepe.state (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT year_fky FOREIGN KEY (year_key)
        REFERENCES Phonepe.year (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE Phonepe.pincode_table_transaction
(
    pin_code_key character varying(256) NOT NULL,
    pincode bigint,
    total_transaction_count bigint,
    total_transaction_amount bigint,
    quarter bigint,
    state_key bigint,
    year_key bigint,
    CONSTRAINT pincode_transcn_pky PRIMARY KEY (pin_code_key),
    CONSTRAINT state_fky FOREIGN KEY (state_key)
        REFERENCES Phonepe.state (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT year_fky FOREIGN KEY (year_key)
        REFERENCES Phonepe.year (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);