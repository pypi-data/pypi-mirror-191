from setup_for_testing import setup
from tkteams import Message
from src.tkemail import Tkemail
from src.tkaws import Tks3


def test_full_message():
    message = Message("Test 32: This is message is sent to Niranjan Kumar by Gyan Ranjan for Testing teams Integration with CMS")
    # message.send()
    message.add_title("Just Testing")
    message.add_url("https://dev-cmsplatform.tekion.xyz/cms/login", "Dev CMS")
    message.add_link_button("https://dev-cmsplatform.tekion.xyz/cms/login", "Dev CMS")
    message.add_link_button("https://stage-cmsplatform.tekioncloud.xyz/cms/login", "Stage CMS")
    message.add_link_button("https://preprod-cmsplatform.tekioncloud.xyz/cms/login", "Preprod CMS")
    message.mention_user("nkumar@tekion.com", "Niranjan Kumar")
    message.mention_user("granjan@tekion.com", "Gyan Ranjan")
    message.cc_users([{"name": "Shubhum Kumar Gupta", "email": "shubhamkg@tekion.com"}])
    message.add_images(["https://mma.prnewswire.com/media/1583755/Tekion_logo.jpg?w=400"])
    message.print()
    # message.add_codeblock('{"gyaan" : "Ranjan"}')
    # Teams().send_message(message)
    return True



setup()
test_full_message()
