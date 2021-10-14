from typing import OrderedDict

import pandas as pd

from emailme import construct_email_from_template
from emailme import df_to_dct


def test_construct():
    args = OrderedDict()
    args["intro"] = "Hello There"
    args["body"] = "Here is your update"
    args["conclusion"] = "Goodbye"

    msg = construct_email_from_template(
        args, "template.html", "test@example.com"
    )
    assert msg


def test_df_to_dct():
    df = pd.read_csv("tests/odds_10_11_2021_17_33.tsv", sep="\t")

    df = df[["Matchup", "record", "draftkings"]]
    dct = df_to_dct(df)
    assert "Matchup" in dct["cols"]


if __name__ == "__main__":
    test_construct()
    test_df_to_dct()
