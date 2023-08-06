from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.directdebitoutbound_collection_reject_request_reject_code import (
    DirectdebitoutboundCollectionRejectRequestRejectCode,
)

T = TypeVar("T", bound="DirectdebitoutboundCollectionRejectRequest")


@attr.s(auto_attribs=True)
class DirectdebitoutboundCollectionRejectRequest:
    """Collection reject request

    Attributes:
        claim_b_id (str): Collection Claim Business ID Example: A123456B.
        reject_code (DirectdebitoutboundCollectionRejectRequestRejectCode):
    """

    claim_b_id: str
    reject_code: DirectdebitoutboundCollectionRejectRequestRejectCode
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        claim_b_id = self.claim_b_id
        reject_code = self.reject_code.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "claimBId": claim_b_id,
                "rejectCode": reject_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        claim_b_id = d.pop("claimBId")

        reject_code = DirectdebitoutboundCollectionRejectRequestRejectCode(d.pop("rejectCode"))

        directdebitoutbound_collection_reject_request = cls(
            claim_b_id=claim_b_id,
            reject_code=reject_code,
        )

        directdebitoutbound_collection_reject_request.additional_properties = d
        return directdebitoutbound_collection_reject_request

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
