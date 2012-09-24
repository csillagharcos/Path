from django.utils.translation import ugettext_lazy as _

C_SECTION_CHOICES = (
    (0, _('Planned')),
    (1, _('Acute')),
    )

DRG_CODES_CHOICES = (
    ('', _('-- Select --')),
    ('671', '671'),
    ('671A', '671A'),
    ('671B', '671B'),
    ('672', '672'),
    ('673', '673'),
    ('674', '674'),
    )

YES_NO_CHOICES = (
    (0, _('No')),
    (1, _('Yes')),
    )

JOB_CHOICES = (
    (_('Physician'), _('Physician')),
    (_('Nurse'), _('Nurse')),
    (_('Other healthcare worker'), _('Other healthcare worker')),
    (_('Cleaning staff'), _('Cleaning staff')),
    (_('Total number of hospital staff'), _('Total number of hospital staff')),
    (1, _('Other')),
    )

PRINCIPAL_DIAG_CODE_C = (
    ('', _('-- Select --')),
    ('C18', 'C18'),
    ('C19', 'C19'),
    ('C20', 'C20'),
    ('C20.0', 'C21.0'),
    ('C20.1', 'C21.1'),
    ('C20.2', 'C21.2'),
    ('C20.8', 'C21.8'),
    )

PENICILIN_ALLERGY_CHOICES = (
    ('1', _('Immediate')),
    ('2', _('Other')),
    ('3', _('No Information'))
    )

ROUTE_OF_ADMIN_CHOICES = (
    (1, _('IV')),
    (2, _('IM')),
    (3, _('SC')),
    (4, _('Other')),
    (5, _('PO')),
    )

PRINCIPAL_DIAG_CODE_S = (
    ('', _('-- Select --')),
    ('S70.0', 'S70.0'),
    ('S70.1', 'S70.1'),
    ('S70.2', 'S70.2'),
    ('0', _('Other')),
    )


ROUTE_OF_ADMIN_CHOICES_FOUR = (
    (1, _('IV')),
    (2, _('IM')),
    (3, _('SC')),
    (4, _('Other')),
    )


AMI_CHOICES = (
    ('', _('-- Select --')),
    ('I21', 'I21'),
    ('I22', 'I22'),
    )

ADMISSION_STATUS_CHOICES = (
    (0, _('From home/nursing home/community care')),
    (1, _('Transferred from another hospital')),
    )

DISCHARGE_STATUS_CHOICES = (
    (0, _('Home/nursing home/community care')),
    (1, _('Transferred into another hospital')),
    (2, _('Death')),
    (3, _('Discharge at own request')),
    )

STROKE_CHOICES = (
    ('', _('-- Select --')),
    ('I61', 'I61'),
    ('I62', 'I62'),
    ('I63', 'I63'),
    ('I64', 'I64'),
    )

TYPE_OF_ADMISSION = (
    (0, _('Planned')),
    (1, _('Urgent surgical')),
    (2, _('Emergency care')),
    )

DIAGNOSES_GROUP_CHOICES = (
    (0, _('Stroke')),
    (1, _('Hospital acquired pneumonia')),
    (2, _('Hip fracture')),
    (3, _('CABG')),
    (4, _('Knee arthroscopy')),
    (5, _('Inguinal hernia')),
    (6, _('Tonsillectomy and/or adenoidectomy')),
    (7, _('Cholecystectomy')),
    (8, _('Varicose veins - stripping and ligation')),
    )

ICD10_CHOICES = (
    ('', _('-- Select --')),
    (_('Stroke'), (
        ('I61', 'I61'),
        ('I62', 'I62'),
        ('I63', 'I63'),
        ('I64', 'I64'),
        )),
    (_('Hospital acquired pneumonia'), (
        ('J13', 'J13'),
        ('J14', 'J14'),
        ('J15', 'J15'),
        ('J18', 'J18'),
        ('A481', 'A481'),
        )),
    (_('Hip fracture'), (
        ('S720', 'S720'),
        ('S721', 'S721'),
        ('S722', 'S722'),
        )),
    (_('Inguinal hernia'), (
        ('K40', 'K40'),
        )),
    )

DRG_CHOICES = (
    ('', _('-- Select --')),
    (_('CABG'), (
        ('177A', '177A'),
        ('177B', '177B'),
        ('177C', '177C'),
        ('177D', '177D'),
        ('190A', '190A'),
        ('192A', '192A'),
        ('192B', '192B'),
        )),
    (_('Knee arthroscopy'), (
        ('398A', '398A'),
        ('398B', '398B'),
        )),
    (_('Inguinal hernia'), (
        ('281B', '281B'),
        ('282A', '282A'),
        ('282B', '282B'),
        )),
    (_('Tonsillectomy and/or adenoidectomy'), (
        ('097A', '097A'),
        )),
    (_('Cholecystectomy'), (
        ('344', '344'),
        ('345', '345'),
        ('369Z', '369Z'),
        )),
    (_('Varicose veins - stripping and ligation'), (
        ('2030', '2030'),
        )),
    )

TYPE_OF_UNIT = (
    (1, _('Acute department')),
    (2, _('Rehabilitation department')),
)

TYPE_OF_DISCHARGE = (
    (1, _('Transfer to another inpatient hospital')),
    (2, _('Discharge to home, social home')),
    (3, _('Patient left hospital against medical advice')),
    (4, _('In-hospital death')),
    (0, _('Other')),
)

FIELD_OF_REHAB = (
    (0, _('neurology')),
    (1, _('cardiology')),
    (2, _('muskoloskeletal')),
    (3, _('pulmonary')),
    (4, _('other')),
)

DISCHARGE = (
    (0, _('Planned')),
    (1, _('Unplanned')),
)