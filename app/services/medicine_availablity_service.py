from app.models.models import Medicine

def get_all_medicines():
    meds = Medicine.query.all()
    return [m.to_dict() for m in meds]


def search_medicine_by_name(name):
    meds = Medicine.query.filter(
        Medicine.name.ilike(f"%{name}%")
    ).all()
    return [m.to_dict() for m in meds]


def get_medicines_by_category(category):
    meds = Medicine.query.filter(
        Medicine.category.ilike(category)
    ).all()
    return [m.to_dict() for m in meds]


def get_medicine_by_id(medicine_id):
    med = Medicine.query.get(medicine_id)
    return med.to_dict() if med else None