import sys
import xmlrpclib
import re

def create_detail_file_output(records):
  fmt = (
    ('%06d', 'order_number'), #required
    ('%04d', 'line_number'),
    ('%15s', 'stock_number'), #required
    ('%30s', 'description_1'), #required
    ('%30s', 'description_2'), #required
    ('%09d', 'quantity_ordered'), #required (3 implied decimal, ie 12 = 000012000
    ('%09d', 'unit_price'), #required (3 implied decimal, ie 12 = 000012000
    ('%3s', 'unit_of_measure'),
    ('%09d', 'extended_price'),
    ('%02d', 'discount_percent'), #required
    ('%07d', 'discount_amount'), #required
    ('%s', 'client_line_id'),
    ('%2s', 'edi_item_qualifier'),
    ('%15s', 'edi_item_number'),
    ('%15s', 'customer_part_number'),
    ('%1s', 'line_item_taxable'), #required
    ('%04d', 'discount_percent'),
    ('%30s', 'gift_from'),
    ('%30s', 'gift_to'),
    ('%50s', 'gift_txt1'),
    ('%50s', 'gift_txt2'),
    ('%50s', 'gift_txt3'),
    ('%50s', 'gift_txt4'),
    ('%9s', 'serial_number')
  )
  return get_formatted_output(records, fmt)

def create_header_file_output(records):
  """Create the header file output

    :param records: Takes an iterable type of records
  """
  fmt = (
    ('%06d' , 'order_number')          , # required
    ('%3s'  , 'location_number')       ,
    ('%8s'  , 'order_date')            , #required
    ('%8s'  , 'shipping_date')         , #required
    ('%6s'  , 'customer_number')       , #required
    ('%15s' , 'po_number')             ,
    ('%3s'  , 'salesperson_number')    ,
    ('%3s'  , 'ship_via_code')         , #required
    ('%3s'  , 'terms_code')            , #required
    ('%30s' , 'comment')               , #required
    ('%6s'  , 'invoice_number')        , #required
    ('%8s'  , 'invoice_date')          , #required
    ('%9s'  , 'total_price')           , #required
    ('%7s'  , 'total_discount')        , #required
    ('%6s'  , 'bill_to_number')        ,
    ('%30s' , 'bill_to_name')          , #required
    ('%30s' , 'bill_to_address_1')     , #required
    ('%30s' , 'bill_to_address_2')     , #required
    ('%30s' , 'bill_to_address_3')     , #required
    ('%15s' , 'bill_to_city')          , #required
    ('%10s' , 'bill_to_state')         , #required
    ('%10s' , 'bill_to_zip')           , #required
    ('%6s'  , 'ship_to_number')        , #required
    ('%30s' , 'ship_to_name')          , #required
    ('%30s' , 'ship_to_address_1')     , #required
    ('%30s' , 'ship_to_address_2')     , #required
    ('%30s' , 'store_number')          ,
    ('%15s' , 'ship_to_city')          , #required
    ('%10s' , 'ship_to_state')         , #required
    ('%10s' , 'ship_to_zip')           , #required
    ('%15s' , 'ship_via_text')         , #required
    ('%15s' , 'terms_text')            ,
    ('%10s' , 'client_customer_number'),
    ('%10s' , 'department_number')     ,
    ('%5s'  , 'dist_center_number')    ,
    ('%5s'  , 'trading_partner_id')    ,
    ('%6s'  , 'batch_number')          ,
    ('%7s'  , 'vendor_code')           ,
    ('%3s'  , 'brand_code')            ,
    ('%2s'  , 'co_code')               ,
    ('%4s'  , 'carrier_code')          , #required
    ('%25s' , 'shipper_name')          , #required
    ('%8s'  , 'cancel_date')           ,
    ('%1s'  , 'edi')                   ,
    ('%2s'  , 'ship_pay')              ,
    ('%15s' , 'long_customer_number')  ,
    ('%1s'  , 'order_flag')            ,
    ('%3s'  , 'misc_chg_2')            ,
    ('%3s'  , 'misc_chg_3')            ,
    ('%3s'  , 'misc_chg_4')            ,
    ('%3s'  , 'salest_tax_code')       , #required
    ('%7s'  , 'freight_amount')        , #required
    ('%7s'  , 'misc_chg_2_amount')     ,
    ('%7s'  , 'misc_chg_3_amount')     ,
    ('%7s'  , 'misc_chg_4_amount')     ,
    ('%10s' , 'long_order_number')     ,
    ('%1s'  , 'send_email_flag')       ,
    ('%100s', 'email_address')
  )
  return get_formatted_output(records, fmt)

def get_formatted_output(records, fmt):
  """Run the records through the format string and return an array of
  formatted values
  """
  d = re.compile('%\d+d$')
  str_format = ''.join([ a[0] for a in fmt ])
  defaults   = [ 0 if d.match(a[0]) else '' for a in fmt ]
  columns    = [ a[-1] for a in fmt ]
  return [ str_format % tuple([ rec.get(key, defaults[x]) for x, key in enumerate(columns) ]) for rec in records ]

def fake_data():
  return [
    {
      'order_number': 8675309,
      'location_number': 123,
      'order_date': 20100822,
      'shipping_date': 20100825,
      'customer_number': 123456,
      'ship_via_code': 10,
      'terms_code': 'cc',
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

def login(url, username, password):
  c = xmlrpclib.ServerProxy(url)
  sid = c.login(username, password)
  if not sid:
    print "Unable to log in!"
    sys.exit
  return sid

def main():
#  sid = login('https://secure.ateliercologne.com/store/api/xmlrpc',
#              'order_extract',
#              '3xtr@ct0r')
  print "\n".join(create_header_file_output(fake_data()))
  print "\n".join(create_detail_file_output(fake_data()))

if __name__ == '__main__':
  main()
