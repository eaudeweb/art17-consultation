from bs4 import BeautifulSoup


TABS = {
    'species': 'Specii',
    'habitat': 'Habitate',
}


def get_tables(html):
    soup = BeautifulSoup(html)
    tables = soup.find('div', {'class': 'content'}).find_all('table')
    tables = [BSTable(table) for table in tables]
    return tables


def get_property(td_tag, prop_name):
    prop_value = td_tag.get(prop_name)
    return int(prop_value) - 1 if prop_value else 0


class BSTable(object):
    def __init__(self, table_tag):
        tab_id = table_tag.parent.get('id')
        self.title = TABS[tab_id.split('-')[-1]] if tab_id else 'Raport'
        self.colshift = []
        rows = table_tag.find_all('tr')
        self.rows = [BSRow(i, r, self) for i, r in enumerate(rows, start=1)]

    def update_colshift(self, col, rows, shift, source='colspan'):
        if source == 'rowspan' and col - 1 in [c[0] for c in self.colshift]:
            return self.update_colshift(col - 1, rows, shift)
        self.colshift.append((col, rows, shift))


class BSRow(object):
    def __init__(self, idx, tr_tag, table):
        self.idx = idx
        self.table = table
        cells = tr_tag.find_all('th') + tr_tag.find_all('td')
        self.cells = [BSCell(i, c, self) for i, c in enumerate(cells, start=1)]


class BSCell(object):
    def __init__(self, idx, td_tag, row):
        self.col_idx = idx
        self.row = row
        self.colspan = get_property(td_tag, 'colspan')
        self.rowspan = get_property(td_tag, 'rowspan')

        if self.rowspan:
            row.table.update_colshift(
                idx,
                range(row.idx + 1, row.idx + self.rowspan + 1),
                1,
                'rowspan',
            )
        if self.colspan:
            row.table.update_colshift(idx + 1, [row.idx], self.colspan)

        for col_idx, rows, shift in row.table.colshift:
            if idx >= col_idx and self.row.idx in rows:
                self.col_idx += shift

        self.tag = td_tag.name
        self.text = ' '.join(td_tag.text.split())
