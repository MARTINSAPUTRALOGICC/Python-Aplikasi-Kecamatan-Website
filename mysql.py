from flask import (
    Blueprint,
    request,
    Flask,
    redirect,
    url_for,
    flash,
    request,
    current_app,
    session,
)
from forms import (
    insertupdate_user,
    UploadFileForm,
    InsertUpdatebagian,
    Updatesub_bagian,
    UpdateBelanjasub_bagian,
    InsertUpdateNotification,
    InsertBelanjasub_bagian,
    InsertBarang,
    InsertPengajuan,
)
from datetime import datetime

from models import (
    db,
    User,
    Bagian,
    Sub_Bagian,
    Belanja_Camat_sub_bagian,
    Notification,
    Barang,
    Pengajuan_barang,
)
from flask_wtf.csrf import CSRFError
from werkzeug.utils import secure_filename
import os
from PIL import Image

insert_auth = Blueprint("insert_data", __name__)
update_auth = Blueprint("update_data", __name__)
delete_auth = Blueprint("delete_data", __name__)

insert_auth_bagian = Blueprint("insert_data_bagian", __name__)
update_auth_bagian = Blueprint("update_data_bagian", __name__)
delete_auth_bagian = Blueprint("delete_data_bagian", __name__)

update_auth_sub_bagian = Blueprint("update_data_sub_bagian", __name__)


delete_auth_camat = Blueprint("delete_data_camat", __name__)
update_auth_camat = Blueprint("update_data_camat", __name__)


insert_auth_notif = Blueprint("insert_data_notif", __name__)
update_auth_notif = Blueprint("update_data_notif", __name__)
delete_auth_notif = Blueprint("delete_data_notif", __name__)

insert_auth_sub_bagian_belanja = Blueprint("insert_data_belanja", __name__)
upload_fisio_auth = Blueprint("upload_fisio_auth", __name__)
updatepassword_auth = Blueprint("updatepassword_auth", __name__)


insert_auth_barang = Blueprint("insert_data_barang", __name__)
update_auth_barang = Blueprint("update_data_barang", __name__)
delete_auth_barang = Blueprint("delete_data_barang", __name__)


insert_auth_pengajuan = Blueprint("insert_data_pengajuan", __name__)
update_auth_pangajuan = Blueprint("update_data_pengajuan", __name__)
delete_auth_pengajuan = Blueprint("delete_data_pengajuan", __name__)

UPLOAD_FOLDER = "Data_Foto/Foto_User"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@insert_auth.route("/insert", methods=["POST"])
def insert():
    form = insertupdate_user()

    if form.validate_on_submit():
        # Use form data as needed in your logic
        email = form.email.data
        password = form.password.data
        full_name = form.full_name.data
        status = form.status.data

        # Create a new user with the required fields
        user = User(email=email, password=password, full_name=full_name, status=status)

        # Add the user to the session and commit the transaction
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("dashboard"))


@delete_auth.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    user_to_delete = User.query.get(id)

    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("dashboard"))


@update_auth.route("/update/<id>", methods=["GET", "POST"], endpoint="update")
def update(id):
    user = None

    if id.isdigit():
        # If the identifier is a digit, assume it's an ID
        user = User.query.get(int(id))
    else:
        # If it's not a digit, assume it's a username
        user = User.query.filter_by(full_name=id).first()

    if user is None:
        return redirect(url_for("dashboard"))

    form = insertupdate_user(obj=user)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.full_name.data:
                user.full_name = form.full_name.data
            if form.password.data:
                user.password = form.password.data
            if form.status.data:
                user.status = form.status.data
            if form.email.data:
                user.email = form.email.data

    if id.isdigit():
        db.session.commit()
        return redirect(url_for("dashboard"))

    else:
        db.session.commit()
        return redirect(url_for("profile"))


@insert_auth_bagian.route("/insert_bagian", methods=["POST"])
def insert_bagian():
    form = InsertUpdatebagian()

    if form.validate_on_submit():
        # Use form data as needed in your logic
        nama_bagian = form.nama_bagian.data

        # Create a new user with the required fields
        bagian = Bagian(nama_bagian=nama_bagian)

        # Add the user to the session and commit the transaction
        db.session.add(bagian)
        db.session.commit()

        return redirect(url_for("bagian"))


@delete_auth_bagian.route("/delete_bagian/<int:id>", methods=["GET"])
def delete_bagian(id):
    bagian_to_delete = Bagian.query.get(id)

    if bagian_to_delete:
        db.session.delete(bagian_to_delete)
        db.session.commit()
        return redirect(url_for("bagian"))
    else:
        return redirect(url_for("bagian"))


@update_auth_bagian.route(
    "/update_bagian/<id_bagian>", methods=["GET", "POST"], endpoint="update_bagian"
)
def update_bagian(id_bagian):
    selected_bagian = None

    if id_bagian.isdigit():
        # If the identifier is a digit, assume it's an ID
        selected_bagian = Bagian.query.get(int(id_bagian))
    else:
        # If it's not a digit, assume it's a username
        selected_bagian = Bagian.query.filter_by(full_name=id_bagian).first()

    if selected_bagian is None:
        return redirect(url_for("bagian"))

    form = InsertUpdatebagian(obj=selected_bagian)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.nama_bagian.data:
                selected_bagian.nama_bagian = form.nama_bagian.data

    if id_bagian.isdigit():  # Check id_bagian, not id
        db.session.commit()
        return redirect(url_for("bagian"))
    else:
        db.session.commit()
        return redirect(url_for("profile"))


@update_auth_sub_bagian.route(
    "/update_sub_bagian/<id_sub>", methods=["GET", "POST"], endpoint="update_sub_bagian"
)
def update_sub_bagian(id_sub):
    selected_sub_bagian = None

    if id_sub.isdigit():
        # If the identifier is a digit, assume it's an ID
        selected_sub_bagian = Sub_Bagian.query.get(int(id_sub))
    else:
        # If it's not a digit, assume it's a username
        selected_sub_bagian = Sub_Bagian.query.filter_by(full_name=id_sub).first()

    if selected_sub_bagian is None:
        return redirect(url_for("menu_sub_bagian"))

    form = Updatesub_bagian(obj=selected_sub_bagian)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.bagian.data:
                selected_sub_bagian.bagian = form.bagian.data

    if id_sub.isdigit():  # Check id_bagian, not id
        db.session.commit()
        return redirect(url_for("menu_sub_bagian"))
    else:
        db.session.commit()
        return redirect(url_for("profile"))


@insert_auth_sub_bagian_belanja.route("/insert_belanja", methods=["POST"])
def insert_belanja():
    full_name = session["full_name"]
    form = InsertBelanjasub_bagian()

    if form.validate_on_submit():
        # Use form data as needed in your logic
        nama_barang = form.nama_barang.data
        jumlah = int(form.jumlah.data)  # Convert to integer
        harga_satuan = int(form.harga_satuan.data)  # Convert to integer
        total_harga = jumlah * harga_satuan
        status = "Pengajuan"
        bagian = Sub_Bagian.query.filter_by(nama_sub=full_name).first()

        # Create a new user with the required fields
        bagian = Belanja_Camat_sub_bagian(
            nama_barang=nama_barang,
            jumlah=jumlah,
            harga_satuan=harga_satuan,
            total_harga=total_harga,
            status=status,
            bagian=bagian.bagian,
        )

        # Add the user to the session and commit the transaction
        db.session.add(bagian)
        db.session.commit()

        return redirect(url_for("sub_bagian"))


@delete_auth_camat.route("/delete_camat/<int:id_belanja>", methods=["GET"])
def delete_camat(id_belanja):
    camat_to_delete = Belanja_Camat_sub_bagian.query.get(id_belanja)

    if camat_to_delete:
        db.session.delete(camat_to_delete)
        db.session.commit()
        return redirect(url_for("camat"))
    else:
        return redirect(url_for("camat"))


@update_auth_camat.route(
    "/update_camat/<id_belanja>", methods=["GET", "POST"], endpoint="update_camat"
)
def update_camat(id_belanja):
    selected_camat = None

    if id_belanja.isdigit():
        # If the identifier is a digit, assume it's an ID
        selected_camat = Belanja_Camat_sub_bagian.query.get(int(id_belanja))
    else:
        # If it's not a digit, assume it's a username
        selected_camat = Belanja_Camat_sub_bagian.query.filter_by(
            full_name=id_belanja
        ).first()

    if selected_camat is None:
        return redirect(url_for("camat"))

    form = UpdateBelanjasub_bagian(obj=selected_camat)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.status.data:
                selected_camat.status = form.status.data

    if id_belanja.isdigit():  # Check id_bagian, not id
        db.session.commit()
        return redirect(url_for("camat"))
    else:
        db.session.commit()
        return redirect(url_for("profile"))


@insert_auth_notif.route("/insert_notif", methods=["POST"])
def insert_notif():
    form = InsertUpdateNotification()

    if form.validate_on_submit():
        # Use form data as needed in your logic
        pesan = form.pesan.data
        bagian = form.bagian.data
        current_time = datetime.now()

        # Create a new user with the required fields
        notifikasi_data = Notification(
            pesan=pesan, bagian=bagian, tanggal_notif=current_time
        )
        # Add the user to the session and commit the transaction
        db.session.add(notifikasi_data)
        db.session.commit()

        return redirect(url_for("menu_notifikasi"))


@delete_auth_notif.route("/delete_notif/<int:id_notifikasi>", methods=["GET"])
def delete_notif(id_notifikasi):
    Notification_to_delete = Notification.query.get(id_notifikasi)

    if Notification_to_delete:
        db.session.delete(Notification_to_delete)
        db.session.commit()
        return redirect(url_for("menu_notifikasi"))
    else:
        return redirect(url_for("menu_notifikasi"))


@update_auth_notif.route(
    "/update_notif/<id_notifikasi>", methods=["GET", "POST"], endpoint="update_notif"
)
def update_notif(id_notifikasi):
    selected_pesan = None

    if id_notifikasi.isdigit():
        # If the identifier is a digit, assume it's an ID
        selected_pesan = Notification.query.get(int(id_notifikasi))
    else:
        # If it's not a digit, assume it's a username
        selected_pesan = Notification.query.filter_by(full_name=id_notifikasi).first()

    if selected_pesan is None:
        return redirect(url_for("menu_notifikasi"))

    form = InsertUpdateNotification(obj=selected_pesan)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.pesan.data:
                selected_pesan.pesan = form.pesan.data
                selected_pesan.bagian = form.bagian.data

    if id_notifikasi.isdigit():  # Check id_bagian, not id
        db.session.commit()
        return redirect(url_for("menu_notifikasi"))
    else:
        db.session.commit()
        return redirect(url_for("profile"))


@upload_fisio_auth.route("/upload_fisio/<id>", methods=["GET", "POST"])
def upload_fisio(id):
    form = UploadFileForm()

    if form.validate_on_submit():
        try:
            file = form.foto_fisio.data
            username = form.full_name.data
            status = form.status.data

            if file and allowed_file(file.filename):
                upload_folder = os.path.join(
                    os.path.abspath(os.path.dirname(__file__)),
                    "static",
                    UPLOAD_FOLDER,
                    status,
                    username,
                )
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                # Change this to your desired new filename and extension
                new_filename = username + ".png"

                # Replace spaces with underscores in the filename
                new_filename = new_filename.replace(" ", "_")

                file_path = os.path.join(upload_folder, secure_filename(new_filename))
                file.save(file_path)

                if new_filename.lower().endswith(
                    ".jpg"
                ) or new_filename.lower().endswith(".jpeg"):
                    image = Image.open(file_path)
                    image.save(file_path, "PNG")

                if id.isdigit():
                    FotoUpload = os.path.join(
                        UPLOAD_FOLDER, status, username, new_filename
                    )
                    user = User.query.get(int(id))
                    user.Foto_Profile = FotoUpload  # Use capital "F" for Foto_Profile
                else:
                    FotoUpload = os.path.join(
                        UPLOAD_FOLDER, status, username, new_filename
                    )
                    user = User.query.filter_by(full_name=id).first()
                    user.Foto_Profile = FotoUpload  # Use capital "F" for Foto_Profile

                    if id.isdigit():
                        db.session.commit()
                        return redirect(url_for("profile"))
                    else:
                        db.session.commit()
                        return redirect(url_for("profile"))

        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            print(f"An error occurred while processing the file: {str(e)}")

    return redirect(url_for("profile"))


@updatepassword_auth.route("/change_password/<string:id>", methods=["POST"])
def change_password(id):
    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    # Retrieve the user from the database (you should adapt this based on your authentication method)
    user = User.query.filter_by(email=id).first()

    if user:
        # Check if the current password matches the one stored in the database
        if user.password == current_password:
            if new_password == confirm_password:
                # Update the password in the database
                user.password = (
                    new_password  # Replace this line with your database update logic
                )
                db.session.commit()
                flash("Password updated successfully", "success")
                return redirect(url_for("profile"))
            else:
                flash("New password and confirmation password do not match", "danger")
                return redirect(url_for("profile"))

        else:
            flash("Incorrect current password", "danger")
            return redirect(url_for("profile"))
    else:
        flash("User not found", "danger")
        return redirect(url_for("profile"))


@insert_auth_barang.route("/pengurus_barang", methods=["POST"])
def insertbarang():
    form = InsertBarang()

    if form.validate_on_submit():
        # Use form data as needed in your logic
        nama_barangz = form.nama_barang.data
        jumlah_barangz = form.jumlah_barang.data

        # Create a new user with the required fields
        barangz = Barang(nama_barang=nama_barangz, jumlah_barang=jumlah_barangz)

        # Add the user to the session and commit the transaction
        db.session.add(barangz)
        db.session.commit()

        return redirect(url_for("pengurus_barang"))


@delete_auth_barang.route("/delete_barang/<int:id>", methods=["GET"])
def delete_barang(id):
    barang_to_delete = Barang.query.get(id)

    if barang_to_delete:
        db.session.delete(barang_to_delete)
        db.session.commit()
        return redirect(url_for("pengurus_barang"))
    else:
        return redirect(url_for("pengurus_barang"))


@update_auth_barang.route(
    "/update_barang/<id_barang>", methods=["GET", "POST"], endpoint="update_barang"
)
def update_barang(id_barang):
    selected_barang = None

    if id_barang.isdigit():
        # If the identifier is a digit, assume it's an ID
        selected_barang = Barang.query.get(int(id_barang))
    else:
        # If it's not a digit, assume it's a username
        selected_barang = Barang.query.filter_by(nama_barang=id_barang).first()

    if selected_barang is None:
        return redirect(url_for("pengurus_barang"))

    form = InsertBarang(obj=selected_barang)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.nama_barang.data:
                selected_barang.nama_barang = form.nama_barang.data
            if form.jumlah_barang.data:
                selected_barang.jumlah_barang = form.jumlah_barang.data

    if id_barang.isdigit():  # Check id_bagian, not id
        db.session.commit()
        return redirect(url_for("pengurus_barang"))
    else:
        db.session.commit()
        return redirect(url_for("profile"))


@insert_auth_pengajuan.route("/insert_pengajuan", methods=["POST"])
def insert_pengajuan():
    form = InsertPengajuan()

    if form.validate_on_submit():
        # Use form data as needed in your logic
        nama_barangz = form.nama_barang.data
        jumlah_barangz = form.jumlah_barang.data

        current_time = datetime.now()
        nama_pengajuan = session["full_name"]

        Bagian_User = Sub_Bagian.query.filter_by(nama_sub=nama_pengajuan).first()

        barangz = Pengajuan_barang(
            nama_barang=nama_barangz,
            jumlah_barang=jumlah_barangz,
            status="Belum Disetujui",
            nama_pengaju=nama_pengajuan,
            tanggal_pengajuan=current_time,
            bagian=Bagian_User.bagian,
        )

        db.session.add(barangz)
        db.session.commit()

        return redirect(url_for("users"))


@delete_auth_pengajuan.route("/delete_pengajuan/<int:id_pengajuan>", methods=["GET"])
def delete_pengajuan(id_pengajuan):
    pengajuan_to_delete = Pengajuan_barang.query.get(id_pengajuan)

    if pengajuan_to_delete:
        db.session.delete(pengajuan_to_delete)
        db.session.commit()
        return redirect(url_for("users"))
    else:
        return redirect(url_for("pengajuan_barang"))


@update_auth_pangajuan.route(
    "/update_pengajuan/<id_pengajuan>",
    methods=["GET", "POST"],
    endpoint="update_pengajuan",
)
def update_pengajuan(id_pengajuan):
    selected_barang = None

    if id_pengajuan.isdigit():
        # If the identifier is a digit, assume it's an ID
        selected_barang = Pengajuan_barang.query.get(int(id_pengajuan))
    else:
        # If it's not a digit, assume it's a username
        selected_barang = Pengajuan_barang.query.filter_by(status=id_pengajuan).first()

    if selected_barang is None:
        return redirect(url_for("pengajuan_barang"))

    form = InsertPengajuan  (obj=selected_barang)

    if form.validate_on_submit():
        if request.method == "POST":
            if form.status.data:
                selected_barang.status = form.status.data

    if id_pengajuan.isdigit():  # Check id_bagian, not id
        db.session.commit()
        return redirect(url_for("pengajuan_barang"))
    else:
        db.session.commit()
        return redirect(url_for("profile"))
