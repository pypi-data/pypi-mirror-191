import bson
import pymongo

from singer import metadata
from macrometa_source_mongo.sync_strategies import common

from macrometa_source_mongo.errors import MongoInvalidDateTimeException, SyncException

def fetch_table(client, conn_info, stream):
    database = client[conn_info['dbname']]
    collection = database[stream["table_name"]]
    data = []
    rec = {}
    cursor = collection.find({}, sort=[("_id", pymongo.ASCENDING)]).limit(10)

    for row in cursor:
        try:
            rec = {k: common.transform_value(v, [k]) for k, v in row.items()
                              if not isinstance(v, (bson.min_key.MinKey, bson.max_key.MaxKey))}
        except MongoInvalidDateTimeException as ex:
            raise SyncException(
                f"Error syncing collection {stream['tap_stream_id']}, object ID {row['_id']} - {ex}") from ex

        rec = {
            '_id': str(rec['_id']),
            'document': rec
        }
        data.append(rec)

    schema = {"_id": "string", "document": "object"}
    return schema, data


def fetch_samples(client, conn_config, stream):
    """
    Fetch samples for the stream.
    """
    md_map = metadata.to_map(stream['metadata'])
    conn_config['dbname'] = md_map.get(()).get('database-name')
    # Add support for views if needed here
    state = fetch_table(client, conn_config, stream)
    return state
