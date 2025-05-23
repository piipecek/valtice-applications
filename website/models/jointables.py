from website import db

user_role_jointable = db.Table(
    "user_role_jointable",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.UniqueConstraint("user_id", "role_id", name="unique_user_role_constraint"),
)
