import requests

from lxml import etree

from constants import XML_PATH
from invoice_class import RandomInvoice
from copy import deepcopy

# XML to HTML api
API_ENDPOINT = "http://das.detayteknoloji.com/api/versions/1/files/xml/html"


class GenerateInvoice:
    def __init__(self):

        self.root = etree.parse(XML_PATH).getroot()
        self.randomXml = RandomInvoice()
        self.change_values()

        tree = etree.ElementTree(self.root)
        _files = {'files': etree.tostring(tree, encoding='utf8', method='xml')}
        self._return = str(requests.post(url=API_ENDPOINT, files=_files).text)

    def __str__(self):
        return self._return

    def __repr__(self):
        return repr(self._return)

    @staticmethod
    def change_single_values(_root, _key, newvalue, remove_root=False):

        if _root.findall(_key):
            _element = _root.find(_key)
            if not newvalue:
                if remove_root:
                    _element = _element.getparent()
                    elemroot = _element.getparent()
                    elemroot.remove(_element)

                else:
                    elemroot = _element.getparent()
                    elemroot.remove(_root.find(_key))
            else:
                _root.find(_key).text = str(newvalue)
        else:
            pass

    def change_values(self):

        ac = "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}"
        bc = "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}"

        # invoice id
        invoice_id_key = ".//" + bc + "ID"
        self.change_single_values(self.root, invoice_id_key, self.randomXml.InvoiceID)

        # invoice uuid
        invoice_uuid_key = ".//" + bc + "UUID"
        self.change_single_values(self.root, invoice_uuid_key, self.randomXml.InvoiceUUID)

        # invoice date
        invoice_issue_date_key = ".//" + bc + "IssueDate"
        self.change_single_values(self.root, invoice_issue_date_key, self.randomXml.InvoiceIssueDate)

        # Deletion from root is required for waybill number and date !!!

        # waybill id
        dispatch_id_key = ".//" + ac + "DespatchDocumentReference/" + bc + "ID"
        self.change_single_values(self.root, dispatch_id_key, self.randomXml.DispatchID, 1)

        # waybill date
        dispatch_issue_date_key = ".//" + ac + "DespatchDocumentReference/" + bc + "IssueDate"
        self.change_single_values(self.root, dispatch_issue_date_key, self.randomXml.DispatchIssueDate, 1)

        # Order number and date !!!

        # Order id
        order_id_key = "./" + ac + "OrderReference//" + bc + "ID"
        self.change_single_values(self.root, order_id_key, self.randomXml.OrderID, 1)

        # Order Date
        order_issue_date_key = "./" + ac + "OrderReference//" + bc + "IssueDate"
        self.change_single_values(self.root, order_issue_date_key, self.randomXml.OrderIssueDate, 1)

        # Note Info
        note_key = ".//" + bc + "Note"
        self.change_single_values(self.root, note_key, self.randomXml.Note)

        #########################
        #
        # INFORMATION ABOUT THE SENDER:
        #
        #########################

        # Sender nama:
        gonderenfirmakisi_key = ".//" + ac + "AccountingSupplierParty//" + ac + "Party//" + ac + "PartyName//" + bc + "Name"
        self.change_single_values(self.root, gonderenfirmakisi_key, self.randomXml.AccountingSupplierParty.sender_company)

        # sender tax id
        gonderen_vkn_key = ".//" + ac + "AccountingSupplierParty//" + bc + "ID[@schemeID='VKN']"
        self.change_single_values(self.root, gonderen_vkn_key, self.randomXml.AccountingSupplierParty.sender_tax_number, 1)

        # sender TCKN(Turkish republic identification number)
        gonderen_tckn_key = ".//" + ac + "AccountingSupplierParty//" + bc + "ID[@schemeID='TCKN']"
        self.change_single_values(self.root, gonderen_tckn_key, self.randomXml.AccountingSupplierParty.sender_tckn, 1)

        # sender mersis number
        gonderen_mersis_key = ".//" + ac + "AccountingSupplierParty//" + bc + "ID[@schemeID='MERSISNO']"
        self.change_single_values(self.root, gonderen_mersis_key, self.randomXml.AccountingSupplierParty.sender_mersis, 1)

        # sender web address
        gonderenweb_key = ".//" + ac + "AccountingSupplierParty//" + bc + "WebsiteURI"
        self.change_single_values(self.root, gonderenweb_key, self.randomXml.AccountingSupplierParty.sender_web)

        # sender mail address
        gonderenposta_key = ".//" + ac + "AccountingSupplierParty//" + bc + "ElectronicMail"
        self.change_single_values(self.root, gonderenposta_key, self.randomXml.AccountingSupplierParty.sender_mail)

        # sender tel
        gonderentel_key = ".//" + ac + "AccountingSupplierParty//" + bc + "Telephone"
        self.change_single_values(self.root, gonderentel_key, self.randomXml.AccountingSupplierParty.sender_tel)

        # sender fax
        gonderenfax_key = ".//" + ac + "AccountingSupplierParty//" + bc + "Telefax"
        self.change_single_values(self.root, gonderenfax_key, self.randomXml.AccountingSupplierParty.sender_fax)

        # sender country and city
        gonderenililce_key = ".//" + ac + "AccountingSupplierParty//" + bc + "CityName"
        self.change_single_values(self.root, gonderenililce_key, self.randomXml.AccountingSupplierParty.sender_city)

        # sender address
        gonderenadres_key = ".//" + ac + "AccountingSupplierParty//" + bc + "StreetName"
        self.change_single_values(self.root, gonderenadres_key, self.randomXml.AccountingSupplierParty.gonderenadres)

        # sender postal code
        gonderenpostakodu_key = ".//" + ac + "AccountingSupplierParty//" + bc + "PostalZone"
        self.change_single_values(self.root, gonderenpostakodu_key,
                                  self.randomXml.AccountingSupplierParty.sender_postal_code, 1)

        # sender tax office
        gonderenvd_key = ".//" + ac + "AccountingSupplierParty//" + ac + "TaxScheme//*"
        self.change_single_values(self.root, gonderenvd_key, self.randomXml.AccountingSupplierParty.sender_tax_office)

        #########################
        #
        # INFORMATION ABOUT THE BUYER:
        #
        #########################

        # Buyer Company or Person Name
        alicifirmakisi_key = "./" + ac + "AccountingCustomerParty//" + ac + "PartyName//"
        self.change_single_values(self.root, alicifirmakisi_key, self.randomXml.AccountingCustomerParty.buyer_company)

        # Buyer tax number
        alici_vkn_key = "./" + ac + "AccountingCustomerParty//" + bc + "ID[@schemeID='VKN']"
        self.change_single_values(self.root, alici_vkn_key, self.randomXml.AccountingCustomerParty.buyer_tax, 1)

        # Buyer TCKN(Turkish republic identification number)
        alici_tckn_key = "./" + ac + "AccountingCustomerParty//" + bc + "ID[@schemeID='TCKN']"
        self.change_single_values(self.root, alici_tckn_key, self.randomXml.AccountingCustomerParty.buyer_tckn, 1)

        # Buyer web address
        aliciweb_key = "./" + ac + "AccountingCustomerParty//" + bc + "WebsiteURI"
        self.change_single_values(self.root, aliciweb_key, self.randomXml.AccountingCustomerParty.buyer_web)

        # Buyer mail address
        aliciposta_key = "./" + ac + "AccountingCustomerParty//" + bc + "ElectronicMail"
        self.change_single_values(self.root, aliciposta_key, self.randomXml.AccountingCustomerParty.buyer_mail)

        # Buyer Tel
        alicitel_key = "./" + ac + "AccountingCustomerParty//" + bc + "Telephone"
        self.change_single_values(self.root, alicitel_key, self.randomXml.AccountingCustomerParty.buyer_tel)

        # Buyer fax
        alicifax_key = "./" + ac + "AccountingCustomerParty//" + bc + "Telefax"
        self.change_single_values(self.root, alicifax_key, self.randomXml.AccountingCustomerParty.buyer_fax)

        # Buyer country and city
        aliciililce_key = "./" + ac + "AccountingCustomerParty//" + bc + "CityName"
        self.change_single_values(self.root, aliciililce_key, self.randomXml.AccountingCustomerParty.buyer_city)

        # Buyer full address
        aliciadres_key = "./" + ac + "AccountingCustomerParty//" + bc + "StreetName"
        self.change_single_values(self.root, aliciadres_key, self.randomXml.AccountingCustomerParty.buyer_address)

        # Buyer postal code
        alicipostakodu_key = "./" + ac + "AccountingCustomerParty//" + bc + "PostalZone"
        self.change_single_values(self.root, alicipostakodu_key, self.randomXml.AccountingCustomerParty.buyer_postal_code, 1)

        # Buyer tax office
        alicivd_key = "./" + ac + "AccountingCustomerParty//" + ac + "TaxScheme//*"
        self.change_single_values(self.root, alicivd_key, self.randomXml.AccountingCustomerParty.buyer_tax_office)

        #########################
        #
        # INFORMATION ABOUT ITEMS:
        #
        #########################

        invoicelines_root = self.root.find("./" + ac + "InvoiceLine")

        for i, _lines in enumerate(self.randomXml.invoiceLine):
            line_deepcopy = deepcopy(invoicelines_root)
            # item id
            line_deepcopy.find("./" + bc + "ID").text = str(i + 1)
            # item name (goods or services)
            line_deepcopy.find(".//" + ac + "Item//").text = _lines.itemName
            # item quantity and unit code
            line_deepcopy.find("./" + bc + "InvoicedQuantity").text = str(_lines.quantity)
            line_deepcopy.find("./" + bc + "InvoicedQuantity").set('unitCode', _lines.unitCode)
            # item unit price
            line_deepcopy.find(".//" + bc + "PriceAmount").text = str(_lines.itemPriceAmount)
            # item discount rate
            line_deepcopy.find(".//" + bc + "MultiplierFactorNumeric").text = str(_lines.discount_rate)
            # item discount amount
            line_deepcopy.find(".//" + ac + "AllowanceCharge//" + bc + "Amount").text = str(_lines.discount_amount)
            # item tax rate
            line_deepcopy.find(".//" + bc + "Percent").text = str(_lines.taxpercent)
            # item tax amount
            line_deepcopy.find(".//" + bc + "TaxAmount").text = str(_lines.taxamount)
            # item amaount
            line_deepcopy.find(".//" + bc + "LineExtensionAmount").text = str(_lines.total_amount)

            invoicelines_root.addprevious(line_deepcopy)

        elemroot = invoicelines_root.getparent()

        elemroot.remove(invoicelines_root)

        #########################
        #
        # AMOUNT TABLE:
        #
        #########################

        # total amount of goods and services
        malhizmettoplamtutar_key = ".//" + ac + "LegalMonetaryTotal//" + bc + "LineExtensionAmount"
        self.change_single_values(self.root, malhizmettoplamtutar_key, self.randomXml.total_amount)

        # Total discount
        toplamiskonto_key = ".//" + ac + "LegalMonetaryTotal//" + bc + "AllowanceTotalAmount"
        self.change_single_values(self.root, toplamiskonto_key, self.randomXml.total_discount)

        # Tax amount
        hesaplanankdv_key = "./" + ac + "TaxTotal//" + bc + "TaxAmount"
        self.change_single_values(self.root, hesaplanankdv_key, self.randomXml.calculated_vat)

        # Tax rate
        hesaplanankdvorani_key = "./" + ac + "TaxTotal//" + bc + "Percent"
        self.change_single_values(self.root, hesaplanankdvorani_key, self.randomXml.calculated_vat_rate)

        # Total Amount Including Taxes
        vergilerdahiltoplamtutar_key = ".//" + ac + "LegalMonetaryTotal//" + bc + "TaxInclusiveAmount"
        self.change_single_values(self.root, vergilerdahiltoplamtutar_key, self.randomXml.payable_amount)

        # Amount to be paid
        odenecektutar_key = ".//" + ac + "LegalMonetaryTotal//" + bc + "PayableAmount"
        self.change_single_values(self.root, odenecektutar_key, self.randomXml.payable_amount)
