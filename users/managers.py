from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, auth_key, salt, init_vector, **extra_fields):
        if not email:
            raise ValueError(_('The \"email\" field must be set'))

        if not auth_key:
            raise ValueError(_('The \"auth_key\" field must be set'))

        if not salt:
            raise ValueError(_('The \"salt\" field must be set'))

        if not init_vector:
            raise ValueError(_('The \"init_vector\" field must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, auth_key=auth_key, salt=salt, init_vector=init_vector, **extra_fields)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, auth_key, salt, init_vector, **extra_fields):
        return self.create_user(email, auth_key, salt, init_vector, **extra_fields)
