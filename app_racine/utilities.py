from flask import url_for


class PaginationMixin(object):
    @staticmethod
    def to_collection_dict(query, columns, page, per_page,
                           edit_endpoint, delete_endpoint, list_endpoint,
                           view_endpoint=None,
                           **kwargs):
        resources = query.paginate(page=page, per_page=per_page, error_out=False)
        items = [item.to_dict() for item in resources.items]

        data = {
            'count': resources.total,
            'pages': resources,
            'columns': columns,
            'items': items,
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(list_endpoint, page=page,
                                **kwargs),
                'next': url_for(list_endpoint, page=page + 1,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(list_endpoint, page=page - 1,
                                **kwargs) if resources.has_prev else None,
                'last': url_for(list_endpoint, page=resources.pages, **kwargs),
                'first': url_for(list_endpoint, page=1, **kwargs)
            },
            '_manage': {
                'edit': edit_endpoint,
                'delete': delete_endpoint,
                'view': view_endpoint
            }
        }
        return data
