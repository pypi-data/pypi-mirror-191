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

from common.models.service_id_generator import GenerateId


class GEIDClient:
    def get_GEID(self) -> str:
        new_id = GenerateId()
        uniq_id = new_id.generate_id() + '-' + new_id.time_hash()
        return uniq_id

    def get_GEID_bulk(self, number: int) -> list:
        id_list = []
        for _ in range(number):
            new_id = GenerateId()
            uniq_id = new_id.generate_id() + '-' + new_id.time_hash()
            id_list.append(uniq_id)
        return id_list
