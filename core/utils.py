from django.contrib.auth.models import User

class Verification:
    """Работа с профилем перед сохранением"""
    def __init__(self, profile, field_name):
        self.profile = profile
        self.field_name = field_name

    def verification(self, new):
        profile_save = False
        error = 0
        if self.field_name == 'username' and new and new != self.profile.user.username:
            result = self.name_verification(new)
            if result != new:
                error = result
            self.profile.user.username = new
            profile_save = True

        elif self.field_name == 'gender' and new is not None:
            self.profile.gender = new
            profile_save = True

        elif self.field_name == 'birth_date' and new:
            result = self.day_verification(int(new[:4]))
            if not str(result).isdigit():
                error = result
            self.profile.birth_date = new
            profile_save = True

        elif self.field_name == 'description' and new is not None:
            self.profile.description = new
            profile_save = True

        return profile_save, error, self.profile

    def name_verification(self, new_username):
        """Валидация юзернейма"""
        if len(new_username) < 3 or len(new_username) > 15:
            return 'username_incorrect'
        if User.objects.filter(username=new_username).exists():
            return 'username_exists'
        return new_username

    def day_verification(self, birth_year):
        """Валидация даты рождения"""
        if birth_year > 2008:
            return 'date_error'
        return birth_year