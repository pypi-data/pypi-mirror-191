import abc
import http
import json
import logging
import time
from random import randint

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache, caches
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from los_docusign.models import (
    DocusignChoiceConfig,
    DocusignEnvelopeStageData,
    DocusignOrgTemplate,
    DocuSignUserAuth,
)
from los_docusign.utils.client import DocuSignClient
from los_docusign.utils.docusign_helper import get_access_token, get_docusign_user

LOGGER = logging.getLogger("root")


class DocusignAdapter(metaclass=abc.ABCMeta):
    config_key = None  # abstract, should be defined by child classes

    def __init__(self, *args, **kwargs):
        self._setup_organization()
        self.docusign_user = get_docusign_user(organization_pk=self.organization.pk)
        self.access_token = get_access_token(self.docusign_user)
        self._setup_docusign_template()
        self._setup_docusign_client()
        self._setup_log_config()
        self._setup_signing_cache()

    def _setup_signing_cache(self, use_signing_cache=False):
        self.use_signing_cache = use_signing_cache

    def _setup_docusign_template(self):
        try:
            template = DocusignOrgTemplate.objects.get(
                organization_model=ContentType.objects.get(model="organization"),
                organization_pk=self.organization.pk,
                docusign_template__template_type__config_key=self.config_key,
            ).docusign_template
        except DocusignOrgTemplate.DoesNotExist:
            dsua = DocuSignUserAuth.objects.get(default_user=True)
            template = DocusignOrgTemplate.objects.get(
                organization=dsua.organization,
                docusign_template__template_type=DocusignChoiceConfig.DOCUSIGN_TEMPLATE,
            ).docusign_template
        self.docusign_template = template

    def _setup_docusign_client(self):
        self.docusign_client = DocuSignClient(
            access_token=self.access_token,
            timeout=settings.DOCUSIGN_REQUEST_TIMEOUT,
            tenant_schema=settings.SCHEMA_NAME,
        )

    def _setup_log_config(self, *args, **kwargs):
        """
        Dictionary used by ApiHandler to log actions in the database
        """
        self.log_config = None

    @abc.abstractmethod
    def _setup_organization(self) -> dict:
        """
        This should be implemented by the application, and should set the
        organization to self.organization
        """
        raise NotImplementedError("You must implement this method")

    @abc.abstractmethod
    def prepare_payload(
        self, instance, payload, client_user_id, is_embedded_docusign, **kwargs
    ) -> dict:
        """
        This should be implemented by the application, and should return a dictionary in the form of
        """
        raise NotImplementedError("You must implement this method")

    def _error_payload_not_configured_0001(self, connection):
        raise ValidationError(_("Docusign payload not configured"))

    def _error_in_progress_0002(self):
        raise ValidationError(
            _(
                "DocuSign for this application is already in process, please try again after some time."
            )
        )

    def _error_high_volume_throttle_0003(self):
        raise ValidationError(
            _(
                "Our electronic signature process is currently experiencing high volume and we are throttling requests to protect your experience. Please return after one or two hours to complete your signature process. Your application is complete and your place in line is reserved."
            )
        )

    def _error_docusigning_failed_0004(self):
        raise ValidationError(_("Docusigning Failed"))

    def _error_high_volume_throttle_0005(self):
        raise ValidationError(
            _(
                "Our electronic signature process is currently experiencing high volume and we are throttling requests to protect your experience. Please return after one or two hours to complete your signature process. Your application is complete and your place in line is reserved."
            )
        )

    def _error_high_volume_throttle_0006(self):
        raise ValidationError(
            _(
                "Our electronic signature process is currently experiencing high volume and we are throttling requests to protect your experience. Please return after one or two hours to complete your signature process. Your application is complete and your place in line is reserved."
            )
        )

    def _error_unknown_0007(self, loan, exception):
        raise ValidationError(
            _(
                "Our electronic signature process is currently experiencing high volume and we are throttling requests to protect your experience. Please return after one or two hours to complete your signature process. Your application is complete and your place in line is reserved."
            )
        )

    def process_docusign_error(
        self, instance, docusign_envelope_stage_data, envelope_result
    ):
        error_text = json.loads(envelope_result.text)
        error_code = error_text["errorCode"]
        if error_code in [
            "HOURLY_APIINVOCATION_LIMIT_EXCEEDED",
            "BURST_APIINVOCATION_LIMIT_EXCEEDED",
        ]:
            raise Exception(
                "DocuSign API THROTTLING Error: {error_text}".format(
                    error_text=envelope_result.text
                )
            )
        else:
            docusign_envelope_stage_data.record_status = "F"
            docusign_envelope_stage_data.error_message = envelope_result.text

            # Since we are creating a new instance
            docusign_envelope_stage_data.save()  # nosemgrep
            raise Exception(
                "DocuSign Error: Failed to create the envelope for application"
                " id: {instance_id} : {error_text}".format(
                    instance_id=instance, error_text=envelope_result.text
                )
            )

    def _get_envelope_content_type(self, instance):
        return ContentType.objects.get(
            model=instance._meta.model_name, app_label=instance._meta.app_label
        )

    def get_client_user_id(self, is_embedded_docusign):
        return str(randint(10000, 99999)) if is_embedded_docusign else None

    def _create_current_status(self, envelope_id, envelope_status, signers):
        recipients = []
        for signer in signers:
            recipient = {
                "name": signer["name"],
                "email": signer["email"],
                "recipient_id": signer["recipientId"],
                "routing_order": signer["routingOrder"],
                "custom_fields": {"CustomField": signer["customFields"][0]},
                "status": "created",
                "phone_auth": {
                    "fail_count": None,
                    "status": None,
                    "last_event_time": None,
                },
            }
            recipients.append(recipient)
        return {
            "envelope_status": envelope_status,
            "envelopeId": envelope_id,
            "recipients": sorted(recipients, key=lambda x: x["routing_order"]),
        }

    def send_for_docusign(
        self,
        payload,
        phase,
        instance=None,
        is_embedded_docusign=False,
        return_url="https://www.google.com",
        **kwargs,
    ):
        lock_name = f"send_for_docusign:{instance.pk}"
        lock = caches["default"].lock(lock_name, timeout=60)
        if not lock.acquire(blocking=False):
            return self._error_in_progress_0002()
        docusign_envelope_stage_data = DocusignEnvelopeStageData(
            docusign_user=self.docusign_user,
            object_pk=instance.pk if instance else None,
        )

        docusign_envelope_stage_data.docusign_user = self.docusign_user

        docusign_envelope_stage_data.object_pk = instance.pk if instance else None

        docusign_envelope_stage_data.content_type = self._get_envelope_content_type(
            instance
        )

        if not payload:
            docusign_template = self.docusign_template
            docusign_los_payload = docusign_template.docusign_payload
        else:
            docusign_los_payload = payload

        if docusign_los_payload is None:
            return self._error_payload_not_configured_0001()

        if payload:
            request_payload = docusign_los_payload
        else:
            request_payload = json.loads(docusign_los_payload)

        # If consent is required, then a dict with consent url will be returned by the wrapper.
        if isinstance(self.access_token, dict):
            raise Exception(
                "Docusign Consent is required for the user: {error_text}".format(
                    error_text=self.access_token
                )
            )

        client_user_id = self.get_client_user_id(
            is_embedded_docusign=is_embedded_docusign
        )

        docusign_payload = self.prepare_payload(
            payload=request_payload,
            instance=instance,
            client_user_id=client_user_id,
            is_embedded_docusign=is_embedded_docusign,
            phase=phase,
            **kwargs,
        )

        return self._send_for_docusign(
            docusign_envelope_stage_data=docusign_envelope_stage_data,
            client_user_id=client_user_id,
            phase=phase,
            instance=instance,
            return_url=return_url,
            is_embedded_docusign=is_embedded_docusign,
            **docusign_payload,
        )

    def _check_for_existing_envelope(
        self,
        instance,
        return_url,
        phase,
        signer_email,
        signer_name,
        docusign_envelope_stage_data,
    ):
        latest_unsigned_embedded_envelope = DocusignEnvelopeStageData.objects.filter(
            object_pk=instance.pk if instance else None,
            envelope_status="sent",
            phase=phase,
            is_removed=False,
        ).first()
        if latest_unsigned_embedded_envelope:
            client_user_id = latest_unsigned_embedded_envelope.client_user_id
            envelope_id = latest_unsigned_embedded_envelope.envelope_id

            # WIP DocuSign from the application directly
            # TODO: move to process_embedded_docusign
            params = {
                "envelope_id": envelope_id,
                "authenticationMethod": "None",
                "email": signer_email,
                "userName": signer_name,
                "clientUserId": client_user_id,
                "access_token": "Bearer " + self.access_token,
                "returnUrl": return_url,
            }
            envelope_result = self.docusign_client.generate_docusign_preview_url(
                params, self.log_config
            )
            if self.use_signing_cache:
                cache.set(f"docusign_embedded_signing:{self.id}", True, 600)
            if envelope_result.status_code != 201:
                return self.process_docusign_error(
                    instance, docusign_envelope_stage_data, envelope_result
                )

            return envelope_result

    def _send_for_docusign(
        self,
        docusign_envelope_stage_data,
        client_user_id,
        request_payload,
        phase,
        instance,
        is_embedded_docusign,
        signer_email,
        signer_name,
        return_url,
        **kwargs
    ):
        """
        Handle common logic for sending data to docusign.  This should not be called directly by the application.
        """
        docusign_envelope_stage_data.client_user_id = client_user_id

        existing_envelope_result = self._check_for_existing_envelope(
            instance,
            return_url,
            phase,
            signer_email,
            signer_name,
            docusign_envelope_stage_data,
        )
        if existing_envelope_result:
            return existing_envelope_result

        envelope_result = self.docusign_client.create_envelope(
            request_payload, self.log_config
        )
        docusign_envelope_stage_data.envelope_response = envelope_result.text

        if envelope_result.status_code == 201:
            resp = json.loads(envelope_result.text)
            docusign_envelope_stage_data.record_status = "S"
            docusign_envelope_stage_data.envelope_id = resp["envelopeId"]
            docusign_envelope_stage_data.envelope_status = resp["status"]
            docusign_envelope_stage_data.phase = phase
            current_status = self._create_current_status(
                resp["envelopeId"],
                resp["status"],
                request_payload["recipients"]["signers"],
            )
            docusign_envelope_stage_data.current_status = current_status

            self._envelope_response_audit_log(
                instance, docusign_envelope_stage_data, current_status, resp
            )

            if is_embedded_docusign:
                params = {
                    "envelope_id": resp["envelopeId"],
                    "authenticationMethod": "None",
                    "email": signer_email,
                    "userName": signer_name,
                    "clientUserId": client_user_id,
                    "returnUrl": return_url,
                }
                envelope_result = self.docusign_client.generate_docusign_preview_url(
                    params, self.log_config
                )
                if envelope_result.status_code != 201:
                    return self.process_docusign_error(
                        instance, docusign_envelope_stage_data, envelope_result
                    )
                if self.use_signing_cache:
                    cache.set(f"docusign_embedded_signing:{instance.id}", True, 600)
        else:
            return self.process_docusign_error(
                instance, docusign_envelope_stage_data, envelope_result
            )

        # Since we are creating a new instance
        docusign_envelope_stage_data.save()  # nosemgrep
        return envelope_result

    def _envelope_response_audit_log(
        self, instance, docusign_envelope_stage_data, current_status, resp
    ):
        pass

    def initiate_docusign(
        self,
        return_url,
        phase,
        instance,
        payload=None,
        is_embedded_docusign=False,
        request=None,
        **kwargs,
    ):
        if cache.get("docusign_rate_reset", None):
            return self._error_high_volume_throttle_0003()

        try:
            response = self.send_for_docusign(
                payload=payload,
                phase=phase,
                instance=instance,
                is_embedded_docusign=is_embedded_docusign,
                return_url=return_url,
                request=request,
                **kwargs,
            )

            if response.status_code == http.HTTPStatus.CREATED:
                # check the rate limit remaining.
                # x_rate_limit = int(response.headers["X-RateLimit-Limit"])
                # ten_percent_of_rate_limit = x_rate_limit * 0.1

                x_rate_limit_remaining = int(response.headers["X-RateLimit-Remaining"])
                if x_rate_limit_remaining == 0:
                    reset_timestamp = int(response.headers["X-RateLimit-Reset"])
                    calculated_timeout = reset_timestamp - int(time.time())
                    cache.set(
                        "docusign_rate_reset",
                        reset_timestamp,
                        timeout=calculated_timeout,
                    )
                return response.json()["url"] if is_embedded_docusign else return_url
            elif response.status_code in [
                http.HTTPStatus.BAD_REQUEST,
                http.HTTPStatus.UNAUTHORIZED,
                http.HTTPStatus.NOT_FOUND,
                http.HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            ]:
                error_text = json.loads(response.text)
                error_code = error_text["errorCode"]
                if error_code == "HOURLY_APIINVOCATION_LIMIT_EXCEEDED":
                    if not cache.get("docusign_rate_reset", None):
                        reset_timestamp = int(response.headers["X-RateLimit-Reset"])
                        calculated_timeout = reset_timestamp - int(time.time())
                        cache.set(
                            "docusign_rate_reset",
                            reset_timestamp,
                            timeout=calculated_timeout,
                        )
                    return self._error_high_volume_throttle_0006()
                elif error_code == "BURST_APIINVOCATION_LIMIT_EXCEEDED":
                    if not cache.get("docusign_rate_reset", None):
                        # Setting the timeout to 30 seconds as for burst limit
                        reset_timestamp = int(response.headers["X-RateLimit-Reset"])
                        cache.set("docusign_rate_reset", reset_timestamp, timeout=30)

                    return self._error_high_volume_throttle_0005()
                else:
                    return self._error_docusigning_failed_0004()
        except Exception as excp:
            # TODO: Handle this with correct error code.
            return self._error_unknown_0007(instance, excp)
            raise
