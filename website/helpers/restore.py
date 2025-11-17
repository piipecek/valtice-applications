import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from website.models.billing import Billing
from website.models.meal import Meal
from website.models.role import Role
from website.models.trida import Trida
from website.models.user import User
from website.models.meal_order import Meal_order
from website import db


def restore(xlsx_file) -> dict:
    result = {
        "success": True,
        "message": ""
    }
    
    pd_excel = pd.read_excel(xlsx_file, sheet_name=None)
    
    # check if the sheets match the table names
    expected_sheets = pd_excel.keys()
    db_keys = db.metadata.tables.keys()
    for sheet in expected_sheets:
        if sheet not in db_keys:
            result["success"] = False
            result["message"] = f"Sheet '{sheet}' neodpovídá žádné databázové tabulce."
            return result
    for table in db_keys:
        if table not in expected_sheets:
            result["success"] = False
            result["message"] = f"Databázová tabulka '{table}' nemá odpovídající sheet ve vloženém souboru."
            return result
    
    # Replace NaN with None
    for sheet_name, df in pd_excel.items():
        pd_excel[sheet_name] = df.where(pd.notnull(df), None)
        
        
    # billing
    for b in Billing.get_all():
        b.delete()
    df_billing = pd_excel['billing']
    for _, row in df_billing.iterrows():
        row_dict = row.to_dict()
        row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}

        billing = Billing()
        billing.id = row_dict['id']
        billing.type = row_dict['type']
        billing.display_name = row_dict['display_name']
        billing.system_name = row_dict['system_name']
        billing.czk = row_dict['czk']
        billing.eur = row_dict['eur']
        billing.update()
    
    
    # meal
    for m in Meal.get_all():
        m.delete()
    df_meal = pd_excel['meal']
    for _, row in df_meal.iterrows():
        row_dict = row.to_dict()
        row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
        
        meal = Meal()
        meal.id = row_dict['id']
        meal.type = row_dict['type']
        meal.location = row_dict['location']
        meal.is_vegetarian = row_dict['is_vegetarian']
        meal.update()
    pass


    # role
    for r in Role.get_all():
        r.delete()
    df_role = pd_excel['role']
    for _, row in df_role.iterrows():
        row_dict = row.to_dict()
        row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}

        role = Role()
        role.id = row_dict['id']
        role.system_name = row_dict['system_name']
        role.display_name = row_dict['display_name']
        role.update()
        
    # user - zatim bez relationships
    for u in User.get_all():
        u.delete()
    df_user = pd_excel['user']
    for _, row in df_user.iterrows():
        row_dict = row.to_dict()
        row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}

        user = User()
        user.id = row_dict['id']
        user.name = row_dict['name']
        user.surname = row_dict['surname']
        user.email = row_dict['email']
        user.phone = row_dict['phone']
        user.date_of_birth = row_dict['date_of_birth']
        user.is_student = row_dict['is_student']
        user.is_under_16 = row_dict['is_under_16']
        user.passport_number = row_dict['passport_number']
        user.datetime_created = row_dict['datetime_created']
        user.is_this_year_participant = row_dict['is_this_year_participant']
        user.is_ssh_member = row_dict['is_ssh_member']
        user.is_active_participant = row_dict['is_active_participant']
        user.is_student_of_partner_zus = row_dict['is_student_of_partner_zus']
        user.datetime_class_pick = row_dict['datetime_class_pick']
        user.datetime_registered = row_dict['datetime_registered']
        user.datetime_calculation_email = row_dict['datetime_calculation_email']
        user.accomodation_type = row_dict['accomodation_type']
        user.accomodation_count = row_dict['accomodation_count']
        user.musical_education = row_dict['musical_education']
        user.musical_instrument = row_dict['musical_instrument']
        user.repertoire = row_dict['repertoire']
        user.comment = row_dict['comment']
        user.admin_comment = row_dict['admin_comment']
        user.meals = row_dict['meals']
        user.billing_currency = row_dict['billing_currency']
        user.billing_date_paid = row_dict['billing_date_paid']
        user.billing_gift = row_dict['billing_gift']
        user.billing_correction = row_dict['billing_correction']
        user.billing_correction_reason = row_dict['billing_correction_reason']
        user.billing_food_correction = row_dict['billing_food_correction']
        user.billing_food_correction_reason = row_dict['billing_food_correction_reason']
        user.billing_accomodation_correction = row_dict['billing_accomodation_correction']
        user.billing_accomodation_correction_reason = row_dict['billing_accomodation_correction_reason']
        user.tutor_travel = row_dict['tutor_travel']
        user.tutor_license_plate = row_dict['tutor_license_plate']
        user.tutor_arrival = row_dict['tutor_arrival']
        user.tutor_departure = row_dict['tutor_departure']
        user.tutor_accompanying_names = row_dict['tutor_accompanying_names']
        user.tutor_address = row_dict['tutor_address']
        user.tutor_bank_account = row_dict['tutor_bank_account']
        user.password = row_dict['password']
        user.must_change_password_upon_login = row_dict['must_change_password_upon_login']
        user.confirmed_email = row_dict['confirmed_email']
        user.is_locked = row_dict['is_locked']
        user.update()
        
    
    # trida - zatim bez relationships
    for t in Trida.get_all():
        t.delete()
    df_trida = pd_excel['trida']
    for _, row in df_trida.iterrows():
        row_dict = row.to_dict()
        row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}

        trida = Trida()
        trida.id = row_dict['id']
        trida.short_name_cz = row_dict['short_name_cz']
        trida.full_name_cz = row_dict['full_name_cz']
        trida.short_name_en = row_dict['short_name_en']
        trida.full_name_en = row_dict['full_name_en']
        trida.capacity = row_dict['capacity']
        trida.has_capacity = row_dict['has_capacity']
        trida.secondary_billing_behavior = row_dict['secondary_billing_behavior']
        trida.is_time_exclusive = row_dict['is_time_exclusive']
        trida.age_group = row_dict['age_group']
        trida.update()
        
    # meal_orders - uz s relationships
    for mo in Meal_order.get_all():
        mo.delete()
    df_meal_order = pd_excel['meal_order']
    for _, row in df_meal_order.iterrows():
        row_dict = row.to_dict()
        row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}

        meal_order = Meal_order()
        meal_order.id = row_dict['id']
        meal_order.count = row_dict['count']
        meal_order.user_id = row_dict['user_id']
        meal_order.meal_id = row_dict['meal_id']
        meal_order.update()
        
    
    # user_role_jointable
    user_role_jointable = pd_excel['user_role_jointable']
    db.session.execute(db.text("DELETE FROM user_role_jointable;"))
    
    for _, row in user_role_jointable.iterrows():
        row_dict = row.to_dict()
        row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
        db.session.execute(db.text(f"INSERT INTO user_role_jointable (user_id, role_id) VALUES ({row_dict['user_id']}, {row_dict['role_id']});",))
    db.session.commit()
    
    # user_secondary_class_jointable
    user_secondary_class_jointable = pd_excel['user_secondary_class_jointable']
    db.session.execute(db.text("DELETE FROM user_secondary_class_jointable;"))
    for _, row in user_secondary_class_jointable.iterrows():
        row_dict = row.to_dict()
        row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
        db.session.execute(db.text(f"INSERT INTO user_secondary_class_jointable (user_id, class_id) VALUES ({row_dict['user_id']}, {row_dict['class_id']});",))
    db.session.commit()
    
    # parents
    df_user = pd_excel['user']
    for _, row in df_user.iterrows():
        row_dict = row.to_dict()
        row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
        if row_dict['parent_id']:
            user = User.get_by_id(row_dict['id'])
            user.parent_id = row_dict['parent_id']
            user.update()
    
    # tutor_id in trida
    df_trida = pd_excel['trida']
    for _, row in df_trida.iterrows():
        row_dict = row.to_dict()
        row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
        if row_dict['tutor_id']:
            trida = Trida.get_by_id(row_dict['id'])
            trida.tutor_id = row_dict['tutor_id']
            trida.update()
            
    # primary_class_id in user
    df_user = pd_excel['user']
    for _, row in df_user.iterrows():
        row_dict = row.to_dict()
        row_dict = {k: (None if pd.isna(v) else v) for k, v in row_dict.items()}
        if row_dict['primary_class_id']:
            user = User.get_by_id(row_dict['id'])
            user.primary_class_id = row_dict['primary_class_id']
            user.update()
    
    return result