'''
Created on 7 Jul 2021

@author: jacklok
'''

from flask import Blueprint, request, session 
from flask_restful import abort
import logging
from trexlib.utils.log_util import get_tracelog
from flask_restful import Api
from trexmodel.utils.model.model_util import create_db_client
from flask.json import jsonify
from datetime import datetime
from trexapi.decorators.api_decorators import auth_token_required,\
    outlet_key_required
from trexlib.utils.string_util import is_not_empty
from trexmodel.models.datastore.customer_models import Customer
from trexmodel.models.datastore.user_models import User
from trexadmin.libs.http import create_rest_message
from trexadmin.libs.http import StatusCode
from trexmodel.models.datastore.merchant_models import Outlet,\
    MerchantAcct, MerchantUser
from trexapi.forms.customer_api_forms import CustomerDetailsNewForm, CustomerDetailsUpdateForm,\
    CustomerSearchForm
from werkzeug.datastructures import ImmutableMultiDict
import gettext
from trexapi.controllers.user_api_routes import user_details_dict
from trexmodel.models.datastore.transaction_models import CustomerTransaction
from trexapi.utils.api_helpers import get_logged_in_api_username

logger = logging.getLogger('api')


customer_api_bp = Blueprint('customer_api_base_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/customers')

logger = logging.getLogger('api')

customer_api = Api(customer_api_bp)



@customer_api_bp.route('/register', methods=['POST'])
@auth_token_required
@outlet_key_required
def create_customer():
    customer_data_in_json   = request.get_json()
    register_customer_form  = CustomerDetailsNewForm(ImmutableMultiDict(customer_data_in_json))
    
    logger.debug('create_customer: customer_data_in_json=%s', customer_data_in_json)
    
    try:
        if register_customer_form.validate():
            logger.debug('customer registration input is valid')
            db_client = create_db_client(caller_info="create_customer")
            
            is_email_used           = False
            is_mobile_phone_used    = False
            customer_is_exist       = False
            created_customer        = None
            created_user_acct       = None
            
            outlet_key  = request.headers.get('x-outlet-key')
            acct_id     = request.headers.get('x-acct-id')
            
            logger.debug('outlet_key=%s', outlet_key)
            logger.debug('acct_id=%s', acct_id)
            
            with db_client.context():
                merchant_acct   = MerchantAcct.fetch(acct_id)
                outlet          = Outlet.fetch(outlet_key)
                
                email           = customer_data_in_json.get('email')
                mobile_phone    = customer_data_in_json.get('mobile_phone')
                
                birth_date              = customer_data_in_json.get('birth_date')
                            
                if is_not_empty(birth_date):
                    birth_date = datetime.strptime(birth_date, '%d/%m/%Y')
                
                logger.debug('birth_date=%s', birth_date)

                
                logger.debug('email=%s', email)
                logger.debug('mobile_phone=%s', mobile_phone)
                
                if is_not_empty(email):
                    created_user_acct = User.get_by_email(email)
                    
                    #if created_user_acct and created_user_acct.is_email_verified:
                    if created_user_acct:    
                        is_email_used = True
                
                if is_not_empty(mobile_phone):
                    mobile_phone = mobile_phone.replace(" ", "")
                    created_user_acct = User.get_by_mobile_phone(mobile_phone)
                    
                    #if created_user_acct and created_user_acct.is_mobile_phone_verified:
                    if created_user_acct:
                        is_mobile_phone_used = True
                
                
                logger.debug('is_email_used=%s', is_email_used)
                logger.debug('is_mobile_phone_used=%s', is_mobile_phone_used)
                
                if merchant_acct and outlet:
                        
                    logger.debug('merchant_acct.key_in_str=%s', merchant_acct.key_in_str)
                    logger.debug('outlet.merchant_acct_key=%s', outlet.merchant_acct_key)
                    
                    if merchant_acct.key_in_str == outlet.merchant_acct_key: 
                        logger.debug('Valid granted outlet key for merchant acct')
                                                    
                        if is_email_used:
                            created_customer = Customer.get_by_email(email)
                            
                        elif is_mobile_phone_used:
                            created_customer = Customer.get_by_mobile_phone(mobile_phone)
                        
                        if is_email_used or is_mobile_phone_used:
                            if created_customer is None:
                                logger.debug('User account have been created, but customer account is not yet created')
                                
                                created_user_acct = User.update(created_user_acct,
                                                                name                    = customer_data_in_json.get('name'), 
                                                                email                   = customer_data_in_json.get('email'), 
                                                                gender                  = customer_data_in_json.get('gender'),
                                                                birth_date              = birth_date,
                                                                mobile_phone            = mobile_phone, 
                                                                password                = customer_data_in_json.get('password'),
                                                                )
                                
                                created_customer        = Customer.create_from_user(outlet, created_user_acct, customer_data_in_json.get('merchant_reference_code'))
                            
                            else:
                                customer_is_exist = True
                                logger.warn('Customer account using same email or mobile phone have been created')
                        else:
                            created_customer        = Customer.create( 
                                                            outlet                  = outlet, 
                                                            name                    = customer_data_in_json.get('name'), 
                                                            email                   = customer_data_in_json.get('email'), 
                                                            gender                  = customer_data_in_json.get('gender'),
                                                            birth_date              = birth_date,
                                                            mobile_phone            = mobile_phone, 
                                                            merchant_reference_code = customer_data_in_json.get('merchant_reference_code'), 
                                                            password                = customer_data_in_json.get('password'),
                                                            )
                        logger.debug('created_customer=%s', created_customer)
                    else:
                        logger.warn('Invalid granted outlet key')
                else:
                    logger.warn('Invalid granted outlet key')
            
                if customer_is_exist:
                    if is_email_used==True:
                        return create_rest_message('Email have been taken', status_code=StatusCode.BAD_REQUEST)
                    
                    elif is_mobile_phone_used==True:
                        return create_rest_message('Mobile phone have been taken', status_code=StatusCode.BAD_REQUEST)
                    
                
                if created_customer:
                    created_user_acct = created_customer.registered_user_acct
                    response_data = {
                                'customer_key'              : created_customer.key_in_str,
                                'registered_datetime'       : created_customer.registered_datetime.strftime("%d-%m-%Y %H:%M:%S"),
                                'merchant_reference_code'   : created_customer.merchant_reference_code,
                                'reference_code'            : created_customer.reference_code,
                                'merchant_account_key'      : acct_id,
                                'company_name'              : merchant_acct.company_name,
                                'outlet_key'                : outlet_key,  
                                
                                }
                
                    logger.debug('response_data=%s', response_data)
                    
                    response_data.update(user_details_dict(created_user_acct))
                    
                    return create_rest_message(status_code=StatusCode.OK, **response_data)
                    
                else:
                    return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            
        else:
            logger.warn('customer registration input is invalid')
            error_message = register_customer_form.create_rest_return_error_message()
            
            return create_rest_message(error_message, status_code=StatusCode.BAD_REQUEST)
    except:
        logger.error('Fail to register customer due to %s', get_tracelog())
        
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)


@customer_api_bp.route('/reference-code/<ref_code>', methods=['GET'])
@auth_token_required
def read_customer(ref_code):
    
    logger.debug('ref_code=%s', ref_code)
    
    if is_not_empty(ref_code):
        db_client = create_db_client(caller_info="read_customer")
        
        acct_id     = request.headers.get('x-acct-id')
        
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(acct_id)
            customer = Customer.get_by_reference_code(ref_code, merchant_acct)
            
        
        if customer:
        
            user_details = customer.registered_user_acct
            customer_details_dict = customer.to_dict(date_format="%d-%m-%Y", datetime_format="%d-%m-%Y %H:%M:%S")
            customer_details_dict['customer_key']               = customer.key_in_str
            customer_details_dict['is_email_verified']          = user_details.is_email_verified
            customer_details_dict['is_mobile_phone_verified']   = user_details.is_mobile_phone_verified
            
            if 'entitled_voucher_summary' in customer_details_dict:
                customer_details_dict['voucher_summary']            = customer.entitled_voucher_summary
                del customer_details_dict['entitled_voucher_summary']
            
            return jsonify(customer_details_dict)
            
        else:
            logger.warn('Customer with reference code (%s) is not found', ref_code)
            return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            
    else:
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)
    
@customer_api_bp.route('/customer-key/<customer_key>', methods=['GET'])
@auth_token_required
def read_customer_by_customer_key(customer_key):
    
    logger.debug('customer_key=%s', customer_key)
    
    if is_not_empty(customer_key):
        db_client = create_db_client(caller_info="read_customer_by_customer_key")
        
        with db_client.context():
            customer = Customer.fetch(customer_key)
            
        
        if customer:
            '''
            customer_property_list = ['name', 'email', 'mobile_phone', 'gender', 'birth_date', 'merchant_reference_code']
            
            response_data = {
                        'customer_key'              : customer.key_in_str,
                        'registered_datetime'       : customer.registered_datetime.strftime("%d-%m-%Y %H:%M:%S"),
                        'merchant_reference_code'   : customer.merchant_reference_code,
                        'merchant_account_key'      : customer.registered_merchant_acct_key,
                        'outlet_key'                : customer.registered_outlet_key,  
                        'user_details'              : user_details_dict(user_details_dict), 
                        }
            '''
            
            user_details = customer.registered_user_acct
            customer_details_dict = customer.to_dict(date_format="%d-%m-%Y", datetime_format="%d-%m-%Y %H:%M:%S")
            customer_details_dict['customer_key']               = customer.key_in_str
            customer_details_dict['is_email_verified']          = user_details.is_email_verified
            customer_details_dict['is_mobile_phone_verified']   = user_details.is_mobile_phone_verified
            
            if 'entitled_voucher_summary' in customer_details_dict:
                customer_details_dict['voucher_summary']            = customer.entitled_voucher_summary
                del customer_details_dict['entitled_voucher_summary']
            
            return jsonify(customer_details_dict)
            #return jsonify(response_data)
            
        else:
            logger.warn('Customer with customer_key (%s) is not found', customer_key)
            return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            
    else:
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)    


@customer_api_bp.route('/customer-key/<customer_key>', methods=['PUT'])
@auth_token_required
def update_customer(customer_key):
    customer_data_in_json   = request.get_json()
    updating_customer_form  = CustomerDetailsUpdateForm(ImmutableMultiDict(customer_data_in_json))
    
    logger.debug('update_customer: customer_data_in_json=%s', customer_data_in_json)
    
    try:
        if updating_customer_form.validate():
            logger.debug('customer update input is valid')
            db_client = create_db_client(caller_info="update_customer")
            
            is_email_used                           = False
            is_mobile_phone_used                    = False
            customer_is_exist                       = False
            updating_customer                       = None
            checking_user_acct                      = None
            is_customer_email_changed               = False
            is_customer_mobile_phone_changed        = False
            is_used_email_same_user_acct            = False
            is_used_mobile_phone_same_user_acct     = False
            
            with db_client.context():
                email               = customer_data_in_json.get('email')
                mobile_phone        = customer_data_in_json.get('mobile_phone')
                
                if mobile_phone:
                    mobile_phone = mobile_phone.replace(" ", "")
                
                updating_customer   = Customer.fetch(customer_key)
                
                if updating_customer:
                    customer_is_exist = True
                    is_customer_email_changed           = updating_customer.email!=email
                    is_customer_mobile_phone_changed    = updating_customer.mobile_phone!=mobile_phone
                
                if is_customer_email_changed:
                    if is_not_empty(email):
                        checking_user_acct = User.get_by_email(email)
                        
                        if checking_user_acct:
                            is_email_used = True
                            is_used_email_same_user_acct = checking_user_acct.key_in_str == updating_customer.registered_user_acct_key
                        
                if is_customer_mobile_phone_changed:
                    if is_not_empty(mobile_phone):
                        checking_user_acct = User.get_by_mobile_phone(mobile_phone)
                    
                        if checking_user_acct:
                            is_mobile_phone_used = True
                            is_used_mobile_phone_same_user_acct = checking_user_acct.key_in_str == updating_customer.registered_user_acct_key
                                
                logger.debug('is_customer_email_changed=%s', is_customer_email_changed)
                logger.debug('is_customer_mobile_phone_changed=%s', is_customer_mobile_phone_changed)
                logger.debug('is_email_used=%s', is_email_used)
                logger.debug('is_mobile_phone_used=%s', is_mobile_phone_used)
                logger.debug('is_used_email_same_user_acct=%s', is_used_email_same_user_acct)
                logger.debug('is_used_mobile_phone_same_user_acct=%s', is_used_mobile_phone_same_user_acct)
                
                if is_email_used==False and is_mobile_phone_used==False:
                    logger.debug('Going to update customer details') 
                    
                    birth_date              = customer_data_in_json.get('birth_date')
                        
                    if is_not_empty(birth_date):
                        birth_date = datetime.strptime(birth_date, '%d/%m/%Y')
                    
                    logger.debug('birth_date=%s', birth_date)
                    
                    Customer.update(customer=updating_customer, 
                                    name                    = customer_data_in_json.get('name'), 
                                    email                   = customer_data_in_json.get('email'), 
                                    gender                  = customer_data_in_json.get('gender'),
                                    birth_date              = birth_date,
                                    mobile_phone            = mobile_phone, 
                                    password                = customer_data_in_json.get('password'),
                                    )
                
                
                if customer_is_exist:
                    if is_email_used==True:
                        return create_rest_message('Email have been taken', status_code=StatusCode.BAD_REQUEST)
                    
                    elif is_mobile_phone_used==True:
                        return create_rest_message('Mobile phone have been taken', status_code=StatusCode.BAD_REQUEST)
                    else:
                        return create_rest_message(status_code=StatusCode.OK)
                else:
                    return create_rest_message(gettext('Customer is not exis'), status_code=StatusCode.BAD_REQUEST)
            
        else:
            logger.warn('customer registration input is invalid')
            error_message = updating_customer_form.create_rest_return_error_message()
            
            return create_rest_message(error_message, status_code=StatusCode.BAD_REQUEST)
    except:
        logger.error('Fail to register customer due to %s', get_tracelog())
        
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)
        
@customer_api_bp.route('/<ref_code>', methods=['DELETE'])
@auth_token_required 
def delete_customer(ref_code):
    if is_not_empty(ref_code):
        is_found = False
        db_client = create_db_client(caller_info="read_customer")
        with db_client.context():
            customer = Customer.get_by_reference_code(ref_code) 
            if customer:
                customer.delete()
                is_found = True
        
        if is_found:
            return create_rest_message(status_code=StatusCode.NO_CONTENT)
        else:
            return create_rest_message(gettext('Customer is not exist'), status_code=StatusCode.BAD_REQUEST)
    else:
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)        


@customer_api_bp.route('/search/<limit>', methods=['POST'])
#@auth_token_required
def search_customer(limit):
    
    search_member_data_in_json   = request.get_json()
    search_customer_form         = CustomerSearchForm(ImmutableMultiDict(search_member_data_in_json))
    
    logger.debug('search_member_data_in_json=%s', search_member_data_in_json)
    
    db_client = create_db_client(caller_info="search_customer")
    customer_list = []
    if search_customer_form.validate():
        name                        = search_customer_form.name.data
        mobile_phone                = search_customer_form.mobile_phone.data
        email                       = search_customer_form.email.data
        reference_code              = search_customer_form.reference_code.data
        merchant_reference_code     = search_customer_form.merchant_reference_code.data
    
        acct_id     = request.headers.get('x-acct-id')
        
        logger.debug('acct_id=%s', acct_id)
        logger.debug('name=%s', name)
        logger.debug('email=%s', email)
        logger.debug('reference_code=%s', reference_code)
        logger.debug('merchant_reference_code=%s', merchant_reference_code)
        
        limit_int = int(limit)
        
        with db_client.context():
            merchant_acct   = MerchantAcct.fetch(acct_id)
            (search_results, total_count, next_cursor)  = Customer.search_merchant_customer(merchant_acct, 
                                                                                            name                    = name, 
                                                                                            email                   = email, 
                                                                                            mobile_phone            = mobile_phone, 
                                                                                            reference_code          = reference_code,
                                                                                            merchant_reference_code = merchant_reference_code,
                                                                                            limit                   = limit_int,
                                                                                            )
        
            for c in search_results:
                user_details = c.registered_user_acct
                customer_details_dict = c.to_dict(date_format="%d-%m-%Y", datetime_format="%d-%m-%Y %H:%M:%S")
                customer_details_dict['customer_key']               = c.key_in_str
                customer_details_dict['is_email_verified']          = user_details.is_email_verified
                customer_details_dict['is_mobile_phone_verified']   = user_details.is_mobile_phone_verified
                
                if 'entitled_voucher_summary' in customer_details_dict:
                    customer_details_dict['voucher_summary']            = c.entitled_voucher_summary
                    del customer_details_dict['entitled_voucher_summary'] 
                
                
                customer_list.append(customer_details_dict)
    
        #return create_rest_message(status_code=StatusCode.OK, customer_list=customer_list)
        return jsonify(customer_list)
    else:
        return create_rest_message(gettext('Invalid input'), status_code=StatusCode.BAD_REQUEST)

@customer_api_bp.route('/<reference_code>/sales-transaction/limit/<limit>', methods=['GET'])
@auth_token_required
def list_customer_sales_transaction(reference_code, limit):
    
    logger.debug('reference_code=%s', reference_code)
    
    if is_not_empty(reference_code):
        limit_int = int(limit, 10)
        acct_id   = request.headers.get('x-acct-id')
        db_client = create_db_client(caller_info="read_customer_sales_transaction")
        transactions_list = []
        with db_client.context():
            merchant_acct = MerchantAcct.fetch(acct_id)
            customer = Customer.get_by_reference_code(reference_code, merchant_acct)
            
        
        if customer:
            dict_properties  = ['transaction_id', 'invoice_id', 'remarks', 'tax_amount', 'transact_amount', 'reward_giveaway_method',
                               'entitled_reward_summary', 'entitled_voucher_summary', 'entitled_prepaid_summary', 
                               'transact_outlet_details', 
                               'transact_datetime', 'created_datetime',  'transact_outlet_key', 'is_revert', 'reverted_datetime',
                               'transact_by_username', 'is_reward_redeemed', 'is_sales_transaction', 'allow_to_revert',
                               ]
            with db_client.context():
                result       = CustomerTransaction.list_customer_transaction(customer, limit=limit_int)
                for r in result:
                    transactions_list.append(r.to_dict(dict_properties=dict_properties,  date_format="%d-%m-%Y", datetime_format="%d-%m-%Y %H:%M:%S"))
            
            return jsonify(transactions_list)
            
        else:
            logger.warn('Customer transaction with reference code (%s) is not found', reference_code)
            return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            
    else:
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)
    
@customer_api_bp.route('/<reference_code>/sales-transaction/transaction_id/<transaction_id>/revert', methods=['POST'])
@auth_token_required
def revert_customer_sales_transaction(reference_code, transaction_id):
    
    logger.debug('transaction_id=%s', transaction_id)
    
    if is_not_empty(reference_code) and is_not_empty(transaction_id):
        acct_id   = request.headers.get('x-acct-id')
        db_client = create_db_client(caller_info="revert_customer_sales_transaction")
        
        with db_client.context():
            merchant_acct           = MerchantAcct.fetch(acct_id)
            customer                = Customer.get_by_reference_code(reference_code, merchant_acct)
            customer_transaction    = CustomerTransaction.get_by_transaction_id(transaction_id);
        
        if customer_transaction:
            with db_client.context():
                merchant_username       = get_logged_in_api_username()
                reverted_by             = MerchantUser.get_by_username(merchant_username)
                customer_transaction.revert(customer, reverted_by)
            
            return create_rest_message(status_code=StatusCode.OK, reverted_datetime = customer_transaction.reverted_datetime.strftime('%d-%m-%Y %H:%M:%S'))
        else:    
            return create_rest_message(gettext('Failed to find transaction'), status_code=StatusCode.BAD_REQUEST)
        
        
            
    else:
        return create_rest_message(gettext('Missing reference code or transaction id'), status_code=StatusCode.BAD_REQUEST)    
    
#customer_api.add_resource(CustomerResource)    