DATE_FORMAT_HISTORY = '%d-%m-%Y'

ROLE_MISSING = 'missing'
ROLE_AGGREGATED = 'aggregated'
ROLE_DRAFT = 'final-draft'
ROLE_FINAL = 'assessment'

ROLE_CONS_COMMENT = 'comment'
ROLE_CONS_COMMENT_DRAFT = 'comment-draft'
ROLE_CONS_FINAL = 'final'

CONS_ROLES = [ROLE_CONS_COMMENT, ROLE_CONS_COMMENT_DRAFT, ROLE_CONS_FINAL]

RECORD_ROLES = {
    ROLE_MISSING: 'The data was missing',
    ROLE_AGGREGATED: 'Initial role',
    ROLE_DRAFT: 'Assessment being edited',
    ROLE_FINAL: 'Final record, ready for consultation',
}
