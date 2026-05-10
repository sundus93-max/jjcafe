-- Run this in MySQL Workbench if migration fails

CREATE TABLE IF NOT EXISTS cafe_ordernotification (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255) NOT NULL,
    is_read TINYINT(1) NOT NULL DEFAULT 0,
    created_at DATETIME(6) NOT NULL DEFAULT NOW(6),
    order_id BIGINT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES cafe_order(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)  REFERENCES auth_user(id)  ON DELETE CASCADE
);

INSERT IGNORE INTO django_migrations (app, name, applied)
VALUES ('cafe', '0010_ordernotification', NOW());
