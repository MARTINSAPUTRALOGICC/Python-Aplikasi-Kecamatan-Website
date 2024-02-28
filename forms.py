from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, validators
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Email, InputRequired


class insertupdate_user(FlaskForm):
    email = StringField("email")
    password = PasswordField("password")
    status = IntegerField("status")
    full_name = StringField("full_name")
    foto_profile = StringField("foto_profile")
    submit = SubmitField("submit_register")


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit_login = SubmitField("submit_login")


class UploadFileForm(FlaskForm):
    foto_fisio = FileField("foto_fisio", validators=[InputRequired()])
    full_name = StringField("full_name")  # Change 'username' to 'fullname'
    status = StringField("status")  # Change 'username' to 'fullname'


class UpdatePasswordForm(FlaskForm):
    current_password = StringField("current_password")
    new_password = StringField("new_password")
    confirm_password = StringField("confirm_password")
    email = StringField("email")


class Updatesub_bagian(FlaskForm):
    bagian = StringField("bagian")


class InsertUpdatebagian(FlaskForm):
    nama_bagian = StringField("nama_bagian")


class InsertUpdateNotification(FlaskForm):
    pesan = StringField("pesan", validators=[DataRequired()])
    bagian = StringField("bagian", validators=[DataRequired()])


class InsertBelanjasub_bagian(FlaskForm):
    nama_barang = StringField("nama_barang")
    jumlah = StringField("jumlah")
    harga_satuan = StringField("total_harga")


class UpdateBelanjasub_bagian(FlaskForm):
    status = StringField("status")


class InsertBarang(FlaskForm):
    nama_barang = StringField("nama_barang")
    jumlah_barang = IntegerField("jumlah_barang")


class InsertPengajuan(FlaskForm):
    nama_barang = StringField("nama_barang")
    jumlah_barang = IntegerField("jumlah_barang")
    status = StringField("status")
    nama_pengaju = StringField("nama_pengaju")
    bagian = StringField("bagian")
    
    

