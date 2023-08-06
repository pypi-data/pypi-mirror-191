"""
An order is a confirmation of a transaction (a receipt), which can contain multiple line items, each represented by an Offer that has been accepted by the customer.

https://schema.org/Order
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class Order(BaseModel):
    """An order is a confirmation of a transaction (a receipt), which can contain multiple line items, each represented by an Offer that has been accepted by the customer.

    References:
        https://schema.org/Order
    Note:
        Model Depth 3
    Attributes:
        potentialAction: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates a potential Action, which describes an idealized action in which this thing would play an 'object' role.
        mainEntityOfPage: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): Indicates a page (or other CreativeWork) for which this thing is the main entity being described. See [background notes](/docs/datamodel.html#mainEntityBackground) for details.
        subjectOf: (Optional[Union[List[Union[str, Any]], str, Any]]): A CreativeWork or Event about this Thing.
        url: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): URL of the item.
        alternateName: (Union[List[Union[str, Any]], str, Any]): An alias for the item.
        sameAs: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): URL of a reference Web page that unambiguously indicates the item's identity. E.g. the URL of the item's Wikipedia page, Wikidata entry, or official website.
        description: (Union[List[Union[str, Any]], str, Any]): A description of the item.
        disambiguatingDescription: (Union[List[Union[str, Any]], str, Any]): A sub property of description. A short description of the item used to disambiguate from other, similar items. Information from other properties (in particular, name) may be necessary for the description to be useful for disambiguation.
        identifier: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): The identifier property represents any kind of identifier for any kind of [[Thing]], such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links. See [background notes](/docs/datamodel.html#identifierBg) for more details.
        image: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): An image of the item. This can be a [[URL]] or a fully described [[ImageObject]].
        name: (Union[List[Union[str, Any]], str, Any]): The name of the item.
        additionalType: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): An additional type for the item, typically used for adding more specific types from external vocabularies in microdata syntax. This is a relationship between something and a class that the thing is in. In RDFa syntax, it is better to use the native RDFa syntax - the 'typeof' attribute - for multiple types. Schema.org tools may have only weaker understanding of extra types, in particular those defined externally.
        orderStatus: (Optional[Union[List[Union[str, Any]], str, Any]]): The current status of the order.
        isGift: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): Indicates whether the offer was accepted as a gift for someone other than the buyer.
        confirmationNumber: (Union[List[Union[str, Any]], str, Any]): A number that confirms the given order or payment has been received.
        broker: (Optional[Union[List[Union[str, Any]], str, Any]]): An entity that arranges for an exchange between a buyer and a seller.  In most cases a broker never acquires or releases ownership of a product or service involved in an exchange.  If it is not clear whether an entity is a broker, seller, or buyer, the latter two terms are preferred.
        paymentDueDate: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): The date that payment is due.
        seller: (Optional[Union[List[Union[str, Any]], str, Any]]): An entity which offers (sells / leases / lends / loans) the services / goods.  A seller may also be a provider.
        discount: (Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]): Any discount applied (to an Order).
        discountCurrency: (Union[List[Union[str, Any]], str, Any]): The currency of the discount.Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system) (LETS) and other currency types, e.g. "Ithaca HOUR".
        customer: (Optional[Union[List[Union[str, Any]], str, Any]]): Party placing the order or paying the invoice.
        paymentDue: (Optional[Union[List[Union[datetime, str, Any]], datetime, str, Any]]): The date that payment is due.
        acceptedOffer: (Optional[Union[List[Union[str, Any]], str, Any]]): The offer(s) -- e.g., product, quantity and price combinations -- included in the order.
        paymentMethodId: (Union[List[Union[str, Any]], str, Any]): An identifier for the method of payment used (e.g. the last 4 digits of the credit card).
        merchant: (Optional[Union[List[Union[str, Any]], str, Any]]): 'merchant' is an out-dated term for 'seller'.
        partOfInvoice: (Optional[Union[List[Union[str, Any]], str, Any]]): The order is being paid as part of the referenced Invoice.
        orderNumber: (Union[List[Union[str, Any]], str, Any]): The identifier of the transaction.
        paymentMethod: (Optional[Union[List[Union[str, Any]], str, Any]]): The name of the credit card or other method of payment for the order.
        discountCode: (Union[List[Union[str, Any]], str, Any]): Code used to redeem a discount.
        orderDelivery: (Optional[Union[List[Union[str, Any]], str, Any]]): The delivery of the parcel related to this order or order item.
        orderedItem: (Optional[Union[List[Union[str, Any]], str, Any]]): The item ordered.
        billingAddress: (Optional[Union[List[Union[str, Any]], str, Any]]): The billing address for the order.
        paymentUrl: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): The URL for sending a payment.
        orderDate: (Optional[Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]]): Date order was placed.

    """

    type_: str = Field(default="Order", alias="@type", const=True)
    potentialAction: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates a potential Action, which describes an idealized action in which this thing"
        "would play an 'object' role.",
    )
    mainEntityOfPage: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="Indicates a page (or other CreativeWork) for which this thing is the main entity being"
        "described. See [background notes](/docs/datamodel.html#mainEntityBackground)"
        "for details.",
    )
    subjectOf: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A CreativeWork or Event about this Thing.",
    )
    url: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="URL of the item.",
    )
    alternateName: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An alias for the item.",
    )
    sameAs: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="URL of a reference Web page that unambiguously indicates the item's identity. E.g. the"
        "URL of the item's Wikipedia page, Wikidata entry, or official website.",
    )
    description: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A description of the item.",
    )
    disambiguatingDescription: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A sub property of description. A short description of the item used to disambiguate from"
        "other, similar items. Information from other properties (in particular, name) may"
        "be necessary for the description to be useful for disambiguation.",
    )
    identifier: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="The identifier property represents any kind of identifier for any kind of [[Thing]],"
        "such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for"
        "representing many of these, either as textual strings or as URL (URI) links. See [background"
        "notes](/docs/datamodel.html#identifierBg) for more details.",
    )
    image: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="An image of the item. This can be a [[URL]] or a fully described [[ImageObject]].",
    )
    name: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The name of the item.",
    )
    additionalType: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="An additional type for the item, typically used for adding more specific types from external"
        "vocabularies in microdata syntax. This is a relationship between something and a class"
        "that the thing is in. In RDFa syntax, it is better to use the native RDFa syntax - the 'typeof'"
        "attribute - for multiple types. Schema.org tools may have only weaker understanding"
        "of extra types, in particular those defined externally.",
    )
    orderStatus: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The current status of the order.",
    )
    isGift: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="Indicates whether the offer was accepted as a gift for someone other than the buyer.",
    )
    confirmationNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A number that confirms the given order or payment has been received.",
    )
    broker: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An entity that arranges for an exchange between a buyer and a seller. In most cases a broker"
        "never acquires or releases ownership of a product or service involved in an exchange."
        "If it is not clear whether an entity is a broker, seller, or buyer, the latter two terms"
        "are preferred.",
    )
    paymentDueDate: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="The date that payment is due.",
    )
    seller: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An entity which offers (sells / leases / lends / loans) the services / goods. A seller may"
        "also be a provider.",
    )
    discount: Union[
        List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat
    ] = Field(
        default=None,
        description="Any discount applied (to an Order).",
    )
    discountCurrency: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The currency of the discount.Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217),"
        'e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies)'
        'for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)'
        '(LETS) and other currency types, e.g. "Ithaca HOUR".',
    )
    customer: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Party placing the order or paying the invoice.",
    )
    paymentDue: Optional[
        Union[List[Union[datetime, str, Any]], datetime, str, Any]
    ] = Field(
        default=None,
        description="The date that payment is due.",
    )
    acceptedOffer: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The offer(s) -- e.g., product, quantity and price combinations -- included in the order.",
    )
    paymentMethodId: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An identifier for the method of payment used (e.g. the last 4 digits of the credit card).",
    )
    merchant: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="'merchant' is an out-dated term for 'seller'.",
    )
    partOfInvoice: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The order is being paid as part of the referenced Invoice.",
    )
    orderNumber: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The identifier of the transaction.",
    )
    paymentMethod: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The name of the credit card or other method of payment for the order.",
    )
    discountCode: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Code used to redeem a discount.",
    )
    orderDelivery: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The delivery of the parcel related to this order or order item.",
    )
    orderedItem: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The item ordered.",
    )
    billingAddress: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The billing address for the order.",
    )
    paymentUrl: Optional[
        Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]
    ] = Field(
        default=None,
        description="The URL for sending a payment.",
    )
    orderDate: Optional[
        Union[List[Union[datetime, str, Any, date]], datetime, str, Any, date]
    ] = Field(
        default=None,
        description="Date order was placed.",
    )
