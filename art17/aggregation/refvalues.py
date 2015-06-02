import json
import os
from flask import current_app


REQUIRED_FIELDS = {
    'habitat': ["range", "coverage_range"],
    'species': ["habitat", "population_range", "population_units", "range"]
}


def load_refval(filename):
    dir = current_app.config.get('REFVAL_DIR', '.')
    filepath = os.path.join(dir, filename)

    data = {}
    if not os.path.exists(filepath):
        print "Missing: ", filepath
    else:
        with open(filepath, 'r') as fin:
            try:
                data = json.load(fin)
            except ValueError:
                print "Invalid json: ", filepath
    return data


def save_refval(filename, data):
    dir = current_app.config.get('REFVAL_DIR', '.')
    filepath = os.path.join(dir, filename)

    with open(filepath, 'w') as fout:
        json.dump(data, fout, indent=1)
        print "Saved: ", filepath


def load_species_refval():
    return load_refval('species.json')


def save_species_refval(data):
    return save_refval('species.json', data)


def load_habitat_refval():
    return load_refval('habitats.json')


def save_habitat_refval(data):
    return save_refval('habitats.json', data)


def refvalue_ok(refvalue, subject_type):
    if not refvalue:
        return None
    required = REQUIRED_FIELDS[subject_type]
    for k in required:
        if not any(refvalue[k].values()):
            return False
    return True


def extract_key(refval, key):
    for k, v in refval.iteritems():
        if key in k:
            return v
    return None


def get_subject_refvals(page, subject):
    if page == 'species':
        refvals = load_species_refval()
    elif page == 'habitat':
        refvals = load_habitat_refval()
    else:
        raise NotImplementedError()

    data = [(k[len(subject) + 1:], v) for k, v in refvals.iteritems() if
            k.startswith(subject)]

    return data


def get_subject_refvals_wip(page, subject):
    from art17.models import RefValue

    result = RefValue.query.filter_by(page=page, object_code=subject)
    data = {}
    for row in result:
        region = row.object_region
        group = row.group
        if region not in data:
            data[region] = {}
        if group not in data[region]:
            data[region][group] = {}
        data[region][group][row.name] = (
            unicode(row.value) if row.value else None
        )

    return data


def get_subject_refvals_mixed(page, subject):
    data = dict(get_subject_refvals(page, subject))
    wip = get_subject_refvals_wip(page, subject)
    for region, rvalues in data.iteritems():
        for group, values in rvalues.iteritems():
            for name in values:
                wip_data = wip.get(region, {}).get(group, {}).get(name)
                if wip_data:
                    data[region][group][name] = wip_data
    return data


def set_subject_refvals_wip(page, subject, data):
    from art17.models import RefValue, db

    qs = RefValue.query.filter_by(page=page, object_code=subject)
    for k, value in data.iteritems():
        region, group, name = k.split('=')
        existing = qs.filter_by(object_region=region, group=group,
                                name=name).first()
        if existing:
            if value:
                if value != existing.value:
                    existing.value = value
            else:
                db.session.delete(existing)
        else:
            if value:
                existing = RefValue(page=page, object_code=subject,
                                    object_region=region, group=group,
                                    name=name,
                                    value=value)
                db.session.add(existing)

    db.session.commit()
