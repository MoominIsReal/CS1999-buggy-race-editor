import sqlite3
import config as Config

# important:
# -------------------------------------------------------------
# This script initialises your database for you using SQLite,
# just to get you started... there are better ways to express
# the data you're going to need... especially outside SQLite.
# For example... maybe flag_pattern should be an ENUM (which
# is available in most other SQL databases), or a foreign key
# to a pattern table?
#
# Also... the name of the database (here, in SQLite, it's a
# filename) appears in more than one place in the project.
# That doesn't feel right, does it?
#
# -------------------------------------------------------------

con = sqlite3.connect(Config.DATABASE_FILE)
print("- Opened database successfully in file \"{}\"".format(Config.DATABASE_FILE))

# using Python's triple-quote for multi-line strings:

con.execute("""

  CREATE TABLE IF NOT EXISTS buggies (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    qty_wheels            INTEGER DEFAULT 4,
    power_type            VARCHAR(20) DEFAULT "petrol",
    power_units           INTEGER DEFAULT 1,
    aux_power_type        VARCHAR(20) DEFAULT "none",
    aux_power_units       INTEGER DEFAULT 0,
    hamster_booster       INTEGER DEFAULT 0,
    flag_color_primary    VARCHAR(20) DEFAULT "#ffffff",
    flag_color_secondary  VARCHAR(20) DEFAULT "#000000",
    flag_pattern          VARCHAR(20) DEFAULT "plain",
    tyres                 VARCHAR(20) DEFAULT "knobbly",
    qty_tyres             INTEGER DEFAULT 4,
    armour                VARCHAR(20) DEFAULT "none",
    attack                VARCHAR(20) DEFAULT "none",
    qty_attacks           INTEGER DEFAULT 0,
    fireproof             BOOLEAN DEFAULT false,
    insulated             BOOLEAN DEFAULT false,
    antibiotic            BOOLEAN DEFAULT false,
    banging               BOOLEAN DEFAULT false,
    algo                  VARCHAR(20) DEFAULT "steady"
  )

""")

print("- Table \"buggies\" exists OK")

cur = con.cursor()

cur.execute("SELECT * FROM buggies LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
    cur.execute("INSERT INTO buggies (qty_wheels) VALUES (4)")
    con.commit()
    print("- Added one 4-wheeled buggy")
else:
    print("- Found a buggy in the database, nice")
print("- done")

con.close()
