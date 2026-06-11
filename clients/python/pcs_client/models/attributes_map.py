from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.bool_attribute import BoolAttribute
    from ..models.date_attribute import DateAttribute
    from ..models.date_time_attribute import DateTimeAttribute
    from ..models.decimal_attribute import DecimalAttribute
    from ..models.decimal_range_attribute import DecimalRangeAttribute
    from ..models.float_attribute import FloatAttribute
    from ..models.float_range_attribute import FloatRangeAttribute
    from ..models.integer_attribute import IntegerAttribute
    from ..models.integer_range_attribute import IntegerRangeAttribute
    from ..models.list_of_date_times_attribute import ListOfDateTimesAttribute
    from ..models.list_of_dates_attribute import ListOfDatesAttribute
    from ..models.list_of_decimals_attribute import ListOfDecimalsAttribute
    from ..models.list_of_floats_attribute import ListOfFloatsAttribute
    from ..models.list_of_integers_attribute import ListOfIntegersAttribute
    from ..models.list_of_object_ids_attribute import ListOfObjectIdsAttribute
    from ..models.list_of_strings_attribute import ListOfStringsAttribute
    from ..models.list_of_ur_ls_attribute import ListOfURLsAttribute
    from ..models.list_of_uui_ds_attribute import ListOfUUIDsAttribute
    from ..models.map_of_date_times_attribute import MapOfDateTimesAttribute
    from ..models.map_of_dates_attribute import MapOfDatesAttribute
    from ..models.map_of_decimals_attribute import MapOfDecimalsAttribute
    from ..models.map_of_floats_attribute import MapOfFloatsAttribute
    from ..models.map_of_integers_attribute import MapOfIntegersAttribute
    from ..models.map_of_object_ids_attribute import MapOfObjectIdsAttribute
    from ..models.map_of_strings_attribute import MapOfStringsAttribute
    from ..models.map_of_ur_ls_attribute import MapOfURLsAttribute
    from ..models.map_of_uui_ds_attribute import MapOfUUIDsAttribute
    from ..models.object_id_attribute import ObjectIdAttribute
    from ..models.string_attribute import StringAttribute
    from ..models.text_attribute import TextAttribute
    from ..models.url_attribute import URLAttribute
    from ..models.uuid_attribute import UUIDAttribute


T = TypeVar("T", bound="AttributesMap")


@_attrs_define
class AttributesMap:
    """Map of attribute name to attribute"""

    additional_properties: dict[
        str,
        BoolAttribute
        | DateAttribute
        | DateTimeAttribute
        | DecimalAttribute
        | DecimalRangeAttribute
        | FloatAttribute
        | FloatRangeAttribute
        | IntegerAttribute
        | IntegerRangeAttribute
        | ListOfDatesAttribute
        | ListOfDateTimesAttribute
        | ListOfDecimalsAttribute
        | ListOfFloatsAttribute
        | ListOfIntegersAttribute
        | ListOfObjectIdsAttribute
        | ListOfStringsAttribute
        | ListOfURLsAttribute
        | ListOfUUIDsAttribute
        | MapOfDatesAttribute
        | MapOfDateTimesAttribute
        | MapOfDecimalsAttribute
        | MapOfFloatsAttribute
        | MapOfIntegersAttribute
        | MapOfObjectIdsAttribute
        | MapOfStringsAttribute
        | MapOfURLsAttribute
        | MapOfUUIDsAttribute
        | ObjectIdAttribute
        | StringAttribute
        | TextAttribute
        | URLAttribute
        | UUIDAttribute,
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.bool_attribute import BoolAttribute
        from ..models.date_attribute import DateAttribute
        from ..models.date_time_attribute import DateTimeAttribute
        from ..models.decimal_attribute import DecimalAttribute
        from ..models.decimal_range_attribute import DecimalRangeAttribute
        from ..models.float_attribute import FloatAttribute
        from ..models.float_range_attribute import FloatRangeAttribute
        from ..models.integer_attribute import IntegerAttribute
        from ..models.integer_range_attribute import IntegerRangeAttribute
        from ..models.list_of_date_times_attribute import ListOfDateTimesAttribute
        from ..models.list_of_dates_attribute import ListOfDatesAttribute
        from ..models.list_of_decimals_attribute import ListOfDecimalsAttribute
        from ..models.list_of_floats_attribute import ListOfFloatsAttribute
        from ..models.list_of_integers_attribute import ListOfIntegersAttribute
        from ..models.list_of_object_ids_attribute import ListOfObjectIdsAttribute
        from ..models.list_of_strings_attribute import ListOfStringsAttribute
        from ..models.list_of_ur_ls_attribute import ListOfURLsAttribute
        from ..models.list_of_uui_ds_attribute import ListOfUUIDsAttribute
        from ..models.map_of_dates_attribute import MapOfDatesAttribute
        from ..models.map_of_decimals_attribute import MapOfDecimalsAttribute
        from ..models.map_of_floats_attribute import MapOfFloatsAttribute
        from ..models.map_of_integers_attribute import MapOfIntegersAttribute
        from ..models.map_of_object_ids_attribute import MapOfObjectIdsAttribute
        from ..models.map_of_strings_attribute import MapOfStringsAttribute
        from ..models.map_of_ur_ls_attribute import MapOfURLsAttribute
        from ..models.map_of_uui_ds_attribute import MapOfUUIDsAttribute
        from ..models.object_id_attribute import ObjectIdAttribute
        from ..models.string_attribute import StringAttribute
        from ..models.text_attribute import TextAttribute
        from ..models.url_attribute import URLAttribute
        from ..models.uuid_attribute import UUIDAttribute

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, StringAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, TextAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, IntegerAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, BoolAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, FloatAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, DateAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, DateTimeAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, UUIDAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, ObjectIdAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, DecimalAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, URLAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, FloatRangeAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, IntegerRangeAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, DecimalRangeAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, ListOfStringsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, ListOfIntegersAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, ListOfFloatsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, ListOfDecimalsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, ListOfUUIDsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, ListOfObjectIdsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, ListOfURLsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, ListOfDatesAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, ListOfDateTimesAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MapOfStringsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MapOfIntegersAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MapOfFloatsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MapOfDecimalsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MapOfUUIDsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MapOfObjectIdsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MapOfURLsAttribute):
                field_dict[prop_name] = prop.to_dict()
            elif isinstance(prop, MapOfDatesAttribute):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bool_attribute import BoolAttribute
        from ..models.date_attribute import DateAttribute
        from ..models.date_time_attribute import DateTimeAttribute
        from ..models.decimal_attribute import DecimalAttribute
        from ..models.decimal_range_attribute import DecimalRangeAttribute
        from ..models.float_attribute import FloatAttribute
        from ..models.float_range_attribute import FloatRangeAttribute
        from ..models.integer_attribute import IntegerAttribute
        from ..models.integer_range_attribute import IntegerRangeAttribute
        from ..models.list_of_date_times_attribute import ListOfDateTimesAttribute
        from ..models.list_of_dates_attribute import ListOfDatesAttribute
        from ..models.list_of_decimals_attribute import ListOfDecimalsAttribute
        from ..models.list_of_floats_attribute import ListOfFloatsAttribute
        from ..models.list_of_integers_attribute import ListOfIntegersAttribute
        from ..models.list_of_object_ids_attribute import ListOfObjectIdsAttribute
        from ..models.list_of_strings_attribute import ListOfStringsAttribute
        from ..models.list_of_ur_ls_attribute import ListOfURLsAttribute
        from ..models.list_of_uui_ds_attribute import ListOfUUIDsAttribute
        from ..models.map_of_date_times_attribute import MapOfDateTimesAttribute
        from ..models.map_of_dates_attribute import MapOfDatesAttribute
        from ..models.map_of_decimals_attribute import MapOfDecimalsAttribute
        from ..models.map_of_floats_attribute import MapOfFloatsAttribute
        from ..models.map_of_integers_attribute import MapOfIntegersAttribute
        from ..models.map_of_object_ids_attribute import MapOfObjectIdsAttribute
        from ..models.map_of_strings_attribute import MapOfStringsAttribute
        from ..models.map_of_ur_ls_attribute import MapOfURLsAttribute
        from ..models.map_of_uui_ds_attribute import MapOfUUIDsAttribute
        from ..models.object_id_attribute import ObjectIdAttribute
        from ..models.string_attribute import StringAttribute
        from ..models.text_attribute import TextAttribute
        from ..models.url_attribute import URLAttribute
        from ..models.uuid_attribute import UUIDAttribute

        d = dict(src_dict)
        attributes_map = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> (
                BoolAttribute
                | DateAttribute
                | DateTimeAttribute
                | DecimalAttribute
                | DecimalRangeAttribute
                | FloatAttribute
                | FloatRangeAttribute
                | IntegerAttribute
                | IntegerRangeAttribute
                | ListOfDatesAttribute
                | ListOfDateTimesAttribute
                | ListOfDecimalsAttribute
                | ListOfFloatsAttribute
                | ListOfIntegersAttribute
                | ListOfObjectIdsAttribute
                | ListOfStringsAttribute
                | ListOfURLsAttribute
                | ListOfUUIDsAttribute
                | MapOfDatesAttribute
                | MapOfDateTimesAttribute
                | MapOfDecimalsAttribute
                | MapOfFloatsAttribute
                | MapOfIntegersAttribute
                | MapOfObjectIdsAttribute
                | MapOfStringsAttribute
                | MapOfURLsAttribute
                | MapOfUUIDsAttribute
                | ObjectIdAttribute
                | StringAttribute
                | TextAttribute
                | URLAttribute
                | UUIDAttribute
            ):
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_0 = StringAttribute.from_dict(data)

                    return componentsschemas_attribute_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_1 = TextAttribute.from_dict(data)

                    return componentsschemas_attribute_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_2 = IntegerAttribute.from_dict(data)

                    return componentsschemas_attribute_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_3 = BoolAttribute.from_dict(data)

                    return componentsschemas_attribute_type_3
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_4 = FloatAttribute.from_dict(data)

                    return componentsschemas_attribute_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_5 = DateAttribute.from_dict(data)

                    return componentsschemas_attribute_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_6 = DateTimeAttribute.from_dict(data)

                    return componentsschemas_attribute_type_6
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_7 = UUIDAttribute.from_dict(data)

                    return componentsschemas_attribute_type_7
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_8 = ObjectIdAttribute.from_dict(data)

                    return componentsschemas_attribute_type_8
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_9 = DecimalAttribute.from_dict(data)

                    return componentsschemas_attribute_type_9
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_10 = URLAttribute.from_dict(data)

                    return componentsschemas_attribute_type_10
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_11 = FloatRangeAttribute.from_dict(data)

                    return componentsschemas_attribute_type_11
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_12 = IntegerRangeAttribute.from_dict(data)

                    return componentsschemas_attribute_type_12
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_13 = DecimalRangeAttribute.from_dict(data)

                    return componentsschemas_attribute_type_13
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_14 = ListOfStringsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_14
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_15 = ListOfIntegersAttribute.from_dict(data)

                    return componentsschemas_attribute_type_15
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_16 = ListOfFloatsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_16
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_17 = ListOfDecimalsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_17
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_18 = ListOfUUIDsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_18
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_19 = ListOfObjectIdsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_19
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_20 = ListOfURLsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_20
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_21 = ListOfDatesAttribute.from_dict(data)

                    return componentsschemas_attribute_type_21
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_22 = ListOfDateTimesAttribute.from_dict(data)

                    return componentsschemas_attribute_type_22
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_23 = MapOfStringsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_23
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_24 = MapOfIntegersAttribute.from_dict(data)

                    return componentsschemas_attribute_type_24
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_25 = MapOfFloatsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_25
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_26 = MapOfDecimalsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_26
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_27 = MapOfUUIDsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_27
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_28 = MapOfObjectIdsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_28
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_29 = MapOfURLsAttribute.from_dict(data)

                    return componentsschemas_attribute_type_29
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_attribute_type_30 = MapOfDatesAttribute.from_dict(data)

                    return componentsschemas_attribute_type_30
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_attribute_type_31 = MapOfDateTimesAttribute.from_dict(data)

                return componentsschemas_attribute_type_31

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        attributes_map.additional_properties = additional_properties
        return attributes_map

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> (
        BoolAttribute
        | DateAttribute
        | DateTimeAttribute
        | DecimalAttribute
        | DecimalRangeAttribute
        | FloatAttribute
        | FloatRangeAttribute
        | IntegerAttribute
        | IntegerRangeAttribute
        | ListOfDatesAttribute
        | ListOfDateTimesAttribute
        | ListOfDecimalsAttribute
        | ListOfFloatsAttribute
        | ListOfIntegersAttribute
        | ListOfObjectIdsAttribute
        | ListOfStringsAttribute
        | ListOfURLsAttribute
        | ListOfUUIDsAttribute
        | MapOfDatesAttribute
        | MapOfDateTimesAttribute
        | MapOfDecimalsAttribute
        | MapOfFloatsAttribute
        | MapOfIntegersAttribute
        | MapOfObjectIdsAttribute
        | MapOfStringsAttribute
        | MapOfURLsAttribute
        | MapOfUUIDsAttribute
        | ObjectIdAttribute
        | StringAttribute
        | TextAttribute
        | URLAttribute
        | UUIDAttribute
    ):
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: BoolAttribute
        | DateAttribute
        | DateTimeAttribute
        | DecimalAttribute
        | DecimalRangeAttribute
        | FloatAttribute
        | FloatRangeAttribute
        | IntegerAttribute
        | IntegerRangeAttribute
        | ListOfDatesAttribute
        | ListOfDateTimesAttribute
        | ListOfDecimalsAttribute
        | ListOfFloatsAttribute
        | ListOfIntegersAttribute
        | ListOfObjectIdsAttribute
        | ListOfStringsAttribute
        | ListOfURLsAttribute
        | ListOfUUIDsAttribute
        | MapOfDatesAttribute
        | MapOfDateTimesAttribute
        | MapOfDecimalsAttribute
        | MapOfFloatsAttribute
        | MapOfIntegersAttribute
        | MapOfObjectIdsAttribute
        | MapOfStringsAttribute
        | MapOfURLsAttribute
        | MapOfUUIDsAttribute
        | ObjectIdAttribute
        | StringAttribute
        | TextAttribute
        | URLAttribute
        | UUIDAttribute,
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
