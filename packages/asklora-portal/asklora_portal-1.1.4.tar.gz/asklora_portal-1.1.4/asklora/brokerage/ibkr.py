from base64 import b64decode
from datetime import date
from typing import Optional

from asklora.brokerage.client import BaseRestClient
from asklora.brokerage.enums import DAMAllowedCurrenciesEnum, DAMEnumerationsTypeEnum
from asklora.brokerage.models import DAMApplicationPayload, InstructionSet
from asklora.brokerage.vars import DAMSettings
from asklora.dam import DAM
from asklora.pgp import PGPHelper
from asklora.utils.common import deep_get


class DAMECAClient(BaseRestClient):
    def __init__(self):
        # check environment variables
        dam_settings = DAMSettings()

        # assign attributes
        self.base_payload = dict(CSID=dam_settings.DAM_CSID)

        super().__init__(base_url=dam_settings.DAM_ECA_URL)

    # ===================== Schema and Healthcheck =====================

    def check_api(self) -> dict:
        return self.post("healthcheck", self.base_payload)

    def get_enumerations(
        self,
        enum_type: DAMEnumerationsTypeEnum,
        currency: Optional[str] = None,
        form_number: Optional[str] = None,
    ) -> str:
        if enum_type == DAMEnumerationsTypeEnum.EDD_AVT and form_number is None:
            raise ValueError("Need form number data for this enum type")

        if enum_type == DAMEnumerationsTypeEnum.FIN_INFO_RANGES and currency is None:
            raise ValueError("Need currency data for this enum type")

        payload = self.base_payload
        payload["type"] = enum_type.value

        if currency:
            if currency not in DAMAllowedCurrenciesEnum:
                raise ValueError("Invalid currency code")

            payload["currency"] = currency

        if form_number:
            payload["formNumber"] = form_number

        response = self.post("getEnumerations", self.base_payload, raw_response=True)
        decoded_response = b64decode(response).decode("utf-8")

        return decoded_response

    # ===================== Create Accounts and Updating Account Information =====================

    def create_account(
        self,
        applicant_data: DAMApplicationPayload,
        pgp_helper: PGPHelper,
    ) -> str | None:
        payload = self.base_payload
        payload["payload"] = DAM.generate_application_payload(
            applicant_data,
            pgp_helper=pgp_helper,
        )

        # send the response
        response = self.post("create", data=payload)

        try:
            response["fileData"]["data"] = DAM.decode_xml_response(
                deep_get(response, ["fileData", "data"]),
                pgp_helper=pgp_helper,
            )
        except Exception:
            pass

        return response

    # ===================== View Account Information and Registration Tasks =====================

    def get_pending_tasks(
        self,
        account_ids: Optional[list[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> dict:
        payload = self.base_payload

        if account_ids:
            payload["accountIDs"] = account_ids

        if start_date and end_date:
            payload["startDate"] = start_date
            payload["endDate"] = end_date

        return self.post("getPendingTasks", self.base_payload)

    def get_registration_tasks(
        self,
        account_ids: Optional[list[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        get_docs: Optional[bool] = None,
    ) -> dict:
        payload = self.base_payload

        if account_ids:
            payload["accountIDs"] = account_ids

        if get_docs is not None:
            payload["getDocs"] = "T" if get_docs else "F"

        if get_docs is None and (start_date and end_date):
            payload["startDate"] = start_date
            payload["endDate"] = end_date

        return self.post("getRegistrationTasks", self.base_payload)

    def get_account_details(self, account_ids: list[str]) -> dict:
        payload = self.base_payload
        payload["accountIDs"] = account_ids

        return self.post("getAccountDetails", self.base_payload)


class DAMFBClient(BaseRestClient):
    def __init__(self):
        # check environment variables
        dam_settings = DAMSettings()

        # assign attributes
        self.base_payload = dict(CSID=dam_settings.DAM_CSID)

        super().__init__(base_url=dam_settings.DAM_FB_URL)

    def create_instruction(
        self,
        instruction: InstructionSet | str,
        pgp_helper: PGPHelper,
    ) -> dict:
        if isinstance(instruction, InstructionSet):
            instruction = instruction.to_xml(
                pretty_print=True,
                encoding="UTF-8",
                skip_empty=True,
                xml_declaration=True,
            ).decode()

        encoded_instruction = DAM.encode_file_payload(
            instruction,
            file_name="instructions.xml",
            pgp_helper=pgp_helper,
        )

        payload = self.base_payload
        payload["request"] = encoded_instruction

        # send the request
        response = self.post("new-request", self.base_payload)

        if "details" in response:
            response["details"] = DAM.decode_xml_response(
                response.get("details"),
                pgp_helper=pgp_helper,
            )

        return response

    def get_status(self, instruction_id: int, pgp_helper: PGPHelper) -> dict:
        encoded_instruction_ids = DAM.encode_file_payload(
            str(instruction_id),
            file_name="instruction_ids.txt",
            pgp_helper=pgp_helper,
        )

        payload = self.base_payload
        payload["instruction_set_id"] = encoded_instruction_ids

        response = self.post("get-status", self.base_payload)

        if "details" in response:
            response["details"] = DAM.decode_xml_response(
                response.get("details"),
                pgp_helper=pgp_helper,
            )

        return response

    def get_updates(self, since: date | str, pgp_helper: PGPHelper) -> dict:
        since = since if isinstance(since, str) else since.strftime("%Y-%m-%d")

        encoded_date = DAM.encode_file_payload(
            since,
            file_name="instruction_ids.txt",
            pgp_helper=pgp_helper,
        )

        payload = self.base_payload
        payload["since_yyyy-mm-dd"] = encoded_date

        response = self.post("get_updated_upload_ids", self.base_payload)

        if "details" in response:
            response["details"] = DAM.decode_xml_response(
                response.get("details"),
                pgp_helper=pgp_helper,
            )

        return response
