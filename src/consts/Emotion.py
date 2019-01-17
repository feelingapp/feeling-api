from enum import Enum


class Emotion(Enum):
    AMAZING = 1
    GREAT = 2
    UNSURE = 3
    ANGRY = 4
    UPSET = 5

    @staticmethod
    def getId(name):
        """Get an emotion's ID given a name"""

        try:
            return Emotion[name.upper()].value
        except:
            return None

    @staticmethod
    def list():
        """Returns a list of all the emotions"""

        return [emotion.name for emotion in list(Emotion)]
