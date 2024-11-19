-- создаем таблички

CREATE TABLE IF NOT EXISTS Владелец (
    owner_id SERIAL PRIMARY KEY,
    type_of_owner VARCHAR(15) NOT NULL,
    name VARCHAR(30) NOT NULL,
    owners_fullname VARCHAR(80) NOT NULL,
    contact VARCHAR(13) NOT NULL
);

CREATE TABLE IF NOT EXISTS "Место проведения досуга" (
    object_id SERIAL PRIMARY KEY,
    owner_id INT NOT NULL,
    type VARCHAR(20) NOT NULL,
    address VARCHAR(80) NOT NULL,
    name VARCHAR(30) NOT NULL,
    number_of_places INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES Владелец (owner_id)  ON DELETE CASCADE   
);

CREATE TABLE IF NOT EXISTS Популярность (
    popularity_id SERIAL PRIMARY KEY,
    object_id INT NOT NULL,
    event_date DATE NOT NULL,
    number_of_visitors INT NOT NULL,
    FOREIGN KEY (object_id) REFERENCES "Место проведения досуга" (object_id) ON DELETE CASCADE  
);

CREATE TABLE IF NOT EXISTS Мероприятие (
    event_id SERIAL PRIMARY KEY,
    object_id INT NOT NULL,
    fut_event_date DATE Not NULL,
    event_name VARCHAR(90) NOT NULL,
    event_type VARCHAR(30) NOT NULL,
    FOREIGN KEY (object_id) REFERENCES "Место проведения досуга" (object_id) ON DELETE CASCADE  
);

CREATE TABLE IF NOT EXISTS Дата_открытия (
    date_id SERIAL PRIMARY KEY,
    object_id INT NOT NULL,
    opening_date DATE NOT NULL,
    closing_date DATE,
    FOREIGN KEY (object_id) REFERENCES "Место проведения досуга" (object_id) ON DELETE CASCADE  
);

CREATE INDEX idx_opening_date ON Дата_открытия (opening_date);

--УДАЛЕНИЕ
CREATE OR REPLACE PROCEDURE delete_city_object(p_object_id INT)  
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM "Место проведения досуга" WHERE object_id = p_object_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_owner(p_owner_id INT)  
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM Владелец WHERE owner_id = p_owner_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_popularity(p_popularity_id INT)  
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM Популярность WHERE popularity_id = p_popularity_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_event(p_event_id INT) 
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM Мероприятие WHERE event_id = p_event_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_date_record(p_date_id INT) 
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM Дата_открытия WHERE date_id = p_date_id;
END;
$$;

-- ТРИГГЕР НА УДАЛЕНИЕ ЗАПИСЕЙ ИЗ ОБЪЕКТОВ

CREATE OR REPLACE FUNCTION notify_after_delete() RETURNS TRIGGER AS $$
BEGIN
    RAISE NOTICE 'Cascade deletion for object with ID % completed.', OLD.object_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_delete_notify_trigger
AFTER DELETE ON "Место проведения досуга"
FOR EACH ROW EXECUTE FUNCTION notify_after_delete();

-- ДОБАВЛЕНИЕ

CREATE OR REPLACE PROCEDURE add_owner(
    p_contact VARCHAR(13),
    p_type_of_owner VARCHAR(15),
    p_name VARCHAR(30),
    p_owners_fullname VARCHAR(80)
) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO Владелец (contact, type_of_owner, name, owners_fullname)
    VALUES (p_contact, p_type_of_owner, p_name, p_owners_fullname);
END;
$$;

CREATE OR REPLACE PROCEDURE add_city_object(
    p_type VARCHAR(20),
    p_address VARCHAR(80),
    p_name VARCHAR(30),
    p_number_of_places INT,
    p_owner_id INT
) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO "Место проведения досуга" (type, address, name, number_of_places, owner_id)
    VALUES (p_type, p_address, p_name, p_number_of_places, p_owner_id);
END;
$$;

CREATE OR REPLACE PROCEDURE add_popularity(
    p_event_date DATE,
    p_number_of_visitors INT,
    p_object_id INT
) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO Популярность (event_date, number_of_visitors, object_id)
    VALUES (p_event_date, p_number_of_visitors, p_object_id);
END;
$$;

CREATE OR REPLACE PROCEDURE add_event(
    p_fut_event_date DATE,
    p_event_name VARCHAR(90),
    p_event_type VARCHAR(30),
    p_object_id INT
) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO Мероприятие (fut_event_date, event_name, event_type, object_id)
    VALUES (p_fut_event_date, p_event_name, p_event_type, p_object_id);
END;
$$;

CREATE OR REPLACE PROCEDURE add_date(
    p_opening_date DATE,
    p_closing_date DATE,
    p_object_id INT
) LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO Дата_открытия (opening_date, closing_date, object_id)
    VALUES (p_opening_date, p_closing_date, p_object_id);
END;
$$;

-- Просмотр списка объектов города на текущую дату

CREATE OR REPLACE VIEW current_city_objects AS
SELECT
    o.object_id,
    o.name,
    o.type,
    o.address,
    op.opening_date,
    op.closing_date
FROM "Место проведения досуга" o
JOIN Дата_открытия op ON o.object_id = op.object_id
WHERE op.opening_date <= CURRENT_DATE
  AND (op.closing_date IS NULL OR op.closing_date >= CURRENT_DATE);

--Просмотр списка мероприятий на ближайшие 2 недели

CREATE OR REPLACE VIEW upcoming_events AS
SELECT
    e.fut_event_date,
    e.event_name,
    o.name AS object_name,
    o.address
FROM Мероприятие e
JOIN "Место проведения досуга" o ON e.object_id = o.object_id
WHERE e.fut_event_date BETWEEN CURRENT_DATE AND (CURRENT_DATE + INTERVAL '14 days');

--Просмотр списка объектов заданного типа на текущую датy

CREATE OR REPLACE FUNCTION get_city_objects_by_type(p_type VARCHAR)
RETURNS TABLE (
    object_id INT,
    name VARCHAR,
    type VARCHAR,
    address VARCHAR,
    opening_date DATE,
    closing_date DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT c.object_id, c.name, c.type, c.address, c.opening_date, c.closing_date
    FROM current_city_objects c
    WHERE c.type = p_type;
END;
$$ LANGUAGE plpgsql;

--РЕДАКТИРОВАНИЕ

CREATE OR REPLACE PROCEDURE update_city_object(
    p_object_id INT,
    p_type VARCHAR(20),
    p_address VARCHAR(80),
    p_name VARCHAR(30),
    p_number_of_places INT,
    p_owner_id INT
) LANGUAGE plpgsql AS $$
BEGIN
    UPDATE "Место проведения досуга"
    SET type = p_type,
        address = p_address,
        name = p_name,
        number_of_places = p_number_of_places,
        owner_id = p_owner_id
    WHERE object_id = p_object_id;
END;
$$;

CREATE OR REPLACE PROCEDURE update_owner(
    p_owner_id INT,
    p_contact VARCHAR(13),
    p_type_of_owner VARCHAR(15),
    p_name VARCHAR(30),
    p_owners_fullname VARCHAR(80)
) LANGUAGE plpgsql AS $$
BEGIN
    UPDATE Владелец
    SET contact = p_contact,
        type_of_owner = p_type_of_owner,
        name = p_name,
        owners_fullname = p_owners_fullname
    WHERE owner_id = p_owner_id;
END;
$$;

CREATE OR REPLACE PROCEDURE update_popularity(
    p_popularity_id INT,
    p_event_date DATE,
    p_number_of_visitors INT
) LANGUAGE plpgsql AS $$
BEGIN
    UPDATE Популярность
    SET event_date = p_event_date,
        number_of_visitors = p_number_of_visitors
    WHERE popularity_id = p_popularity_id;
END;
$$;

CREATE OR REPLACE PROCEDURE update_event(
    p_event_id INT,
    p_fut_event_date DATE,
    p_event_name VARCHAR(90),
    p_event_type VARCHAR(30)
) LANGUAGE plpgsql AS $$
BEGIN
    UPDATE Мероприятие
    SET fut_event_date = p_fut_event_date,
        event_name = p_event_name,
        event_type = p_event_type
    WHERE event_id = p_event_id;
END;
$$;

CREATE OR REPLACE PROCEDURE update_date(
    p_date_id INT,
    p_opening_date DATE,
    p_closing_date DATE
) LANGUAGE plpgsql AS $$
BEGIN
    UPDATE Дата_открытия
    SET opening_date = p_opening_date,
        closing_date = p_closing_date
    WHERE date_id = p_date_id;
END;
$$;