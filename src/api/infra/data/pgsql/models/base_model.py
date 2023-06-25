import peewee

# The database ORM access.
database_proxy = peewee.DatabaseProxy()


class BaseModel(peewee.Model):
    """The PostgreSQL base model.

    Args:
        peewee (peewee.Model): The ORM database model.
    """

    class Meta:
        """Initializes the database."""

        database = database_proxy
