from flask import (
    Flask,
    redirect,
    url_for,
    render_template,
    make_response,
    request,
    flash,
    session,
    jsonify,
)
import base64


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO


from constant import (
    LOGINPAGE,
    SERVER,
    USER_SERVER,
    PASSWORD_SERVER,
    DATABASE,
    column_names,
    column_barang,
    DASHBOARD_ADMIN,
    colum_names_bagian,
    DASHBOARD_bagian,
    DASHBOARD_MENU_sub_bagian,
    DASHBOARD_CAMAT,
    colum_sub_bagian,
    colum_belanja_camat,
    DASHOARD_NOTIFIKASI,
    colum_notifikasi,
    DASHBOARD_sub_bagian,
    colum_belanja_sub_bagian,
    column_pengajuan_barang,
    column_pengajuan_barang_users,
    DASHBOARD_PDF_sub_bagian,
    DASBOARD_BARANG,
    PDF_TEMPLATE,
    DASHBOARD_PDF_CAMAT,
    DASHBOARD_PENGURUS_BARANG,
    DASHBOARD_STOK_BARANG,
    DASHBOARD_USERS,
)

from forms import (
    LoginForm,
    insertupdate_user,
    UploadFileForm,
    UpdatePasswordForm,
    InsertUpdatebagian,
    Updatesub_bagian,
    UpdateBelanjasub_bagian,
    InsertUpdateNotification,
    InsertBelanjasub_bagian,
    InsertPengajuan,
)
from flask_wtf.csrf import CSRFProtect, generate_csrf

from mysql import (
    insert_auth,
    delete_auth,
    update_auth,
    upload_fisio_auth,
    updatepassword_auth,
    delete_auth_bagian,
    insert_auth_bagian,
    update_auth_bagian,
    update_auth_sub_bagian,
    delete_auth_camat,
    update_auth_camat,
    insert_auth_notif,
    update_auth_notif,
    delete_auth_notif,
    insert_auth_sub_bagian_belanja,
    insert_auth_barang,
    update_auth_barang,
    delete_auth_barang,
    update_auth_pangajuan,
    insert_auth_pengajuan,
    delete_auth_pengajuan,
)

from API import (
    api,
    api_token,
    logout,
    registrasi,
    registrasi_bagian,
    notifikasi,
    belanja,
    daftarbelanja,
    daftarbelanjasub_bagian,
    select_bagian,
    select_sub_bagian,
    select_notifikasi,
    select_user_api,
    select_notifikasi_bagian,
    delete_user,
    delete_bagian,
    delete_notifikasi,
    delete_belanja,
    update_user,
    update_bagian,
    update_sub_bagian,
    update_notifikasi,
    update_belanja,
    changepass,
)

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session as SQLAlchemySession
import os
from models import (
    db,
    User,
    Sidebar,
    Notification,
    Bagian,
    Sub_Bagian,
    Belanja_Camat_sub_bagian,
    Barang,
    Pengajuan_barang,
)
from datetime import datetime, timedelta
from xhtml2pdf import pisa
from flask_cors import CORS


app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5008"}})


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql://{USER_SERVER}:{PASSWORD_SERVER}@{SERVER}/{DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.permanent_session_lifetime = timedelta(days=30)  # Adjust the lifetime as needed
app.register_blueprint(insert_auth)
app.register_blueprint(update_auth)
app.register_blueprint(delete_auth)
app.register_blueprint(insert_auth_bagian)
app.register_blueprint(delete_auth_bagian)
app.register_blueprint(update_auth_bagian)
app.register_blueprint(update_auth_sub_bagian)
app.register_blueprint(delete_auth_camat)
app.register_blueprint(update_auth_camat)
app.register_blueprint(insert_auth_notif)
app.register_blueprint(update_auth_notif)
app.register_blueprint(delete_auth_notif)
app.register_blueprint(insert_auth_sub_bagian_belanja)
app.register_blueprint(api_token)
app.register_blueprint(api)
app.register_blueprint(logout)
app.register_blueprint(registrasi)
app.register_blueprint(registrasi_bagian)
app.register_blueprint(notifikasi)
app.register_blueprint(belanja)
app.register_blueprint(daftarbelanja)
app.register_blueprint(daftarbelanjasub_bagian)
app.register_blueprint(select_bagian)
app.register_blueprint(select_sub_bagian)
app.register_blueprint(select_notifikasi)
app.register_blueprint(select_notifikasi_bagian)
app.register_blueprint(select_user_api)
app.register_blueprint(delete_user)
app.register_blueprint(delete_bagian)
app.register_blueprint(delete_notifikasi)
app.register_blueprint(delete_belanja)
app.register_blueprint(update_user)
app.register_blueprint(update_bagian)
app.register_blueprint(update_sub_bagian)
app.register_blueprint(update_notifikasi)
app.register_blueprint(update_belanja)
app.register_blueprint(changepass)
app.register_blueprint(insert_auth_barang)
app.register_blueprint(update_auth_barang)
app.register_blueprint(delete_auth_barang)
app.register_blueprint(insert_auth_pengajuan)
app.register_blueprint(update_auth_pangajuan)
app.register_blueprint(delete_auth_pengajuan)

app.config["WTF_CSRF_ENABLED"] = False

app.secret_key = "many random bytes"

csrf = CSRFProtect(app)  # Inisialisasi CSRF protection
app.config["WTF_CSRF_TIME_LIMIT"] = 3600  # in seconds


@app.route("/", methods=["GET", "POST"])
def index():
    full_name = request.cookies.get("full_name")
    if full_name:
        return redirect(url_for("dashboard"))
    else:
        login_form = LoginForm()

    if request.method == "POST":
        if "submit_login" in request.form and login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter_by(email=email).first()

            if user and user.password == password:
                csrf_token = generate_csrf()
                session["full_name"] = user.full_name
                session["csrf_token"] = csrf_token
                session["status"] = user.status

                resp = make_response(redirect(url_for("dashboard")))
                expiration_date = datetime.now() + timedelta(days=30)
                resp.set_cookie("full_name", user.full_name, expires=expiration_date)
                resp.set_cookie("status", str(user.status), expires=expiration_date)
                return resp
            else:
                message = "Password atau Email Salah!!"
                flash(message, "error")  # Flash the error message
                return redirect(url_for("index"))

    html_content = render_template(LOGINPAGE, login_form=login_form)

    response = make_response(html_content)

    # Set the Cache-Control header to prevent caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, no-store"

    return response


@app.route("/pdf_camat", methods=["GET", "POST"])
def pdf_camat():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string
        data_bagian = Bagian.query.all()
        bagian_options = [(bagian.nama_bagian) for bagian in data_bagian]

        if status == "2":
            form = UpdateBelanjasub_bagian()
            camat = Pengajuan_barang.query.all()

            full_name = session["full_name"]
            csrf_token = session["csrf_token"]

            # Query the database to retrieve the user's data
            user_data = User.query.filter_by(full_name=full_name).first()

            modified_data_camat = []

            for data_camat in camat:
                modified_user = [
                    data_camat.id_pengajuan,
                    data_camat.nama_barang,
                    data_camat.jumlah_barang,
                    data_camat.status,
                    data_camat.tanggal_pengajuan,
                    data_camat.nama_pengaju,
                    data_camat.bagian,
                ]
                modified_data_camat.append(modified_user)

            sidebar_items = []  # Define it at the beginning
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

            data_list = [
                {
                    "input_type": "select",
                    "name": "bagian",
                    "options": bagian_options,
                }
            ]

            # Assuming you have a 'DASHBOARD' template defined
            html_content = render_template(
                DASHBOARD_PDF_CAMAT,  # Replace with your template name
                camat=modified_data_camat,
                colum_belanja_camat=colum_belanja_camat,  # You need to define 'column_names'
                sidebar_items=sidebar_items,
                data_list1=data_list,
                form=form,
                user=user_data,
                csrf_token=csrf_token,
            )

            response = make_response(html_content)

            # Set the Cache-Control header to prevent caching
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate, no-store"

            return response
        else:
            return redirect(url_for("logout"))  # Redirect to the logout p

    return


@app.route("/generate_pdf_camat", methods=["GET"])
def generate_pdf_camat():
    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    image_file_ttd = open("static/images/ttd.jpg", "rb")

    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string
        total_belanja = 0
        if status == "2":
            with open("static/images/logo.png", "rb") as image_file:
                startdate = request.args.get("startDate")
                enddate = request.args.get("endDate")
                bagian = request.args.get("Bagian")

                image_data = base64.b64encode(image_file.read()).decode("utf-8")
                image_ttd = base64.b64encode(image_file_ttd.read()).decode("utf-8")

                sub_bagian = Pengajuan_barang.query.filter(
                    Pengajuan_barang.bagian == bagian,
                    Pengajuan_barang.status == "Di Setujui",
                    Pengajuan_barang.tanggal_pengajuan.between(startdate, enddate),
                ).all()

            modified_data_sub_bagian = []

            for data_sub_bagian in sub_bagian:
                modified_user = [
                    data_sub_bagian.id_pengajuan,
                    data_sub_bagian.nama_barang,
                    data_sub_bagian.jumlah_barang,
                    data_sub_bagian.status,
                    data_sub_bagian.tanggal_pengajuan,
                    data_sub_bagian.nama_pengaju,
                    data_sub_bagian.bagian,
                ]
                modified_data_sub_bagian.append(modified_user)

                total_belanja += data_sub_bagian.jumlah_barang

            rendered_html = render_template(
                PDF_TEMPLATE,
                data_bagian=bagian,
                startdate=startdate,
                enddate=enddate,
                sub_bagian=modified_data_sub_bagian,
                total_belanja=total_belanja,
                image_data=image_data,
                image_ttd=image_ttd,
            )

            # Create a buffer to store the PDF
            buffer = BytesIO()

            # Convert HTML to PDF
            pisa.CreatePDF(rendered_html, dest=buffer)

            # Move the buffer's cursor to the beginning
            buffer.seek(0)

            # Create a Flask response with the PDF
            # Create a Flask response with the PDF
            response = make_response(buffer.getvalue())
            response.headers["Content-Type"] = "application/pdf"
            response.headers[
                "Content-Disposition"
            ] = f"inline; filename=Laporan_Anggaran_{bagian}_{startdate}_{enddate}.pdf"

            return response

    else:
        return redirect(url_for("logout"))  # Redirect to the logout p

    return


@app.route("/profile", methods=["GET", "POST"])
def profile():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    # Get the currently logged-in user's username from the session

    form = insertupdate_user()
    form1 = UploadFileForm()
    form2 = UpdatePasswordForm()
    full_name = session["full_name"]
    csrf_token = session["csrf_token"]
    # Query the database to retrieve the user's data
    user = User.query.filter_by(full_name=full_name).first()
    status = session.get("status")

    data_hitung = 1  # Set the count_user value as needed

    sidebar_items = []  # Define it at the beginning
    sidebar_data = Sidebar.query.filter_by(level_user=status).all()
    # Fetch all sidebar items (replace 'Sidebar' with your actual model name)

    # Modify the sidebar data as needed
    for item in sidebar_data:
        sidebar_item = {
            "name": item.name_side,
            "icon": item.icon_side,
            "url": item.url_side,
        }
        sidebar_items.append(sidebar_item)

    html_content = render_template(
        "profile.html",
        sidebar_items=sidebar_items,
        data_hitung=data_hitung,
        user=user,
        form=form,
        form1=form1,
        form2=form2,
        csrf_token=csrf_token,
    )

    response = make_response(html_content)

    # Set the Cache-Control header to prevent caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, no-store"

    return response


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    session.permanent = True
    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    status = session.get("status")

    if status is not None:
        status = str(status)  # Convert status to a string

        if status == "1":
            return redirect(url_for("admin"))
        elif status == "2":
            return redirect(url_for("camat"))
        elif status == "3":
            return redirect(url_for("users"))
        elif status == "4":
            return redirect(url_for("pengurus_barang"))


@app.route("/users", methods=["GET", "POST"])
def users():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string

        if status == "3":
            form = InsertPengajuan()
            barang = Barang.query.filter(Barang.jumlah_barang > 0).all()

            barang_options = [(barangz.nama_barang) for barangz in barang]

            full_name = session["full_name"]
            csrf_token = session["csrf_token"]

            # Query the database to retrieve the user's data
            user_data = User.query.filter_by(full_name=full_name).first()
            sub_bagianz = Sub_Bagian.query.filter_by(nama_sub=full_name).first()

            pengajuan = Pengajuan_barang.query.filter_by(
                bagian=sub_bagianz.bagian
            ).all()

            count_id_pengajuan = 1
            modified_pengajuan = []

            for pengajuanz in pengajuan:
                modified_user = [
                    count_id_pengajuan,
                    pengajuanz.nama_barang,
                    pengajuanz.jumlah_barang,
                    pengajuanz.status,
                    pengajuanz.tanggal_pengajuan,
                ]
                modified_pengajuan.append(modified_user)
                count_id_pengajuan += 1

            sidebar_items = []  # Define it at the beginning
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

            data_list = [
                {
                    "label": "Status",
                    "input_type": "select",
                    "name": "status",
                    "value": status,
                    "options": status,
                },
            ]

            data_list1 = [
                {
                    "label": "Nama Barang",
                    "input_type": "select",
                    "name": "nama_barang",
                    "options": barang_options,
                    "required": "1",
                },
                {
                    "label": "Jumlah Barang",
                    "input_type": "number",
                    "min": "1",
                    "name": "jumlah_barang",
                    "required": "1",
                },
            ]

            # Assuming you have a 'DASHBOARD' template defined
            html_content = render_template(
                DASHBOARD_USERS,  # Replace with your template name
                pengajuan=modified_pengajuan,
                colum_names_barang=column_pengajuan_barang_users,  # You need to define 'column_names'
                sidebar_items=sidebar_items,
                data_list=data_list,
                data_list1=data_list1,
                form=form,
                user=user_data,
                csrf_token=csrf_token,
            )

            response = make_response(html_content)

            # Set the Cache-Control header to prevent caching
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate, no-store"

            return response
        else:
            return redirect(url_for("logout"))


@app.route("/pengurus_barang", methods=["GET", "POST"])
def pengurus_barang():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string

        if status == "4":
            form = insertupdate_user()
            barangs = Barang.query.all()

            full_name = session["full_name"]
            csrf_token = session["csrf_token"]

            # Query the database to retrieve the user's data
            user_data = User.query.filter_by(full_name=full_name).first()

            modified_barang = []

            for barangz in barangs:
                modified_user = [
                    barangz.id_barang,
                    barangz.nama_barang,
                    barangz.jumlah_barang,
                ]
                modified_barang.append(modified_user)

            sidebar_items = []  # Define it at the beginning
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

            data_list = [
                {
                    "label": "Nama Barang",
                    "input_type": "text",
                    "name": "nama_barang",
                    "value": "nama_barang",
                },
                {
                    "label": "Jumlah Barang",
                    "input_type": "number",
                    "min": "1",
                    "name": "jumlah_barang",
                    "value": "jumlah_barang",
                },
            ]

            data_list1 = [
                {
                    "label": "Nama Barang",
                    "input_type": "text",
                    "name": "nama_barang",
                    "required": "1",
                },
                {
                    "label": "Jumlah Barang",
                    "input_type": "number",
                    "min": "1",
                    "name": "jumlah_barang",
                    "required": "1",
                },
            ]

            # Assuming you have a 'DASHBOARD' template defined
            html_content = render_template(
                DASBOARD_BARANG,  # Replace with your template name
                barangs=modified_barang,
                colum_names_barang=column_barang,  # You need to define 'column_names'
                sidebar_items=sidebar_items,
                data_list=data_list,
                data_list1=data_list1,
                form=form,
                user=user_data,
                csrf_token=csrf_token,
            )

            response = make_response(html_content)

            # Set the Cache-Control header to prevent caching
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate, no-store"

            return response
        else:
            return redirect(url_for("logout"))


@app.route("/stokbarang", methods=["GET", "POST"])
def stokbarang():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string

        if status == "3":
            form = insertupdate_user()
            barangs = Barang.query.all()

            full_name = session["full_name"]
            csrf_token = session["csrf_token"]

            # Query the database to retrieve the user's data
            user_data = User.query.filter_by(full_name=full_name).first()

            modified_barang = []

            for barangz in barangs:
                modified_user = [
                    barangz.id_barang,
                    barangz.nama_barang,
                    barangz.jumlah_barang,
                ]
                modified_barang.append(modified_user)

            sidebar_items = []  # Define it at the beginning
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

            data_list = [
                {
                    "label": "Nama Barang",
                    "input_type": "text",
                    "name": "nama_barang",
                    "value": "nama_barang",
                },
                {
                    "label": "Jumlah Barang",
                    "input_type": "number",
                    "min": "1",
                    "name": "jumlah_barang",
                    "value": "jumlah_barang",
                },
            ]

            data_list1 = [
                {
                    "label": "Nama Barang",
                    "input_type": "text",
                    "name": "nama_barang",
                    "required": "1",
                },
                {
                    "label": "Jumlah Barang",
                    "input_type": "number",
                    "min": "1",
                    "name": "jumlah_barang",
                    "required": "1",
                },
            ]

            # Assuming you have a 'DASHBOARD' template defined
            html_content = render_template(
                DASHBOARD_STOK_BARANG,  # Replace with your template name
                barangs=modified_barang,
                colum_names_barang=column_barang,  # You need to define 'column_names'
                sidebar_items=sidebar_items,
                data_list=data_list,
                data_list1=data_list1,
                form=form,
                user=user_data,
                csrf_token=csrf_token,
            )

            response = make_response(html_content)

            # Set the Cache-Control header to prevent caching
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate, no-store"

            return response
        else:
            return redirect(url_for("logout"))


@app.route("/pengajuan_barang", methods=["GET", "POST"])
def pengajuan_barang():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string

        if status == "4":
            form = InsertPengajuan()
            pengajuan = Pengajuan_barang.query.all()
            barang = Barang.query.filter(Barang.jumlah_barang > 0).all()

            barang_options = [(barangz.nama_barang) for barangz in barang]

            full_name = session["full_name"]
            csrf_token = session["csrf_token"]

            # Query the database to retrieve the user's data
            user_data = User.query.filter_by(full_name=full_name).first()

            modified_pengajuan = []

            for pengajuanz in pengajuan:
                modified_user = [
                    pengajuanz.id_pengajuan,
                    pengajuanz.nama_barang,
                    pengajuanz.jumlah_barang,
                    pengajuanz.status,
                    pengajuanz.tanggal_pengajuan,
                    pengajuanz.nama_pengaju,
                    pengajuanz.bagian,
                ]
                modified_pengajuan.append(modified_user)

            sidebar_items = []  # Define it at the beginning
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

            data_list = [
                {
                    "label": "Status",
                    "input_type": "select",
                    "name": "status",
                    "value": status,
                    "options": status,
                },
            ]

            data_list1 = [
                {
                    "label": "Nama Barang",
                    "input_type": "select",
                    "name": "nama_barang",
                    "options": barang_options,
                    "required": "1",
                },
                {
                    "label": "Jumlah Barang",
                    "input_type": "number",
                    "min": "1",
                    "name": "jumlah_barang",
                    "required": "1",
                },
            ]

            # Assuming you have a 'DASHBOARD' template defined
            html_content = render_template(
                DASHBOARD_PENGURUS_BARANG,  # Replace with your template name
                pengajuan=modified_pengajuan,
                colum_names_barang=column_pengajuan_barang,  # You need to define 'column_names'
                sidebar_items=sidebar_items,
                data_list=data_list,
                data_list1=data_list1,
                form=form,
                user=user_data,
                csrf_token=csrf_token,
            )

            response = make_response(html_content)

            # Set the Cache-Control header to prevent caching
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate, no-store"

            return response
        else:
            return redirect(url_for("logout"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string

        if status == "1":
            form = insertupdate_user()
            users = User.query.all()

            full_name = session["full_name"]
            csrf_token = session["csrf_token"]

            # Query the database to retrieve the user's data
            user_data = User.query.filter_by(full_name=full_name).first()

            modified_data = []

            for user in users:
                modified_user = [user.id, user.email, "*******", user.status]
                modified_data.append(modified_user)

            sidebar_items = []  # Define it at the beginning
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

            data_list = [
                {
                    "label": "Email",
                    "input_type": "email",
                    "name": "email",
                    "value": "email",
                },
                {
                    "label": "Password",
                    "input_type": "password",
                    "name": "password",
                    "value": "password",
                },
                {
                    "label": "Status",
                    "input_type": "select",
                    "name": "status",
                    "options": [
                        ("Super Admin", "1"),
                        ("Camat", "2"),
                        ("sub_bagian", "3"),
                    ],
                },
            ]

            data_list1 = [
                {
                    "label": "Email",
                    "input_type": "email",
                    "name": "email",
                    "required": "1",
                },
                {
                    "label": "Full Name",
                    "input_type": "text",
                    "name": "full_name",
                    "required": "1",
                },
                {
                    "label": "Password",
                    "input_type": "password",
                    "name": "password",
                    "required": "1",
                },
                {
                    "label": "Status",
                    "input_type": "select",
                    "name": "status",
                    "required": "1",
                    "options": [
                        ("1", "Super Admin"),
                        ("2", "Camat"),
                        ("3", "sub_bagian"),
                    ],
                },
            ]

            # Assuming you have a 'DASHBOARD' template defined
            html_content = render_template(
                DASHBOARD_ADMIN,  # Replace with your template name
                users=modified_data,
                column_names=column_names,  # You need to define 'column_names'
                sidebar_items=sidebar_items,
                data_list=data_list,
                data_list1=data_list1,
                form=form,
                user=user_data,
                csrf_token=csrf_token,
            )

            response = make_response(html_content)

            # Set the Cache-Control header to prevent caching
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate, no-store"

            return response
        else:
            return redirect(url_for("logout"))  # Redirect to the logout page


@app.route("/bagian", methods=["GET", "POST"])
def bagian():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string

        if status == "1":
            form = InsertUpdatebagian()

            bagian = Bagian.query.all()

            full_name = session["full_name"]
            csrf_token = session["csrf_token"]

            # Query the database to retrieve the user's data
            user_data = User.query.filter_by(full_name=full_name).first()

            modified_data_bagian = []

            for bagian in bagian:
                modified_bagian = [
                    bagian.id_bagian,
                    bagian.nama_bagian,
                ]  # Assuming 'password' is the third column
                modified_data_bagian.append(modified_bagian)

            sidebar_items = []  # Define it at the beginning
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

            data_list = [
                {
                    "label": "Nama Bagian",
                    "input_type": "text",
                    "name": "nama_bagian",
                    "value": "nama_bagian",
                },
            ]

            data_list1 = [
                {
                    "label": "Nama Bagian",
                    "input_type": "text",
                    "name": "nama_bagian",
                    "required": "1",
                },
            ]

            # Assuming you have a 'DASHBOARD' template defined
            html_content = render_template(
                DASHBOARD_bagian,  # Replace with your template name
                bagian=modified_data_bagian,
                colum_names_bagian=colum_names_bagian,  # You need to define 'column_names'
                sidebar_items=sidebar_items,
                data_list=data_list,
                data_list1=data_list1,
                form=form,
                user=user_data,
                csrf_token=csrf_token,
            )

            response = make_response(html_content)

            # Set the Cache-Control header to prevent caching
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate, no-store"

            return response
        else:
            return redirect(url_for("logout"))


@app.route("/menu_sub_bagian", methods=["GET", "POST"])
def menu_sub_bagian():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string

        if status == "1":
            form = Updatesub_bagian()
            sub_bagianz = Sub_Bagian.query.all()
            data_bagian = Bagian.query.all()

            full_name = session["full_name"]
            csrf_token = session["csrf_token"]

            # Query the database to retrieve the user's data
            user_data = User.query.filter_by(full_name=full_name).first()

            modified_data_sub_bagian = []

            for sub_bagian_bagian in sub_bagianz:
                modified_sub_bagian = [
                    sub_bagian_bagian.id_sub,
                    sub_bagian_bagian.nama_sub,
                    sub_bagian_bagian.bagian,
                ]  # Assuming 'password' is the third column
                modified_data_sub_bagian.append(modified_sub_bagian)

            sidebar_items = []  # Define it at the beginning
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

            bagian_options = [(bagian.nama_bagian) for bagian in data_bagian]

            # Add the 'bagian' field options to the 'data_list' dictionary
            data_list = [
                {
                    "label": "Nama bagian",
                    "input_type": "select",
                    "name": "bagian",
                    "options": bagian_options,
                }
            ]

            # Assuming you have a 'DASHBOARD' template defined
            html_content = render_template(
                DASHBOARD_MENU_sub_bagian,  # Replace with your template name
                sub_bagianz=modified_data_sub_bagian,
                colum_sub_bagian=colum_sub_bagian,  # You need to define 'column_names'
                sidebar_items=sidebar_items,
                data_list=data_list,
                form=form,
                user=user_data,
                csrf_token=csrf_token,
            )

            response = make_response(html_content)

            # Set the Cache-Control header to prevent caching
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate, no-store"

            return response
        else:
            return redirect(url_for("logout"))


@app.route("/sub_bagian", methods=["GET", "POST"])
def sub_bagian():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in
    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string

        if status == "3":
            form = InsertBelanjasub_bagian()

            full_name = session["full_name"]
            csrf_token = session["csrf_token"]
            bagian = sub_bagian.query.filter_by(nama_sub=full_name).first()
            sub_bagian = Belanja_Camat_sub_bagian.query.filter_by(
                bagian=bagian.bagian
            ).all()
            # Query the database to retrieve the user's data
            user_data = User.query.filter_by(full_name=full_name).first()
            count_result = Notification.query.filter_by(bagian=bagian.bagian).count()
            notifikasi_nilai = Notification.query.filter_by(bagian=bagian.bagian).all()

            modified_data_notifikasi = []

            for notifikasi_data in notifikasi_nilai:
                modified_user = [
                    notifikasi_data.id_notifikasi,
                    notifikasi_data.pesan,
                    notifikasi_data.bagian,
                    notifikasi_data.tanggal_notif,
                ]
                modified_data_notifikasi.append(modified_user)

            modified_data_sub_bagian = []

            for data_sub_bagian in sub_bagian:
                modified_user = [
                    data_sub_bagian.id_belanja,
                    data_sub_bagian.nama_barang,
                    data_sub_bagian.jumlah,
                    data_sub_bagian.harga_satuan,
                    data_sub_bagian.total_harga,
                    data_sub_bagian.status,
                    data_sub_bagian.tanggal_pengajuan,
                ]
                modified_data_sub_bagian.append(modified_user)

            sidebar_items = []  # Define it at the beginning
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

            data_list1 = [
                {
                    "label": "Nama Barang",
                    "input_type": "text",
                    "name": "nama_barang",
                    "placeholder": "conntoh : nama_barang",
                },
                {
                    "label": "Harga Satuan",
                    "input_type": "text",
                    "name": "harga_satuan",
                    "placeholder": "conntoh : 10000",
                },
                {
                    "label": "Jumlah",
                    "input_type": "text",
                    "name": "jumlah",
                    "placeholder": "conntoh : 10",
                },
            ]

            # Assuming you have a 'DASHBOARD' template defined
            html_content = render_template(
                DASHBOARD_sub_bagian,  # Replace with your template name
                sub_bagian=modified_data_sub_bagian,
                colum_belanja_sub_bagian=colum_belanja_sub_bagian,  # You need to define 'column_names'
                sidebar_items=sidebar_items,
                data_hitung=count_result,
                notifikasi_nilai=modified_data_notifikasi,
                data_list1=data_list1,
                form=form,
                user=user_data,
                csrf_token=csrf_token,
            )

            response = make_response(html_content)

            # Set the Cache-Control header to prevent caching
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate, no-store"

            return response
        else:
            return redirect(url_for("logout"))  # Redirect to the logout p

    return


@app.route("/menu_notifikasi", methods=["GET", "POST"])
def menu_notifikasi():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string
        notifikasi_data = None

        if status == "2":
            form = InsertUpdateNotification()
            notifikasi_nilai = Notification.query.all()
            data_bagian = Bagian.query.all()
            bagian_options = [(bagian.nama_bagian) for bagian in data_bagian]

            # Add the 'bagian' field options to the 'data_list' dictionary

            full_name = session["full_name"]
            csrf_token = session["csrf_token"]

            # Query the database to retrieve the user's data
            user_data = User.query.filter_by(full_name=full_name).first()

            modified_data_notifikasi = []

            for notifikasi_data in notifikasi_nilai:
                modified_user = [
                    notifikasi_data.id_notifikasi,
                    notifikasi_data.pesan,
                    notifikasi_data.bagian,
                    notifikasi_data.tanggal_notif,
                ]
                modified_data_notifikasi.append(modified_user)

            sidebar_items = []  # Define it at the beginning
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

            data_list = [
                {
                    "label": "Pesan",
                    "input_type": "textArea",
                    "name": "pesan",
                    "value": notifikasi_data.pesan if notifikasi_data else "",
                },
                {
                    "label": "Nama bagian",
                    "input_type": "select",
                    "name": "bagian",
                    "options": bagian_options,
                },
            ]

            data_list1 = [
                {
                    "label": "Pesan",
                    "input_type": "textArea",
                    "name": "pesan",
                    "value": notifikasi_data.pesan if notifikasi_data else "",
                },
                {
                    "label": "Nama bagian",
                    "input_type": "select",
                    "name": "bagian",
                    "options": bagian_options,
                },
            ]

            # Assuming you have a 'DASHBOARD' template defined
            html_content = render_template(
                DASHOARD_NOTIFIKASI,  # Replace with your template name
                notifikasi_nilai=modified_data_notifikasi,
                colum_notifikasi=colum_notifikasi,  # You need to define 'column_names'
                sidebar_items=sidebar_items,
                data_list=data_list,
                data_list1=data_list1,
                bagian_options=bagian_options,
                form=form,
                user=user_data,
                csrf_token=csrf_token,
            )

            response = make_response(html_content)

            # Set the Cache-Control header to prevent caching
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate, no-store"

            return response
        else:
            return redirect(url_for("logout"))


@app.route("/camat", methods=["GET", "POST"])
def camat():
    session.permanent = True

    if "full_name" not in session:
        return redirect(
            url_for("logout")
        )  # Redirect to the login page if not logged in

    status = session.get("status")
    if status is not None:
        status = str(status)  # Convert status to a string

        if status == "2":
            form = InsertPengajuan()
            barang = Barang.query.filter(Barang.jumlah_barang > 0).all()

            barang_options = [(barangz.nama_barang) for barangz in barang]

            full_name = session["full_name"]
            csrf_token = session["csrf_token"]

            # Query the database to retrieve the user's data
            user_data = User.query.filter_by(full_name=full_name).first()

            pengajuan = Pengajuan_barang.query.all()

            count_id_pengajuan = 1
            modified_pengajuan = []

            for pengajuanz in pengajuan:
                modified_user = [
                    pengajuanz.id_pengajuan,
                    pengajuanz.nama_barang,
                    pengajuanz.jumlah_barang,
                    pengajuanz.status,
                    pengajuanz.tanggal_pengajuan,
                    pengajuanz.nama_pengaju,
                    pengajuanz.bagian,
                ]
                modified_pengajuan.append(modified_user)
                count_id_pengajuan += 1

            sidebar_items = []  # Define it at the beginning
            sidebar_data = Sidebar.query.filter_by(level_user=status).all()

            # Modify the sidebar data as needed
            for item in sidebar_data:
                sidebar_item = {
                    "name": item.name_side,
                    "icon": item.icon_side,
                    "url": item.url_side,
                }
                sidebar_items.append(sidebar_item)

            data_list = [
                {
                    "label": "Status",
                    "input_type": "select",
                    "name": "status",
                    "value": status,
                    "options": status,
                },
            ]

            data_list1 = [
                {
                    "label": "Nama Barang",
                    "input_type": "select",
                    "name": "nama_barang",
                    "options": barang_options,
                    "required": "1",
                },
                {
                    "label": "Jumlah Barang",
                    "input_type": "number",
                    "min": "1",
                    "name": "jumlah_barang",
                    "required": "1",
                },
            ]

            # Assuming you have a 'DASHBOARD' template defined
            html_content = render_template(
                DASHBOARD_CAMAT,  # Replace with your template name
                pengajuan=modified_pengajuan,
                colum_names_barang=column_pengajuan_barang,  # You need to define 'column_names'
                sidebar_items=sidebar_items,
                data_list=data_list,
                data_list1=data_list1,
                form=form,
                user=user_data,
                csrf_token=csrf_token,
            )

            response = make_response(html_content)

            # Set the Cache-Control header to prevent caching
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate, no-store"

            return response
        else:
            return redirect(url_for("logout"))


@app.route("/logout")
def logout():
    session.pop("full_name", None)

    resp = make_response(redirect(url_for("index")))
    resp.delete_cookie("full_name")
    return resp


if __name__ == "__main__":
    app.register_blueprint(upload_fisio_auth, url_prefix="/upload_fisio_auth")
    app.register_blueprint(updatepassword_auth, url_prefix="/updatepassword_auth")
    app.run(debug=True, port=5008)
