import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('hospital.sqlite')
cur = conn.cursor()

# Make some fresh tables
cur.executescript('''
DROP TABLE IF EXISTS Hospital;
DROP TABLE IF EXISTS Provinsi;

CREATE TABLE Hospital (
    id  INTEGER PRIMARY KEY,
    provinsi_id INTEGER,
    Hospital TEXT UNIQUE,
    FOREIGN KEY (provinsi_id) REFERENCES Provinsi(id)
);

CREATE TABLE Provinsi (
    id  INTEGER PRIMARY KEY UNIQUE,
    Province TEXT UNIQUE
);
''')

handle = open('Hospital_Indonesia_datasets.csv')

for line in handle:
    if line.startswith('id'): continue
    line = line.strip()
    pieces = line.split(';')

    Hospital = pieces[1]
    Province = pieces[2]

    print(Hospital,Province)

    cur.execute('''INSERT OR IGNORE INTO Provinsi (Province) VALUES (?)''', (Province,))
        
        # take ID province
    cur.execute('''SELECT id FROM Provinsi WHERE Province = ?''', (Province,))
    provinsi_id = cur.fetchone()[0]

        # input hospital data to hospital table
    cur.execute('''INSERT OR IGNORE INTO Hospital (provinsi_id, Hospital) VALUES (?, ?)''', (provinsi_id, Hospital))

cur.execute('''
    SELECT Provinsi.Province, COUNT(Hospital.id) AS NOH
    FROM Hospital
    JOIN Provinsi ON Hospital.provinsi_id = Provinsi.id
    GROUP BY Provinsi.Province
''')

# take query result
data = cur.fetchall()  # List of tuples (Province, Number of Hospitals)

conn.commit()
conn.close()

provinces = [row[0] for row in data]
num_hospitals = [row[1] for row in data]

plt.figure(figsize=(12, 6))
plt.barh(provinces, num_hospitals, color='skyblue')
plt.xlabel('Number of Hospitals')
plt.ylabel('Province')
plt.title('Number of Hospitals in Each Province')
plt.show()
