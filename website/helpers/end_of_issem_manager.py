from website.models.user import User
from website.models.role import Role
from website.models.meal_order import Meal_order

def end_of_issem():
    ucty = User.get_all()
    ucastnici = [u for u in ucty if len(u.roles) == 0]
    lektori = [u for u in ucty if Role.get_by_system_name("tutor") in u.roles]

    for u in ucastnici:
        u: User
        u.primary_class = None
        u.secondary_classes = []
        u.is_this_year_participant = False
        u.datetime_calculation_email = None
        u.datetime_class_pick = None
        u.datetime_registered = None
        u.billing_date_paid = None
        u.admin_comment = None
        u.billing_correction = 0
        u.billing_correction_reason = None
        u.billing_food_correction = 0
        u.billing_food_correction_reason = None
        u.billing_accomodation_correction = 0
        u.billing_accomodation_correction_reason = None        
        u.update()

    for l in lektori:
        l: User
        l.tutor_arrival = None
        l.tutor_departure = None
        l.update()
        
    for u in ucty:
        u: User
        u.meal_orders = []
        u.update()
        
    for m in Meal_order.get_all():
        m: Meal_order
        m.delete()
        
        