# import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import OrderedDict

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape

# from email.mime.image import MIMEImage

SENDER = os.environ["EMAIL"]
RECIEVER = os.environ["EMAIL"]
PWD = os.environ["APP_PWD"]

PATH_TO_TEMPS = "emailme/templates/"


def _upack_table(dct):
    """Private function used to unpack dictionary based tables as html

    Args:
        dct : {"cols":[headers], "rows": [rows]}
    """
    env = Environment(
        loader=FileSystemLoader(PATH_TO_TEMPS),
        autoescape=select_autoescape(
            enabled_extensions=(), disabled_extensions=("html",)
        ),
    )
    table_temp = env.get_template("table.html")

    header = "".join([f"<th>{x}</th>" for x in dct["cols"]])

    # datas = []
    # for row in dct['rows']:
    #     d = []
    #     for data in datas:
    #         d.append(f"<td>{data}</td>")
    #     datas.append(d)

    body = "".join(
        [
            f"<tr>{''.join(x)}</tr>\n\t"
            for x in [[f"<td>{d}</td>" for d in row] for row in dct["rows"]]
        ]
    )

    htm_str = table_temp.render(header=header, body=body)
    return htm_str


def construct_email_from_template(
    email_args, template_file, to, subject=None, table=None
):
    """Function used to construct an email

    Args:
        email_args ([type]): the args passed into the template
        template_file ([type]): The template file to use e.g. template.html
        to (str): email address to send email to
        subject (str, optional): Subject of the email. Defaults to None.
        table (dict, optional): A table to add. Defaults to None.

    Returns:
        MIMEMultipart: The email message passed to the send_email function
    """
    # now = datetime.datetime.now()
    env = Environment(
        loader=FileSystemLoader(PATH_TO_TEMPS),
        autoescape=select_autoescape(
            enabled_extensions=(), disabled_extensions=("html",)
        ),
    )

    template = env.get_template(template_file)

    if table:
        email_args["extra"] = _upack_table(table)

    htm = template.render(**email_args)
    text = "".join([str(x) + "\n" for x in email_args.values()])

    # img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Hello" if not subject else subject
    msg["From"] = SENDER
    msg["To"] = to

    text = MIMEText(text, "plain")
    html = MIMEText(htm, "html")

    msg.attach(text)
    msg.attach(html)

    # image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    # msg.attach(image)
    return msg


def send_email(to, message):
    """Sends a given email

    Args:
        to (str): Email address to send to
        message (MIMEMultipart): The email message
    """
    # Endpoint for the SMTP Gmail server (Don't change this!)
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    # Login with your Gmail account using SMTP
    smtp_server.login(SENDER, PWD)
    smtp_server.sendmail(SENDER, to, message.as_string())

    # Close our endpoint
    smtp_server.close()

    return


def main():
    args = OrderedDict()
    args["intro"] = "Hello There"
    args["body"] = "Here is your update"
    args["conclusion"] = "Goodbye"

    msg = construct_email_from_template(args, "template.html", RECIEVER)
    send_email(RECIEVER, msg)


if __name__ == "__main__":
    main()
