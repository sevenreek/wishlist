from sqlmodel import SQLModel

class Updateable(SQLModel):
    def update(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
        return self

