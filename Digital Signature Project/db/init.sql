USE login;

CREATE TABLE IF NOT EXISTS accounts (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    hashed_pswd VARCHAR(255) NOT NULL,
    salt VARCHAR(200) NOT NULL,
    email VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS documents (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    hashed_content LONGBLOB NOT NULL,
    id_account INT(11) NOT NULL,
    digital_sign LONGBLOB NOT NULL,
    FOREIGN KEY (id_account) REFERENCES accounts (id) ON DELETE CASCADE
);

INSERT INTO accounts (username, hashed_pswd, salt, email, is_admin) VALUES
("admin", "$2b$12$PLxppS36SOpp9sRNBUSYoOX5VJwEttbWBvI/nGf9exLWf8u9h8ara", "$2b$12$PLxppS36SOpp9sRNBUSYoO", "admin@admin.it", 1);
