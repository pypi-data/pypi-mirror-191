"""
A card payment method of a particular brand or name.  Used to mark up a particular payment method and/or the financial product/service that supplies the card account.Commonly used values:* http://purl.org/goodrelations/v1#AmericanExpress* http://purl.org/goodrelations/v1#DinersClub* http://purl.org/goodrelations/v1#Discover* http://purl.org/goodrelations/v1#JCB* http://purl.org/goodrelations/v1#MasterCard* http://purl.org/goodrelations/v1#VISA       

https://schema.org/CreditCard
"""

from __future__ import annotations

from datetime import *
from time import *
from typing import *

from pydantic import *


class CreditCard(BaseModel):
    """A card payment method of a particular brand or name.  Used to mark up a particular payment method and/or the financial product/service that supplies the card account.Commonly used values:* http://purl.org/goodrelations/v1#AmericanExpress* http://purl.org/goodrelations/v1#DinersClub* http://purl.org/goodrelations/v1#Discover* http://purl.org/goodrelations/v1#JCB* http://purl.org/goodrelations/v1#MasterCard* http://purl.org/goodrelations/v1#VISA

    References:
        https://schema.org/CreditCard
    Note:
        Model Depth 6
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
        serviceArea: (Optional[Union[List[Union[str, Any]], str, Any]]): The geographic area where the service is provided.
        broker: (Optional[Union[List[Union[str, Any]], str, Any]]): An entity that arranges for an exchange between a buyer and a seller.  In most cases a broker never acquires or releases ownership of a product or service involved in an exchange.  If it is not clear whether an entity is a broker, seller, or buyer, the latter two terms are preferred.
        provider: (Optional[Union[List[Union[str, Any]], str, Any]]): The service provider, service operator, or service performer; the goods producer. Another party (a seller) may offer those services or goods on behalf of the provider. A provider may also serve as the seller.
        areaServed: (Union[List[Union[str, Any]], str, Any]): The geographic area where a service or offered item is provided.
        slogan: (Union[List[Union[str, Any]], str, Any]): A slogan or motto associated with the item.
        award: (Union[List[Union[str, Any]], str, Any]): An award won by or for this item.
        termsOfService: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Human-readable terms of service documentation.
        review: (Optional[Union[List[Union[str, Any]], str, Any]]): A review of the item.
        availableChannel: (Optional[Union[List[Union[str, Any]], str, Any]]): A means of accessing the service (e.g. a phone bank, a web site, a location, etc.).
        isRelatedTo: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to another, somehow related product (or multiple products).
        serviceAudience: (Optional[Union[List[Union[str, Any]], str, Any]]): The audience eligible for this service.
        isSimilarTo: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to another, functionally similar product (or multiple products).
        audience: (Optional[Union[List[Union[str, Any]], str, Any]]): An intended audience, i.e. a group for whom something was created.
        logo: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): An associated logo.
        providerMobility: (Union[List[Union[str, Any]], str, Any]): Indicates the mobility of a provided service (e.g. 'static', 'dynamic').
        hoursAvailable: (Optional[Union[List[Union[str, Any]], str, Any]]): The hours during which this service or contact is available.
        brand: (Optional[Union[List[Union[str, Any]], str, Any]]): The brand(s) associated with a product or service, or the brand(s) maintained by an organization or business person.
        serviceOutput: (Optional[Union[List[Union[str, Any]], str, Any]]): The tangible thing generated by the service, e.g. a passport, permit, etc.
        produces: (Optional[Union[List[Union[str, Any]], str, Any]]): The tangible thing generated by the service, e.g. a passport, permit, etc.
        hasOfferCatalog: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates an OfferCatalog listing for this Organization, Person, or Service.
        category: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): A category for the item. Greater signs or slashes can be used to informally indicate a category hierarchy.
        aggregateRating: (Optional[Union[List[Union[str, Any]], str, Any]]): The overall rating, based on a collection of reviews or ratings, of the item.
        serviceType: (Union[List[Union[str, Any]], str, Any]): The type of service being offered, e.g. veterans' benefits, emergency relief, etc.
        offers: (Optional[Union[List[Union[str, Any]], str, Any]]): An offer to provide this item&#x2014;for example, an offer to sell a product, rent the DVD of a movie, perform a service, or give away tickets to an event. Use [[businessFunction]] to indicate the kind of transaction offered, i.e. sell, lease, etc. This property can also be used to describe a [[Demand]]. While this property is listed as expected on a number of common types, it can be used in others. In that case, using a second type, such as Product or a subtype of Product, can clarify the nature of the offer.
        annualPercentageRate: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The annual rate that is charged for borrowing (or made by investing), expressed as a single percentage number that represents the actual yearly cost of funds over the term of a loan. This includes any fees or additional costs associated with the transaction.
        interestRate: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The interest rate, charged or paid, applicable to the financial product. Note: This is different from the calculated annualPercentageRate.
        feesAndCommissionsSpecification: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Description of fees, commissions, and other terms applied either to a class of financial product, or by a financial service organization.
        requiredCollateral: (Union[List[Union[str, Any]], str, Any]): Assets required to secure loan or credit repayments. It may take form of third party pledge, goods, financial instruments (cash, securities, etc.)
        loanType: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): The type of a loan or credit.
        currency: (Union[List[Union[str, Any]], str, Any]): The currency in which the monetary amount is expressed.Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system) (LETS) and other currency types, e.g. "Ithaca HOUR".
        renegotiableLoan: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): Whether the terms for payment of interest can be renegotiated during the life of the loan.
        gracePeriod: (Optional[Union[List[Union[str, Any]], str, Any]]): The period of time after any due date that the borrower has to fulfil its obligations before a default (failure to pay) is deemed to have occurred.
        loanTerm: (Optional[Union[List[Union[str, Any]], str, Any]]): The duration of the loan or credit agreement.
        amount: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The amount of money.
        loanRepaymentForm: (Optional[Union[List[Union[str, Any]], str, Any]]): A form of paying back money previously borrowed from a lender. Repayment usually takes the form of periodic payments that normally include part principal plus interest in each payment.
        recourseLoan: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): The only way you get the money back in the event of default is the security. Recourse is where you still have the opportunity to go back to the borrower for the rest of the money.
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
        serviceArea: (Optional[Union[List[Union[str, Any]], str, Any]]): The geographic area where the service is provided.
        broker: (Optional[Union[List[Union[str, Any]], str, Any]]): An entity that arranges for an exchange between a buyer and a seller.  In most cases a broker never acquires or releases ownership of a product or service involved in an exchange.  If it is not clear whether an entity is a broker, seller, or buyer, the latter two terms are preferred.
        provider: (Optional[Union[List[Union[str, Any]], str, Any]]): The service provider, service operator, or service performer; the goods producer. Another party (a seller) may offer those services or goods on behalf of the provider. A provider may also serve as the seller.
        areaServed: (Union[List[Union[str, Any]], str, Any]): The geographic area where a service or offered item is provided.
        slogan: (Union[List[Union[str, Any]], str, Any]): A slogan or motto associated with the item.
        award: (Union[List[Union[str, Any]], str, Any]): An award won by or for this item.
        termsOfService: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Human-readable terms of service documentation.
        review: (Optional[Union[List[Union[str, Any]], str, Any]]): A review of the item.
        availableChannel: (Optional[Union[List[Union[str, Any]], str, Any]]): A means of accessing the service (e.g. a phone bank, a web site, a location, etc.).
        isRelatedTo: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to another, somehow related product (or multiple products).
        serviceAudience: (Optional[Union[List[Union[str, Any]], str, Any]]): The audience eligible for this service.
        isSimilarTo: (Optional[Union[List[Union[str, Any]], str, Any]]): A pointer to another, functionally similar product (or multiple products).
        audience: (Optional[Union[List[Union[str, Any]], str, Any]]): An intended audience, i.e. a group for whom something was created.
        logo: (Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]]): An associated logo.
        providerMobility: (Union[List[Union[str, Any]], str, Any]): Indicates the mobility of a provided service (e.g. 'static', 'dynamic').
        hoursAvailable: (Optional[Union[List[Union[str, Any]], str, Any]]): The hours during which this service or contact is available.
        brand: (Optional[Union[List[Union[str, Any]], str, Any]]): The brand(s) associated with a product or service, or the brand(s) maintained by an organization or business person.
        serviceOutput: (Optional[Union[List[Union[str, Any]], str, Any]]): The tangible thing generated by the service, e.g. a passport, permit, etc.
        produces: (Optional[Union[List[Union[str, Any]], str, Any]]): The tangible thing generated by the service, e.g. a passport, permit, etc.
        hasOfferCatalog: (Optional[Union[List[Union[str, Any]], str, Any]]): Indicates an OfferCatalog listing for this Organization, Person, or Service.
        category: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): A category for the item. Greater signs or slashes can be used to informally indicate a category hierarchy.
        aggregateRating: (Optional[Union[List[Union[str, Any]], str, Any]]): The overall rating, based on a collection of reviews or ratings, of the item.
        serviceType: (Union[List[Union[str, Any]], str, Any]): The type of service being offered, e.g. veterans' benefits, emergency relief, etc.
        offers: (Optional[Union[List[Union[str, Any]], str, Any]]): An offer to provide this item&#x2014;for example, an offer to sell a product, rent the DVD of a movie, perform a service, or give away tickets to an event. Use [[businessFunction]] to indicate the kind of transaction offered, i.e. sell, lease, etc. This property can also be used to describe a [[Demand]]. While this property is listed as expected on a number of common types, it can be used in others. In that case, using a second type, such as Product or a subtype of Product, can clarify the nature of the offer.
        annualPercentageRate: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The annual rate that is charged for borrowing (or made by investing), expressed as a single percentage number that represents the actual yearly cost of funds over the term of a loan. This includes any fees or additional costs associated with the transaction.
        interestRate: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The interest rate, charged or paid, applicable to the financial product. Note: This is different from the calculated annualPercentageRate.
        feesAndCommissionsSpecification: (Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]): Description of fees, commissions, and other terms applied either to a class of financial product, or by a financial service organization.
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
        supersededBy: (Optional[Union[List[Union[str, Any]], str, Any]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
        floorLimit: (Optional[Union[List[Union[str, Any]], str, Any]]): A floor limit is the amount of money above which credit card transactions must be authorized.
        cashBack: (Optional[Union[List[Union[str, StrictBool, Any, StrictInt, StrictFloat]], str, StrictBool, Any, StrictInt, StrictFloat]]): A cardholder benefit that pays the cardholder a small percentage of their net expenditures.
        contactlessPayment: (Optional[Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]]): A secure method for consumers to purchase products or services via debit, credit or smartcards by using RFID or NFC technology.
        monthlyMinimumRepaymentAmount: (Optional[Union[List[Union[str, Any, StrictInt, StrictFloat]], str, Any, StrictInt, StrictFloat]]): The minimum payment is the lowest amount of money that one is required to pay on a credit card statement each month.

    """

    type_: str = Field(default="CreditCard", alias="@type", const=True)
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
    serviceArea: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The geographic area where the service is provided.",
    )
    broker: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An entity that arranges for an exchange between a buyer and a seller. In most cases a broker"
        "never acquires or releases ownership of a product or service involved in an exchange."
        "If it is not clear whether an entity is a broker, seller, or buyer, the latter two terms"
        "are preferred.",
    )
    provider: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The service provider, service operator, or service performer; the goods producer."
        "Another party (a seller) may offer those services or goods on behalf of the provider."
        "A provider may also serve as the seller.",
    )
    areaServed: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The geographic area where a service or offered item is provided.",
    )
    slogan: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A slogan or motto associated with the item.",
    )
    award: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An award won by or for this item.",
    )
    termsOfService: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="Human-readable terms of service documentation.",
    )
    review: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A review of the item.",
    )
    availableChannel: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A means of accessing the service (e.g. a phone bank, a web site, a location, etc.).",
    )
    isRelatedTo: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to another, somehow related product (or multiple products).",
    )
    serviceAudience: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The audience eligible for this service.",
    )
    isSimilarTo: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to another, functionally similar product (or multiple products).",
    )
    audience: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An intended audience, i.e. a group for whom something was created.",
    )
    logo: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="An associated logo.",
    )
    providerMobility: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Indicates the mobility of a provided service (e.g. 'static', 'dynamic').",
    )
    hoursAvailable: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The hours during which this service or contact is available.",
    )
    brand: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The brand(s) associated with a product or service, or the brand(s) maintained by an organization"
        "or business person.",
    )
    serviceOutput: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The tangible thing generated by the service, e.g. a passport, permit, etc.",
    )
    produces: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The tangible thing generated by the service, e.g. a passport, permit, etc.",
    )
    hasOfferCatalog: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates an OfferCatalog listing for this Organization, Person, or Service.",
    )
    category: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="A category for the item. Greater signs or slashes can be used to informally indicate a"
        "category hierarchy.",
    )
    aggregateRating: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The overall rating, based on a collection of reviews or ratings, of the item.",
    )
    serviceType: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The type of service being offered, e.g. veterans' benefits, emergency relief, etc.",
    )
    offers: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An offer to provide this item&#x2014;for example, an offer to sell a product, rent the"
        "DVD of a movie, perform a service, or give away tickets to an event. Use [[businessFunction]]"
        "to indicate the kind of transaction offered, i.e. sell, lease, etc. This property can"
        "also be used to describe a [[Demand]]. While this property is listed as expected on a number"
        "of common types, it can be used in others. In that case, using a second type, such as Product"
        "or a subtype of Product, can clarify the nature of the offer.",
    )
    annualPercentageRate: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The annual rate that is charged for borrowing (or made by investing), expressed as a single"
        "percentage number that represents the actual yearly cost of funds over the term of a loan."
        "This includes any fees or additional costs associated with the transaction.",
    )
    interestRate: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The interest rate, charged or paid, applicable to the financial product. Note: This"
        "is different from the calculated annualPercentageRate.",
    )
    feesAndCommissionsSpecification: Union[
        List[Union[str, AnyUrl, Any]], str, AnyUrl, Any
    ] = Field(
        default=None,
        description="Description of fees, commissions, and other terms applied either to a class of financial"
        "product, or by a financial service organization.",
    )
    requiredCollateral: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Assets required to secure loan or credit repayments. It may take form of third party pledge,"
        "goods, financial instruments (cash, securities, etc.)",
    )
    loanType: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="The type of a loan or credit.",
    )
    currency: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The currency in which the monetary amount is expressed.Use standard formats: [ISO 4217"
        'currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker'
        "symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies,"
        'e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system)'
        '(LETS) and other currency types, e.g. "Ithaca HOUR".',
    )
    renegotiableLoan: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="Whether the terms for payment of interest can be renegotiated during the life of the loan.",
    )
    gracePeriod: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The period of time after any due date that the borrower has to fulfil its obligations before"
        "a default (failure to pay) is deemed to have occurred.",
    )
    loanTerm: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The duration of the loan or credit agreement.",
    )
    amount: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The amount of money.",
    )
    loanRepaymentForm: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A form of paying back money previously borrowed from a lender. Repayment usually takes"
        "the form of periodic payments that normally include part principal plus interest in"
        "each payment.",
    )
    recourseLoan: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="The only way you get the money back in the event of default is the security. Recourse is"
        "where you still have the opportunity to go back to the borrower for the rest of the money.",
    )
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
    serviceArea: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The geographic area where the service is provided.",
    )
    broker: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An entity that arranges for an exchange between a buyer and a seller. In most cases a broker"
        "never acquires or releases ownership of a product or service involved in an exchange."
        "If it is not clear whether an entity is a broker, seller, or buyer, the latter two terms"
        "are preferred.",
    )
    provider: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The service provider, service operator, or service performer; the goods producer."
        "Another party (a seller) may offer those services or goods on behalf of the provider."
        "A provider may also serve as the seller.",
    )
    areaServed: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The geographic area where a service or offered item is provided.",
    )
    slogan: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="A slogan or motto associated with the item.",
    )
    award: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="An award won by or for this item.",
    )
    termsOfService: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="Human-readable terms of service documentation.",
    )
    review: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A review of the item.",
    )
    availableChannel: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A means of accessing the service (e.g. a phone bank, a web site, a location, etc.).",
    )
    isRelatedTo: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to another, somehow related product (or multiple products).",
    )
    serviceAudience: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The audience eligible for this service.",
    )
    isSimilarTo: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A pointer to another, functionally similar product (or multiple products).",
    )
    audience: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An intended audience, i.e. a group for whom something was created.",
    )
    logo: Optional[Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any]] = Field(
        default=None,
        description="An associated logo.",
    )
    providerMobility: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="Indicates the mobility of a provided service (e.g. 'static', 'dynamic').",
    )
    hoursAvailable: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The hours during which this service or contact is available.",
    )
    brand: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The brand(s) associated with a product or service, or the brand(s) maintained by an organization"
        "or business person.",
    )
    serviceOutput: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The tangible thing generated by the service, e.g. a passport, permit, etc.",
    )
    produces: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The tangible thing generated by the service, e.g. a passport, permit, etc.",
    )
    hasOfferCatalog: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Indicates an OfferCatalog listing for this Organization, Person, or Service.",
    )
    category: Union[List[Union[str, AnyUrl, Any]], str, AnyUrl, Any] = Field(
        default=None,
        description="A category for the item. Greater signs or slashes can be used to informally indicate a"
        "category hierarchy.",
    )
    aggregateRating: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="The overall rating, based on a collection of reviews or ratings, of the item.",
    )
    serviceType: Union[List[Union[str, Any]], str, Any] = Field(
        default=None,
        description="The type of service being offered, e.g. veterans' benefits, emergency relief, etc.",
    )
    offers: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="An offer to provide this item&#x2014;for example, an offer to sell a product, rent the"
        "DVD of a movie, perform a service, or give away tickets to an event. Use [[businessFunction]]"
        "to indicate the kind of transaction offered, i.e. sell, lease, etc. This property can"
        "also be used to describe a [[Demand]]. While this property is listed as expected on a number"
        "of common types, it can be used in others. In that case, using a second type, such as Product"
        "or a subtype of Product, can clarify the nature of the offer.",
    )
    annualPercentageRate: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The annual rate that is charged for borrowing (or made by investing), expressed as a single"
        "percentage number that represents the actual yearly cost of funds over the term of a loan."
        "This includes any fees or additional costs associated with the transaction.",
    )
    interestRate: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The interest rate, charged or paid, applicable to the financial product. Note: This"
        "is different from the calculated annualPercentageRate.",
    )
    feesAndCommissionsSpecification: Union[
        List[Union[str, AnyUrl, Any]], str, AnyUrl, Any
    ] = Field(
        default=None,
        description="Description of fees, commissions, and other terms applied either to a class of financial"
        "product, or by a financial service organization.",
    )
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
    supersededBy: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="Relates a term (i.e. a property, class or enumeration) to one that supersedes it.",
    )
    floorLimit: Optional[Union[List[Union[str, Any]], str, Any]] = Field(
        default=None,
        description="A floor limit is the amount of money above which credit card transactions must be authorized.",
    )
    cashBack: Optional[
        Union[
            List[Union[str, StrictBool, Any, StrictInt, StrictFloat]],
            str,
            StrictBool,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="A cardholder benefit that pays the cardholder a small percentage of their net expenditures.",
    )
    contactlessPayment: Optional[
        Union[List[Union[str, StrictBool, Any]], str, StrictBool, Any]
    ] = Field(
        default=None,
        description="A secure method for consumers to purchase products or services via debit, credit or smartcards"
        "by using RFID or NFC technology.",
    )
    monthlyMinimumRepaymentAmount: Optional[
        Union[
            List[Union[str, Any, StrictInt, StrictFloat]],
            str,
            Any,
            StrictInt,
            StrictFloat,
        ]
    ] = Field(
        default=None,
        description="The minimum payment is the lowest amount of money that one is required to pay on a credit"
        "card statement each month.",
    )
