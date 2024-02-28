from flask import Blueprint, jsonify, request, Flask
from models import db, User, Sub_Bagian, Bagian, Notification, Belanja_Camat_sub_bagian


# Create the Flask application instance
api_token = Blueprint("API_TOKEN", __name__)
api = Blueprint("API_LOGIN", __name__)
logout = Blueprint("API_LOGOUT", __name__)
registrasi = Blueprint("API_REGISTRASI", __name__)
registrasi_bagian = Blueprint("API_REGISTRASI_bagian", __name__)
notifikasi = Blueprint("API_NOTIFIKASI", __name__)
belanja = Blueprint("API_BELANJA", __name__)
daftarbelanja = Blueprint("API_DAFTAR_BELANJA", __name__)
daftarbelanjasub_bagian = Blueprint("API_DAFTAR_BELANJA_sub_bagian", __name__)

select_user_api = Blueprint("API_USER_API", __name__)
select_bagian = Blueprint("API_bagian", __name__)
select_sub_bagian = Blueprint("API_sub_bagian", __name__)
select_notifikasi = Blueprint("API_SELECT_NOTIFIKASI", __name__)
select_notifikasi_bagian = Blueprint("API_SELECT_NOTIFIKASI_bagian", __name__)


delete_user = Blueprint("API_DELETE_USER", __name__)
delete_bagian = Blueprint("API_DELETE_bagian", __name__)
delete_sub_bagian = Blueprint("API_DELETE_sub_bagian", __name__)
delete_notifikasi = Blueprint("API_DELETE_NOTIFIKASI", __name__)
delete_belanja = Blueprint("API_DELETE_BELANJA", __name__)

update_user = Blueprint("API_UPDATE_USER", __name__)
update_bagian = Blueprint("API_UPDATE_bagian", __name__)
update_sub_bagian = Blueprint("API_UPDATE_sub_bagian", __name__)
update_notifikasi = Blueprint("API_UPDATE_NOTIFIKASI", __name__)
update_belanja = Blueprint("API_UPDATE_BELANJA", __name__)
changepass = Blueprint("API_UPDATE_PASSWORD", __name__)


@api.route("/api-login", methods=["POST"])
def api_login():
    email = request.form.get("email")
    password_api = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user is not None:
        if user.status == 1:
            if user and user.password == password_api:
                response = {
                    "message": "Login Sukses",
                    "status": "success",
                    "username": user.full_name,
                    "user_status": user.status,
                    "bagian": "tidak ada",
                    "user-id": user.id,
                    # Use a different key name here
                }
                return jsonify(response), 200

        elif user.status == 2:
            if user and user.password == password_api:
                response = {
                    "message": "Login Sukses",
                    "status": "success",
                    "username": user.full_name,
                    "user_status": user.status,
                    "bagian": "tidak ada",
                    "user-id": user.id,
                    # Use a different key name here
                }
                return jsonify(response), 200

        elif user.status == 3:
            if user and user.password == password_api:
                bagian = Sub_Bagian.query.filter_by(nama_sub_bagian=user.full_name).first()
                response = {
                    "message": "Login Sukses",
                    "status": "success",
                    "username": user.full_name,
                    "user_status": user.status,
                    "bagian": bagian.bagian,
                    "user-id": user.id,
                    # Use a different key name here
                }
                return jsonify(response), 200

    # Handle the case where user.status is not 1, 2, or 3
    response = {"message": "Login failed. Invalid password.", "status": "error"}
    return jsonify(response), 401  # tambahkan pernyataan return di sini


@logout.route("/api-logout", methods=["POST"])
def api_logout():
    response = {
        "message": "Berhasil Logout..",
        "status": "success",
    }
    return jsonify(response), 200


@registrasi.route("/api-registrasi", methods=["POST"])
def api_registrasi():
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    password = request.form.get("password")
    status = request.form.get("status")

    # Validate required fields
    if not full_name or not email or not password or not status:
        response = {
            "message": "Full name, password, email, and status masih kosong.",
            "status": "Failed",
        }
        return jsonify(response), 400

    # Check if the email is already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        response = {"message": "Email sudah terdaftar.", "status": "Failed"}
        return jsonify(response), 202

    new_user = User(full_name=full_name, email=email, password=password, status=status)

    db.session.add(new_user)
    db.session.commit()

    response = {"message": "Berhasil Registrasi", "status": "success"}
    return jsonify(response), 200


@registrasi_bagian.route("/api-registrasi-bagian", methods=["POST"])
def api_registrasi_bagian():
    nama_bagian = request.form.get("nama_bagian")

    # Validate required fields
    if not nama_bagian:
        response = {
            "message": "Nama bagian masih kosong.",
            "status": "Failed",
        }
        return jsonify(response), 400

    # Check if the email is already registered
    existing_user = Bagian.query.filter_by(nama_bagian=nama_bagian).first()
    if existing_user:
        response = {"message": "Nama bagian sudah terdaftar.", "status": "Failed"}
        return jsonify(response), 202

    new_bagian = Bagian(nama_bagian=nama_bagian)

    db.session.add(new_bagian)
    db.session.commit()

    response = {"message": "Berhasil Mendaftar bagian", "status": "success"}
    return jsonify(response), 200


@notifikasi.route("/api-notifikasi", methods=["POST"])
def api_notifikasi():
    nama_bagian = request.form.get("nama_bagian")
    pesan = request.form.get("pesan")

    namabagian = Bagian.query.filter_by(id_bagian=nama_bagian).first()

    if not nama_bagian or not pesan:
        response = {
            "message": "Nama bagian masih kosong atau Pesan masih kosong",
            "status": "Failed",
        }
        return jsonify(response), 400

    new_notifikasi = Notification(pesan=pesan, bagian=namabagian.nama_bagian)

    db.session.add(new_notifikasi)
    db.session.commit()

    response = {"message": "Berhasil membuat Notifikasi", "status": "success"}
    return jsonify(response), 200


@belanja.route("/api-belanja", methods=["POST"])
def api_belanja():
    nama_barang = request.form.get("nama_barang")
    jumlah = int(request.form.get("jumlah"))
    harga_satuan = int(request.form.get("harga_satuan"))
    bagian = request.form.get("bagian")
    total_harga = jumlah * harga_satuan
    status = "Pengajuan"

    if not nama_barang or not jumlah or not harga_satuan or not bagian:
        response = {
            "message": "Nama Barang, Jumlah,Harga_satuan,bagian masih kosong.",
            "status": "Failed",
        }
        return jsonify(response), 400

    new_belanja = Belanja_Camat_sub_bagian(
        nama_barang=nama_barang,
        jumlah=jumlah,
        harga_satuan=harga_satuan,
        total_harga=total_harga,
        status=status,
        bagian=bagian,
    )

    db.session.add(new_belanja)
    db.session.commit()

    response = {"message": "Berhasil Pengajuan Belanja", "status": "success"}
    return jsonify(response), 200


# bagian select api
@daftarbelanja.route("/api-daftar-belanja", methods=["GET"])
def get_all_belanja():
    belanja_entries = Belanja_Camat_sub_bagian.query.all()

    if not belanja_entries:
        response = {"message": "Belanja entries not found.", "status": "error"}
        return jsonify(response), 404

    belanja_list = []
    for entry in belanja_entries:
        belanja_data = {
            "id_belanja": entry.id_belanja,
            "nama_barang": entry.nama_barang,
            "jumlah": entry.jumlah,
            "harga_satuan": entry.harga_satuan,
            "total_harga": entry.total_harga,
            "status": entry.status,
            "bagian": entry.bagian,
            "tanggal_pengajuan": entry.tanggal_pengajuan.strftime(
                "%Y-%m-%d"
            ),  # Format the date
        }
        belanja_list.append(belanja_data)

    response = {"message": "Success", "status": "success", "data": belanja_list}
    return jsonify(response), 200


@daftarbelanjasub_bagian.route("/api-daftar-belanja-sub_bagian", methods=["GET"])
def get_all_belanja_sub_bagian():
    nama_bagian = request.args.get("nama_bagian")

    belanja_entries = Belanja_Camat_sub_bagian.query.filter_by(bagian=nama_bagian).all()
    if not belanja_entries:
        response = {"message": "Belanja entries not found.", "status": "error"}
        return jsonify(response), 404

    belanja_list = []
    for entry in belanja_entries:
        belanja_data = {
            "id_belanja": entry.id_belanja,
            "nama_barang": entry.nama_barang,
            "jumlah": entry.jumlah,
            "harga_satuan": entry.harga_satuan,
            "total_harga": entry.total_harga,
            "status": entry.status,
            "tanggal_pengajuan": entry.tanggal_pengajuan.strftime(
                "%Y-%m-%d"
            ),  # Format the date
        }
        belanja_list.append(belanja_data)

    response = {"message": "Success", "status": "success", "data": belanja_list}
    return jsonify(response), 200


@select_user_api.route("/api-list-user", methods=["GET"])
def get_all_user():
    user = User.query.all()
    if not user:
        response = {"message": "Users entries not found.", "status": "error"}
        return jsonify(response), 404

    user_list = []
    for entry in user:
        user_data = {
            "id": entry.id,
            "email": entry.email,
            "password": entry.password,
            "status": entry.status,
        }
        user_list.append(user_data)

    response = {"message": "Success", "status": "success", "data": user_list}
    return jsonify(response), 200


@select_bagian.route("/api-bagian", methods=["GET"])
def get_all_bagian():
    bagian = bagian.query.all()
    if not bagian:
        response = {"message": "bagian entries not found.", "status": "error"}
        return jsonify(response), 404

    bagian_list = []
    for entry in bagian:
        bagian_data = {
            "id_bagian": entry.id_bagian,
            "nama_bagian": entry.nama_bagian,
        }
        bagian_list.append(bagian_data)

    response = {"message": "Success", "status": "success", "data": bagian_list}
    return jsonify(response), 200


@select_sub_bagian.route("/api-sub_bagian", methods=["GET"])
def get_all_sub_bagian():
    sub_bagian = sub_bagian.query.all()
    if not sub_bagian:
        response = {"message": "Kepala bagian entries not found.", "status": "error"}
        return jsonify(response), 404

    sub_bagian_list = []
    for entry in sub_bagian:
        sub_bagian_data = {
            "id_kepala": entry.id_kepala,
            "nama_sub_bagian": entry.nama_sub_bagian,
            "bagian": entry.bagian,
        }
        sub_bagian_list.append(sub_bagian_data)

    response = {"message": "Success", "status": "success", "data": sub_bagian_list}
    return jsonify(response), 200


@select_notifikasi.route("/api-notifikasi", methods=["GET"])
def get_all_notifikasi():
    notifikasi = Notification.query.all()
    if not notifikasi:
        response = {"message": "Notifikasi entries not found.", "status": "error"}
        return jsonify(response), 404

    notifikasi_list = []
    for entry in notifikasi:
        notifikasi_data = {
            "id_notifikasi": entry.id_notifikasi,
            "pesan": entry.pesan,
            "bagian": entry.bagian,
            "tanggal_notif": entry.tanggal_notif,
        }
        notifikasi_list.append(notifikasi_data)

    response = {"message": "Success", "status": "success", "data": notifikasi_list}
    return jsonify(response), 200


@select_notifikasi_bagian.route("/api-notifikasi-bagian", methods=["GET"])
def get_all_notifikasi_bagian():
    bagian = request.args.get("bagian")
    notifikasi = Notification.query.filter_by(bagian=bagian).all()
    jumlah = Notification.query.filter_by(bagian=bagian).count()
    if not notifikasi:
        response = {"message": "Notifikasi entries not found.", "status": "error"}
        return jsonify(response), 404

    notifikasi_list = []
    for entry in notifikasi:
        notifikasi_data = {
            "id_notifikasi": entry.id_notifikasi,
            "pesan": entry.pesan,
            "bagian": entry.bagian,
            "tanggal_notif": entry.tanggal_notif,
        }
        notifikasi_list.append(notifikasi_data)

    response = {
        "message": "Success",
        "status": "success",
        "data": notifikasi_list,
        "jumlah_pesan": jumlah,
    }
    return jsonify(response), 200


# bagian delete api
@delete_user.route("/api-delete-user", methods=["POST"])
def delete_user_api():
    user_id = request.form.get("id")
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    response = {
        "message": "user berhasil di delete ",
        "status": "success",
    }
    return jsonify(response), 200


@delete_bagian.route("/api-delete-bagian", methods=["POST"])
def delete_bagian_api():
    id_bagian = request.form.get("id_bagian")
    bagian = bagian.query.get(id_bagian)
    if bagian:
        db.session.delete(bagian)
        db.session.commit()
    response = {
        "message": "bagian berhasil di delete ",
        "status": "success",
    }
    return jsonify(response), 200


@delete_notifikasi.route("/api-delete-notifikasi", methods=["POST"])
def delete_notifikasi_api():
    id_notifikasi = request.form.get("id_notifikasi")
    notifikasi = Notification.query.get(id_notifikasi)

    if notifikasi:
        db.session.delete(notifikasi)
        db.session.commit()
    response = {
        "message": "notifikasi berhasil  di delete ",
        "status": "success",
    }
    return jsonify(response), 200


@delete_belanja.route("/api-delete-belanja", methods=["POST"])
def delete_belanja_api():
    belanja_id = request.form.get("id_belanja")
    belanja = Belanja_Camat_sub_bagian.query.get(belanja_id)

    if belanja:
        db.session.delete(belanja)
        db.session.commit()
    response = {
        "message": "daftar belanja berhasil  di delete ",
        "status": "success",
    }
    return jsonify(response), 200


# bagian update api
@update_user.route("/api-update-user", methods=["POST"])
def update_user_api():
    id = request.form.get("id")
    email_update = request.form.get("email")
    password_update = request.form.get("password")
    status_update = request.form.get("status")

    if id and email_update and password_update and status_update:
        # Find the user by ID
        user = User.query.get(int(id))

        # Update user information
        if user:
            user.email = email_update
            user.password = password_update
            user.status = status_update

            # Commit the changes to the database
            db.session.commit()

        response = {
            "message": "Berhasil Mengupdate Data User ",
            "status": "success",
        }
        return jsonify(response), 200
    if not id or not email_update or not password_update or not status_update:
        response = {
            "message": "Data Masih Kosong... ",
            "status": "Failed",
        }
    return jsonify(response), 202


@changepass.route("/api-changepass", methods=["POST"])
def changepassword():
    id = request.form.get("id")
    konfirmasi_baru = request.form.get("password_konfirmasi")

    if id and konfirmasi_baru:
        # Find the user by ID
        user = User.query.get(int(id))

        # Update user information
        if user:
            user.password = konfirmasi_baru

            # Commit the changes to the database
            db.session.commit()

        response = {
            "message": "Berhasil Mengupdate Data User ",
            "status": "success",
        }
        return jsonify(response), 200
    if not id or not konfirmasi_baru:
        response = {
            "message": "Data Masih Kosong... ",
            "status": "Failed",
        }
    return jsonify(response), 202


@update_bagian.route("/api-update-bagian", methods=["POST"])
def update_bagian_api():
    id_bagian = request.form.get("id_bagian")
    nama_bagian = request.form.get("nama_bagian")

    if id_bagian and nama_bagian:
        bagian = bagian.query.get(int(id_bagian))

        if bagian:
            bagian.nama_bagian = nama_bagian

            db.session.commit()

        response = {
            "message": "Berhasil Mengupdate Data bagian ",
            "status": "success",
        }
        return jsonify(response), 200
    if not id_bagian or not nama_bagian:
        response = {
            "message": "Data Masih Kosong... ",
            "status": "Failed",
        }
    return jsonify(response), 202


@update_sub_bagian.route("/api-update-sub_bagian", methods=["POST"])
def update_sub_bagian_api():
    id_kepala = request.form.get("id_kepala")
    nama_bagian = request.form.get("nama_bagian")
    namabagian = Bagian.query.filter_by(id_bagian=nama_bagian).first()

    if id_kepala and nama_bagian:
        # Find the user by ID
        sub_bagian = sub_bagian.query.get(int(id_kepala))

        # Update user information
        if sub_bagian:
            sub_bagian.bagian = namabagian.nama_bagian

            # Commit the changes to the database
            db.session.commit()

        response = {
            "message": "Berhasil Mengupdate Data Kepala bagian ",
            "status": "success",
        }
        return jsonify(response), 200
    if not id_kepala or not nama_bagian:
        response = {
            "message": "Data Masih Kosong... ",
            "status": "Failed",
        }
    return jsonify(response), 202


@update_notifikasi.route("/api-update-notifikasi", methods=["POST"])
def update_notifikasi_api():
    id_notifikasi = request.form.get("id_notifikasi")
    pesan = request.form.get("pesan")
    id_bagian = request.form.get("bagian")
    bagian_nama = Bagian.query.filter_by(id_bagian=id_bagian).first()

    if id_notifikasi and pesan:
        # Find the notification by ID
        notifikasi = Notification.query.get(int(id_notifikasi))

        # Update notification information
        if notifikasi:
            notifikasi.pesan = pesan
            notifikasi.bagian = bagian_nama.nama_bagian

            # Commit the changes to the database
            db.session.commit()

            response = {
                "message": "Berhasil Mengupdate Data Notifikasi",
                "status": "success",
            }
            return jsonify(response), 200
        else:
            response = {
                "message": "Notifikasi tidak ditemukan",
                "status": "Failed",
            }
            return jsonify(response), 404

    else:
        response = {
            "message": "Data masih kosong",
            "status": "Failed",
        }
        return jsonify(response), 400


@update_belanja.route("/api-update-belanja", methods=["POST"])
def update_belanja_api():
    id_belanja = request.form.get("id_belanja")
    status = request.form.get("status")

    if id_belanja and status:
        # Find the user by ID
        belanja = Belanja_Camat_sub_bagian.query.get(int(id_belanja))

        # Update user information
        if belanja:
            belanja.status = status

            # Commit the changes to the database
            db.session.commit()

        response = {
            "message": "Berhasil Mengupdate Data Belanja ",
            "status": "success",
        }
        return jsonify(response), 200
    if not id_belanja or not status:
        response = {
            "message": "Data Masih Kosong... ",
            "status": "Failed",
        }
    return jsonify(response), 202
