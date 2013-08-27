#!/usr/bin/env python

# ./dump.py; dropdb art17_mdb; createdb art17_mdb; psql art17_mdb < schema.sql; psql art17_mdb < data.sql

import subprocess
import re
from path import path

MDB = 'Article17-database.mdb'
outdir = path(__file__).abspath().parent

tables = [
    'data_gmeasures',
    'data_greintroduction_of_species',
    'data_greport',
    'data_habitats',
    'data_habitats_check_list',
    'data_habitattype_regions',
    'data_species',
    'data_species_regions',
    'data_measures',
    'data_notes',
    'data_pressures_threats',
    'data_pressures_threats_pol',
    'data_species_check_list',
    'sys_import',
    'sys_info_be',
    'sys_user',
    'data_htypical_species',
]


def fix_schema(schema):
    out = []
    for line in schema.splitlines():
        if 'MSysNavPane' in line:
            continue
        line = re.sub(r'Postgres_Unknown 0x\d\d', 'TEXT', line)
        line = re.sub(r'\bCREATE UNIQUE INDEX\b', 'CREATE INDEX', line)
        line = re.sub(r'\bBOOL\b', 'INTEGER', line)
        out.append(line)
    return '\n'.join(out)


with (outdir / 'schema.sql').open('wb') as f:
    schema = subprocess.check_output(['mdb-schema', MDB, 'postgres'])
    f.write(fix_schema(schema))

with (outdir / 'data.sql').open('wb') as f:
    f.write('\set ON_ERROR_STOP\n\n')
    f.flush()
    for table in tables:
        subprocess.check_call(['mdb-export', '-I', 'postgres', '-q', "'",
                               MDB, table], stdout=f)
