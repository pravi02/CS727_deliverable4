from sqlalchemy import text
from sqlalchemy.orm import session


# from sqlalchemy.orm import session


def create_sales_amount_triggers(session):
    # SQL for the "AFTER INSERT" trigger
    insert_trigger_sql = """
    DELIMITER $$

    CREATE TRIGGER update_sales_amount_after_insert
    AFTER INSERT ON processed_line_items
    FOR EACH ROW
    BEGIN
        DECLARE total_sales_amount DECIMAL(10, 2);
        DECLARE all_fulfilled INT;

        SELECT SUM(p.price_per_unit * pl.allocated_quantity)
        INTO total_sales_amount
        FROM processed_line_items pl
        JOIN product p ON pl.inventory_id = p.product_id
        WHERE pl.process_id_id = NEW.process_id_id;

        UPDATE order_process
        SET sales_amount = total_sales_amount
        WHERE transaction_id = NEW.process_id_id;

        SELECT COUNT(*) INTO all_fulfilled
        FROM customer_order_items coi
        LEFT JOIN processed_line_items pli ON coi.line_item_id = pli.customer_line_item_id
        WHERE coi.order_id = (SELECT customer_order_id FROM order_process WHERE transaction_id = NEW.process_id_id)
        AND (coi.quantity > IFNULL(pli.allocated_quantity, 0));

        IF all_fulfilled = 0 THEN
            UPDATE order_process
            SET order_processed = TRUE
            WHERE transaction_id = NEW.process_id_id;
        END IF;
    END $$

    DELIMITER ;
    """

    # SQL for the "AFTER UPDATE" trigger
    update_trigger_sql = """
    DELIMITER $$

    CREATE TRIGGER update_sales_amount_after_update
    AFTER UPDATE ON processed_line_items
    FOR EACH ROW
    BEGIN
        DECLARE total_sales_amount DECIMAL(10, 2);
        DECLARE all_fulfilled INT;

        SELECT SUM(p.price_per_unit * pl.allocated_quantity)
        INTO total_sales_amount
        FROM processed_line_items pl
        JOIN product p ON pl.inventory_id = p.product_id
        WHERE pl.process_id_id = NEW.process_id_id;

        UPDATE order_process
        SET sales_amount = total_sales_amount
        WHERE transaction_id = NEW.process_id_id;

        SELECT COUNT(*) INTO all_fulfilled
        FROM customer_order_items coi
        LEFT JOIN processed_line_items pli ON coi.line_item_id = pli.customer_line_item_id
        WHERE coi.order_id = (SELECT customer_order_id FROM order_process WHERE transaction_id = NEW.process_id_id)
        AND (coi.quantity > IFNULL(pli.allocated_quantity, 0));

        IF all_fulfilled = 0 THEN
            UPDATE order_process
            SET order_processed = TRUE
            WHERE transaction_id = NEW.process_id_id;
        END IF;
    END $$

    DELIMITER ;
    """

    # Execute both trigger creation queries
    session.execute(text(insert_trigger_sql))
    session.execute(text(update_trigger_sql))
    session.commit()


# Assuming you have a valid session
create_sales_amount_triggers(session)
