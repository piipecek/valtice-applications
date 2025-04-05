from website.models.user import User

def end_of_issem():
    for u in User.get_all():
        u: User
        u.primary_class = None
        u.secondary_classes = []
        u.is_this_year_participant = False
        u.update()