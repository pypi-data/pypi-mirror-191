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


class ConfigCenterPolicy:
    @staticmethod
    def get_granted(srv_namespace):
        return {'service_download': ConfigCenterPolicy.service_download()}.get(srv_namespace, [])

    @staticmethod
    def service_download():
        return [
            'DOWNLOAD',
            'KEYCLOAK',
            'MINIO',
            'REDIS',
            'NEO4J_SERVICE',
            'PROVENANCE_SERVICE',
            'QUEUE_SERVICE',
            'UTILITY_SERVICE',
            'DATA_OPS_GR',
            'DATA_OPS_UTIL',
            'DATASET_SERVICE',
            'RDS_HOST',
            'RDS_PORT',
            'RDS_USER',
            'RDS_PWD',
            'RDS_DBNAME',
            'RDS_SCHEMA_DEFAULT',
            'OPEN_TELEMETRY_ENABLED',
            'CORE_ZONE_LABEL',
            'GREEN_ZONE_LABEL',
        ]
