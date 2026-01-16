from mongoengine import Document, StringField, ListField, URLField, DateTimeField, IntField, BooleanField

class AlgorithmTheory(Document):
    meta = {'collection': 'algorithm_theory'}

    name = StringField(required=True, unique=True)               # Algorithm name (e.g., FCFS)
    category = StringField(required=True)                        # Category, e.g., CPU Scheduling
    overview = StringField(required=True)                        # Brief explanation / description
    advantages = ListField(StringField())                        # List of advantages
    disadvantages = ListField(StringField())                     # List of disadvantages
    youtube_link = URLField()                                     # Optional YouTube video link
    extra_details = StringField()                                 # Any other notes / details
    created_at = DateTimeField()                                  # Optional timestamp
    updated_at = DateTimeField()
