"Module providing Record base data class."

import re
import os

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

from paperstack.data.constants import COLUMNS
from paperstack.filesystem.file import File


class Record:
    """Library record handling validation. This is the most basic data
    class in the program. Database information will be deserialized into
    this. Each `Record` instance will be in charge of its own BibTeX entry
    when exporting.

    Parameters
    ----------
    record : dict
        The entries of the record.
    config : paperstack.filesystem.config.Config
    messenger : paperstack.interface.message.Messenger
    delay_setup : bool
        Whether to delay validation and setup in order to first build up
        record.

    Attributes
    ----------
    RECORD_TYPE : {'article', 'book', 'website'}
        The type of record.
    REQUIREMENTS : list
        A list of requirement tuples.
    record : dict
        The entries of the record.
    config : paperstack.filesystem.config.Config
    messenger : paperstack.interface.message.Messenger
    """

    RECORD_TYPE = None
    REQUIREMENTS = []

    def __init__(self, record, config, messenger, delay_setup=False):
        self.record = record
        self.config = config
        self.messenger = messenger

        if not delay_setup:
            self.setup()
            self.validate()


    @property
    def requirements(self):
        "Get record requirements."

        return self.__class__.REQUIREMENTS


    def tabulate_horizontal(self):
        """Represent the record as a horizontal table.

        Returns
        -------
        str
        """

        record = {}

        for key, value in self.record.items():
            if value is not None:
                width = max(len(key), len(value))

                key = key.center(width, ' ')
                value = value.ljust(width, ' ')

                record[key] = value

        output = '│ ' + ' │ '.join(record.keys()) + ' │'

        header_width = len(output) - 2

        output += '\n'
        output += '│ ' + ' │ '.join(record.values()) + ' │'

        output = '┌' + '─' * header_width + '┐' + '\n' + output
        output += '\n' + '└' + '─' * header_width + '┘'

        return output


    def tabulate_vertical(self, column_width):
        """Represent the record as a vertical table.

        Parameters
        ----------
        column_width : str
            The maximum string width of the entries.

        Returns
        -------
        str
        """

        keys = map(str, self.record.keys())
        values = map(str, self.record.values())

        key_width = min(max(*map(len, keys)), column_width)
        value_width = min(max(*map(len, values)), column_width)

        output_lines = []

        for key, value in self.record.items():
            if value is not None:
                value = value.replace('\n', ' ')

                if len(key) > column_width:
                    key = key[:column_width - 5].strip() + '[...]'

                if len(value) > column_width:
                    value = value[:column_width - 5].strip() + '[...]'

                key = key.ljust(key_width, ' ')
                value = value.ljust(value_width, ' ')

                output_lines.append(f'│ {key} │ {value} │')

        output = '\n'.join(output_lines)

        header_width = len(output.split('\n', maxsplit=1)[0]) - 2

        output = '┌' + '─' * header_width + '┐' + '\n' + output
        output += '\n' + '└' + '─' * header_width + '┘'

        return output


    def __str__(self):
        output = self.tabulate_horizontal()

        output_lines = output.split('\n')
        output_width = max(*map(len, output_lines))

        terminal_width = os.get_terminal_size().columns

        if output_width > terminal_width:
            column_width = terminal_width // 2 - 4 # account for box chars
            output = self.tabulate_vertical(column_width)

        return output


    def validate(self):
        """Validate record according to requirements. Fields can be marked
        as required and constraints can be placed based on type and pattern
        matching.
        """

        for requirement in self.requirements:
            field, _, field_type, required, pattern = requirement

            if field in self.record and self.record[field]:
                if not isinstance(self.record[field], field_type):
                    self.messenger.send_error(
                        'Invalid record. Expected type `{}` for field "{}", but instead got `{}`.'.format(
                            field_type.__name__,
                            field,
                            type(self.record[field]).__name__
                        )
                    )
                elif pattern is not None and not re.match(pattern, self.record[field]):
                    self.messenger.send_error(
                        f'Invalid record. Field `{field}` does not match pattern `{pattern}`.'
                    )
            elif required:
                self.messenger.send_error(f'Invalid record. Field `{field}` required.')
            else:
                self.record[field] = None


    def generate_id(self):
        """Generate unique record ID (later used as BibTeX key) based on
        configuration.

        Returns
        -------
        str
        """

        record_type = self.__class__.RECORD_TYPE

        if record_type is None:
            raise NotImplementedError

        record_id = self.config.get(record_type, 'id-format').strip()

        item_pattern = re.compile(r'(\w+)@(\d+)')

        for field, length in item_pattern.findall(record_id):
            length = int(length)

            if field not in self.record:
                self.messenger.send_error(f'Cannot create record ID with non-existent field `{field}`.')

            if field == 'author':
                authors = self.record['author'].split(' and ')[:length]
                sub = '-'.join(authors)
            else:
                sub = self.record[field][:length].strip()

            record_id = record_id.replace(f'{field}@{length}', sub)

        record_id = re.sub(r'\s', '-', record_id)
        record_id = re.sub(r'[^0-9A-Za-z-]', '', record_id)
        record_id = record_id.lower()

        return record_id


    def setup(self):
        "Set up record."

        if 'record_id' not in self.record or self.record['record_id'] is None:
            self.record['record_id'] = self.generate_id()


    def to_sql(self):
        "Export to SQL (SQL insert command)."

        fields = 'record_type, {}'.format(
            ', '.join(self.record.keys())
        )

        values = '"{}", '.format(self.__class__.RECORD_TYPE)

        values += ', '.join(
            '"{}"'.format(
                value.replace('"', '%QUOTE')
            ) if value else 'NULL' for value in self.record.values()
        )

        return f'INSERT INTO library ({fields}) VALUES ({values})'


    def to_bibtex(self):
        "Export to BibTeX."

        raise NotImplementedError


    def download_pdf(self, scraper):
        """Download PDF from database using scraper.

        Parameters
        ----------
        scraper : paperstack.data.scraper.Scraper
        """

        data_path = File(self.config.get('paths', 'data'), True)
        save_path = data_path.join(
            '{}.pdf'.format(self.record['record_id'])
        )

        scraper.download_pdf(save_path)

        if 'path' in scraper.record and scraper.record['path']:
            self.record['path'] = scraper.record['path']


class Article(Record):
    """Article record for academic papers.

    Parameters
    ----------
    record : dict
        The entries of the record."""

    RECORD_TYPE = 'article'
    REQUIREMENTS = [
        ('author', 'Author', str, True, None),
        ('title', 'Title', str, True, None),
        ('tags', 'Tags', str, False, None),
        ('journal', 'Journal', str, True, None),
        ('year', 'Year', str, True, None),
        ('abstract', 'Abstract', str, False, None),
        ('volume', 'Volume', str, False, None),
        ('number', 'Number', str, False, None),
        ('pages', 'Pages', str, False, None),
        ('month', 'Month', str, False, None),
        ('doi', 'DOI', str, False, None),
        ('issn', 'ISSN', str, False, None),
        ('bibnote', 'Bibnote', str, False, None),
        ('bibcode', 'Bibcode', str, False, None),
        ('note', 'Note', str, False, None),
        ('path', 'Path', str, False, None),
        ('record_id', 'Record ID', str, True, None)
    ]


    def to_bibtex(self):
        database = BibDatabase()

        entries = [
            ('record_id', 'ID'),
            ('author', 'author'),
            ('title', 'title'),
            ('journal', 'journal'),
            ('year', 'year'),
            ('abstract', 'abstract'),
            ('volume', 'volume'),
            ('number', 'number'),
            ('pages', 'pages'),
            ('month', 'month'),
            ('doi', 'doi'),
            ('bibnote', 'comment'),
        ]

        bibtex_entries = {
            'ENTRYTYPE': 'article'
        }

        for record_key, bibtex_key in entries:
            if record_key in self.record and self.record[record_key]:
                bibtex_entries[bibtex_key] = str(self.record[record_key])

        database.entries = [bibtex_entries]

        writer = BibTexWriter()
        writer.indent = '    '

        return bibtexparser.dumps(database, writer)


record_constructors = {
    'article': Article
}


def build_record(record_list, config, messenger):
    """Build `Record` instance from well-ordered record list. This is the
    type of list that would come from a SELECT query.

    Parameters
    ----------
    record_list : list
    config : paperstack.filesystem.config.Config
    messenger : paperstack.interface.message.Messenger
    """

    record_dict = {
        COLUMNS[i][0] : value.replace('%QUOTE', '"') if value else value
        for i, value in enumerate(record_list)
    }

    constructor = record_constructors[record_list[1]]

    record = constructor(record_dict, config, messenger)

    return record
