import uuid
from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str
    membership: bool

    class Config:
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "username": "johndoe",
                "membership": True
            }
        }



class Team(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    captain: Optional[User]
    members: list[User]

    class Config:
        schema_extra = {
            "example" : {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Team A",
                "captain": {
                    "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                    "username": "johndoe",
                    "membership": True
                },
                "members": [
                    {
                        "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                        "username": "johndoe",
                        "membership": True
                    }
                ]
            }
        }
