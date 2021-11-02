import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()


cria_tabela= "CREATE TABLE if not exists hoteis(hotel_id text PRIMARY_KEY, nome text, estrelas real, diaria real, cidade text)"

cria_hotel="INSERT INTO TABLE hoteis VALUES ('alpha', 'alpha hotel', 4.3, 344, 'Bahia')"

cursor.execute(cria_tabela)
cursor.execute(cria_hotel)
connection.commit()
connection.close()