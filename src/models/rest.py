from sqlalchemy import or_


class Rest:

    @classmethod
    def add_search(cls, query, request):
        search = request.args.get('search')
        if not search:
            return query
        table = cls.__table__
        search_fields = cls.get_search_fields()
        filters_list = [table.c[column].ilike(f"%{search.lower()}%") for column in search_fields]
        return query.filter(or_(*filters_list))

    @classmethod
    def add_pagination(cls, query, request):
        page = request.args.get('page')
        limit = request.args.get('limit')
        if not page or not limit:
            return query
        offset = (int(page) - 1) * int(limit)
        return query.offset(offset).limit(limit)

    @classmethod
    def get_search_fields(cls):
        return cls.search_fields