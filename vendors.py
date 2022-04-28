from flask import render_template, request, redirect, url_for
from app import app
import psycopg2
from dbconfig import config

conn = None


def get_vendors():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT vendor_id, vendor_name, address FROM vendors ORDER BY vendor_id")
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows


def insert_vendors(vendor_name, address):
    sql = """INSERT INTO vendors(vendor_name, address)
             VALUES(%s,%s) RETURNING vendor_id;"""
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (vendor_name, address,))
        vendor_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return vendor_id


def delete_vendors(vendor_id):
    sql = """delete from vendors where vendor_id = %s;"""
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (vendor_id,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return 1


def update_vendors(vendor_name, vendor_id, address):
    sql = """update vendors set vendor_name = %s, address = %s where vendor_id = %s;"""
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (vendor_name, address, vendor_id,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return 1


def search_vendors(id):
    sql = "select * from vendors where vendor_id =%s"
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (id,))
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows


@app.route('/vendor')
def vendors():
    rows = get_vendors()
    return render_template('vendors.html', rows=rows)


@app.route('/new_vendor', methods=['GET', 'POST'])
def New_vendor():
    name = request.form.get("pname")
    address = request.form.get("address")
    if request.method == 'POST':
        insert_vendors(name, address)
        return redirect(url_for('vendors'))
    return render_template('new_vendor.html')


@app.route('/delete_vendor/<int:id>', methods=['GET', 'POST'])
def delete_vendor(id):
    delete_vendors(id)
    return redirect(url_for('vendors'))


@app.route('/update_vendor/<int:id>', methods=['GET', 'POST'])
def update_vendor(id):
    rows = search_vendors(id)
    if request.method == 'POST':
        name = request.form.get("pname")
        address = request.form.get("address")
        update_vendors(name, id, address)
        return redirect(url_for('vendors'))
    return render_template('update_vendor.html', rows=rows)