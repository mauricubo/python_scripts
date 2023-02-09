import smtplib
import os

class Email:

    USER_EMAIL = os.getenv("USER_EMAIL") 
    USER_PASSWORD = os.getenv("USER_PASSWORD") 

    def send_email(self, dest_to: str, subject: str, message: str) -> bool:
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
		# connection to smtp server
                connection.starttls()
                connection.login(user=self.USER_EMAIL, password=self.USER_PASSWORD)
		# building message
                msg = f"Subject:{subject}\n\n {message}".encode("utf-8")
		# sending message to dest
                connection.sendmail(from_addr=self.USER_EMAIL, to_addrs=dest_to,
                                    msg=msg)
                return True
        except Exception as ex:
            print(ex)
        return False
