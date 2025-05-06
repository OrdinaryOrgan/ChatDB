from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from database.db_config import MONGODB_CONFIG, MONGODB_DATABASE

class MongoDBUser:
    def __init__(self):
        self.mongo_config = MONGODB_CONFIG.copy()
        self.client = None
        self.db = None

    def __del__(self):
        if self.client is not None:
            self.client.close()

    def login(self):
        try:
            self.client = MongoClient(**MONGODB_CONFIG)
            self.db = self.client[MONGODB_DATABASE]
            self.client.admin.command('ping')  # 测试是否连通
            return "Login_Success"
        except (ConnectionFailure, OperationFailure) as e:
            print("Login failed:", e)
            return f"Login failed: {str(e)}"

    def list_collections(self):
        """
        List all collection names along with 2 sample documents from each.
        """
        if self.db is None:
            return {}
        result = {}
        for name in self.db.list_collection_names():
            collection = self.db[name]
            docs = list(collection.find().limit(1))
            result[name] = docs
        return result

    def execute_query(self, collection_name: str, method: str, args = None, **kwargs) -> dict | list:
        if method == "list_collections":
            return self.list_collections()
        if not collection_name:
            raise ValueError("collection_name is required for this operation.")
        args = args or []
        if not isinstance(args, (list, tuple)):
            raise ValueError("args must be a list or tuple.")
        collection = self.db[collection_name]
        if method == "aggregate":
            if len(args) == 1 and isinstance(args[0], list):
                pipeline = args[0]
            else:
                pipeline = list(args)
            if not isinstance(pipeline, list) or not all(isinstance(s, dict) for s in pipeline):
                raise ValueError("aggregate expects a list of pipeline stages (list of dict).")
            cursor = collection.aggregate(pipeline, **kwargs)
            return list(cursor)
        if str(method).startswith('find'):
            flt = args[0] if len(args) > 0 else {}
            proj = args[1] if len(args) > 1 else None
            if not isinstance(flt, dict):
                raise ValueError("find filter must be a dict.")
            if proj is not None and not isinstance(proj, dict):
                raise ValueError("find projection must be a dict or None.")
            cursor = collection.find(flt, proj, **kwargs)
            docs = list(cursor)
            print(f"Returned {len(docs)} documents")
            return docs
        if method == "count_documents":
            if len(args) < 1 or not isinstance(args[0], dict):
                raise ValueError("count_documents expects a filter dict as first argument.")
            flt = args[0]
            count = collection.count_documents(flt, **kwargs)
            return {"count": count}
        if method in ("insert_one", "insert_many"):
            docs = args[0] if len(args) > 0 else None
            if method == "insert_one":
                if not isinstance(docs, dict):
                    raise ValueError("insert_one expects a single document (dict).")
                result = collection.insert_one(docs, **kwargs)
                return {"inserted_id": str(result.inserted_id)}
            else:
                if not isinstance(docs, list):
                    raise ValueError("insert_many expects a list of documents.")
                result = collection.insert_many(docs, **kwargs)
                ids = [str(_id) for _id in result.inserted_ids]
                return {"inserted_ids": ids}
        if method in ("update_one", "update_many"):
            if len(args) < 2 or not all(isinstance(a, dict) for a in args[:2]):
                raise ValueError(f"{method} expects (filter: dict, update: dict).")
            flt, upd = args[0], args[1]
            res = getattr(collection, method)(flt, upd, **kwargs)
            return {"matched_count": res.matched_count, "modified_count": res.modified_count}
        if method in ("delete_one", "delete_many"):
            if len(args) < 1 or not isinstance(args[0], dict):
                raise ValueError(f"{method} expects (filter: dict).")
            flt = args[0]
            res = getattr(collection, method)(flt, **kwargs)
            return {"deleted_count": res.deleted_count}
        raise ValueError(f"Unsupported method: {method}")