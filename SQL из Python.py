# Создайте программу для управления клиентами на Python.
# Требуется хранить персональную информацию о клиентах:
# имя,
# фамилия,
# email,
# телефон.
# Сложность в том, что телефон у клиента может быть не один, а два, три и даже больше. А может и вообще не быть телефона, 
# например, он не захотел его оставлять.

# Вам необходимо разработать структуру БД для хранения информации и несколько функций на Python для управления данными.
# Функция, создающая структуру БД (таблицы).
# Функция, позволяющая добавить нового клиента.
# Функция, позволяющая добавить телефон для существующего клиента.
# Функция, позволяющая изменить данные о клиенте.
# Функция, позволяющая удалить телефон для существующего клиента.
# Функция, позволяющая удалить существующего клиента.
# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
# Функции выше являются обязательными, но это не значит, что должны быть только они. При необходимости можете создавать дополнительные функции и классы.

# Также предоставьте код, демонстрирующий работу всех написанных функций.
import psycopg2
from psycopg2 import Error


def drop_table(cur):
    """Удаляет таблицы, если они существуют."""
    cur.execute("""
        DROP TABLE phones;
        DROP TABLE data_table;
    """)
    
def create_table (cur):
    '''Функция, создающая структуру БД (таблицы).'''        
    cur.execute("""
        CREATE TABLE IF NOT EXISTS data_table(
            id SERIAL PRIMARY KEY,
            name VARCHAR(40) NOT NULL,
            surname VARCHAR(40) NOT NULL,
            email VARCHAR(40) UNIQUE NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES data_table(id) ON DELETE CASCADE,
            phone VARCHAR(20)
        );
    """)
    print("Таблицы созданы (если не существовали)")
        
def add_client(cur, name, surname, email, phones=None):
    '''Функция, позволяющая добавить нового клиента'''
    cur.execute('''
        INSERT INTO data_table(name, surname, email)
        VALUES(%s, %s, %s)
        RETURNING id;
    ''', (name, surname, email))
    client_id = cur.fetchone()[0]
    
    if phones:
        for phone in phones:
            cur.execute(''' 
                INSERT INTO phones(client_id, phone)
                VALUES(%s, %s);
            ''', (client_id, phone))
    print(f"Клиент {name} {surname} добавлен с ID {client_id}.")
                    
def add_phone_client(cur, email, phones):
    '''Функция, позволяющая добавить телефон для существующего клиента.'''
    client_id = check_verification(cur, email)
    if client_id:
        for phone in phones:
            cur.execute('''
                INSERT INTO phones(client_id, phone)
                VALUES(%s, %s);
            ''', (client_id[0], phone))
        phones_str = ', '.join(phones)
        print(f'телефон(-ы) {phones_str} добавлен(-ы) для клинта с email= {email}')
    else:
        print(f"Клиента с email = {email} не существует.")

def changing_information(cur, email, name=None, surname=None, phones=None, new_email=None):
    '''Функция, позволяющая изменить данные о клиенте'''
    client_information = check_verification(cur, email)
    if client_information: 
        if phones:
            deleting_phone(cur, email)
            for phone in phones:
                cur.execute("""
                    INSERT INTO phones (client_id, phone)
                    VALUES (%s, %s);
                """, (client_information[0], phone))
            print(f"Телефон(-ы) клиента с email = {email} обновлены.")
                
        if name or surname or new_email:
            cur.execute("""
                UPDATE data_table 
                SET 
                    name = COALESCE(%s, name),
                    surname = COALESCE(%s, surname), 
                    email = COALESCE(%s, email)
                WHERE id=%s;
            """, (name, surname, new_email, client_information[0]))
            print(f"Данные клиента с email = {email} обновлены.")
    else:
        print(f"Клиента с email = {email} не существует.")

def deleting_phone(cur, email):
    '''Функция, позволяющая удалить телефон для существующего клиента.'''
    client_information = check_verification(cur, email)
    if client_information:
        cur.execute('''
            DELETE FROM phones WHERE client_id=%s;
        ''',(client_information[0],))
        print(f"Телефоны клиента с email = {email} удалены.")
    else:
        print(f"Клиента с email = {email} не существует.")
    
def delete_client(cur, email):
    '''Функция, позволяющая удалить существующего клиента'''
    client_information = check_verification(cur, email)
    if client_information:
        cur.execute('''
            DELETE FROM data_table WHERE id=%s;
        ''', (client_information[0],))
        
def check_verification(cur, email):
    """Проверяет существование клиента по email"""
    cur.execute('''
        SELECT * FROM data_table WHERE email=%s;
    ''', (email,))
    response = cur.fetchone()
    if response:
        return response
    else:
        return None

def find_client(cur, name=None, surname=None, email=None, phone=None):
    """Ищет клиента по имени, фамилии, email или телефону."""
    query = '''
        SELECT d.id, d.name, d.surname, d.email, STRING_AGG(p.phone, ', ') AS phones
        FROM data_table d
        LEFT JOIN phones p ON d.id = p.client_id
        WHERE 1=1
    '''
    params = []
    if name:
        query += " AND d.name = %s"
        params.append(name)
    if surname:
        query += " AND d.surname = %s"
        params.append(surname)
    if email:
        query += " AND d.email = %s"
        params.append(email)
    if phone:
        query += " AND p.phone = %s"
        params.append(phone)
    
    query += " GROUP BY d.id, d.name, d.surname, d.email"
    
    cur.execute(query, tuple(params))
    return cur.fetchall()
    
def all(cur):
    '''Выводит всю информацию о клиентах и их телефонах.'''
    cur.execute('''
        SELECT d.id, d.name, d.surname, d.email, STRING_AGG(p.phone, ', ') AS phones
        FROM data_table d
        LEFT JOIN phones p ON d.id = p.client_id
        GROUP BY d.id, d.name, d.surname, d.email
    ''')
    print("Результаты из data_table и phones:")
    for row in cur.fetchall():
        print(row)                   

try:
    with psycopg2.connect(database='customer_base', user='postgres', password='@danilWrestling89', client_encoding='UTF8') as conn:
        with conn.cursor() as cur:
            drop_table(cur)
            create_table(cur)
            add_client(cur, 'Данил', 'Добронравов', 'danil@mail.ru', ['81111111111'])
            add_client(cur, 'Юля', 'Лисичка', 'lisa@mail.ru')
            add_client(cur, 'Жора', 'Якутов', 'qwert@mail.ru', ['82222222222', '83333333333'])
            add_phone_client(cur, 'lisa@mail.ru', ['84444444444', '85555555555']) 
            changing_information(cur, 'lisa@mail.ru', name='Юлия',surname='Добронравова', phones=['86666666666', '87777777777'], new_email='new@mai.ru')
            deleting_phone(cur, 'new@mai.ru')
            delete_client(cur, 'danil@mail.ru' )
            check_verification(cur, 'danil@mail.ru')
            # Поиск клиента
            print("Результаты поиска:")
            print(find_client(cur, 'Жора'))
            print(find_client(cur, phone='82222222222'))
            print(find_client(cur, email='qwert@mail.ru'))
            all(cur)
            conn.commit()
except Error as e:
    print(f"Ошибка при работе с базой данных: {e}")
finally:
    if conn:
        conn.close()
        print("Соединение с базой данных закрыто.")
    

            
    

