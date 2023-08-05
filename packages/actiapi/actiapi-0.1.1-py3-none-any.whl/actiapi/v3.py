"""Pull data from CentrePoint API v3."""
import logging
from typing import Any, Dict, List, Union

import requests

from actiapi import ActiGraphClient


class ActiGraphClientV3(ActiGraphClient):
    BASE_URL = "https://api.actigraphcorp.com"
    AUTH_API = "https://auth.actigraphcorp.com/connect/token"

    @staticmethod
    def _generate_headers(token: str, raw: bool = False):
        headers = {}
        if not raw:
            headers["Accept"] = "application/json"
            headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer {token}"
        return headers

    def _get_access_token(self, scope: str):
        endpoint = self.AUTH_API
        request_body = {
            "client_id": self.api_access_key,
            "client_secret": self.api_secret_key,
            "scope": scope,
            "grant_type": "client_credentials",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(
            endpoint, data=request_body, headers=headers, verify=True
        )
        try:
            return response.json()["access_token"]
        except KeyError:
            raise RuntimeError(
                "No access token! Make sure you have API_ACCESS_KEY and API_SECRET_KEY!"
            )

    def get_files(
        self,
        user: Union[int, str],
        study_id: int,
    ) -> List[str]:
        results = []
        offset = 0
        limit = 100

        token = self._get_access_token(
            "DataAccess",
        )

        while True:
            resource_uri_subject_rawdata = f"/dataaccess/v3/files/studies/{study_id}/subjects/{user}/raw-accelerometer?fileFormat=avro&offset={offset}&limit=100"
            headers_subject_rawdata = self._generate_headers(token)
            subject_rawdata_info = requests.get(
                self.BASE_URL + resource_uri_subject_rawdata,
                headers=headers_subject_rawdata,
            )
            subject_rawdata = subject_rawdata_info.json()
            total_count = subject_rawdata["totalCount"]

            for raw_file in subject_rawdata["items"]:
                results.append(raw_file["downloadUrl"])
            if offset + limit >= total_count:
                break
            offset += limit

        if len(results) == 0:
            logging.error("No raw data found.")
            return []

        return results

    def get_study_metadata(self, study_id) -> List[Dict[str, Any]]:
        """Save all study metadata to file."""
        offset = 0
        limit = 100

        subject_metadata = []
        token = self._get_access_token("CentrePoint")
        while True:
            response = requests.get(
                f"{self.BASE_URL}/centrepoint/v3/Studies/{study_id}/Subjects?offset={offset}",
                headers=self._generate_headers(token),
            ).json()
            total_count = response["totalCount"]
            subject_metadata.extend(response["items"])
            offset += limit
            if offset >= total_count:
                break
        return subject_metadata
