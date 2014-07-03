from math import ceil


class Paginator(object):

    def __init__(self, **kwargs):
        count = kwargs.get('count', None)

        self.objects = list(kwargs.pop('objects', []))
        self.per_page = int(kwargs.pop('per_page', 10))
        self.page = self.validate(kwargs.pop('page', 1))
        self._num_pages = self._count = None
        if count:
            self._count = count

    def validate(self, page):
        try:
            page = int(page)
        except (TypeError, ValueError):
            page = 1
        return page

    def results(self):
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        return self.objects[start:end]

    @property
    def count(self):
        if self._count is None:
            self._count = len(self.objects)
        return self._count

    @property
    def pages(self):
        if self._num_pages is None:
            self._num_pages = int(ceil(self.count / float(self.per_page)))
        return self._num_pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_page_number(self):
        return self.page + 1

    @property
    def previous_page_number(self):
        return self.page - 1

    def __iter__(self):
        last = 0
        left_edge = left_current = right_edge = 2
        right_current=5

        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

