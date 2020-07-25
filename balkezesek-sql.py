'''
név;         első;        utolsó;      súly;   magasság
 0             1             2           3        4
Jim Abbott;  1989-04-08;  1999-07-21;  200;      75
'''
import sqlite3
conn = sqlite3.connect('balkezesek.db')
c = conn.cursor()

def sql(sql_parancs, *args):
    c.execute(sql_parancs, *args)
    return c.fetchall()

sql(" DROP TABLE IF EXISTS balkezesek ")
sql("""
    CREATE TABLE IF NOT EXISTS balkezesek
    (név      TEXT,
    első      TEXT,
    utolsó    TEXT,
    súly      INTEGER,
    magasság  INTEGER)
""")
conn.commit()

with open('balkezesek.csv', encoding='latin2') as f:
    fejlec = f.readline().strip()
    for sor in f:
        sql( "INSERT INTO balkezesek VALUES (?,?,?,?,?)", (sor.strip().replace(',','.').split(';') ) )
conn.commit()

#3. Hány adatsor van az állományban?
sorok_szama= sql(" SELECT count() FROM  balkezesek ")[0][0]    
print( f'3. feladat: {sorok_szama}' )

#4. Írja ki azok nevér és magasságát akik utoljára 1999 októberében léptek pályára.
fetch = sql(" SELECT név, magasság FROM  balkezesek WHERE utolsó LIKE  '1999-10-%' ")
print(   f'4. feladat: ' )
[ print( f'        {név}, {magasság * 2.54:.1f} cm' ) for név, magasság in fetch ]

#5. Kérjen be a felhasználótól egy 1990 és 1999 közötti évszámot
print(   f'5. feladat: ' )
while True:
    év = input('Kérek egy 1990 és 1999 közötti évszámot!:')
    if '1990' <= év <= '1999':
        break
    else:
        print(f'Hibás adat!', end='')

#6. Mennyi az átlagsúlya fontban az {év} évben pályára lépett játékosoknak két tizedesre kerekítve.
átlagsúly = sql(f" SELECT AVG(súly) FROM  balkezesek WHERE első <= '{év}-12-32'  AND '{év}-00-00' < utolsó    " )[0][0]
print( f'6. feladat: {átlagsúly:.2f} font' )



