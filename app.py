from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
import config as Config

app = Flask(__name__)


# ------------------------------------------------------------
# the index page
# ------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=Config.BUGGY_RACE_SERVER_URL)


# ------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
# ------------------------------------------------------------
@app.route('/new', methods=['POST', 'GET'])
def create_buggy():
    err = False
    wheels_err = False
    qty_err = False
    power_err = False
    aux_power_err = False
    value_err_msg = "Please enter a valid number"
    even_num_msg = "Please enter an even number of wheels"
    qty_wheels_int = 0

    if request.method == 'GET':
        return render_template("buggy-form.html")
    elif request.method == 'POST':
        msg = ""

        try:
            qty_wheels = request.form['qty_wheels']
            power_type = request.form['power_type']
            power_units = request.form['power_units']
            aux_power_type = request.form['aux_power_type']
            aux_power_units = request.form['aux_power_units']
            hamster_booster = request.form['hamster_booster']
            flag_color_primary = request.form['flag_color_primary']
            flag_color_secondary = request.form['flag_color_secondary']
            flag_pattern = request.form['flag_pattern']
            tyres = request.form['tyres']
            qty_tyres = request.form['qty_tyres']
            armour = request.form['armour']
            attack = request.form['attack']
            qty_attacks = request.form['qty_attacks']
            fireproof = request.form['fireproof']
            insulated = request.form['insulated']
            antibiotic = request.form['antibiotic']
            banging = request.form['banging']
            algo = request.form['algo']

            msg = f"qty_wheels={qty_wheels}"

            with sql.connect(Config.DATABASE_FILE) as con:

                if not qty_wheels.isdigit():
                    err = True
                    wheels_err = True
                else:
                    qty_wheels_int = int(request.form['qty_wheels'])

                if qty_wheels_int % 2 != 0:
                    err = True
                    qty_err = True

                if not power_units.isdigit():
                    err = True
                    power_err = True

                if not aux_power_units.isdigit():
                    err = True
                    aux_power_err = True

                cur = con.cursor()
                cur.execute(
                    "UPDATE buggies set qty_wheels=?, power_type=?, power_units=?, aux_power_type=?,"
                    " aux_power_units=?, hamster_booster=?,"
                    " flag_color_primary=?, flag_color_secondary=?, flag_pattern=?,"
                    " tyres=?,qty_tyres=?,armour=?,attack=?,qty_attacks=?,"
                    "fireproof=?, insulated=?, antibiotic=?, banging=?, algo=? WHERE id=?",
                    (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster,
                     flag_color_primary, flag_color_secondary, flag_pattern, tyres,
                     qty_tyres, armour, attack, qty_attacks, fireproof, insulated,
                     antibiotic, banging, algo, Config.DEFAULT_BUGGY_ID))
                con.commit()
                msg = "Record successfully saved"

        except Exception as e:
            con.rollback()
            print(e)
            msg = "error in update operation"
        finally:
            con.close()
            if err:
                return render_template("buggy-form.html", wheels_err=wheels_err, power_err=power_err,
                                       aux_power_err=aux_power_err, qty_err=qty_err, value_err_msg=value_err_msg,
                                       even_num_msg=even_num_msg)
            else:
                return render_template("updated.html", msg=msg)


# ------------------------------------------------------------
# a page for displaying the buggy
# ------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(Config.DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone()
    return render_template("buggy.html", buggy=record)


# ------------------------------------------------------------
# a page for displaying the buggy
# ------------------------------------------------------------
@app.route('/new')
def edit_buggy():
    return render_template("buggy-form.html")


# ------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
# ------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(Config.DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", Config.DEFAULT_BUGGY_ID)
    return jsonify(
        {k: v for k, v in dict(zip(
            [column[0] for column in cur.description], cur.fetchone())).items()
         if (v != "" and v is not None)
         }
    )


# ------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
# ------------------------------------------------------------
@app.route('/delete', methods=['POST'])
def delete_buggy():
    try:
        msg = "deleting buggy"
        with sql.connect(Config.DATABASE_FILE) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM buggies")
            con.commit()
            msg = "Buggy deleted"
    except:
        con.rollback()
        msg = "error in delete operation"
    finally:
        con.close()
        return render_template("updated.html", msg=msg)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
