try:
    from pymongo import MongoClient
    from pymongo.collection import Collection
    from pymongo.errors import BulkWriteError
except ImportError:
    raise ImportError('PyMongo is not installed in your machine.')

from datetime import datetime, timedelta, date as Date
import os, click

class TwitterDate:
    TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    def __init__(self, time: str, format: str = None):
        if isinstance(time, Date):
            self.date = time
        else:
            self.date = datetime.strptime(time, format)
    def __str__(self):
        return self.date.strftime(self.TIME_FORMAT)
    def __repr__(self): return str(self)
    def __sub__(self, other):
        return self.date - other.date
    def add(self, days):
        return TwitterDate(self.date + timedelta(days=days))


class MongoDB(object):
    """
    Available collection action
    ===========================
    find_one, find, count, remove, update, aggregate
    
    Information to keep track of 
    ============================
    depress_tweet
    -------------
        _id : 1494474914518429697 
        text : "Aku takde la diagnosed with depression tapi pernah lalui kaunseling an..." 
        time : 2022-02-18T00:52:40.000+00:00 
        usr : 856050224 
        reply_to : 1349154596866834434 
        usr_data : Object 
            description : "1/4 of BBB Crew. Pembaca fiksyen. ada curious cat rupanya https://t.co..." 
            created_at : "2012-10-01T08:34:55.000Z" 
            username : "amal_is_reading" 
            name : "ms. amalina" 
            id : "856050224" 
            public_metrics : Object 
                followers_count : 1511 
                following_count : 273 
                tweet_count : 58253 
                listed_count : 11
        loc_data : null
    
    depress_user
    ------------
        _id : 1494352344053686278
        text : "U S auto safety regulators have launched another investigation of Tesl..."
        time : 2022-02-17T16:45:37.000+00:00
        usr : 16261627
    """
    @property
    def list_database_names(self): return self.client.list_database_names()
    @property
    def list_collection_names(self): return self._db.list_collection_names()

    def __init__(self, usr='usr', pwd='pwd', host='localhost', port=27017, db_name=None, drop_n_create=False):
        try:
            self.client = MongoClient(host=host, port=port, username=usr, password=pwd, maxPoolSize=200)
        except Exception as error:
            raise Exception(error)
        if drop_n_create: self.drop_db(db_name)
        self.use(db_name)
        self._tbl = None

    def use(self, db_name):
        self._db = self.client[db_name]

    def check_db(self, db=None):
        db_name = self._db.name if not db else db
        if not db_name in self.list_database_names:
            raise ValueError('Database is empty/not created.')

    def check_tbl(self, tbl=None):
        tbl_name = self._tbl.name if not tbl else self._db[tbl].name
        if not tbl_name in self.list_collection_names:
            raise ValueError('Collection is empty/not created.')

    def get_overall_details(self):
        client = self.client
        details = {
            (db, [tbl for tbl in client[db].collection_names()]) 
            for db in client.database_names()
        }
        return details

    def create_db(self, db_name=None):
        self._database = self.client[db_name]
        print("database %s is created"%self.client.database_names())

    def create_tbl(self, tbl_name=None):
        self.check_db()
        self._tbl = self._db[tbl_name]
        print("collection %s is created"%self._db.collection_names(include_system_collections=False))

    def drop_db(self, db_name: str):
        self._db, self._tbl = None, None
        return self.client.drop_database(db_name)
    
    def drop_tbl(self, tbl_name):
        self._db[tbl_name].drop(); self._tbl = None

    def insert_many(self, tbl_name, records):
        try:
            result = self._db[tbl_name].insert_many(records, ordered=False)
            return result.inserted_ids
        except BulkWriteError:
            print("Warning: duplicate insersion, will continue")
            pass
    
    def select(self, tbl_name=None, limit=0, filter={}, project={}):
        cur: Collection = self._tbl if not tbl_name else self._db[tbl_name]
        if cur is None:
            raise('you have to specify {tbl_name} argument !')
        return cur.find(filter, project, limit=limit)
