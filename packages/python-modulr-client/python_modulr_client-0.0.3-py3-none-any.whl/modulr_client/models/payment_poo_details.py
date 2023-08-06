from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_charge import PaymentCharge
    from ..models.payment_payment_details import PaymentPaymentDetails
    from ..models.payment_ultimate_payer import PaymentUltimatePayer


T = TypeVar("T", bound="PaymentPOODetails")


@attr.s(auto_attribs=True)
class PaymentPOODetails:
    """Details relating to payment originated overseas

    Attributes:
        additional_remittance_information (Union[Unset, str]):
        charge_details (Union[Unset, PaymentCharge]):
        original_payment_details (Union[Unset, PaymentPaymentDetails]):
        ultimate_payer (Union[Unset, PaymentUltimatePayer]):
    """

    additional_remittance_information: Union[Unset, str] = UNSET
    charge_details: Union[Unset, "PaymentCharge"] = UNSET
    original_payment_details: Union[Unset, "PaymentPaymentDetails"] = UNSET
    ultimate_payer: Union[Unset, "PaymentUltimatePayer"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        additional_remittance_information = self.additional_remittance_information
        charge_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.charge_details, Unset):
            charge_details = self.charge_details.to_dict()

        original_payment_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.original_payment_details, Unset):
            original_payment_details = self.original_payment_details.to_dict()

        ultimate_payer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ultimate_payer, Unset):
            ultimate_payer = self.ultimate_payer.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if additional_remittance_information is not UNSET:
            field_dict["additionalRemittanceInformation"] = additional_remittance_information
        if charge_details is not UNSET:
            field_dict["chargeDetails"] = charge_details
        if original_payment_details is not UNSET:
            field_dict["originalPaymentDetails"] = original_payment_details
        if ultimate_payer is not UNSET:
            field_dict["ultimatePayer"] = ultimate_payer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.payment_charge import PaymentCharge
        from ..models.payment_payment_details import PaymentPaymentDetails
        from ..models.payment_ultimate_payer import PaymentUltimatePayer

        d = src_dict.copy()
        additional_remittance_information = d.pop("additionalRemittanceInformation", UNSET)

        _charge_details = d.pop("chargeDetails", UNSET)
        charge_details: Union[Unset, PaymentCharge]
        if isinstance(_charge_details, Unset):
            charge_details = UNSET
        else:
            charge_details = PaymentCharge.from_dict(_charge_details)

        _original_payment_details = d.pop("originalPaymentDetails", UNSET)
        original_payment_details: Union[Unset, PaymentPaymentDetails]
        if isinstance(_original_payment_details, Unset):
            original_payment_details = UNSET
        else:
            original_payment_details = PaymentPaymentDetails.from_dict(_original_payment_details)

        _ultimate_payer = d.pop("ultimatePayer", UNSET)
        ultimate_payer: Union[Unset, PaymentUltimatePayer]
        if isinstance(_ultimate_payer, Unset):
            ultimate_payer = UNSET
        else:
            ultimate_payer = PaymentUltimatePayer.from_dict(_ultimate_payer)

        payment_poo_details = cls(
            additional_remittance_information=additional_remittance_information,
            charge_details=charge_details,
            original_payment_details=original_payment_details,
            ultimate_payer=ultimate_payer,
        )

        payment_poo_details.additional_properties = d
        return payment_poo_details

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
