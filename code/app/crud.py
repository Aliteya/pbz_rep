# crud.py
from .database import conn

# добавление
def add_owner(contact, type_of_owner, name, owners_fullname):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL add_owner(%s, %s, %s, %s);
            """, (contact, type_of_owner, name, owners_fullname))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
def add_object(type, adress, name, number_of_places,owner_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL add_city_object(%s, %s, %s, %s, %s);
            """, (type, adress, name, number_of_places,owner_id))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
def add_popularity(event_date, number_of_visitors, object_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL add_popularity(%s, %s, %s);
            """, (event_date, number_of_visitors, object_id))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
def add_event(fut_event_date, event_name, event_type, object_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL add_event(%s, %s, %s, %s);
            """, (fut_event_date, event_name, event_type, object_id))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
def add_date(opening_date, closing_date, object_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL add_date(%s, %s, %s);
            """, (opening_date, closing_date, object_id))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

# редактирование
def update_owner(owner_id, contact, type_of_owner, name, owners_fullname):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL update_owner(%s, %s, %s, %s, %s);
            """, (owner_id, contact, type_of_owner, name, owners_fullname))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
def update_object(object_id, type, adress, name, number_of_places,owner_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL update_city_object(%s, %s, %s, %s, %s, %s);
            """, (object_id, type, adress, name, number_of_places,owner_id))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
def update_popularity(popularity_id, event_date, number_of_visitors):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL update_popularity(%s, %s, %s);
            """, (popularity_id, event_date, number_of_visitors))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
def update_event(event_id, fut_event_date, event_name, event_type):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL update_event(%s, %s, %s, %s);
            """, (event_id, fut_event_date, event_name, event_type))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
def update_date(date_id, opening_date, closing_date):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL update_date(%s, %s, %s);
            """, (date_id, opening_date, closing_date))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
# удаление
def delete_owner(owner_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL delete_owner(%s);
            """, (owner_id,))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

def delete_city_object(object_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL delete_city_object(%s);
            """, (object_id,))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

def delete_popularity(popularity_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL delete_popularity(%s);
            """, (popularity_id,))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
def delete_event(event_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL delete_event(%s);
            """, (event_id,))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
def delete_date(date_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CALL delete_date_record(%s);
            """, (date_id,))
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    
# особые просмотры
def fetch_current_objects():
    try:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM current_city_objects;""")
            curr_objects = cursor.fetchall()
            return curr_objects
    except Exception as e:
        print(f"Error fetching current objects: {e}")
        return []
    
def fetch_upcoming_events():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM upcoming_events;")
            events = cursor.fetchall() 
            return events
    except Exception as e:
        print(f"Error fetching upcoming events: {e}")
        return []
    
def fetch_curr_type_objects(obj_type):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM get_city_objects_by_type(%s);
            """, (obj_type,))
            curr_type_obj = cursor.fetchall()
        return curr_type_obj
    except Exception as e:
        print(f"Error fetching current objects by type: {e}")
        return []

# вспомогательные просмотры

def get_owner_by_id(owner_id):
    try:
        with conn.cursor() as cursor:
            query = "SELECT owner_id, contact, type_of_owner, name, owners_fullname FROM Владелец WHERE owner_id = %s"
            cursor.execute(query, (owner_id,))
            owner = cursor.fetchone()
            return owner
    except Exception as e:
        print(f"Error fetching current objects: {e}")
        return []

def get_object_by_id(object_id):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT object_id, owner_id, type, address, name, number_of_places FROM "Место проведения досуга" WHERE object_id = %s'
            cursor.execute(query, (object_id,))
            object = cursor.fetchone()
            return object
    except Exception as e:
        print(f"Error fetching current objects: {e}")
        return []  

def get_popularity_by_id(popularity_id):
    try:
        with conn.cursor() as cursor:
            query = "SELECT popularity_id, object_id, event_date, number_of_visitors FROM Популярность WHERE popularity_id = %s"
            cursor.execute(query, (popularity_id,))
            popularity = cursor.fetchone()
            return popularity
    except Exception as e:
        print(f"Error fetching current objects: {e}")
        return []

def get_event_by_id(event_id):
    try:
        with conn.cursor() as cursor:
            query = "SELECT event_id, object_id, fut_event_date, event_name, event_type FROM Мероприятие WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            event = cursor.fetchone()
            return event
    except Exception as e:
        print(f"Error fetching current objects: {e}")
        return []

def get_date_by_id(date_id):
    try:
        with conn.cursor() as cursor:
            query = "SELECT date_id, object_id, opening_date, closing_date FROM Дата_открытия WHERE date_id = %s"
            cursor.execute(query, (date_id,))
            date = cursor.fetchone()
            return date
    except Exception as e:
        print(f"Error fetching current objects: {e}")
        return []

#----------ALL-----------------

def get_owners():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT owner_id, contact, type_of_owner, name, owners_fullname FROM Владелец")
            owners = cursor.fetchall()
            return owners
    except Exception as e:
        print(f"Error fetching owners: {e}")
        return [] 
    
def get_objects():
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT object_id, owner_id, type, address, name, number_of_places FROM "Место проведения досуга"')
            objects = cursor.fetchall()
            return objects
    except Exception as e:
        print(f"Error fetching objects: {e}")
        return [] 
    
def get_popularities():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT popularity_id, object_id, event_date, number_of_visitors FROM Популярность")
            popularities = cursor.fetchall()
            return popularities
    except Exception as e:
        print(f"Error fetching popularities: {e}")
        return [] 

def get_events():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT event_id, object_id, fut_event_date, event_name, event_type FROM Мероприятие")
            events = cursor.fetchall()
            return events
    except Exception as e:
        print(f"Error fetching events: {e}")
        return [] 
    
def get_dates():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT date_id, object_id, opening_date, closing_date FROM Дата_открытия")
            dates = cursor.fetchall()
            return dates
    except Exception as e:
        print(f"Error fetching dates: {e}")
        return [] 
    