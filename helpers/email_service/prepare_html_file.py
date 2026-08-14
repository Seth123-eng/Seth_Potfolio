

import bs4


async def prepare_html_file(
        link:str|None, user_email:str, file_path:str, reason:str,
        user_name:str|None=None, msg:str|None=None
) -> str:

    """
    prepares the html file for email sending\n

    attributes:\n
    1.link ; either for password reset or account activation\n
    2. user_email\n
    3. file_path ; either for password reset or account activation\n
    """
    
    with open(file_path, "r") as file:
        html_content = file.read()

    soup = bs4.BeautifulSoup(html_content, "lxml")
    

    if reason == "submit_contact_us_form":

        user_email_div = soup.find("div", id="user-email-div")
        msg_body = soup.find("div", id="msg-body-div")

        if user_email_div and msg_body:
            user_email_div.string = user_email
            msg_body.string=msg #type:ignore

    elif reason == "send_reply_email":
            
            user_email_div = soup.find("div", id="user-email-div")
            msg_body = soup.find("div", id="msg-body-div")
    
            if user_email_div and msg_body:
                user_email_div.string = user_email
                msg_body.string=msg #type:ignore

    else:
         print("Email sending reason not defined")

    return str(soup)