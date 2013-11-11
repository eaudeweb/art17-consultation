import flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView as ModelView_base
from flask.ext.principal import Permission
from art17.auth import need
from art17 import models

admin = Admin(name="Art17")


class ModelView(ModelView_base):

    def __init__(self, model, **kwargs):
        super(ModelView, self).__init__(model, models.db.session)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def is_accessible(self):
        return Permission(need.admin).can()


admin.add_view(ModelView(models.DataSpeciesRegion))
admin.add_view(ModelView(models.DataHabitattypeRegion))
admin.add_view(ModelView(models.NotificationUser))
