from sqlalchemy import Column, ForeignKey, Integer, String

from models import BaseModel


class FeelingHashtag(BaseModel):
    __tablename__ = "feeling_hashtags"

    feeling_id = Column(Integer, ForeignKey("feeling.id"), nullable=False)
    hashtag_id = Column(Integer, ForeignKey("hashtag.id"), nullable=False)

    def __init__(self, feeling_id, hashtag_id):
        self.feeling_id = feeling_id
        self.hashtag_id = hashtag_id

    def __repr__(self):
        return "<FeelingHashtag(id='{}', feeling_id='{}', hashtag_id='{}', created_at='{}', updated_at='{}')>".format(
            self.id, self.feeling_id, self.hashtag_id, self.created_at, self.updated_at
        )
