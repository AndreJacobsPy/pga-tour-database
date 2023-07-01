import sqlalchemy as pgsql
import pandas as pd
import os, re
from transform import transformations, sg_formatting, add_id_fields
from hidden import URL
from sqlalchemy.exc import IntegrityError

PATH = '/Users/andrejacobs/Desktop/pga-tour-database/data/'
URL_CONN = URL


def players(data: pd.DataFrame) -> None:
    db = pgsql.create_engine(URL)

    with db.connect() as db:

        query = pgsql.text("select name from players")
        player_in = [i[0] for i in list(db.execute(query))]

        df = data.query(f'name not in {player_in}')
        df['name'].to_sql('players', db, if_exists='append', index=False)

        print(f'{df["name"].size} rows inserted')

        db.commit()


def rounds(rd_num: int) -> None:
    db = pgsql.create_engine(URL)
    with db.connect() as db:
        query = pgsql.text('select max(tournament_id) from tournaments')
        tid = list(db.execute(query))[0][0]

        insert = pgsql.text(f'insert into rounds (tournament_id, round) values ({tid}, {rd_num})')

        try:
            db.execute(insert)
            print('Successful insert')
        except IntegrityError:
            print('Insert failed')

        db.commit()


def strokes_gained(data: pd.DataFrame) -> None:
    with pgsql.create_engine(URL).connect() as db:

        try:
            data.to_sql('strokesgained', db, index=False, if_exists='append')
            db.commit()
            
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

        df = add_id_fields(df)
        df = sg_formatting(df)
        strokes_gained(df)
        

if __name__ =="__main__":
   main() 