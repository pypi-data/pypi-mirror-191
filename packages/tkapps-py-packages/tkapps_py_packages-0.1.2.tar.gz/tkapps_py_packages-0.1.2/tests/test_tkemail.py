from tests.setup import test_setup
from src.tkemail import Tkemail
# from src.tkaws import Tks3, Tkses, Tklambda, Tkdynamodb


def test_email_message():
    email_message = Tkemail()
    email_message.add_sender("gurugyaan@gmail.com")
    email_message.add_recipient(['granjan@tekion.com'])
    email_message.add_email_in_cc(['nkumar@tekion.com'])
    email_message.add_subject("Test 2: Email for common Repository Demo")
    # email_message.add_body("Hello")
    email_message.add_html_body("<p>Hello Gyaan</p>")
    email_message.add_attachment(["/Users/gyanranjan/Desktop/python.zip"])
    # email_message.add_attachment_from_s3("/gyaan.pdf", "test_bucket")
    email_response = email_message.send()
    # response = Tkses("us-west-1").send_email(email_message)
    return email_response



test_setup()
test_email_message()
