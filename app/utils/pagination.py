from sqlalchemy.orm import Query

def paginate_query(query: Query, page: int, page_size: int):
    return query.offset((page - 1) * page_size).limit(page_size)
