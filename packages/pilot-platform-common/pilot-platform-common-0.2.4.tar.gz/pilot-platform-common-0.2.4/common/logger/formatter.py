# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from functools import lru_cache
from logging import LogRecord
from typing import Any
from typing import Dict

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom formatter to format logging records as json strings."""

    @lru_cache(1)
    def get_namespace(self) -> str:
        """Get namespace for current service."""

        namespace = os.environ.get('namespace', 'unknown')

        return namespace

    def add_fields(self, log_record: Dict[str, Any], record: LogRecord, message_dict: Dict[str, Any]) -> None:
        """Add custom fields into the log record."""

        super().add_fields(log_record, record, message_dict)

        log_record['level'] = record.levelname
        log_record['namespace'] = self.get_namespace()
        log_record['sub_name'] = record.name


def get_formatter() -> CustomJsonFormatter:
    """Return instance of default formatter."""

    return CustomJsonFormatter(fmt='%(asctime)s %(namespace)s %(sub_name)s %(level)s %(message)s')
