use traffic_control;
ALTER TABLE fines
MODIFY COLUMN payment_date TIMESTAMP NULL DEFAULT NULL;

DELIMITER $$

CREATE TRIGGER set_payment_date_on_insert
BEFORE INSERT ON fines
FOR EACH ROW
BEGIN
    IF NEW.fine_status = 'Paid' THEN
        SET NEW.payment_date = CURRENT_TIMESTAMP;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER set_payment_date_on_update
BEFORE UPDATE ON fines
FOR EACH ROW
BEGIN
    IF NEW.fine_status = 'Paid' THEN
        SET NEW.payment_date = CURRENT_TIMESTAMP;
    END IF;
END$$

DELIMITER ;use traffic_control;
ALTER TABLE fines
MODIFY COLUMN payment_date TIMESTAMP NULL DEFAULT NULL;

DELIMITER $$

CREATE TRIGGER set_payment_date_on_insert
BEFORE INSERT ON fines
FOR EACH ROW
BEGIN
    IF NEW.fine_status = 'Paid' THEN
        SET NEW.payment_date = CURRENT_TIMESTAMP;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER set_payment_date_on_update
BEFORE UPDATE ON fines
FOR EACH ROW
BEGIN
    IF NEW.fine_status = 'Paid' THEN
        SET NEW.payment_date = CURRENT_TIMESTAMP;
    END IF;
END$$

DELIMITER ;


