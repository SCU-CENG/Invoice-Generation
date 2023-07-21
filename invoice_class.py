# -*- coding: utf-8 -*-

import numpy as np
import random

from random import randint as ri
from random import randrange
from datetime import timedelta
from datetime import datetime
from string import ascii_lowercase, digits

charlist = ascii_lowercase[:6] + digits

tax_list = np.loadtxt("csv_file/tax_list.csv", dtype=str, delimiter="\t")
company_list = np.loadtxt("csv_file/company_list.csv", dtype=str, delimiter="\t")
itm_list = open("csv_file/item_list.csv", "r", encoding="utf8").read().replace("\xa0", "").splitlines()[1:]

note_list = open("csv_file/note_list.csv", "r").read().replace("\xa0", "").splitlines()[1:]
address_list = open("csv_file/addresses.csv").read().replace("\xa0", "").splitlines()[1:]
tel_list = open("csv_file/telephone.csv").read().replace("\xa0", "").splitlines()[1:]
fax_list = open("csv_file/fax_number.csv").read().replace("\xa0", "").splitlines()[1:]

# birim miktar tipleri paket, kg, m2, ton vs.
quantity_types = ["TNE", "BX", "LTR", "C62", "KGM", "NT", "MTR", "MMQ", "PA", "NCL", "DZN", "DAY"]


class RandomInvoice:
    def __init__(self):

        # invoice id
        # GIB yerine EFA, I54, S01
        self.InvoiceID = "GIB" + random.choice(["2018", "2019", "2020", "2021", "2022"]) + str("%09d" % ri(0, 9999))

        # uuid = ettn
        self.InvoiceUUID = self.ett_string(8) + "-" + self.ett_string(4) + "-" + self.ett_string(
            4) + "-4" + self.ett_string(3) + "-" + self.ett_string(12)

        # invoice date
        self.InvoiceIssueDate = self.generate_date()

        # invoice type
        self.InvoiceTypeCode = "SATIS"

        # invoice profile
        self.InvoiceProfileID = "EARSIVFATURA"

        # waybill id
        if ri(0, 50) > 42:

            if ri(0, 50) > 46:
                say = ri(1, 4)
                txt = ''
                for ts in range(say):
                    txt += str("%06d" % ri(0, 999999))
                    txt += ' '
                self.DispatchID = txt
            else:
                self.DispatchID = str("%06d" % ri(0, 999999))

            # waybill date
            self.DispatchIssueDate = self.generate_date(False)
        else:
            self.DispatchID = False
            self.DispatchIssueDate = False

        if ri(0, 50) > 46:
            # Order id and date
            self.OrderID = str("%10d" % ri(0, 9999999999))
            self.OrderIssueDate = self.generate_date(False)
        else:
            self.OrderID = False
            self.OrderIssueDate = False

        # Note
        if ri(0, 10) > 4:
            self.Note = random.choice(note_list)
        else:
            self.Note = False

        # Sender information
        self.AccountingSupplierParty = AccountingSupplierParty()

        # Receiver Informations
        self.AccountingCustomerParty = AccountingCustomerParty()

        # count of line list
        line_list = np.zeros(1175, np.int32)
        line_list[0:120] = 1  # 220
        line_list[120:220] = 2  # 150
        line_list[220:315] = 3  # 120
        line_list[315:405] = 4  # 90
        line_list[405:485] = 5  # 80
        line_list[485:560] = 6  # 75
        line_list[560:628] = 7  # 68
        line_list[628:688] = 8  # 60
        line_list[688:740] = 9  # 52
        line_list[740:784] = 10  # 44
        line_list[784:822] = 11  # 38
        line_list[822:854] = 12  # 32
        line_list[854:880] = 13  # 26
        line_list[880:902] = 14  # 22
        line_list[902:920] = 15  # 18
        line_list[920:935] = 16  # 15
        line_list[935:947] = 17  # 12
        line_list[947:957] = 18  # 10
        line_list[957:966] = 19  # 9
        line_list[966:974] = 20  # 8

        for i in range(974, 1000):
            line_list[i:i + 1] = ri(21, 30)

        line_list[1000:1100] = 1
        line_list[1100:1150] = 2
        line_list[1150:1175] = 3

        # select count of line list
        line_count = random.choice(line_list)

        # item list
        self.invoiceLine = [InvoiceLine() for i in range(line_count)]

        # Information on the PAYMENT

        # Goods/Service Total Amount
        self.total_amount = sum([i.total_amount_without_discount for i in self.invoiceLine])

        # Total discount
        self.total_discount = sum([i.discount_amount for i in self.invoiceLine])

        # Get the most occurrence vat in the list
        vat_list = [i.taxpercent for i in self.invoiceLine]
        self.calculated_vat_rate = max(vat_list, key=vat_list.count)
        self.calculated_vat = sum([i.taxamount for i in self.invoiceLine])

        # Payable Amount
        self.payable_amount = self.total_amount - self.total_discount + self.calculated_vat

        # Payment Means
        self.PaymentMeans = PaymentMeans()

    @staticmethod
    def generate_date(full=True):
        start = datetime.strptime('1/1/2015 11:59 PM', '%d/%m/%Y %I:%M %p')
        end = datetime.strptime('1/1/2025 12:00 AM', '%d/%m/%Y %I:%M %p')
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        k = start + timedelta(seconds=random_second)

        if full:
            return k.strftime('%Y-%m-%d %H:%M')

        else:
            return k.strftime('%Y-%m-%d')

    @staticmethod
    def ett_string(_size):

        return ''.join(random.choice(charlist) for _ in range(_size))


class PaymentMeans:
    def __init__(self):
        self.PaymentMeansCode = ""
        self.PaymentDueDate = ""
        self.InstructionNote = ""


class AccountingCustomerParty:
    def __init__(self):

        # Receiver Information

        # select company randomly
        _company_name, _mail, _type = random_firma_vkn_mail()

        _tax_number = ri(1000000000, 9999999999)

        self.buyer_type = _type
        self.buyer_company = _company_name

        # alıcı tipine göre tckn yada vkn yazdırılabilir.

        if _type == "firma":
            self.buyer_tax = _tax_number
            self.buyer_tckn = False

            if ri(1, 9) > 8:
                _tckn = ri(10000000000, 99999999999)
                self.buyer_tckn = _tckn + 1 if _tckn % 2 == 0 else _tckn

        else:
            self.buyer_tax = False
            self.buyer_tckn = _tax_number

            if ri(1, 9) > 8:
                self.buyer_tax = ri(1000000000, 9999999999)

        self.buyer_mail = _mail

        self.buyer_web = "www." + str(_mail.split("@")[1])

        city, tax_office = city_district()

        self.buyer_city = city
        self.buyer_tax_office = tax_office

        self.buyer_address = random.choice(address_list)

        self.buyer_postal_code = "58000"

        self.buyer_tel = random.choice(tel_list)

        self.buyer_fax = random.choice(fax_list)

        if ri(0, 10) > 1:
            self.buyer_postal_code = ' '

        if ri(1, 10) > 7:
            self.buyer_web = ' '
            self.buyer_mail = ' '
            self.buyer_tel = ' '
            self.buyer_fax = ' '
        else:
            if ri(0, 10) > 7:
                self.buyer_web = ' '

            if ri(0, 10) > 7:
                self.buyer_mail = ' '

            if ri(1, 10) > 7:
                self.sender_tel = ' '
                self.sender_fax = ' '
            else:
                if ri(1, 9) > 4:
                    self.sender_fax = ' '


class AccountingSupplierParty:
    def __init__(self):

        # SENDER INFO

        # randomly select city, county and tax office
        city, tax_office = city_district()

        self.sender_city = city
        self.sender_tax_office = tax_office

        # rastgele firma vkn, adı, maili ve şahıs/firma tipini seç
        _company_name, _mail, _type = random_firma_vkn_mail()

        _tax_number = ri(1000000000, 9999999999)

        self.sender_type = _type
        self.sender_company = _company_name

        # tckn or tax number can be printed depending on the sender's type.

        if _type == "firma":
            self.sender_tax_number = _tax_number
            self.sender_tckn = False

            if ri(0, 10) > 7:
                _tckn = ri(10000000000, 99999999999)
                self.sender_tckn = _tckn + 1 if _tckn % 2 == 0 else _tckn

        else:
            self.sender_tax_number = False
            self.sender_tckn = _tax_number

            if ri(0, 10) > 9:
                self.sender_tax_number = ri(1000000000, 9999999999)

        self.sender_mersis = str("%016d" % random.randint(99999999999999, 9999999999999999))

        self.sender_mail = _mail

        self.sender_web = "www." + str(_mail.split("@")[1])

        self.gonderenadres = random.choice(address_list)

        self.sender_postal_code = "03000"

        self.sender_tel = random.choice(tel_list)
        self.sender_fax = random.choice(fax_list)

        if ri(1, 10) > 4:
            self.sender_mersis = False

        if ri(1, 10) > 7:
            self.sender_mail = ' '

        if ri(1, 10) > 7:
            self.sender_web = ' '

        if ri(1, 10) > 4:
            self.sender_postal_code = False

        if ri(1, 10) > 7:
            self.sender_tel = ' '
            self.sender_fax = ' '
        else:
            if ri(1, 9) > 4:
                self.sender_fax = ' '


class InvoiceLine:
    def __init__(self):

        # Goods - Service Name
        self.itemName = random.choice(itm_list)

        # Quantity Type & Quantity and Unit Price
        self.unitCode = random.choice(quantity_types)
        self.quantity = ri(1, 100)
        self.itemPriceAmount = ri(3, 250)

        ######
        # If there is a discount field, it will be all, otherwise it will be empty.
        ######

        # discount rate ... attention 1=%100
        self.discount_rate = 0

        # discount amount
        self.discount_amount = 0

        if ri(0, 10) > 8:
            self.discount_rate = ri(1, 10) / 100.
            self.discount_amount = (self.quantity * self.itemPriceAmount) * self.discount_rate

        ######

        # Total Amount : LineExtensionAmount # calculated area olacak !
        # For non-discounted goods and services only!
        self.total_amount_without_discount = (self.quantity * self.itemPriceAmount)

        self.total_amount = (self.quantity * self.itemPriceAmount) - self.discount_amount

        # tax-related fields
        # tax rate
        self.taxpercent = random.choice([8, 18])

        # tax amount  --> will be calculated area!
        self.taxamount = self.total_amount * (self.taxpercent / 100.)


# choose randomly from list of companies, first element name, next mail, last type:
def random_firma_vkn_mail(tip=False):
    if not tip:
        return random.choice(company_list)
    else:
        _elem = random.choice(company_list)
        if tip in _elem[2]:
            return _elem
        else:
            return random_firma_vkn_mail(tip)


def city_district():
    elem = random.choice(tax_list)
    if "mal" in elem[2].lower():
        return city_district()

    if ri(0, 10) > 3:
        return '', elem[2]
    else:
        return elem[1] + "/ " + elem[0], elem[2]


def random_tel_fax():
    pass
