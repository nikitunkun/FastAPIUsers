from typing import Optional

from sqlalchemy import MetaData


class Metadata:
    metadata: Optional[MetaData] = None

    @classmethod
    def get(cls) -> MetaData:
        if cls.metadata is None:
            cls.metadata = MetaData()

        return cls.metadata
