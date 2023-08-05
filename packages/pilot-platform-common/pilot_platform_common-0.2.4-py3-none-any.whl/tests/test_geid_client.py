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

from common.geid.geid_client import GEIDClient


class TestGEIDClient:
    client = GEIDClient()

    def test_01_get_GEID(self):
        geid = self.client.get_GEID()
        assert type(geid) == str
        assert len(geid) == 47

    def test_02_get_bulk_GEID(self):
        geids = self.client.get_GEID_bulk(5)
        assert type(geids) == list
        assert len(geids) == 5
