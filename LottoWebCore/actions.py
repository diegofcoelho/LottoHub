from django.contrib import messages
from django.contrib.auth.models import User

from LottoWebCore.methods import create_hash, sendMail
from LottoWebCore.models import MiddleMan


def create_tickets():
    return 0


# noinspection PyUnusedLocal,SpellCheckingInspection
def RequestToUser(modeladmin=None, request=None, selection=None):
    if selection:
        for entry in selection:
            if not entry.analysed:
                full_name = entry.name.split(' ')
                first_name = full_name[0]
                last_name = ' '.join(full_name[1:len(full_name)])
                pwd = create_hash()
                #
                user_obj = User(first_name=first_name,
                                last_name=last_name,
                                username=entry.username,
                                email=entry.email,
                                password=pwd)
                user_obj.save()
                #
                mm_obj = MiddleMan.objects.get(user=user_obj)
                mm_obj.phone = entry.phone
                mm_obj.picture = entry.social_media
                mm_obj.raffle = entry.raffle
                mm_obj.directory = entry.directory
                mm_obj.save()
                #
                data = {'username': entry.username,
                        'raffle': entry.raffle,
                        'name': first_name,
                        'pwd': pwd}
                #
                sendMail('USR', data)
                #
                entry.analysed = True
                entry.save()
                #
                messages.success(request, "User created sucessfully!")
            else:
                messages.error(request, "User was analysed previously!")

                # from django.contrib import messages
                # self.message_user(request, "The message", level=messages.ERROR)
                # Сan also be used(messages.ERROR, messages.WARNING, messages.DEBUG, messages.INFO, messages.SUCCESS)


RequestToUser.short_description = "Create User from Selected Request"
