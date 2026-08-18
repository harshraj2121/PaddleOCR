from pydantic import BaseModel


class FormCreate(BaseModel):

    application_number : str | None
    applicant_name : str | None
    form_id : str | None
    gender : str | None
    contact_number : str | None
    email : str | None
    city: str | None
    complete_address : str | None
    form_type : str | None
    submission_date : str | None
    martial_status : str | None
    source_file: str | None