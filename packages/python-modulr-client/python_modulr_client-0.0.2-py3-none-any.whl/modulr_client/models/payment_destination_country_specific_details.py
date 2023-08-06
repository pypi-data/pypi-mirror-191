from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.payment_destination_country_specific_details_bank_code_type import (
    PaymentDestinationCountrySpecificDetailsBankCodeType,
)
from ..models.payment_destination_country_specific_details_bank_country import (
    PaymentDestinationCountrySpecificDetailsBankCountry,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentDestinationCountrySpecificDetails")


@attr.s(auto_attribs=True)
class PaymentDestinationCountrySpecificDetails:
    """Further details required, depending on the destination's country

    Attributes:
        bank_address (Union[Unset, str]): The address of the destination bank. Example: 2100 Broadway.
        bank_branch_code (Union[Unset, str]): The code of the destination bank's branch. Example: 44-04.
        bank_branch_name (Union[Unset, str]): The name of the destination bank's branch. Example: New York.
        bank_city (Union[Unset, str]): The city in which the destination bank resides. Example: New York City.
        bank_code (Union[Unset, str]): The code identifying the target bank on its respective national network. This is
            not the BIC/SWIFT code. This is known as the 'ABA code' in the U.S., 'ISFC' in India, 'routing number' in
            Canada, and so on.
        bank_code_type (Union[Unset, PaymentDestinationCountrySpecificDetailsBankCodeType]): The code type identifying
            the target bank on its respective national network.
            This is known as the 'ABA code' in the U.S., 'ISFC' in India, 'routing number' in Canada, and so on. Example:
            ABA.
        bank_country (Union[Unset, PaymentDestinationCountrySpecificDetailsBankCountry]): The country in which the
            destination bank resides. Example: US.
        bank_name (Union[Unset, str]): The name of the destination bank. Example: Apple Bank.
        business (Union[Unset, bool]): The type of the beneficiary. 'true' for businesses, 'false' otherwise. Example:
            True.
        chinese_id (Union[Unset, str]): The 18 digit identification code of the beneficiary. Applies to Chinese
            beneficiaries only. Example: 01101201901018889.
        province (Union[Unset, str]): The province in which the beneficiary resides. Applies only to beneficiaries
            residing in China. Example: Zhejiang.
    """

    bank_address: Union[Unset, str] = UNSET
    bank_branch_code: Union[Unset, str] = UNSET
    bank_branch_name: Union[Unset, str] = UNSET
    bank_city: Union[Unset, str] = UNSET
    bank_code: Union[Unset, str] = UNSET
    bank_code_type: Union[Unset, PaymentDestinationCountrySpecificDetailsBankCodeType] = UNSET
    bank_country: Union[Unset, PaymentDestinationCountrySpecificDetailsBankCountry] = UNSET
    bank_name: Union[Unset, str] = UNSET
    business: Union[Unset, bool] = UNSET
    chinese_id: Union[Unset, str] = UNSET
    province: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bank_address = self.bank_address
        bank_branch_code = self.bank_branch_code
        bank_branch_name = self.bank_branch_name
        bank_city = self.bank_city
        bank_code = self.bank_code
        bank_code_type: Union[Unset, str] = UNSET
        if not isinstance(self.bank_code_type, Unset):
            bank_code_type = self.bank_code_type.value

        bank_country: Union[Unset, str] = UNSET
        if not isinstance(self.bank_country, Unset):
            bank_country = self.bank_country.value

        bank_name = self.bank_name
        business = self.business
        chinese_id = self.chinese_id
        province = self.province

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bank_address is not UNSET:
            field_dict["bankAddress"] = bank_address
        if bank_branch_code is not UNSET:
            field_dict["bankBranchCode"] = bank_branch_code
        if bank_branch_name is not UNSET:
            field_dict["bankBranchName"] = bank_branch_name
        if bank_city is not UNSET:
            field_dict["bankCity"] = bank_city
        if bank_code is not UNSET:
            field_dict["bankCode"] = bank_code
        if bank_code_type is not UNSET:
            field_dict["bankCodeType"] = bank_code_type
        if bank_country is not UNSET:
            field_dict["bankCountry"] = bank_country
        if bank_name is not UNSET:
            field_dict["bankName"] = bank_name
        if business is not UNSET:
            field_dict["business"] = business
        if chinese_id is not UNSET:
            field_dict["chineseId"] = chinese_id
        if province is not UNSET:
            field_dict["province"] = province

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bank_address = d.pop("bankAddress", UNSET)

        bank_branch_code = d.pop("bankBranchCode", UNSET)

        bank_branch_name = d.pop("bankBranchName", UNSET)

        bank_city = d.pop("bankCity", UNSET)

        bank_code = d.pop("bankCode", UNSET)

        _bank_code_type = d.pop("bankCodeType", UNSET)
        bank_code_type: Union[Unset, PaymentDestinationCountrySpecificDetailsBankCodeType]
        if isinstance(_bank_code_type, Unset):
            bank_code_type = UNSET
        else:
            bank_code_type = PaymentDestinationCountrySpecificDetailsBankCodeType(_bank_code_type)

        _bank_country = d.pop("bankCountry", UNSET)
        bank_country: Union[Unset, PaymentDestinationCountrySpecificDetailsBankCountry]
        if isinstance(_bank_country, Unset):
            bank_country = UNSET
        else:
            bank_country = PaymentDestinationCountrySpecificDetailsBankCountry(_bank_country)

        bank_name = d.pop("bankName", UNSET)

        business = d.pop("business", UNSET)

        chinese_id = d.pop("chineseId", UNSET)

        province = d.pop("province", UNSET)

        payment_destination_country_specific_details = cls(
            bank_address=bank_address,
            bank_branch_code=bank_branch_code,
            bank_branch_name=bank_branch_name,
            bank_city=bank_city,
            bank_code=bank_code,
            bank_code_type=bank_code_type,
            bank_country=bank_country,
            bank_name=bank_name,
            business=business,
            chinese_id=chinese_id,
            province=province,
        )

        payment_destination_country_specific_details.additional_properties = d
        return payment_destination_country_specific_details

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
