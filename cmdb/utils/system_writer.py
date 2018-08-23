"""
Writer module for database based system configurations
"""


class SystemWriter:
    """

    """
    def __init__(self, writer):
        """

        Args:
            writer:
        """
        self.writer = writer

    def write(self, _id: str, data: dict) -> str:
        """

        Args:
            _id:
            data:

        Returns:

        """
        raise NotImplementedError

    def verify(self, _id: int, data: dict) -> bool:
        """

        Returns:

        """
        raise NotImplementedError


class SystemSettingsWriter(SystemWriter):
    """

    """
    COLLECTION = 'settings.conf'

    def __init__(self, database_manager):
        """

        Args:
            database_manager:
        """
        super(SystemSettingsWriter, self).__init__(database_manager)

    def write(self, _id: str, data: dict) -> str:
        """

        Args:
            _id:
            data:

        Returns:

        """
        from cmdb.data_storage.database_manager import NoDocumentFound
        try:
            writing_document = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': _id})
        except NoDocumentFound:
            raise NoEntryFoundError(_id)
        writing_document.update(data)
        ack = self.writer.update(
            collection=self.COLLECTION,
            public_id=writing_document['public_id'],
            data=writing_document
        )
        return ack

    def verify(self, _id: str, data: dict) -> bool:
        """

        Args:
            _id:
            data:

        Returns:

        """
        verify_document = self.writer.find_one_by(collection=self.COLLECTION, filter={'_id': _id})
        if verify_document != data:
            return False
        return True


class NoEntryFoundError(Exception):

    def __init__(self, _id):
        super().__init__()
        self.message = "Entry with the id {} was not found".format(_id)
