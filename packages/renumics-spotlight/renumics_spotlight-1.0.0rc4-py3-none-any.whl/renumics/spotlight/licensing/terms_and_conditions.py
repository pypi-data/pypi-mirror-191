"""
Renumics GTC verification.
"""

import hashlib
import os
from pathlib import Path

from renumics.spotlight import appdirs
from renumics.spotlight._build_variant import __build_variant__

TERMS = """
                 General Terms and Conditions of Renumics GmbH
                     for Software Subscription und Support

                            § 1 Scope of Application

1.  These General Terms and Conditions (hereinafter referred to as „GTC“) apply
    to the temporary provision and licensing of the software Renumics Spotlight
    for data curation including the integrated algorithms (hereinafter
    collectively referred to as „Software“) as well as the provision of support
    services by Renumics GmbH, Haid-und-Neu-Str. 7, 76131 Karlsruhe (hereinafter
    referred to as „Renumics“). Customers of Renumics are exclusively
    entrepreneurs within the meaning of sec. 14 of the German Civil Code (BGB).

2.  In the event of contradictions, Customer-specific provisions in Renumics’
    offer shall take precedence over these GTC. These GTC in their current
    version shall also apply to all future contracts between Renumics and
    Customer concerning the provision and licensing of software, even if this is
    not expressly referred to again.

3.  Customer's terms and conditions of purchase or other terms and conditions
    shall not apply, even if Renumics should render services without expressly
    contradicting Customer's terms and conditions.

4.  Unless otherwise agreed, for third-party software and open-source software
    supplied by Renumics to Customer, the contractual and licensing conditions
    of the respective manufacturer or supplier or the respective applicable
    open-source licensing conditions shall apply. These may contain, in
    particular, provisions on the granting of rights of use and on warranty and
    liability that deviate from these Terms and Conditions. Renumics shall draw
    Customer's attention to the contractual and licensing conditions for such
    third-party software when concluding the contract, e.g., in the offer. If
    there are gaps in the contractual and licensing conditions for the
    third-party software, the provisions of these GTC shall apply in addition.

                         § 2 Conclusion and Amendments

1.  Offers of Renumics are subject to change and non-binding, unless the offer
    is designated in writing as binding. Customer is bound by its declarations
    to conclude contracts for four (4) weeks.

2.  The contracting parties shall conclude a uniform contract on the provision
    of the Software on a rental basis (subscription) and the provision of the
    support services defined within these GTC against payment of a uniform
    annual usage fee. Part of each subscription is a minimum number of user
    licenses. Customer may purchase additional licenses for further users at any
    time or terminate licenses in compliance with the agreed notice periods,
    provided that this does not cause the number of licenses to fall below the
    agreed minimum. A sale of software or licenses to Customer does not take
    place.

3.  Renumics reserves the right to adjust the GTC and other parts of the
    contract during the contract period. Customer shall be notified of new
    versions in writing or by e-mail, highlighting the adaptations. They shall
    become effective if Customer does not object to the new version in writing
    within six (6) weeks of receipt of the notification of amendment. Customer
    shall be expressly informed of the consequences of its failure to do so when
    it is notified of the amendments. If Customer objects to the new version,
    the contractual relationship shall continue under the original terms and
    conditions but may be terminated for cause by Renumics with three (3)
    months' notice period.

                          § 3 Dates and Force majeure

1.  Dates and deadlines are approximate and non-binding, unless they are
    expressly designated as binding in Renumics‘ offer. The adherence to agreed
    dates and deadlines requires the timely receipt of all required documents,
    information and decisions of Customer.

2.  Events beyond the control of a contracting party, such as force majeure,
    strikes, lockouts, non-delivery or delay of supplies by third parties
    despite the conclusion of congruent hedging transactions, which make
    delivery or performance considerably more difficult or temporarily
    impossible, shall entitle the affected contracting party to postpone the
    performance of its obligations by the duration of the hindrance and a
    reasonable restart time. The contracting parties shall notify each other
    without delay of the occurrence and termination of such circumstances.

                       § 4 Scope of Delivery and Services

1.  The features and functions of the Software, the type and scope of the
    licenses acquired and the amount of the remuneration are set out in
    Renumics‘ offer and in the respective product description of the Software,
    which is part of the documentation. Customer receives the Software by
    download or electronic transmission in the current version at the time of
    delivery exclusively in object code. Customer is not entitled to the
    provision of the source code of the Software. Together with the Software,
    Customer receives documentation integrated into the Software and the license
    key required for the activation of the licenses.

2.  Customer shall host and operate the Software as an on-premise solution in
    its own responsibility on its own workstations or servers. Unless otherwise
    agreed by the contracting parties, Customer shall be responsible for the
    installation and integration of the Software into its existing system
    environment, for compliance with the system requirements, for the smooth
    interaction between the Software and its hardware, and for interactions
    between the delivered Software and other programs of Customer.

3.  In the course of ongoing improvement and further development of the
    Software, functions may be added, amended or omitted during the contract
    period, provided that this does not lead to any significant restriction of
    the contractually agreed scope of functions, the achievement of the purpose
    of the contract is not jeopardized thereby and the adaption is reasonable
    for Customer.

4.  Consulting and support services for the application of the Software that go
    beyond the provision of the support services (cf. § 6), e.g. adaptation and
    configuration of the Software or the algorithms integrated in the Software,
    preparation of customer data, training of Customer's employees or
    commissioning support, shall only be provided on the basis of a separate
    agreement.

5.  Customer shall support Renumics to the necessary extent in the performance
    of the service, shall observe the system requirements defined by Renumics
    for the use of the Software and shall take appropriate precautions in the
    event of a loss of data (e.g. by making regular data backups) within the
    scope of its obligation to minimize damage. Customer shall be responsible
    for the proper archiving and backup of its data by making regular backup
    copies in accordance with the risk.

                   § 5 Granting of Rights to use the Software

1.  In relation to Customer, Renumics is and remains the sole and exclusive
    owner of all rights - including all copyrights, patent rights and industrial
    property rights - to the Software (including the algorithms integrated into
    the Software) as well as to any adaptations, supplements and other further
    developments of the Software and algorithms created by Renumics during the
    cooperation. Customer shall only receive the non-exclusive rights to use the
    Software described in the offer and in this § 5.

2.  Customer remains the owner of all rights to its own pre-existing algorithms
    and to its data that it processes with the Software.

3.  Renumics grants Customer the non-exclusive, non-transferable and
    non-sublicensable right, limited in time to the term of the contract, to use
    and apply the Software for Customer's own business purposes as agreed or as
    provided by both contracting parties.

4.  Customer may store and operate the Software on the workstations or servers
    specified in the contract in terms of type and number and use it with the
    agreed type and number of users (named user model). Upon request of Customer
    Renumics will transfer licenses to new workstations or servers or to new
    users usually within one (1) month. Within the scope of the contractual use,
    Customer shall be entitled to reproduce the Software to the extent required
    and to make the necessary backup copies, which shall be marked as such.
    Copyright and other property right notices within the provided Software must
    neither be removed nor changed by Customer.

5.  Sublicensing, leasing and other forms of temporary provision of the Software
    to third parties, use in SaaS, outsourcing or data center operations or any
    other use of the Software by or for third parties against or without payment
    shall require the prior written consent of Renumics. Companies affiliated
    with Customer under company law shall also be deemed to be third parties.

6.  Customer shall not be entitled to translate, edit or redesign the Software
    beyond the mandatory scope permitted by law - in particular the scope
    regulated by section 69d of the German Copyright Act. The disassembly and
    decompilation of the Software in order to establish the interoperability of
    the Software with other programs is only permitted within the mandatory
    limits of section 69e of the German Copyright Act and if Renumics does not
    voluntarily provide the necessary information and documents for this purpose
    within a reasonable period of time despite a written request by Customer.

7.  If Customer receives the Software for testing purposes, Customer's rights of
    use shall be limited to such actions that serve to determine the condition
    of the Software and its suitability for Customer's operational purposes. Any
    further actions of use, in particular productive operation, shall be
    inadmissible, as shall the creation of copies (including backup copies),
    editing and decompilation of the Software. In addition, the terms of use of
    this § 5 shall also apply to test licenses. After expiry of the agreed test
    period, Customer shall delete the Software from its systems completely and
    irretrievably and shall confirm the deletion to Renumics in writing upon
    request.

8.  Any use of the Software beyond the agreed conditions requires the prior
    written consent of Renumics. If the use takes place without this consent,
    Renumics shall invoice Customer for the remuneration incurred for the
    further use in accordance with its respectively valid price list (also
    retroactively). Claims for damages remain reserved. Customer is obligated to
    notify Renumics in advance of any change that affects its rights of use.

                       § 6 Provision of Support Services

1.  During the contract period, Renumics provides the following support
    services, which are covered by the flat annual usage fee:

    (i)   providing updates to the Software

    (ii)  correction of defects in the Software

    (iii) telephone and e-mail support

2.  All support services are provided remotely during Renumics‘ normal business
    hours (Monday to Friday from 9:00 to 17:00 CET, excluding public holidays in
    Baden-Wuerttemberg).

3.  As a general rule, only the current version of the Software released by
    Renumics at any given time shall be subject to support by Renumics. For
    older versions of the Software, Renumics shall continue to provide support
    services during a transition period of one (1) year after the release of a
    new version. In addition, Renumics shall only provide support services in
    relation to older versions of the Software after a separate order has been
    placed and against compensation of additional expenses incurred.

4.  Updates shall be provided in object code by download or electronic
    transmission. A provision of the source code of updates is not owed.
    Customer is responsible for the installation of updates. The license
    conditions in § 5 shall also apply to the updates provided to the Customer.
    Customer shall check each update for freedom from defects before start of
    productive use. With the start of the productive use of the update, the
    rights to the Software version replaced by the update shall automatically
    expire.

5.  Customer shall report any defects and malfunctions promptly and, in the case
    of notification by telephone, subsequently in text form (in particular by
    e-mail), stating the more detailed circumstances of their occurrence, their
    effects and possible causes. Customer shall provide all necessary documents
    and information required by Renumics for fault diagnosis and treatment and,
    if necessary, grant access to its IT infrastructure and to the Software on
    site. Customer shall support Renumics in the analysis and correction of
    errors to a reasonable extent, e.g. by following instructions from Renumics
    to eliminate or circumvent a defect.

6.  The telephone and e-mail support serves to assist Customer with technical
    problems in connection with the use of the Software that Customer cannot
    solve himself, as well as to report defects and malfunctions. The support is
    available to Customer during the normal business hours of Renumics. Not part
    of the support is in particular the technical and organizational advice to
    Customer concerning the use of the Software.

7.  In particular, the following services are not included in the scope of
    support services and are therefore only to be provided by Renumics by
    separate agreement and for additional remuneration:

    (i)   services on Customer's premises and services outside Renumics‘
          business hours;

    (ii)  provision of successor products or upgrades of the Software with a
          substantially amended or extended scope of functions;

    (iii) analysis and elimination of malfunctions and errors not caused by the
          Software, e.g. due to faulty IT infrastructure of Customer, faulty or
          incompatible third-party software, faulty, outdated or incomplete
          data, faulty interfaces, system parameters amended by Customer or
          amendments to the system environment or other interventions by
          Customer in the Software or software environment;

    (iv)  necessary conversions and adaptations of the Software to another
          hardware or operating system or after an amendment of third-party
          software;

    (v)	  individual extensions and adaptations of the Software or algorithms to
          new requirements of Customer or support for such customer-specific
          components.

8.  Unless otherwise agreed, the services not included in the scope of support
    pursuant to this § 6 shall be compensated by the Customer on the basis of
    the agreed daily/hourly rates.

                     § 7 Remuneration and Terms of Payment

1.  A uniform annual usage fee is charged for subscription and support, the
    amount of which depends on the number of licensed users. The usage fee shall
    be invoiced to Customer by Renumics annually in advance at the beginning of
    each contract year. The amount of the usage fee and the further terms of
    payment shall primarily result from Renumics‘ offer.

2.  Unless otherwise agreed, additional services shall be remunerated on a time
    and material basis at the daily or hourly rates specified in the offer. If a
    scope of services is stated in the offer, this shall, in the absence of an
    express agreement to the contrary, be deemed to be a mere estimate of the
    time and effort required. The remuneration shall be invoiced to Customer on
    a monthly basis at the beginning of the month following the performance of
    the service, upon presentation of the activities reports customary at Renumics.

3.  The remuneration of travel time and the reimbursement of travel and other
    incidental expenses shall be governed by the provisions of the offer. All
    prices are subject to the applicable statutory value added tax. Payments are
    to be made by Customer at the latest 30 days after receipt of the invoice
    without deduction.

4.  If Customer is in default with the payment of the usage fee, Renumics is
    entitled to revoke the rights of use granted and to discontinue the further
    provision of services after a prior reminder and an appropriate grace
    period. Further rights of Renumics due to the delay in payment (in
    particular, a termination for cause) remain unaffected.

                                  § 8 Warranty

1.  Customer shall report any defects in the Software to Renumics in a
    comprehensible form in writing or by e-mail promptly after the Software has
    been provided or, in the case of hidden defects, promptly after their
    discovery. Customer shall take all reasonable and necessary measures to
    determine, limit and document any defects that have occurred.

2.  During the contract period, Renumics warrants that the Software has the
    features and functionalities described in the product description and that
    the contractual use of the Software does not infringe any third-party
    rights. Claims can only be asserted by Customer due to defects that are
    reproducible or can be comprehensibly described by Customer. Functional
    impairments resulting from improper operation of the Software by Customer,
    from Customer's system environment, from incomplete or incorrect data or
    data that does not meet Renumics requirements or from other circumstances
    within Customer's sphere of risk do not constitute a defect. The liability
    for defects requires that Customer complies with the system requirements and
    operating conditions specified by Renumics and does not amend the Software
    or use it contrary to the contractual specifications (e.g. in a different
    system environment), unless Customer proves that the defect is independent
    of this.

3.  Renumics does not assume any warranty for the quality or suitability of the
    Software for the fulfillment of certain customer-specific tasks and
    applications or for the correctness and accuracy of the measurement, process
    and other processing results achieved with the Software. The processing
    results achieved with the Software also depend in particular on the nature
    and quality of Customer's data, processes and algorithms; Customer alone is
    responsible for this. Customer shall always check the processing results
    achieved with the Software before using them as a basis for its technical or
    business decisions.

4.  If a defect of the Software occurs during the contract period, Renumics
    shall meet its warranty obligations by way of subsequent performance, which
    may be effected at Renumics‘ discretion by way of subsequent delivery of
    defect-free software (e.g. in the form of an update) or elimination of the
    defect. The elimination of the defect may also consist of Renumics initially
    showing Customer reasonable possibilities of avoiding or circumventing the
    effects of the defect (workaround).

5.  If the rectification of a defect finally fails (at least three attempts per
    defect) or is finally refused by Renumics, Customer may reduce the usage fee
    or terminate the contract for good cause. Customer may only assert the right
    of termination pursuant to section 543 Sec. 2 No. 1 German Civil Code on the
    condition that he has previously requested Renumics in writing to provide
    subsequent performance within a reasonable period of at least two (2) weeks
    and that the period has expired without success. In the event of an only
    insignificant deviation of the Software from the agreed quality, there shall
    be no right of termination. Customer is not entitled to withdraw from the
    contract. Renumics shall pay damages and compensation for futile expenses
    due to a defect within the limits set out in § 10.

6.  If Renumics provides services in the analysis for and/or elimination of
    defects without being obligated to do so, Renumics may demand separate
    remuneration for this from Customer on a time and material basis. This shall
    apply in particular if a defect reported by Customer cannot be proven or
    cannot be attributed to Renumics. There shall be no claim to additional
    remuneration if Customer is not at fault, in particular because it was not
    apparent to Customer that there was no defect in the Software.

                      § 9 Infringements of Property Rights

1.  During the term of the contract, Renumics warrants that the Software
    provided to Customer is free from third-party intellectual property rights
    and shall indemnify Customer against third-party claims based on the
    infringement of intellectual property rights in accordance with the
    following provisions.

2.  If third parties assert claims against Customer based on the infringement of
    their intellectual property rights by the Software, Customer shall
    immediately inform Renumics hereof comprehensively and in written form.
    Renumics shall be entitled, but is not obliged, to settle the dispute with
    the third party in and out of court on its own. In the event that Renumics
    acts upon this authorization, Customer shall reasonable assist Renumics free
    of charge. Customer shall not recognize any third-party claims on its own
    discretion.

3.  If the Software shows a defect of title during the term of the contract,
    Renumics shall obtain any rights required for the lawful use of the Software
    on behalf of the Customer within the scope of subsequent performance.
    Alternatively, Renumics may also replace the affected Software with
    equivalent software if this is reasonable for Customer. If an infringement
    of third-party intellectual property rights and/or a legal dispute about the
    claims of the third party can be eliminated or avoided by Customer using a
    more up-to-date version of the Software provided free of charge by Renumics,
    Customer is obligated to adopt and use such version within the scope of its
    obligation to mitigate damages, unless Customer proves that the use of the
    more up-to-date version is unreasonable for it.

4.  Renumics shall indemnify Customer within the liability limits set forth in
    § 10 of these GTC from all damages arising from the infringement of
    intellectual property rights, insofar as these are based on a defect of
    title for which Renumics is responsible and provided that the Software is
    used by Customer in accordance with the license and contract provisions. In
    all other respects, the provisions for material defects in § 8 shall apply
    accordingly to any claims asserted by Customer based on defects of title.

5.  In particular, Renumics shall not be liable if claims of a third party based
    on alleged infringements of intellectual property rights are based on the
    fact that the Software was amended by Customer or used in violation of the
    contractually agreed conditions of use or for purposes other than those
    contractually agreed.

                                 § 10 Liability

1.  If Renumics provides Customer with the Software or renders services free of
    charge, e.g., during a free test phase, Renumics shall only be liable in
    this respect for intentional and grossly negligent breaches of obligation.

2.  Contrary to the statutory provision of section 536a German Civil Code,
    Renumics shall only be liable for defects that already existed at the time
    of contract conclusion if Renumics is responsible for such defects.

3.  In all other respects, Renumics shall only provide compensation for damage
    and loss as well as for futile expenses, irrespective of the legal grounds,
    to the following extent:

    a.  in the case of intentional wrongdoing and gross negligence as well as in
        the case of the assumption of a guarantee in full amount;

    b.  in all other cases only in the event of a breach of a material
        contractual obligation, without which the achievement of the purpose of
        the contract would be jeopardized and on the fulfillment of which
        Customer may therefore regularly rely, and insofar limited to the amount
        of compensation for typical and foreseeable damage.

4.  Customer shall take all necessary and reasonable measures to prevent or
    limit damages, in particular Customer shall ensure the regular backup of its
    programs, algorithms and data. Renumics shall only be liable for the
    retrieval of data within the limits of § 10 subsection 3 if Customer has
    ensured that the data can be reproduced at any time with reasonable effort.

5.  The above limitations of liability shall also apply to the legal
    representatives, vicarious agents and employees of Renumics.

6.  Liability for damages arising from injury to life, limb or health and under
    the German Product Liability Act shall remain unaffected by the above
    provisions.

                    § 11 Confidentiality and Data Protection

1.  The contracting parties undertake to maintain confidentiality about all
    business secrets of the other party entrusted to them, made accessible to
    them or otherwise made known to them, as well as about other business
    relations and operational facts, to use such confidential information only
    for the purpose provided for in the individual contract and not to disclose
    it to third parties. Confidential information of Renumics includes in
    particular the Software in all formats and development stages, algorithms,
    technical documents and documentation, operating instructions, samples,
    models and drawings. The obligation to treat business secrets as
    confidential shall remain in force for a further three (3) years beyond the
    end of the contract.

2.  In particular, the Customer is prohibited from exploiting, examining,
    reverse engineering or imitating confidential information in any way, either
    itself or through third parties. Customer's right to decompile software
    under § 5 subsection 6 of these GTC shall remain unaffected.

3.  The contracting parties shall provide access to the confidential information
    only to those of their employees and subcontractors who are bound to
    confidentiality and who need to have knowledge for the purposes of the
    individual contract.

4.  The obligation to maintain confidentiality shall not apply to confidential
    information which was already known to the recipient without an obligation
    to maintain confidentiality or which is or becomes generally known without
    the recipient being responsible for this or which is lawfully disclosed to
    the recipient by a third party without an obligation to maintain
    confidentiality or which has demonstrably been independently developed by
    the recipient.

5.  The contracting parties undertake to properly store all business objects,
    data carriers and documents made available to them by the other contracting
    party and to hand them over to the other contracting party at any time upon
    request. In particular, they shall ensure that, as far as possible,
    unauthorized third parties are not able to inspect them.

6.  Renumics does not process any personal data of Customer with the Software.
    Notwithstanding the foregoing, Renumics shall obligate its employees
    entrusted with the performance of the contract in writing to treat personal
    data confidential and to comply with the General Data Protection Regulation
    (GDPR) prior to their deployment. If the Customer provides access to its
    personal data to Renumics, it shall ensure that the relevant legal
    requirements for transfer to and processing by Renumics (and, if applicable,
    its subcontractors) are met.

7.  If Customer agrees to be named as a reference Customer, Renumics may include
    Customer's name in a list of references for its own advertising purposes
    and, in this context, also use Customer's corporate identifiers, brands and
    logos in printed publications and online, in particular on Renumics‘
    website.

                           § 12 Term and Termination

1.  The contract comes into force upon signature by both contracting parties.

2.  If Customer receives the Software for testing purposes for a limited test
    period, the contract shall end automatically upon expiry of the agreed test
    period, unless the contracting parties agree on an extension of the test
    period beforehand.

3.  In all other cases, the contract shall have an initial binding term of one
    (1) contract year from its entry into force. Thereafter, it shall be
    extended by further periods of 12 months unless it is terminated by one of
    the contracting parties with three (3) months' notice prior to the expiry of
    the relevant term.

4.  Licenses or users may be terminated individually (partial termination)
    subject to the agreed notice periods, provided that the agreed minimum
    number of licenses or users remains in place. A separate termination of the
    support services is not possible, i.e. subscription and support can only be
    terminated jointly.

5.  The right of both contracting parties to extraordinary termination for good
    cause shall remain unaffected. Good cause shall exist for Renumics in
    particular if Customer is more than four (4) weeks in default with a
    significant part of the remuneration due or if Customer otherwise breaches
    material contractual obligations and does not cease this breach within one
    (1) week even after being requested to do so by Renumics.

6.  Upon termination of the contract, Customer shall immediately cease using the
    Software, return or destroy the data carriers and backup copies created by
    Renumics, uninstall the Software from all workstations and servers and
    delete any remaining parts of the Software from its IT systems. Upon request
    of Renumics, Customer shall confirm the fulfillment of the aforementioned
    obligations in writing.

7.  If the contract is terminated by Renumics for a good cause for which
    Customer is responsible, Renumics shall retain the claim to the full
    remuneration until the expiry of the current contract period.

8.  Any termination must be in writing to be effective.

                             § 13 Final Provisions

1.  Any assignment or transfer of contractual rights and obligations by Customer
    to third parties - including affiliated companies of Customer - shall
    require the prior written consent of Renumics. Section 354a of the German
    Commercial Code remains unaffected.

2.  All amendments and supplements to the contract must be made in writing to be
    effective (transmission by e-mail satisfies the written form requirement).
    The written form requirement can itself only be waived in writing.

3.  The law of the Federal Republic of Germany shall apply, excluding the
    conflict of laws rules of private international law and excluding the UN
    Convention on Contracts for the International Sale of Goods. The exclusive
    place of jurisdiction for all disputes arising in connection with the
    contract is Karlsruhe, Germany. Renumics shall also have the right to bring
    an action before any other national or international court of competent
    jurisdiction.

4.  Should individual provisions of these GTC be or become invalid or if there
    are any gaps, this shall not affect the validity of the remaining
    provisions. The invalid or missing provision shall be replaced by a valid
    provision that comes as close as possible to the economic intentions of the
    contracting parties at the time of the conclusion of the contract.

   General Terms and Conditions of Renumics GmbH, version 1.0, status 18.02.2022
"""


class TermsAndConditionsNotAccepted(Exception):
    """
    Renumics GTC are not accepted.
    """


def verify_terms_and_conditions() -> None:
    """
    Check whether Renumics GTC are accepted. Prompt if not.
    Save hashes of the accepted GTC texts on the local system.
    """
    if __build_variant__ == "core":
        return
    gtc_text = TERMS
    gtc_hash = _stable_hash(gtc_text)
    confirmation_file = _get_confirmation_file()
    accepted_hashes = []
    if confirmation_file.is_file():
        accepted_hashes.extend(confirmation_file.read_text().split("\n"))
    if gtc_hash not in accepted_hashes:
        if (
            os.environ.get("SPOTLIGHT_ACCEPT_TERMS_AND_CONDITIONS", "").lower()
            != "true"
        ):
            print(gtc_text)
            while True:
                reply = input("Do you agree (yes/no/export)? ").strip(" \t\n\ufeff")
                if reply.lower() == "export":
                    out_file = Path(".") / "renumics_terms_and_conditions.txt"
                    out_file.write_text(gtc_text)
                    print(
                        f"\nGeneral terms and conditions saved as {out_file.absolute()}."
                    )
                elif reply.lower() == "yes":
                    break
                if reply.lower() == "no":
                    raise TermsAndConditionsNotAccepted(
                        "General terms and conditions of Renumics Spotlight"
                        "software are not accepted."
                    )
        confirmation_file.parent.mkdir(parents=True, exist_ok=True)
        with confirmation_file.open("a") as f:
            f.write(gtc_hash + "\n")


def _stable_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def _get_confirmation_file() -> Path:
    return Path(appdirs.config_dir) / ".gtc-accepted"
