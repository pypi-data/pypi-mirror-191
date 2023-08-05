from coronado.address import Address
from coronado.exceptions import InvalidPayloadError


# --- classes and objects ---

class StrictAddress(Address):
    """
    A subclass of the Address class that requires valid streetAddress,
    postalCode, and countryCode.

    Return
    ------
    `None`

    Raises
    ------
        InvalidPayloadError
    StrictAddress objects **must** these propoerties set and conform to these
    rules:

    - `countryCode` must be a 2-letter ISO-3166 country code
    - `postalCode` must be 1 to 15 characters long, alphanumeric
    - `1 < len(streetAddress) < 500`, free form
    """

    def validate(self) -> None:
        if len(self.postalCode) < 1 or len(self.postalCode) > 15:
            raise InvalidPayloadError('Valid postalCode of 1-15 characters is required.')

        if len(self.countryCode) != 2 or not self.countryCode.isalpha():
            raise InvalidPayloadError('CountryCode must adhere to 2-letter ISO-3166 country code format.')

        if len(self.streetAddress) < 2 or len(self.streetAddress) > 500:
            raise InvalidPayloadError('Valid streetAddress of 2-500 characters is required.')

