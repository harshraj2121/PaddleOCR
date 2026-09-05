from sqlalchemy.orm import Session
from .schemas import FormCreate
from .models import Form

def create_form(db: Session, form_data: FormCreate):
    new_form = Form(
        application_number = form_data.application_number,
        applicant_name = form_data.applicant_name,
        form_id = form_data.form_id,
        gender = form_data.gender,
        contact_number = form_data.contact_number,
        email = form_data.email,
        city = form_data.city,
        complete_address = form_data.complete_address,
        form_type = form_data.form_type,
        submission_date = form_data.submission_date,
        martial_status = form_data.martial_status,
        source_file = form_data.source_file,
    )

    db.add(new_form)
    db.commit()
    db.refresh(new_form)

    return new_form