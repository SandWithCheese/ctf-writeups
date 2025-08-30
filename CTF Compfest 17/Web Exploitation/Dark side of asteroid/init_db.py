import sqlite3
import hashlib

def init_db():
    FLAG = 'COMPFEST17{FAKEFLAG}'
    conn = sqlite3.connect('asteroids.db')
    c = conn.cursor()

    # Users table + kolom profile_url
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'guest',
        profile_picture TEXT DEFAULT '',
        profile_type TEXT DEFAULT ''
        )
    ''')

    # Asteroids table
    c.execute('''
        CREATE TABLE IF NOT EXISTS asteroids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    # Admin secrets table
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin_secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            secret_name TEXT,
            secret_value TEXT,
            access_level INTEGER
        )
    ''')

    # Add default secrets
    secrets = [
        ('Flag', FLAG, 3),
        ('final_message', 'You made it! Remember: the flag belongs to those who trust their own path.', 3),
        ('author_message', 'You sure you can get the flag? Think twice…', 2),
        ('welcome_note', 'Welcome to the Asteroid Admin system!', 1)
    ]
    for s in secrets:
        c.execute('INSERT OR IGNORE INTO admin_secrets (secret_name, secret_value, access_level) VALUES (?, ?, ?)', s)


    # Add some default asteroid data (10 asteroid)
    asteroids = [
        ('Ceres', 'The largest object in the asteroid belt between Mars and Jupiter.'),
        ('Pallas', 'Second-largest asteroid, discovered in 1802.'),
        ('Vesta', 'Brightest asteroid visible from Earth, has a differentiated interior.'),
        ('Hygiea', 'Fourth-largest asteroid, nearly spherical.'),
        ('Eros', 'First asteroid orbited and landed on by a spacecraft (NEAR Shoemaker).'),
        ('Itokawa', 'Visited by Japanese spacecraft Hayabusa.'),
        ("Bennu", "Target of NASA's OSIRIS-REx mission, potentially hazardous."),
        ('Ryugu', "Visited by Japan's Hayabusa2 mission, diamond-shaped."),
        ('Davida', 'One of the largest C-type asteroids.'),
        ('Psyche', "Rich in metal, target of NASA's Psyche mission.")
    ]
    for asteroid in asteroids:
        c.execute('INSERT OR IGNORE INTO asteroids (name, description) VALUES (?, ?)', asteroid)

    conn.commit()
    conn.close()
    print("[+] Database initialized successfully with default data.")

if __name__ == '__main__':
    init_db()
