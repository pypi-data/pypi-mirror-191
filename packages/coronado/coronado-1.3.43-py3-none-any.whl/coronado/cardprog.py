from coronado import TripleObject
from coronado.baseobjects import BASE_CARD_PROGRAM_DICT

import json
import uuid


# *** constants ***

SERVICE_PATH = 'partner/card-programs'
"""
The default service path associated with CardProgram operations.

Usage:

```
CardProgram.initialize(serviceURL, SERVICE_PATH, auth)
```

Users are welcome to initialize the class' service path from regular strings.
This constant is defined for convenience.
"""


# ***

class CardProgram(TripleObject):
    """
    Card programs are logical groupings of card accounts.  A card program is
    often a specific type of card offering by a CardProgram, like a payment card
    associated with its own rewards like miles or cash back.  Card programs may
    also be used for organizing card accounts in arbirtrary groupings.

    Card accounts may not move between card programs, and cannot be represented
    in more than one card program at a time.
    """

    requiredAttributes = [
        'defaultPostalCode',
        'externalID',
        'name',
        'programCurrency',
    ]
    allAttributes = TripleObject(BASE_CARD_PROGRAM_DICT).listAttributes()


    def __init__(self, obj = BASE_CARD_PROGRAM_DICT):
        """
        Create a new instance of a card program.  `obj` must correspond to a
        valid, existing object ID if it's not a collection or JSON.

        Arguments
        ---------
            obj
        An object used for building a valid card program.  The object can
        be one of:

        - A dictionary - a dictionary with instantiation values as described
          in the API documentation
        - A JSON string
        - A Triple objectID

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        TripleObject.__init__(self, obj)


    @classmethod
    def list(klass: object, paramMap = None, **args) -> list:
        """
        Return a list of card programs.

        Arguments
        ---------
            extPublisherID
        An external publisher ID; optional

            extCardProgramID
        An external card program ID; optional

        Returns
        -------
            list
        A list of CardProgram objects

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        paramMap = {
            'extCardProgramID': 'card_program_external_id',
            'extPublisherID': 'publisher_external_id',
        }

        response = super().list(paramMap, **args)
        result = [ CardProgram(obj) for obj in json.loads(response.content)['card_programs'] ]

        return result


    @classmethod
    def create(klass,
        extCardProgramID: str,
        defaultPostalCode: str,
        name: str,
        programCurrency: str = 'USD',
        cardBINs: list = [ ],
        defaultCountryCode: str = 'NA',
        extPublisherID: str = None,
        loyaltyUnit: str = None,
        loyaltyConversionRate: str = None) -> object:
        """
        Creates a card program.

        For full details see `coronado.TripleObject.create()`.

        Arguments
        ---------
            extCardProgramID
        Partner provided external card program ID.

        External IDs are assumed to be stable and never **sensitive**.  External
        IDs need not be unique across publishers, but we encourage the use of
        UUIDs whenever possible.

        External publisher IDs may not match the nnn-nn-nnnn format of US tax
        IDs to prevent accidental inclusion of sensitive information.

            defaultPostalCode
        The postal code for the associated program.

            name
        The card program's display name.

            programCurrency
        3-character ISO-4217 currency code.  At this time only USD is supported.
        Contact Triple for support of additional currencies.  Test and fun codes
        are not supported and will raise an exception.

            cardBINs
        A list of bank identification numbers for the cards in this program.
        These values help validate transactions during reward processing and
        enforce card requirements during purchases through affiliate offers.

            defaultCountryCode
        2-letter ISO-3166 country code.  Defaults to `US`.

            extPublisherID
        Partner-provided external publisher ID, if available.

        Returns
        -------
        An instance of `CardProgram`.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        spec = {
            'card_bins': cardBINs,
            'default_country_code': defaultCountryCode,
            'default_postal_code': defaultPostalCode,
            'external_id': extCardProgramID,
            'loyalty_unit': loyaltyUnit,
            'loyalty_conversion_rate': loyaltyConversionRate,
            'name': name,
            'program_currency': programCurrency,
            'publisher_external_id': extPublisherID,
        }
        return CardProgram(super().create(spec))


    def asSnakeCaseDictionary(self):
        """
        Return a dict representation of the receiver with the attributes
        written in snake_case format.

        Return
        ------
            dict
        A dict representation of the receiver.
        """
        result = {
            'card_bins': self.cardBINs,
            'default_country_code': self.defaultCountryCode,
            'default_postal_code': self.defaultPostalCode,
            'external_id': self.externalID,
            'name': self.name,
            'program_currency': self.programCurrency,
        }
        return result


# +++ support and testing functions ***

def generateMockCardProgram(publisherExternalID):
    """
    Generates a card program on spec, used for unit testing.

    Arguments
    ---------
        publisherExternalID
    A string with a valid publisher external ID.

    Returns
    -------
    An instance of `coronado.cardprogram.CardProgram`.
    """
    spec = {
        'card_bins': [ '425907', '511642', '486010', ],
        'default_country_code': 'US',
        'default_postal_code': '94123',
        'external_id': 'prog-%s' % uuid.uuid4().hex,
        'name': 'Mojito Rewards %s' % uuid.uuid4().hex,
        'program_currency': 'USD',
        'publisher_external_id': publisherExternalID,
    }

    return CardProgram.create(
            extCardProgramID = spec['external_id'],
            defaultPostalCode = spec['default_postal_code'],
            name = spec['name'],
            programCurrency = spec['program_currency'],
            cardBINs = spec['card_bins'],
            defaultCountryCode = spec['default_country_code'],
            extPublisherID = spec['publisher_external_id']
    )

