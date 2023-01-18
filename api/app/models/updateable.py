from sqlmodel import SQLModel

class UpdateableModel(SQLModel):
    def update(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
