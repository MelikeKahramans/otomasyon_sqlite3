import sqlite3
import smtplib
from email.mime.text import MIMEText

# Veritabanı dosyası
db_file = 'database.db'

# E-posta ayarları
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_username = 'your_username'
smtp_password = 'your_password'
from_address = 'your_email@example.com'
to_address = 'recipient@example.com'

def send_email(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_address, [to_address], msg.as_string())
        server.quit()
        print("E-posta gönderildi.")
    except Exception as e:
        print(f"E-posta gönderme hatası: {e}")

def watch_database():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM your_table")  # İzlenen tabloya göre sorguyu güncelleyin
    initial_count = cursor.fetchone()[0]

    try:
        while True:
            cursor.execute("SELECT COUNT(*) FROM your_table")  # İzlenen tabloya göre sorguyu güncelleyin
            current_count = cursor.fetchone()[0]

            if current_count > initial_count:
                diff = current_count - initial_count
                subject = f"Yeni kayıt eklendi: {diff} adet"
                message = f"Veritabanında {diff} yeni kayıt eklendi."
                send_email(subject, message)
                initial_count = current_count

    except KeyboardInterrupt:
        pass

    connection.close()

if __name__ == "__main__":
    watch_database()