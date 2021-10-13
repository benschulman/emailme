from typing import OrderedDict

from emailme import construct_email_from_template


def test_construct():
    args = OrderedDict()
    args["intro"] = "Hello There"
    args["body"] = "Here is your update"
    args["conclusion"] = "Goodbye"

    msg = construct_email_from_template(
        args, "template.html", "test@example.com"
    )
    assert msg


if __name__ == "__main__":
    test_construct()
