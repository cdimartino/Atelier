from __future__ import division
from __future__ import with_statement

import os
import sys
import xmlrpclib
import pickle
import re
from datetime import datetime

__PIDDIR__ = '/var/run/atelier_invoices'

class FileCreator(object):
  def create_batch_file_output(self, record):
    fmt = (
        '{batch_number}',
        ', ',
        '{date}',
        ', ',
        '{time}',
        ', ',
        '{header_count}',
        ', ',
        '{detail_count}'
    )
    return self.get_formatted_output((record, ), ''.join(fmt))

  def create_detail_file_output(self, records):
    fmt = (
      '{order_number!s:0>10.10s}', #required
      '{line_number!s:0>4.4s}',
      '{stock_number!s: <15.15s}', #required
      '{description_1!s: <30.30s}', #required
      '{description_2!s: <30.30s}', #required
      '{quantity_ordered!s:0>9.9s}', #ie 12 = 000012000
      '{unit_price!s:0>9.9s}', #ie 12 = 000012000
      '{unit_of_measure!s: <3.3s}',
      '{extended_price!s:0>9.9s}',
      '  ',
      '{discount_amount!s:0>8.8s}', #required
      '{client_line_id!s: >5.5s}',
      '{edi_item_qualifier!s: <2.2s}',
      '{edi_item_number!s: <15.15s}',
      '{customer_part_number!s: <15.15s}',
      '{line_item_taxable!s: >1.1s}', #required
      '{discount_percent!s:0>4.4s}',
      '{gift_to!s: <30.30s}',
      '{gift_from!s: <30.30s}',
      '{gift_txt1!s: <50.50s}',
      '{gift_txt2!s: <50.50s}',
      '{gift_txt3!s: <50.50s}',
      '{gift_txt4!s: <50.50s}',
      '{serial_number!s: <9.9s}'
    )
    return self.get_formatted_output(records, ''.join(fmt))

  def create_header_file_output(self, records):
    """Create the header file output

      :param records: Takes an iterable type of records
    """
    fmt = (
      '   ',
      '{order_number!s:0>7.7s}',
      '{location_number!s: <3.3s}',
      '{order_date!s: >8.8s}', #required
      '{shipping_date!s: >8.8s}', #required
      '{customer_number!s: <10.10s}', #required
      '{po_number!s: <15.15s}',
      '{salesperson_number!s: <3.3s}',
      '{ship_via_code!s: <3.3s}', #required
      '{terms_code!s: <3.3s}', #required
      '{comment!s: <45.45}', #required
      '{invoice_number!s: <10.10s}', #required
      '{invoice_date!s: <8.8s}', #required
      '{total_price!s:0>9.9s}', #required
      '{total_discount!s:0>7.7s}', #required
      '{bill_to_number!s: <6.6s}',
      '{bill_to_name!s: <30.30s}', #required
      '{bill_to_address_1!s: <30.30s}', #required
      '{bill_to_address_2!s: <30.30s}', #required
      '{bill_to_address_3!s: <30.30s}', #required
      '{bill_to_city!s: <15.15s}', #required
      '{bill_to_state!s: <2.2}', #required
      '{bill_to_zip!s: <10.10s}', #required
      '{bill_to_country!s: <3.3}', #required
      '{ship_to_number!s: <6.6s}', #required
      '{ship_to_name!s: <30.30s}', #required
      '{ship_to_address_1!s: <30.30s}', #required
      '{ship_to_address_2!s: <30.30s}', #required
      '{ship_to_address_3!s: <30.30s}', #required
      '{ship_to_city!s: <15.15s}', #required
      '{ship_to_state!s: <2.2}', #required
      '{ship_to_zip!s: <10.10s}', #required
      '{ship_to_country!s: <3.3}', #required
      '{ship_via_text!s: <15.15s}', #required
      '{terms_text!s: <15.15s}',
      '{client_customer_number!s: <15.15s}',
      '{department_number!s: <10.10s}',
      '{dist_center_number!s: <5.5s}',
      '{trading_partner_id!s: <5.5s}',
      '{batch_number!s: <6.6s}',
      '{vendor_code!s: <7.7s}',
      '{brand_code!s: <3.3s}',
      '{co_code!s: <2.2s}',
      '{carrier_code!s: <4.4s}', #required
      '{shipper_name!s: <25.25s}', #required
      '{cancel_date!s: >8.8s}',
      '{edi!s: >1.1s}',
      '{edi2!s: >1.1s}',
      '{ship_pay!s: <2.2s}',
      '{order_flag!s: <1.1s}',
      '{misc_chg_2!s: <3.3s}',
      '{misc_chg_3!s: <3.3s}',
      '{misc_chg_4!s: <3.3s}',
      '{sales_tax_code!s: <3.3s}', #required
      '{freight_amount!s:0>8.8s}', #required
      '{misc_chg_2_amount!s:0>8.8s}',
      '{misc_chg_3_amount!s:0>8.8s}',
      '{misc_chg_4_amount!s:0>8.8s}',
      '{long_order_number!s:0>10.10s}',
      '{division_number!s: <20.20s}',
      '{currency!s: <3.3s}',
      '{paper_invoice_flag!s: <1.1s}',
      '{send_email_flag!s: >1.1s}',
      '{email_address!s: <100.100s}',
      '{phone_number!s: <20.20s}',
      '{fax_number!s: <20.20s}'
    )
    return self.get_formatted_output(records, ''.join(fmt))

  def get_formatted_output(self, records, fmt):
    """Run the records through the format string and return an array of
    formatted values
    """
    return ( fmt.format(**record) for record in records )

  def fake_data(self, ):
    return [
      {
        'order_number': 8675309,
        'location_number': 123,
        'order_date': 20100822,
        'shipping_date': 20100825,
        'customer_number': 123456,
        'ship_via_code': 10,
        'terms_code': 'Cc',
        'comment': 'Send quickly please',
        'invoice_number': 543345,
        'invoice_date': 20100824,
        'total_price': 120250,
        'total_discount': 0,
        'bill_to_number': 22,
        'bill_to_name': 'Bill Hendrickson',
        'bill_to_address_1': '18 Joan Rd',
        'bill_to_city': 'Sandy',
        'bill_to_state': 'UT',
        'bill_to_zip': 144562233,
        'ship_to_number': 076,
        'ship_to_name': 'Home Plus',
        'ship_to_address_1': '#22233 Utah mall',
        'ship_to_address_2': '123 Big Rd.',
        'ship_to_city': 'Sandier',
        'ship_to_state': 'UT',
        'ship_to_zip': 998992233,
        'ship_via_text': 'None',
        'carrier_code': 12,
        'shipper_name': 'UPS',
        'salest_tax_code': 15,
        'freight_amount': 123430,
        'stock_number': '1123433aa22',
        'description_1': 'delicious goods',
        'description_2': 'they really are delicious',
        'quantity_ordered': 123000,
        'unit_price': 125000,
        'discount_percent': 0,
        'discount_amount': 0,
        'line_item_taxable': 'y'
      },
      {
        'order_number': 8675318,
        'location_number': 128,
        'order_date': 20100813,
        'shipping_date': 20100828,
        'customer_number': 123460,
        'ship_via_code': 8,
        'terms_code': 'cc',
        'comment': 'Send quickly please',
        'invoice_number': 543336,
        'invoice_date': 20100819,
        'total_price': 120243,
        'total_discount': 0,
        'bill_to_number': 22,
        'bill_to_name': 'Bill Hendrickson',
        'bill_to_address_1': '18 Joan Rd',
        'bill_to_city': 'Sandy',
        'bill_to_state': 'UT',
        'bill_to_zip': 144562237,
        'ship_to_number': 076,
        'ship_to_name': 'Home Plus',
        'ship_to_address_1': '#22238 Utah mall',
        'ship_to_address_2': '123 Big Rd.',
        'ship_to_city': 'Sandier',
        'ship_to_state': 'UT',
        'ship_to_zip': 998992237,
        'ship_via_text': 'None',
        'carrier_code': 12,
        'shipper_name': 'UPS',
        'salest_tax_code': 15,
        'freight_amount': 123432,
        'stock_number': '1123433aa22',
        'description_1': 'delicious goods',
        'description_2': 'they really are delicious',
        'quantity_ordered': 123000,
        'unit_price': 125000,
        'discount_percent': 0,
        'discount_amount': 0,
        'line_item_taxable': 'y'
      }
    ]

  def get_credentials(self):
    return dict(
        url = 'https://secure.ateliercologne.com/store/api/xmlrpc',
        username = 'order_extract',
        password = '3xtr@ct0r'
        )


class AtelierSvc(object):
  __sid = None
  __svc = None

  url = None
  username = None
  password = None

  def __init__(self, *args, **kwargs):
    self.url = kwargs['url']
    self.username = kwargs['username']
    self.password = kwargs['password']

  @property
  def sid(self):
    if self.__sid is None:
      sid = self.service.login(self.username, self.password)
      if not sid:
        print "Unable to log in!"
        sys.exit(1)
      self.__sid = sid
    return self.__sid

  @property
  def service(self):
    if self.__svc is None:
      self.__svc = xmlrpclib.ServerProxy(self.url)
    return self.__svc

  def call(self, method, *params):
    return self.service.call(self.sid, method, *params)

  def get_invoices(self, from_dt, to_dt):
    return [
      self.sales_order(i['increment_id']) for \
          i in self.call('sales_order.list', [{'created_at': {'from': from_dt, 'to': to_dt}}])
    ]

  def sales_order(self, id):
    return self.call('sales_order.info', [{'increment_id': id}])


class AtelierInvoiceDao(object):
  @staticmethod
  def map(svc_record, InvoiceOnly=False, BatchNumber=''):
    mapped = []
    for item_number, item in enumerate(svc_record['items']):
      mapped.append(dict(
        batch_number           = '',
        bill_to_address_1      = '', #required (set below)
        bill_to_address_2      = '', #required (set below)
        bill_to_address_3      = '', #required (set below)
        bill_to_city           = svc_record['billing_address']['city'], #required
        bill_to_name           = AtelierInvoiceDao.get_name(svc_record['billing_address']), #required
        bill_to_number         = '',
        bill_to_state          = AtelierInvoiceDao.map_state(svc_record['billing_address']['region']), #required
        bill_to_zip            = svc_record['billing_address']['postcode'], #required
        bill_to_country        = svc_record['billing_address']['country_id'], #required
        brand_code             = '',
        cancel_date            = '',
        carrier_code           = svc_record['shipping_method'], #required
        client_customer_number = '',
        client_line_id         = '',
        co_code                = '',
        comment                = '', #required
        customer_number        = '', #required
        customer_part_number   = '',
        currency               = svc_record.get('order_currency_code'),
        department_number      = '', ##????
        description_1          = item.get('description', '') or '', #required
        description_2          = '', #required
        discount_amount        = 0,
        discount_percent       = int(round(float(item['discount_percent']), 2)) * 100, #required
        discount_percent_short = int(round(float(item['discount_percent']), 2)), #required
        dist_center_number     = '', ##????
        division_number        = '',
        edi                    = 'N', ##????
        edi2                   = 'N', ##????
        edi_item_number        = '', ##????
        edi_item_qualifier     = '', ##????
        email_address          = svc_record['customer_email'],
        extended_price         = 0, ##???? Don't think this is available
        fax_number             = '',
        freight_amount         = int(float(svc_record['payment']['shipping_amount']) * 1000),
        gift_from              = '', ##???? Don't think this is available
        gift_to                = '', ##???? Don't think this is available
        gift_txt1              = '', ##???? Don't think this is available
        gift_txt2              = '', ##???? Don't think this is available
        gift_txt3              = '', ##???? Don't think this is available
        gift_txt4              = '', ##???? Don't think this is available
        invoice_date           = '',
        invoice_number         = '',
        line_item_taxable      = 'Y' if AtelierInvoiceDao.map_state(svc_record['billing_address']['region']) else 'N',
        line_number            = (item_number + 1) * 10, ##As per request
        location_number        = '', ##????
        long_customer_number   = '', ##????
        long_order_number      = '', ##????
        misc_chg_2             = '', ##????
        misc_chg_2_amount      = '', ##????
        misc_chg_3             = '', ##????
        misc_chg_3_amount      = '', ##????
        misc_chg_4             = '', ##????
        misc_chg_4_amount      = '', ##????
        order_date             = AtelierInvoiceDao.format_date(svc_record['created_at']), #required
        order_flag             = '', ##????
        order_number           = int(svc_record['order_id']) + 500000, #required
        paper_invoice_flag     = 'M',
        po_number              = 'WEB%s' % (svc_record['payment']['po_number'], ), ## WEB+PONUM
        phone_number           = '',
        quantity_ordered       = int(float(svc_record['total_qty_ordered'])) * 1000, #ie 12=000012000
        salesperson_number     = 'WEB', ##WEB
        sales_tax_code         = int(float(item['tax_percent']) * 100), #required ##???? ##We don't appear to have tax codes
        send_email_flag        = 'N', ##????
        serial_number          = '', ##????
        ship_pay               = 'PP', ##????
        ship_to_address_1      = '', #required (set below)
        ship_to_address_2      = '', #required (set below)
        ship_to_address_3      = '', #required (set below)
        ship_to_city           = svc_record['shipping_address']['city'], #required
        ship_to_name           = AtelierInvoiceDao.get_name(svc_record['shipping_address']), #required
        ship_to_number         = '', #required
        ship_to_state          = AtelierInvoiceDao.map_state(svc_record['shipping_address']['region']), #required
        ship_to_zip            = svc_record['shipping_address']['postcode'], #required
        ship_to_country        = svc_record['shipping_address']['country_id'], #required
        ship_via_code          = svc_record['shipping_method'], #required
        ship_via_text          = svc_record['shipping_description'], #required
        shipper_name           = svc_record['shipping_method'].upper(), #required
        shipping_date          = '', #required ##Don't think this is provided
        stock_number           = item.get('sku', '') or '', #required ##????
        store_number           = item['store_id'],
        terms_code             = 'CC', ##CC
        terms_text             = 'CREDIT CARD', ##????
        total_discount         = 0, ## As per request
        total_price            = 0, ## As per request
        trading_partner_id     = '', ##????
        unit_of_measure        = 'EA',
        unit_price             = int(round(float(item['price']), 3)) * 1000, #ie 12=000012000
        vendor_code            = '' ##????
        )
      )
      mapped[-1]['bill_to_address_1'], mapped[-1]['bill_to_address_2'], mapped[-1]['bill_to_address_3'] = \
        AtelierInvoiceDao.get_address(svc_record['billing_address']['street'])
      mapped[-1]['ship_to_address_1'], mapped[-1]['ship_to_address_2'], mapped[-1]['ship_to_address_3'] = \
        AtelierInvoiceDao.get_address(svc_record['shipping_address']['street'])

      if InvoiceOnly:
        ## If invoiceonly is set, only run through once (not for all line items)
        break
    return tuple(mapped)

  @staticmethod
  def map_state(name):
    states = dict({
        'Alabama'           : 'AL',
        'Alaska'            : 'AK',
        'American Samoa'    : 'AS',
        'Arizona'           : 'AZ',
        'Arkansas'          : 'AR',
        'California'        : 'CA',
        'Colorado'          : 'CO',
        'Connecticut'       : 'CT',
        'Delaware'          : 'DE',
        'Dist. of Columbia' : 'DC',
        'Florida'           : 'FL',
        'Georgia'           : 'GA',
        'Guam'              : 'GU',
        'Hawaii'            : 'HI',
        'Idaho'             : 'ID',
        'Illinois'          : 'IL',
        'Indiana'           : 'IN',
        'Iowa'              : 'IA',
        'Kansas'            : 'KS',
        'Kentucky'          : 'KY',
        'Louisiana'         : 'LA',
        'Maine'             : 'ME',
        'Maryland'          : 'MD',
        'Marshall Islands'  : 'MH',
        'Massachusetts'     : 'MA',
        'Michigan'          : 'MI',
        'Micronesia'        : 'FM',
        'Minnesota'         : 'MN',
        'Mississippi'       : 'MS',
        'Missouri'          : 'MO',
        'Montana'           : 'MT',
        'Nebraska'          : 'NE',
        'Nevada'            : 'NV',
        'New Hampshire'     : 'NH',
        'New Jersey'        : 'NJ',
        'New Mexico'        : 'NM',
        'New York'          : 'NY',
        'North Carolina'    : 'NC',
        'North Dakota'      : 'ND',
        'Northern Marianas' : 'MP',
        'Ohio'              : 'OH',
        'Oklahoma'          : 'OK',
        'Oregon'            : 'OR',
        'Palau'             : 'PW',
        'Pennsylvania'      : 'PA',
        'Puerto Rico'       : 'PR',
        'Rhode Island'      : 'RI',
        'South Carolina'    : 'SC',
        'South Dakota'      : 'SD',
        'Tennessee'         : 'TN',
        'Texas'             : 'TX',
        'Utah'              : 'UT',
        'Vermont'           : 'VT',
        'Virginia'          : 'VA',
        'Virgin Islands'    : 'VI',
        'Washington'        : 'WA',
        'West Virginia'     : 'WV',
        'Wisconsin'         : 'WI',
        'Wyoming'           : 'WY'
        })
    try:
      return states[name]
    except KeyError:
      ## If state is unknown
      return 'NA'

  @staticmethod
  def get_name(record):
    first_name = record.get('firstname', '')
    last_name = record.get('lastname', '')
    if record.get('middlename'):
      return "%s %s %s" % (first_name, record.get('middlename'), last_name)
    else:
      return "%s %s" % (first_name, last_name)

  @staticmethod
  def get_address(value):
    addr = re.split("[\r\n]+", value, maxsplit=3)
    while len(addr) < 3:
      addr.append('')
    return tuple(addr)

  @staticmethod
  def format_date(date):
    d = re.compile('(\d+)-(\d+)-(\d+)')
    m = d.match(date)
    return "%04d%02d%02d" % ( int(m.group(1)), int(m.group(2)), int(m.group(3)) )


def main():
  now = datetime.now()
  batch_number = now.strftime('%y%m%d')
  creator = FileCreator()

  sys.stderr.write("Getting credentials\n")

  a = AtelierSvc(**creator.get_credentials())
  # Need to pull only invoices since last pull
  sys.stderr.write("Getting invoices\n")
  invoices = a.get_invoices('2010-01-01', '2010-12-01')

  record_counts = dict(
      header = 0,
      detail = 0
  )

  sys.stderr.write("Creating header file\n")
  with open('H%s' % (batch_number, ), 'w') as file:
    for item in invoices:
      for output in creator.create_header_file_output(AtelierInvoiceDao.map(item, InvoiceOnly=True, BatchNumber=batch_number)):
        record_counts['header'] += 1
        file.write(output)
        file.write("\n")

  sys.stderr.write("Creating detail file\n")
  with open('D%s' % (batch_number, ), 'w') as file:
    for item in invoices:
      for output in creator.create_detail_file_output(AtelierInvoiceDao.map(item, BatchNumber=batch_number)):
        record_counts['detail'] += 1
        file.write(output)
        file.write("\n")

  sys.stderr.write("Creating batch file\n")
  with open("B%s" % (batch_number, ), 'w') as file:
    record = {
        'batch_number': batch_number,
        'date': now.strftime('%Y%m%d'),
        'time': now.strftime('%I:%M:%S%p'),
        'header_count': record_counts['header'],
        'detail_count': record_counts['detail']
        }
    for output in creator.create_batch_file_output(record):
      file.write(output)
      file.write("\n")

  sys.stderr.write("Done")

def histfile():
  pass

def get_lock():
  if not os.path.exists(piddir()):
    sys.stderr.write("Piddir: %s does not exist.  Please create this directory and retry.\n" % piddir())
    sys.exit(1)

  if os.path.exists(pidfile()):
    # Check to see if the process is still running
    oldpid = open(pidfile()).read()
    try:
      os.getpgid(int(oldpid))
    except OSError:
      pass
      # This means the pid is not running.  This is ok.
    else:
      sys.stderr.write("Existing process with pid %s.  Exiting.\n" % (oldpid,))
      sys.exit(1)
    os.unlink(pidfile())
  try:
    with open(pidfile(), 'w') as file:
        file.write(str(os.getpid()))
  except IOError:
    sys.stderr.write("Pidfile Error: %s path does exist or is not writable.  Cannot continue\n" % (pidfile(), ))
    sys.exit(1)

def remove_lock():
  os.unlink(pidfile())

def piddir():
  return __PIDDIR__

def pidfile():
  return os.path.join(piddir(), 'running.pid')

def program_name():
  return os.path.basename(sys.argv[0])

if __name__ == '__main__':
  get_lock()
  main()
  remove_lock()
