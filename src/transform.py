import pandas as pd
import sqlalchemy as pgsql
from typing import List
from hidden import URL
import re


def transform_to_int(x: str):
    """
    This function is intended to transform the score column.
    It is designed to be implemented with the `apply` method.
    The function removes values with '-' and replaces them with NA
    so the column can be converted to a numeric dtype.
    """
    try:
        x = x.replace('e', '0')
        return int(x)
    except ValueError:
        return None


def transform_to_float(x: str):
    """
    This function is intended to transform the strokegained columns.
    It is designed to be implemented with the `apply` method.
    The function removes values with '-' and replaces them with NA
    so the column can be converted to a numeric dtype.
    """
    try:
        return float(x)
    except ValueError:
        return None


def transform_name(x: str) -> str:
    x = x.split()
    first = x[-1].title()
    last = x[0].title()

    return f"{first} {last}"

def get_player_id(x: str) -> int:
    db = pgsql.create_engine(URL)
    with db.connect() as db:
        query = pgsql.text(f"select player_id from players where name = '{x}'")
        pid = list(db.execute())[0][0]
        
        return pid

def get_tid() -> int:
    db = pgsql.create_engine(URL)
    with db.connect() as db:
        query = pgsql.text('select max(tournament_id) from tournaments')
        tid = list(db.execute())[0][0]
        
        return tid


def get_rid(tid: int, rd: int) -> int:
    db = pgsql.create_engine(URL)
    with db.connect() as db:
        query = pgsql.text(f"select round_id from rounds where tournament_id = '{tid} and round = '{rd}'")
        rid = list(db.execute(query))[0][0]

        return rid

def transformations(data: pd.DataFrame):
    "Function to perform all transformation in."
    df = data.copy()

    # finding what round is by looking through columns
    r = re.compile('r\d+')
    round_: str = list(filter(r.match, df.columns))[0]

    df['round'] = df[round_].apply(transform_to_int).astype(pd.Int32Dtype())
    df['total'] = df['total'].apply(transform_to_int).astype(pd.Int32Dtype())
    sg_cols: List[str] = [i for i in df.columns if 'sg' in i]

    for col in sg_cols:
        df[col] = df[col].apply(transform_to_float).astype(pd.Float32Dtype())

    df['name'] = df['player name'].apply(transform_name)

    return df


def add_id_fields(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    # finding what round is by looking through columns
    r = re.compile('r\d+')
    round_: str = list(filter(r.match, df.columns))[0]
    rd = round_[1:] if len(round_[1:]) < 4 else 5

    tid = get_tid()
    rid = get_rid(tid, rd)

    df['player_id'] = df['name'].apply(get_player_id)
    df['tournament_id'] = tid
    df['round_id'] = rid

    return df


def sg_formatting(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df.columns = [str(i).replace(' ', '_') for i in data.columns]
    cols = [
        'player_id', 'tournament_id', 'round_id', 'total', 'round', 
        'sg_putt', 'sg_arg', 'sg_app', 'sg_ott', 'sg_t2g', 'sg_total'
    ]

    return df[cols]


if __name__ == '__main__':
    df = pd.read_csv('/Users/andrejacobs/Desktop/pga-tour-database/data/fourth_round_stats.csv')
    print(df.sample(10))
    
    new_df = transformations(df)
    print(new_df.sample(10))
    print(sg_formatting(new_df))