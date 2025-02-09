from website import db

user_role_jointable = db.Table("user_role_jointable",
                               db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                               db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
                               )

user_meal_jointable = db.Table(
    "user_meal_jointable", db.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("meal_id", db.Integer, db.ForeignKey("meal.id"), primary_key=True)
)