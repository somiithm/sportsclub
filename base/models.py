from functools import wraps

from django.db import models
import reversion


def create_revision_if_registered(fn):
    @wraps(fn)
    def wrapper(obj, *args, **kwargs):
        if reversion.is_registered(type(obj)):
            with reversion.create_revision():
                return fn(obj, *args, **kwargs)
        return fn(obj, *args, **kwargs)

    return wrapper


def base_reversion_register(*args, **kwargs):
    """
    Exclude created_at, updated_at for any model that decorates
     itself with this method.
    """
    exclude = list(set(kwargs.pop('exclude', ()) + ('created_at', 'updated_at')))
    kwargs['exclude'] = exclude
    return reversion.register(*args, **kwargs)


class BaseModel(models.Model):
    """
    All models (in other apps) should subclass BaseModel.
    This is just a convenient place to add common functionality and fields
    between models.

    FSM_FIELDS (if used) must be defined on models that inherit from BaseModel.
    This takes care of excluding those fields when calling .save on the model.
    """

    FSM_FIELDS = ()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @create_revision_if_registered
    def save(self, *args, **kwargs):
        """Calls full_clean (excluding FSM_FIELDS)"""
        validated_unique = kwargs.get('validate_unique')
        self.full_clean(exclude=self.FSM_FIELDS, validate_unique=validated_unique)
        return super().save(*args, **kwargs)


    class Meta:
        abstract = True
