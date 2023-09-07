import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory, abort, flash
from database_connection import *
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import uuid
# import aiohttp

# inisiasi variabel
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
app.config.from_pyfile('config.py')
app.secret_key = app.config['APP_KEY']

# Database
key =  app.config['DB_KEY']
f = Fernet(key)

# Route untuk halaman login
@app.route('/login/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Jika user mengirimkan data melalui form login
    if request.method == 'POST':
        # Inisiasi variabel email dan password dari form login
        loginEmail = request.form['loginEmail']
        loginPassword = request.form['loginPassword']
        auth = False
        
        # Eksekusi query untuk mengecek apakah email dan password ada di database dengan data yang dienkripsi
        # users = read_data("SELECT * FROM `user`" ,None, "fetchall")
        query = "SELECT * FROM `user`"
        params = None
        users = read_data(query, params, "fetchall")
            
        for user in users:
            email = user['email']
            password = user['password']

            if email == loginEmail and password == loginPassword:
                # if user['email_validated'] == 1:
                    auth = True
                    break
                # else:
                #     return render_template('login.html',msg='Email belum diverifikasi'), 200
        
        # Jika usernama dan password ada di database, maka user akan diarahkan ke halaman dashboard
        if auth:
            # Inisiasi session untuk menyimpan data user
            session['email'] = user['email']
            session['nama'] = user['nama']
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            session['nim'] = user['nim']
            
            # Redirect user ke halaman dashboard
            return redirect(url_for('dashboard'))
        
        # Jika usernama dan password tidak ada di database, maka user akan diarahkan ke halaman login
        else:
            return render_template('login.html',msg='Email atau password salah'), 200

    # Jika user mengakses halaman login tanpa mengirimkan data melalui form login (GET)
    # check if user is already logged in
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    return render_template('login.html',msg=''), 200

# Route untuk logout
@app.route('/logout/', methods=['GET'])
@app.route('/logout', methods=['GET'])
def logout():
    # Menghapus semua data session
    session.clear()
    # Redirect user ke halaman dashboard
    return redirect(url_for('login'))
    
# Route untuk halaman dashboard
@app.route('/', methods=['GET'])
@app.route('/dashboard/', methods=['GET'])
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))


# Route untuk halaman Daftar Pengguna
@app.route('/user/<user_id>', methods=['GET'])
def user(user_id=None):
    # mysql = connect_db()
    if 'user_id' in session:
        if request.method == 'GET':
            if session['role'] == 'Admin' and user_id == 'all':
                query = "SELECT `user_id`,`nama`,`email`,`role`,`nim` FROM `user`"
                params = None
                users = read_data(query, params, "fetchall")
                if users:
                    for user in users:
                        user['user_id'] = user['user_id']
                        user['nama'] = user['nama']
                        user['email'] = user['email']
                        user['nim'] = user['nim']
                        user['role'] = user['role']
                    return render_template('manajemenUser.html', users=users)
                return render_template('manajemenUser.html', users=None)
            
            elif user_id != None:
                if session['role'] == 'Admin' or session['user_id'] == user_id:
                    # query = f"SELECT * FROM `user` WHERE `user_id` = '{user_id}'"
                    # user = read_data(query, "fetchone")
                    query = "SELECT * FROM `user` WHERE `user_id` = %s"
                    params = (user_id,)
                    user = read_data(query, params, "fetchone")
                    if user:
                        user['nama'] = user['nama']
                        user['email'] = user['email']
                        user['password'] = user['password']
                        return render_template('user.html', user=user)
                    return abort(406)
                return abort(403)
            return abort(400)
        return abort(405)        
    return abort(401)

@app.route('/add_user', methods=['GET', 'POST'])
@app.route('/add_user/', methods=['GET', 'POST'])
def add_user():
    if 'user_id' in session:
        if request.method == 'GET':
            if session['role'] == 'Admin':
                return render_template('addUser.html')
            return abort(403)
        
        elif request.method == 'POST':
            if session['role'] == 'Admin':
                query = "SELECT `email` FROM `user`"
                params = None
                user_emails = read_data(query, params, "fetchall")
                for user_email in user_emails:
                    if request.form['email'] in user_email['email']:
                        return render_template('addUser.html', msg='Email sudah terdaftar')
                    
                nama = request.form['nama']
                nim = request.form['nim']
                email = request.form['email']
                password = request.form['password']
                role = request.form['role']

                prefix = ''
                if role == 'Admin':
                    prefix = 'ADM'
                elif role == 'Mahasiswa':
                    prefix = 'MHS'

                query = "SELECT `user_id` FROM `user` WHERE `user_id` LIKE %s ORDER BY `user_id` DESC LIMIT 1"
                count = read_data(query, (f"{prefix}%",), "fetchone")

                if count:
                    last_user_id = count['user_id']
                    last_user_id_number = int(last_user_id[3:])
                    generated_user_id = f"{prefix}{str(last_user_id_number + 1).zfill(4)}"
                else:
                    generated_user_id = f"{prefix}001"

                query = "INSERT INTO `user` (`user_id`, `email`, `password`, `nama`, `role`, `nim`) VALUES (%s, %s, %s, %s, %s, %s)"
                params = (generated_user_id, email, password, nama, role, nim)
                write_data(query, params)

                return redirect(url_for('user', user_id='all'))
            return abort(403)
        return abort(405)
    return abort(401)

@app.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' in session:
        if request.method == 'GET':
            if session['role'] == 'Admin' or session['user_id'] == user_id:
                query = "SELECT * FROM `user` WHERE `user_id` = %s"
                params = (user_id,)
                user = read_data(query, params, "fetchone")
                return render_template('editUser.html', user=user, msg=""), 201
                # return abort(406)
            return abort(403)
        
        elif request.method == 'POST':
            if session['role'] == 'Admin' or session['user_id'] == user_id:
                editted_user_id = request.form['user_id']
                nama = request.form['new_nama']
                email = request.form['new_email']
                nim = request.form['new_nim']
                role = request.form['new_role']
                current_password = request.form.get('password')
                password = request.form.get('new_password')
                query = "SELECT * FROM `user` WHERE `user_id` = %s"
                params = (editted_user_id,)
                editted_user = read_data(query, params, "fetchall")
                
                for user in editted_user:
                    if user['nama'] != nama:
                        query = "UPDATE `user` SET `nama` = %s WHERE `user_id` = %s"
                        params = (nama, editted_user_id)
                        write_data(query, params)
                        session['nama'] = nama
                        
                        if session['user_id']==editted_user_id:
                            session['nama'] = nama
                                        
                    if user['email'] != email:
                        query = "UPDATE `user` SET `email` = %s WHERE `user_id` = %s"
                        params = (email, editted_user_id)
                        write_data(query, params)
                        
                        if session['user_id']==editted_user_id:
                            session['email'] = email
                    
                    if user['nim'] != nim:
                        query = "UPDATE `user` SET `nim` = %s WHERE `user_id` = %s"
                        params = (nim, editted_user_id)
                        write_data(query, params)
                        
                        if session['user_id']==editted_user_id:
                            session['nim'] = nim

                    if user['role'] != role:
                        query = "UPDATE `user` SET `role` = %s WHERE `user_id` = %s"
                        params = (role, editted_user_id)
                        write_data(query, params)
                   
                        if session['user_id']==editted_user_id:
                            session['role'] = role

                    
                    if current_password != "":
                        if current_password == user['password']:
                            if user['password'] != password:
                                query = "UPDATE `user` SET `password` = %s WHERE `user_id` = %s"
                                params = (password, editted_user_id)
                                write_data(query, params)

                        else:
                            if session['role'] == 'Admin' or session['user_id'] == user_id:
                                query = "SELECT * FROM `user` WHERE `user_id` = %s"
                                params = (user_id,)
                                user = read_data(query, params, "fetchone")
                                if user:
                                    user['nama'] = user['nama']
                                    user['email'] = user['email']
                                    user['password'] = user['password']

                            return render_template('editUser.html', user=user, msg="Password Salah!"), 400
                            
                return redirect(url_for('edit_user', user_id=editted_user_id))
            return abort(403)
        return abort(405)
    return abort(401)

@app.route('/delete_user/<user_id>', methods=['GET'])
def delete_user(user_id):
    if 'user_id' in session:
        if session['role'] == 'Admin':
            query = "SELECT * FROM `user` WHERE `user_id` = %s"
            params = (user_id,)
            to_be_deleted_user = read_data(query, params, "fetchone")
            
            if to_be_deleted_user:
                query = "DELETE FROM `user` WHERE `user_id` = %s"
                write_data(query, params)
    
                return redirect(url_for('user', user_id='all'))
            return abort(406)
        return abort(403)          
    return abort(401)

@app.route('/ruangan/', methods=['GET'])
@app.route('/ruangan', methods=['GET'])
def ruangan():
    # mysql = connect_db()
    if 'user_id' in session:
        if session['role'] == 'Admin':
            query = "SELECT * FROM `ruang_praktikum` ORDER BY `id_ruangan` ASC"
            params = None
            rooms = read_data(query, params)
            return render_template('ruangan.html', rooms=rooms)
        # return error code 403 if user is not a admin
        return abort(403)
    return abort(401)

@app.route('/add_ruangan/', methods=['GET', 'POST'])
@app.route('/add_ruangan', methods=['GET', 'POST'])
def add_ruangan():
    if 'user_id' in session:
        if request.method == 'GET':
            if session['role'] == 'Admin':
                return render_template('addRuangan.html')
            # return abort(403)

        elif request.method == 'POST':
            if session['role'] == 'Admin':
                query = "SELECT `id_ruangan` FROM `ruang_praktikum`"
                params = None
                rooms = read_data(query, params, "fetchall")
                for room in rooms:
                    if request.form['id_ruangan'] in room['id_ruangan']:
                        return render_template('addAlat.html', msg='Ruangan sudah terdaftar')
                    
                nama = request.form['nama']
                id_ruangan = request.form['id_ruangan']
                lokasi = request.form['lokasi']

                query = "INSERT INTO `ruang_praktikum` (`nama`, `id_ruangan`, `lokasi`, `status_peminjaman`) VALUES (%s, %s, %s, %s)"
                params = (nama, id_ruangan, lokasi, "Available")
                write_data(query, params)

                return redirect(url_for('ruangan'))
            return abort(403)
        return abort(405)
    return abort(401)

@app.route('/edit_ruangan/<id_ruangan>', methods=['GET', 'POST'])
def edit_ruangan(id_ruangan):
    if 'user_id' in session:
        if request.method == 'GET':
            if session['role'] == 'Admin':
                query = "SELECT * FROM `ruang_praktikum` WHERE `id_ruangan` = %s"
                params = (id_ruangan,)
                room = read_data(query, params, "fetchone")
                return render_template('editRuangan.html', room=room, msg=""),201
                # return abort(406)
            return abort(403)
        
        elif request.method == 'POST':
            if session['role'] == 'Admin':
                editted_room_id = id_ruangan
                nama = request.form['nama']
                room_id= request.form.get('id_ruangan')
                lokasi = request.form['lokasi']
                query = "SELECT * FROM `ruang_praktikum` WHERE `id_ruangan` = %s"
                params = (room_id,)
                editted_room = read_data(query, params, "fetchall")
                
                for room in editted_room:
                    if room['nama'] != nama:
                        query = "UPDATE `ruang_praktikum` SET `nama` = %s WHERE `id_ruangan` = %s"
                        params = (nama, editted_room_id)
                        write_data(query, params)
                                        
                    if room['id_ruangan'] != room_id:
                        query = "SELECT `id_ruangan` FROM `ruang_praktikum` WHERE `id_ruangan` = %s"
                        params = (room_id,)
                        existing_room = read_data(query, params, "fetchone")

                        if not room_id in existing_room:
                            query = "UPDATE `ruang_praktikum` SET `id_ruangan` = %s WHERE `id_ruangan` = %s"
                            params = (room_id, editted_room_id)
                            write_data(query, params)
                    
                    if room['lokasi'] != lokasi:
                        query = "UPDATE `ruang_praktikum` SET `lokasi` = %s WHERE `id_ruangan` = %s"
                        params = (lokasi, editted_room_id)
                        write_data(query, params)

                return redirect(url_for('ruangan'))
            return abort(403)
        return abort(405)
    return abort(401)

@app.route('/delete_ruangan/<id_ruangan>', methods=['GET'])
def delete_ruangan(id_ruangan):
    if 'user_id' in session:
        if session['role'] == 'Admin':
            query = "SELECT * FROM `ruang_praktikum` WHERE `id_ruangan` = %s"
            params = (id_ruangan,)
            to_be_deleted_room = read_data(query, params, "fetchone")
            
            if to_be_deleted_room:
                query = "DELETE FROM `ruang_praktikum` WHERE `id_ruangan` = %s"
                write_data(query, params)
    
                return redirect(url_for('ruangan'))
            return abort(406)
        return abort(403)          
    return abort(401)
        
@app.route('/alat/', methods=['GET'])
@app.route('/alat', methods=['GET'])
def alat():
    # mysql = connect_db()
    if 'user_id' in session:
        if session['role'] == 'Admin':
            query = "SELECT * FROM `alat_praktikum` ORDER BY `id_alat` ASC"
            params = None
            tools = read_data(query, params)
            return render_template('alat.html', tools=tools)
        # return error code 403 if user is not a admin
        return abort(403)
    return abort(401)

@app.route('/add_alat/', methods=['GET', 'POST'])
@app.route('/add_alat', methods=['GET', 'POST'])
def add_alat():
    if 'user_id' in session:
        if request.method == 'GET':
            if session['role'] == 'Admin':
                return render_template('addAlat.html')
            # return abort(403)

        elif request.method == 'POST':
            if session['role'] == 'Admin':
                query = "SELECT `id_alat` FROM `alat_praktikum`"
                params = None
                tools = read_data(query, params, "fetchall")
                for tool in tools:
                    if request.form['id_alat'] in tool['id_alat']:
                        return render_template('addAlat.html', msg='alat sudah terdaftar')
                    
                nama = request.form['nama']
                id_alat = request.form['id_alat']
                spesifikasi_alat = request.form['spesifikasi_alat']

                query = "INSERT INTO `alat_praktikum` (`nama`, `id_alat`, `spesifikasi_alat`, `status_peminjaman`) VALUES (%s, %s, %s, %s)"
                params = (nama, id_alat, spesifikasi_alat, "Available")
                write_data(query, params)

                return redirect(url_for('alat'))
            return abort(403)
        return abort(405)
    return abort(401)

@app.route('/edit_alat/<id_alat>', methods=['GET', 'POST'])
def edit_alat(id_alat):
    if 'user_id' in session:
        if request.method == 'GET':
            if session['role'] == 'Admin':
                query = "SELECT * FROM `alat_praktikum` WHERE `id_alat` = %s"
                params = (id_alat,)
                tool = read_data(query, params, "fetchone")
                return render_template('editAlat.html', tool=tool, msg=""),201
                # return abort(406)
            return abort(403)
        
        elif request.method == 'POST':
            if session['role'] == 'Admin':
                editted_tool_id = id_alat
                nama = request.form['nama']
                tool_id= request.form.get('id_alat')
                spesifikasi_alat = request.form['spesifikasi_alat']
                query = "SELECT * FROM `alat_praktikum` WHERE `id_alat` = %s"
                params = (id_alat,)
                editted_tool = read_data(query, params, "fetchall")
                for tool in editted_tool:
                    if tool['nama'] != nama:
                        query = "UPDATE `alat_praktikum` SET `nama` = %s WHERE `id_alat` = %s"
                        params = (nama, editted_tool_id)
                        write_data(query, params)
                                        
                    if tool['id_alat'] != tool_id:
                        query = "SELECT `id_alat` FROM `alat_praktikum` WHERE `id_alat` = %s"
                        params = (tool_id,)
                        existing_tool = read_data(query, params, "fetchone")

                        if not existing_tool == []:
                            query = "UPDATE `alat_praktikum` SET `id_alat` = %s WHERE `id_alat` = %s"
                            params = (tool_id, editted_tool_id)
                            write_data(query, params)

                        elif not tool_id in existing_tool:
                            query = "UPDATE `alat_praktikum` SET `id_alat` = %s WHERE `id_alat` = %s"
                            params = (tool_id, editted_tool_id)
                            write_data(query, params)
                    
                    if tool['spesifikasi_alat'] != spesifikasi_alat:
                        query = "UPDATE `alat_praktikum` SET `spesifikasi_alat` = %s WHERE `id_alat` = %s"
                        params = (spesifikasi_alat, editted_tool_id)
                        write_data(query, params)

                return redirect(url_for('alat'))
            return abort(403)
        return abort(405)
    return abort(401)

@app.route('/delete_alat/<id_alat>', methods=['GET'])
def delete_alat(id_alat):
    if 'user_id' in session:
        if session['role'] == 'Admin':
            query = "SELECT * FROM `alat_praktikum` WHERE `id_alat` = %s"
            params = (id_alat,)
            to_be_deleted_room = read_data(query, params, "fetchone")
            
            if to_be_deleted_room:
                query = "DELETE FROM `alat_praktikum` WHERE `id_alat` = %s"
                write_data(query, params)
    
                return redirect(url_for('alat'))
            return abort(406)
        return abort(403)          
    return abort(401)

@app.route('/arsip/', methods=['GET'])
@app.route('/arsip', methods=['GET'])
def arsip():
    # mysql = connect_db()
    if 'user_id' in session:
        if session['role'] == 'Admin':
            query = "SELECT * FROM `arsip_ta` ORDER BY `id_arsip` ASC"
            params = None
            archives = read_data(query, params)
            return render_template('arsip.html', archives=archives)
        # return error code 403 if user is not a admin
        return abort(403)
    return abort(401)

@app.route('/add_arsip/', methods=['GET', 'POST'])
@app.route('/add_arsip', methods=['GET', 'POST'])
def add_arsip():
    if 'user_id' in session:
        if request.method == 'GET':
            if session['role'] == 'Admin':
                return render_template('addArsip.html')
            # return abort(403)

        elif request.method == 'POST':
            if session['role'] == 'Admin':
                query = "SELECT `id_arsip` FROM `arsip_ta`"
                params = None
                archives = read_data(query, params, "fetchall")
                for archive in archives:
                    if request.form['id_arsip'] in archive['id_arsip']:
                        return render_template('addArsip.html', msg='Arsip sudah terdaftar')
                    
                topik_arsip = request.form['topik_arsip']
                id_arsip = request.form['id_arsip']
                tanggal_arsip = request.form['tanggal_arsip']
                penulis_arsip = request.form['penulis_arsip']

                query = "INSERT INTO `arsip_ta` (`topik_arsip`, `id_arsip`, `tanggal_arsip`, `penulis_arsip`, `status_peminjaman`) VALUES (%s, %s, %s, %s, %s)"
                params = (topik_arsip, id_arsip, tanggal_arsip, penulis_arsip, "Available")
                write_data(query, params)

                return redirect(url_for('arsip'))
            return abort(403)
        return abort(405)
    return abort(401)

@app.route('/edit_arsip/<id_arsip>', methods=['GET', 'POST'])
def edit_arsip(id_arsip):
    if 'user_id' in session:
        if request.method == 'GET':
            if session['role'] == 'Admin':
                query = "SELECT * FROM `arsip_ta` WHERE `id_arsip` = %s"
                params = (id_arsip,)
                archive = read_data(query, params, "fetchone")
                return render_template('editarsip.html', archive=archive, msg=""),201
                # return abort(406)
            return abort(403)
        
        elif request.method == 'POST':
            if session['role'] == 'Admin':
                editted_archive_id = id_arsip
                topik_arsip = request.form['topik_arsip']
                archive_id= request.form.get('id_arsip')
                penulis_arsip = request.form['penulis_arsip']
                tanggal_arsip = request.form['tanggal_arsip']
                query = "SELECT * FROM `arsip_ta` WHERE `id_arsip` = %s"
                params = (id_arsip,)
                editted_archive = read_data(query, params, "fetchall")
                for archive in editted_archive:
                    if archive['topik_arsip'] != topik_arsip:
                        query = "UPDATE `arsip_ta` SET `topik_arsip` = %s WHERE `id_arsip` = %s"
                        params = (topik_arsip, editted_archive_id)
                        write_data(query, params)
                                        
                    if archive['id_arsip'] != archive_id:
                        query = "SELECT `id_arsip` FROM `arsip_ta` WHERE `id_arsip` = %s"
                        params = (archive_id,)
                        existing_archive = read_data(query, params, "fetchone")

                        if not existing_archive == []:
                            query = "UPDATE `arsip_ta` SET `id_arsip` = %s WHERE `id_arsip` = %s"
                            params = (archive_id, editted_archive_id)
                            write_data(query, params)

                        elif not archive_id in existing_archive:
                            query = "UPDATE `arsip_ta` SET `id_arsip` = %s WHERE `id_arsip` = %s"
                            params = (archive_id, editted_archive_id)
                            write_data(query, params)
                    
                    if archive['penulis_arsip'] != penulis_arsip:
                        query = "UPDATE `arsip_ta` SET `penulis_arsip` = %s WHERE `id_arsip` = %s"
                        params = (penulis_arsip, editted_archive_id)
                        write_data(query, params)

                    if archive['tanggal_arsip'] != tanggal_arsip:
                        query = "UPDATE `arsip_ta` SET `tanggal_arsip` = %s WHERE `id_arsip` = %s"
                        params = (tanggal_arsip, editted_archive_id)
                        write_data(query, params)

                return redirect(url_for('arsip'))
            return abort(403)
        return abort(405)
    return abort(401)

@app.route('/delete_arsip/<id_arsip>', methods=['GET'])
def delete_arsip(id_arsip):
    if 'user_id' in session:
        if session['role'] == 'Admin':
            query = "SELECT * FROM `arsip_ta` WHERE `id_arsip` = %s"
            params = (id_arsip,)
            to_be_deleted_archive = read_data(query, params, "fetchone")
            
            if to_be_deleted_archive:
                query = "DELETE FROM `arsip_ta` WHERE `id_arsip` = %s"
                write_data(query, params)
    
                return redirect(url_for('arsip'))
            return abort(406)
        return abort(403)          
    return abort(401)

# @app.route('/base', methods=['GET'])
# def base():
#     return render_template('base.html')

# # Error Handling Section
# @app.errorhandler(400)
# def bad_request(error):
#     error = "400 - Bad Request"
#     return render_template('errorPage.html', error=error), 400

# @app.errorhandler(401)
# def unauthorized(error):
#     error = "401 - Unauthorized Access"
#     return render_template('errorPage.html', error=error), 401

# @app.errorhandler(403)
# def forbidden(error):
#     error = "403 - Forbidden Access"
#     return render_template('errorPage.html', error=error), 403

# @app.errorhandler(404)
# def page_not_found(error):
#     error = "404 - Page Not Found"
#     return render_template('errorPage.html', error=error), 404

# @app.errorhandler(405)
# def method_not_allowed(error):
#     error = "405 - Method Not Allowed"
#     return render_template('errorPage.html', error=error), 405

# @app.errorhandler(406)
# def not_acceptable(error):
#     error = "406 - Not Acceptable"
#     return render_template('errorPage.html', error=error), 406

# @app.errorhandler(408)
# def request_timeout(error):
#     error = "408 - Request Timeout"
#     return render_template('errorPage.html', error=error), 408

# @app.errorhandler(409)
# def conflict(error):
#     error = "409 - Conflict"
#     return render_template('errorPage.html', error=error), 409

# @app.errorhandler(500)
# def internal_error(error):
#     error = "500 - Internal Server Error"
#     return render_template('errorPage.html', error=error), 500

# @app.errorhandler(501)
# def not_implemented(error):
#     error = "501 - Not Implemented"
#     return render_template('errorPage.html', error=error), 501

# @app.errorhandler(502)
# def bad_gateway(error):
#     error = "502 - Bad Gateway"
#     return render_template('errorPage.html', error=error), 502

# @app.errorhandler(503)
# def service_unavailable(error):
#     error = "503 - Service Unavailable"
#     return render_template('errorPage.html', error=error), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)