CREATE TABLE user (
	id CHAR(32) NOT NULL COMMENT 'id',
	phone CHAR(11) NOT NULL,
	union_id VARCHAR(64)  NOT NULL,
	open_id VARCHAR(64) NOT NULL ,
	user_is_new BIT NOT NULL,
	invited_num INT NOT NULL DEFAULT 0,
	share_chance_added BIT NOT NULL DEFAULT FALSE ,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	UNIQUE KEY uk_open_id (open_id) ,
	INDEX idx_union_id (union_id)
) ENGINE=INNODB DEFAULT CHARACTER SET=UTF8MB4 COLLATE=UTF8MB4_UNICODE_CI;


CREATE TABLE admin (
	id CHAR(32) NOT NULL COMMENT 'id',
	phone CHAR(11) NOT NULL,
	union_id VARCHAR(64)  NOT NULL,
	open_id VARCHAR(64) NOT NULL ,
	user_is_new BIT NOT NULL,
	invited_num INT NOT NULL DEFAULT 0,
	share_chance_added BIT NOT NULL DEFAULT FALSE ,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	UNIQUE KEY uk_open_id (open_id) ,
	INDEX idx_union_id (union_id)
) ENGINE=INNODB DEFAULT CHARACTER SET=UTF8MB4 COLLATE=UTF8MB4_UNICODE_CI;