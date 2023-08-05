from typing import Optional, Type, Final


class KeyDescriptor:

    def __init__(
        self,
        jsonName: Optional[str] = None,
        pythonType: Optional[Type] = None,
        collectionType: Optional[Type] = None,
        isEncodable: bool = True,
        isDecodable: bool = True
    ) -> None:

        self.jsonName: Final = jsonName
        self.pythonType: Final = pythonType
        self.collectionType: Final = collectionType
        self.isEncodable: Final = isEncodable
        self.isDecodable: Final = isDecodable

    def isList(self) -> bool:
        return self.collectionType is not None and issubclass(self.collectionType, list)
