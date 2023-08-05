from typing import Any, Dict

from pydantic import BaseModel

KeyValues = Dict[str, Any]


class RootBaseModel(BaseModel):
    def dict(self, **kwargs):
        output = super().dict(**kwargs)
        return output["__root__"]

    # def __getattr__(self, *args):
    #     """Override getattr to expose __root__ automatically."""
    #     return self.__root__.__getattribute__(*args)
    #
    # def __len__(self):
    #     return self.__root__.__len__()
