import sqlalchemy as pgsql
import pandas as pd
import os, re
from transform import transformations, sg_formatting
from hidden import URL
from sqlalchemy.exc import IntegrityError

PATH = '/Users/andrejacobs/Desktop/pga-tour-database/data/'
URL_CONN = URL


def players(data: pd.DataFrame) -> None:
    db = pgsql.create_engine(URL)

    query = "select name from players"
    player_in = [i[0] for i in db.execute(query).fetchall()]

    df = data.query(f'name not in {player_in}')
    df['name'].to_sql('players', db, if_exists='append', index=False)

    print(f'{df["name"].size} rows inserted')


def rounds(rd_num: int) -> None:
    db = pgsql.create_engine(URL)
    tid = db.execute('select max(tournament_id) from tournaments').fetchone()[0]
    insert = f'insert into rounds (tournament_id, round) values ({tid}, {rd_num})'

    try:
        db.execute(insert)
        print('Successful insert')
    except IntegrityError:
        print('Insert failed')


def strokes_gained(data: pd.DataFrame) -> None:
    db = pgsql.create_engine(URL)

    try:
        data.to_sql('strokesgained', db, index=False, if_exists='append')
        print(f'successfully inserted {data.shape[0]} rows')
    except IntegrityError:
        print('Insert failed')


def main() -> None:
    for i in os.listdir(PATH):
        data = pd.read_csv(PATH + i)

        r = re.compile('r\d+')
        round_ = list(filter(r.match, data.columns))[0][1:]

        if len(round_) > 3:
            round_ = 5
            
        df = transformations(data)
        rounds(int(round_))
        players(df)

        df = sg_formatting(df)
        strokes_gained(df)
        

if __name__ =="__main__":
   main() 