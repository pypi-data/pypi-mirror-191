import tempfile
from base64 import b64decode, b64encode
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from asklora.brokerage import enums, models
from asklora.logger import logger
from asklora.pgp import PGPHelper
from asklora.utils import get_file_sha1, get_file_size


class DAM:
    @classmethod
    def __generate_application_xml(cls, data: models.DAMApplicationPayload):
        current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        mailing_address = None
        employment_details = None

        w8ben_file = (
            Path(data.w8ben_file)
            if isinstance(data.w8ben_file, str)
            else data.w8ben_file
        )
        proof_of_identity_file = (
            Path(data.proof_of_identity_file)
            if isinstance(data.proof_of_identity_file, str)
            else data.proof_of_identity_file
        )
        proof_of_address_file = (
            Path(data.proof_of_address_file)
            if isinstance(data.proof_of_address_file, str)
            else data.proof_of_address_file
        )

        email = models.Email(email=data.email)
        name = models.Name(
            first=data.first_name,
            last=data.last_name,
            middle=data.middle_name,
        )
        identification = models.Identification(
            citizenship=data.identification_citizenship,
            issuing_country=data.identification_issuing_country,
            national_card=data.identification_number,
        )
        residence = models.Residence(
            country=data.country,
            state=data.state,
            city=data.city,
            postal_code=data.postal_code,
            street_1=data.street_name,
        )

        if not data.is_mailing_address:
            mailing_address = models.MailingAddress(
                country=data.mailing_country,
                state=data.mailing_state,
                city=data.mailing_city,
                postal_code=data.mailing_postal_code,
                street_1=data.mailing_street_name,
            )

        if data.employment_type in [
            enums.EmploymentTypeEnum.EMPLOYED,
            enums.EmploymentTypeEnum.SELFEMPLOYED,
        ]:
            employment_details = models.EmploymentDetails(
                employer=data.employer,
                occupation=data.occupation,
                employer_business=data.employer_business,
                employer_address=models.EmployerAddress(
                    country=data.employer_address_country,
                    state=data.employer_address_state,
                    city=data.employer_address_city,
                    postal_code=data.employer_address_postal_code,
                    street_1=data.employer_address_street_name,
                ),
            )

        tax_residency = models.TaxResidency(
            country=data.tax_country,
            tin_type=enums.TINTypeEnum.NON_US.value,
            tin=data.tin,
        )
        financial_information = models.FinancialInformation(
            sources_of_wealth=[
                models.SourceOfWealth(
                    percentage=100,
                    source_type=data.sow_type.value,
                    is_used_for_funds=True,
                )
            ]
        )
        w8ben = models.W8Ben(
            cert=True,
            part_2_9a_country="N/A",
            name=name.get_full_name(),
            proprietary_form_number="5001",
            blank_form=True,
            tax_form_file="Form5001.pdf",
            foreign_tax_id=data.tin,
        )

        account_holder = models.AccountHolder(
            details=models.AccountHolderDetails(
                external_id=data.user_id,
                same_mail_address=data.is_mailing_address,
                name=name,
                country_of_birth=data.country_of_birth,
                dob=data.date_of_birth,
                email=email,
                residence=residence,
                mailing_address=mailing_address,
                identification=identification,
                tax_residencies=[tax_residency],
                w8ben=w8ben,
                employment_type=data.employment_type,
                employment_details=employment_details,
            ),
            financial_information=financial_information,
        )

        # main models
        customer = models.Customer(
            email=data.email,
            external_id=data.user_id,
            prefix="lora",
            customer_type="INDIVIDUAL",
            md_status_nonpro=False,
            meets_aml_standard=True,
            has_direct_trading_access=False,
            account_holder=account_holder,
        )

        account = models.Account(
            external_id=data.user_id,
            base_currency="USD",
            margin=enums.AccountMarginEnum.CASH.value,
            multicurrency=False,
            drip=False,
            client_active_trading=False,
            trading_permissions=[
                models.TradingPermission(product="STOCKS", country="UNITED STATES"),
                # models.TradingPermission(exchange_group="FOREX"),
            ],
        )
        user = models.User(
            external_individual_id=data.user_id,
            external_user_id=data.user_id,
            prefix="lora",
        )

        documents = [
            models.Document(
                form_no="5001",
                exec_ts=current_timestamp,
                exec_login_ts=current_timestamp,
                signed_by=name.get_full_name(with_initial=True),
                attached_file=models.AttachedFile(
                    file_name=w8ben_file.name,
                    file_length=get_file_size(w8ben_file),
                    sha1_checksum=get_file_sha1(w8ben_file),
                ),
            ),
            models.Document(
                form_no="8001",
                exec_ts=current_timestamp,
                exec_login_ts=current_timestamp,
                proof_of_identity_type="National ID Card",
                signed_by=name.get_full_name(with_initial=True),
                attached_file=models.AttachedFile(
                    file_name=proof_of_identity_file.name,
                    file_length=get_file_size(proof_of_identity_file),
                    sha1_checksum=get_file_sha1(proof_of_identity_file),
                ),
            ),
        ]

        if proof_of_address_file:
            proof_of_address_document = models.Document(
                form_no="8002",
                exec_ts=current_timestamp,
                exec_login_ts=current_timestamp,
                proof_of_address_type=data.proof_of_address_type.value,
                signed_by=name.get_full_name(with_initial=True),
                attached_file=models.AttachedFile(
                    file_name=proof_of_address_file.name,
                    file_length=get_file_size(proof_of_address_file),
                    sha1_checksum=get_file_sha1(proof_of_address_file),
                ),
            )

            documents.append(proof_of_address_document)

        application = models.Application(
            customer=customer,
            accounts=[account],
            users=[user],
            documents=documents,
        )

        applications = models.Applications(applications=[application])

        return applications.to_xml(
            encoder=models.CustomXmlEncoder(),
            pretty_print=True,
            encoding="UTF-8",
            skip_empty=True,
            standalone=True,
        ).decode()

    @classmethod
    def __process_zip_file(cls, files: str, path: Path, file_name="data.zip"):
        zip_file = path.joinpath(file_name)

        with ZipFile(zip_file, "w", ZIP_DEFLATED) as zf:
            for file in files:
                file = Path(file) if isinstance(file, str) else file
                zf.write(file, file.name)

        return zip_file

    @classmethod
    def __encode_file(cls, zip_file: Path) -> str | None:
        try:
            with open(zip_file, "rb") as f:
                file_data = f.read()

                # encode the data to base64
                encoded_data = b64encode(file_data)

                return encoded_data.decode("utf-8").replace("\n", "")

        except FileNotFoundError:
            logger.error("Cannot find file")
        except Exception as e:
            logger.error(f"Cannot encode zip file: {e}")

    @classmethod
    def __encrypt_and_encode_file(
        cls,
        file: Path,
        pgp_helper: PGPHelper,
    ) -> str:
        encrypted_file = file.parent.joinpath(f"encrypted_{file.name}")

        pgp_helper.encrypt_file(file, output=encrypted_file)
        return cls.__encode_file(encrypted_file)

    @classmethod
    def generate_application_payload(
        cls,
        data: models.DAMApplicationPayload,
        pgp_helper: PGPHelper,
        xml_file_name: str = "application.xml",
        zip_file_name: str = "data.zip",
    ):
        xml_data = cls.__generate_application_xml(data)
        attached_files = data.attached_files

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            xml_file = tmp_path.joinpath(xml_file_name)

            # write xml_data to file
            with open(xml_file, "w") as f:
                f.write(xml_data)

            # add the xml to the list of files
            attached_files.append(xml_file)

            # build the zip file
            zip_file = cls.__process_zip_file(
                attached_files,
                path=tmp_path,
                file_name=zip_file_name,
            )

            # encrypt zip file and encode it to base64
            encoded_zip_file = cls.__encrypt_and_encode_file(
                zip_file,
                pgp_helper=pgp_helper,
            )

            return encoded_zip_file

    @classmethod
    def encode_file_payload(
        cls,
        file_content: str,
        file_name: str,
        pgp_helper: PGPHelper,
    ):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            payload_file = tmp_path.joinpath(file_name)

            # write file content
            with open(payload_file, "w") as f:
                f.write(file_content)

            # encrypt the file and encode it to base64
            encoded_file = cls.__encrypt_and_encode_file(
                payload_file,
                pgp_helper=pgp_helper,
            )

            return encoded_file

    @classmethod
    def decode_xml_response(cls, data: str, pgp_helper: PGPHelper):
        encrypted_data = b64decode(data.encode())
        data = pgp_helper.decrypt_payload(encrypted_data)

        return data
