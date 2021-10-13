import datetime
import os
from re import template
from typing import OrderedDict
from jinja2 import Environment, FileSystemLoader, select_autoescape

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

SENDER = os.environ['EMAIL']
RECIEVER = os.environ['EMAIL']
PWD = os.environ['APP_PWD']

PATH_TO_TEMPS = "email_temp/templates/"

def _upack_table(dct):
    """[summary]

    Args:
        dct ([type]): 
    """

    env = Environment(
        loader=FileSystemLoader(PATH_TO_TEMPS),
        autoescape=select_autoescape(enabled_extensions=(),disabled_extensions=('html',))
    )
    table_temp = env.get_template("table.html")

    header = ''.join([f"<th>{x}</th>" for x in dct['cols']])

    # datas = []
    # for row in dct['rows']:
    #     d = []
    #     for data in datas:
    #         d.append(f"<td>{data}</td>")
    #     datas.append(d)

    body = ''.join([f"<tr>{''.join(x)}</tr>\n\t" for x in [[f"<td>{d}</td>" for d in row] for row in dct['rows']]])
    
    htm_str = table_temp.render(header=header, body=body)
    return htm_str




def construct_email_from_template(email_args, template_file, to, subject=None, table=None):
    now = datetime.datetime.now()
    env = Environment(
        loader=FileSystemLoader(PATH_TO_TEMPS),
        autoescape=select_autoescape(enabled_extensions=(),disabled_extensions=('html',))
    )

    template = env.get_template(template_file)

    if table:
        email_args['extra'] = _upack_table(table)

    htm = template.render(**email_args)
    text = ''.join([str(x) + "\n" for x in email_args.values()])

    #img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart("alternative")
    msg['Subject'] = "Hello" if not subject else subject
    msg['From'] = SENDER
    msg['To'] = to

    text = MIMEText(text, "plain")
    html = MIMEText(htm, "html")

    print(htm)
    print(text)

    msg.attach(text)
    msg.attach(html)

    #image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    #msg.attach(image)
    return msg


def send_email(to, message):
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
    args['intro'] = "Hello There"
    args['body'] = 'Here is your update'
    args['conclusion'] = "Goodbye"

    msg = construct_email_from_template(args, "template.html", RECIEVER)
    send_email(RECIEVER, msg)
    
if __name__ == "__main__":
    main()
