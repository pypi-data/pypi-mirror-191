from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.card_card_three_d_secure_authentication_knowledge_base_status import (
    CardCardThreeDSecureAuthenticationKnowledgeBaseStatus,
)
from ..models.card_card_three_d_secure_authentication_otp_sms_status import (
    CardCardThreeDSecureAuthenticationOtpSmsStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CardCardThreeDSecureAuthentication")


@attr.s(auto_attribs=True)
class CardCardThreeDSecureAuthentication:
    """The 3DS authentication method statuses

    Attributes:
        knowledge_base_status (Union[Unset, CardCardThreeDSecureAuthenticationKnowledgeBaseStatus]): The knowledge based
            authentication (KBA) status Example: ENROLLED.
        otp_sms_status (Union[Unset, CardCardThreeDSecureAuthenticationOtpSmsStatus]): The SMS one time password
            authentication status Example: ENROLLED.
    """

    knowledge_base_status: Union[
        Unset, CardCardThreeDSecureAuthenticationKnowledgeBaseStatus
    ] = UNSET
    otp_sms_status: Union[Unset, CardCardThreeDSecureAuthenticationOtpSmsStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        knowledge_base_status: Union[Unset, str] = UNSET
        if not isinstance(self.knowledge_base_status, Unset):
            knowledge_base_status = self.knowledge_base_status.value

        otp_sms_status: Union[Unset, str] = UNSET
        if not isinstance(self.otp_sms_status, Unset):
            otp_sms_status = self.otp_sms_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if knowledge_base_status is not UNSET:
            field_dict["knowledgeBaseStatus"] = knowledge_base_status
        if otp_sms_status is not UNSET:
            field_dict["otpSmsStatus"] = otp_sms_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _knowledge_base_status = d.pop("knowledgeBaseStatus", UNSET)
        knowledge_base_status: Union[Unset, CardCardThreeDSecureAuthenticationKnowledgeBaseStatus]
        if isinstance(_knowledge_base_status, Unset):
            knowledge_base_status = UNSET
        else:
            knowledge_base_status = CardCardThreeDSecureAuthenticationKnowledgeBaseStatus(
                _knowledge_base_status
            )

        _otp_sms_status = d.pop("otpSmsStatus", UNSET)
        otp_sms_status: Union[Unset, CardCardThreeDSecureAuthenticationOtpSmsStatus]
        if isinstance(_otp_sms_status, Unset):
            otp_sms_status = UNSET
        else:
            otp_sms_status = CardCardThreeDSecureAuthenticationOtpSmsStatus(_otp_sms_status)

        card_card_three_d_secure_authentication = cls(
            knowledge_base_status=knowledge_base_status,
            otp_sms_status=otp_sms_status,
        )

        card_card_three_d_secure_authentication.additional_properties = d
        return card_card_three_d_secure_authentication

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
