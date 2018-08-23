from cmdb.object_framework.cmdb_dao import CmdbDAO


class CmdbObject(CmdbDAO):
    """The CMDB object is the basic data wrapper for storing and holding the pure objects within the CMDB.
    """

    COLLECTION = 'objects.data'
    REQUIRED_INIT_KEYS = [
        'type_id',
        'tag',
        'version',
        'creation_time',
        'creator_id',
        'last_editor_id',
        'last_edit_time',
        'active',
        'views',
        'fields',
        'logs'
    ]

    def __init__(self, type_id, tag, version, creation_time, creator_id,
                 last_editor_id, last_edit_time, active, views, fields, logs, **kwargs):
        """init of object

        Args:
            type_id: public type id which implements the object
            tag: current tag of object
            version: current version of object
            creation_time: date of object creation
            creator_id: public id of creation user
            last_editor_id: public id of last author which edits the object
            last_edit_time: last date of editing
            active: object activation status
            views: numbers of views
            fields: data inside fields
            logs: object log
            **kwargs: additional data
        """
        self.type_id = type_id
        self.tag = tag
        self.version = version
        self.creation_time = creation_time
        self.creator_id = creator_id
        self.last_editor_id = last_editor_id
        self.last_edit_time = last_edit_time
        self.active = active
        self.views = views
        self.fields = fields
        self.logs = logs
        super(CmdbObject, self).__init__(**kwargs)

    def get_type_id(self) -> int:
        """get type if of this object

        Returns:
            int: public id of type

        """
        if self.type_id == 0 or self.type_id is None:
            raise TypeNotSetError(self.get_public_id())
        return self.type_id

    def update_view_counter(self) -> int:
        """update the number of times this object was viewd

        Returns:
            int: number of views

        """
        self.views += 1
        return self.views

    def get_all_fields(self) -> list:
        """ get all fields with key value pair

        Returns:
            all fields

        """

        return self.fields

    def get_value(self, field) -> str:
        """get value of an field

        Args:
            field: field_name

        Returns:
            value of field
        """
        for f in self.fields:
            if f['name'] == field:
                return f['value']
            continue
        return None

    def empty_logs(self) -> bool:
        if len(self.logs) > 0:
            return True
        return False


class TypeNotSetError(Exception):

    def __init__(self, public_id):
        super().__init__()
        self.message = 'The object (ID: {}) is not connected with a type'.format(public_id)


class NoLinksAvailableError(Exception):
    """
    @deprecated
    """
    def __init__(self, public_id):
        super().__init__()
        self.message = 'The object (ID: {}) has no links'.format(public_id)
