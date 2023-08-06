'''
Created on 28 Oct 2021

@author: jacklok
'''

from flask import Blueprint, request, url_for, jsonify
import logging, json
from trexapi.decorators.api_decorators import auth_token_required
from trexlib.utils.string_util import is_not_empty, is_empty
from trexadmin.libs.http import create_rest_message
from trexadmin.libs.http import StatusCode
from trexmodel.models.datastore.loyalty_models import LoyaltyDeviceSetting
from trexmodel.utils.model.model_util import create_db_client
from trexmodel.models import merchant_helpers
from trexlib.utils.common.common_util import sort_list
from firebase_admin import firestore
from datetime import datetime
from trexapi.conf import API_ERR_CODE_INVALID_ACTIVATION_CODE


#logger = logging.getLogger('api')
logger = logging.getLogger('debug')

loyalty_api_bp = Blueprint('loyalty_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/loyalty')

@loyalty_api_bp.route('/check-activation', methods=['POST'])
def check_activation():
    
    activation_code = request.args.get('activation_code') or request.form.get('activation_code') or request.json.get('activation_code')
    logger.debug('activation_code=%s', activation_code)
    
    if is_not_empty(activation_code):
        db_client = create_db_client(caller_info="check_activation")
        with db_client.context():
            device_setting = LoyaltyDeviceSetting.get_by_activation_code(activation_code)
        
        if device_setting:
            if device_setting.activated==False:
                return create_rest_message(status_code=StatusCode.OK)
            else:
                return create_rest_message('The code have been used to activate before', status_code=StatusCode.BAD_REQUEST)
        else:
            return create_rest_message('Invalid activate code', status_code=StatusCode.BAD_REQUEST)
    else:
        return create_rest_message('Activation code is required', status_code=StatusCode.BAD_REQUEST)

def getDeviceSetting(activation_code):
    if is_not_empty(activation_code):
        db_client = create_db_client(caller_info="getDeviceSetting")
        with db_client.context():
            device_setting = LoyaltyDeviceSetting.get_by_activation_code(activation_code)
        
        if device_setting:
            logger.info('Found device setting');
            #if pos_setting.activated==False:
            if True:
                logger.info('device activation code is valid');
                device_setting_details = None
                with db_client.context():
                    #is_activated = POSSetting.activate(activation_code)
                    #if is_activated:
                    #merchant_acct                                       = pos_setting.merchant_acct_entity
                    outlet                                              = device_setting.assigned_outlet_entity
                    device_setting_details                              = merchant_helpers.construct_setting_by_outlet(outlet, device_setting=device_setting) 
                    
                    device_setting_details['logo_image_url']            = url_for('system_bp.merchant_logo_image_url', merchant_act_key=device_setting_details.get('account_id'))
                
                #if is_activated:
                if True:
                    
                    logger.debug('device_setting_details=%s', device_setting_details);
                    
                    return create_rest_message(status_code=StatusCode.OK,
                                               **device_setting_details
                                               )
                else:
                    return create_rest_message('Failed to activate', status_code=StatusCode.BAD_REQUEST)
            else:
                logger.info('Device activation code have been used');
                return create_rest_message('The code have been used to activate before', status_code=StatusCode.BAD_REQUEST)
        else:
            logger.info('Device setting record is not found');
            return create_rest_message('Invalid activate code', status_code=StatusCode.BAD_REQUEST, error_code=API_ERR_CODE_INVALID_ACTIVATION_CODE)
    else:
        logger.info('activation_code is empty');
        return create_rest_message('Activation code is required', status_code=StatusCode.BAD_REQUEST)
    
    
def updateActivationAndGetDeviceSetting(activation_code, device_id):
    if is_not_empty(activation_code) and is_not_empty(device_id):
        db_client = create_db_client(caller_info="updateActivationAndGetDeviceSetting")
        with db_client.context():
            device_setting = LoyaltyDeviceSetting.get_by_activation_code(activation_code)
        
        if device_setting:
            logger.info('Device activation code is valid');
            
            is_valid = False
            device_setting_details = None
            
            with db_client.context():
                device_setting = LoyaltyDeviceSetting.get_by_activation_code(activation_code)
                if device_setting.activated:
                    if device_setting.device_id == device_id:
                        is_valid = True
                    
                else:
                    is_valid = True
                    device_setting.activate(device_id)
            
                if is_valid:    
                    device_setting_details                                 = merchant_helpers.construct_setting_by_outlet(device_setting.assigned_outlet_entity, device_setting=device_setting)
                    #pos_setting_details['logo_image_url']               = url_for('system_bp.merchant_logo_image_url', merchant_act_key=pos_setting_details.get('account_id'))
            
            if is_valid:
                
                logger.debug('device_setting_details=%s', device_setting_details);
                
                return create_rest_message(status_code=StatusCode.OK,
                                           **device_setting_details
                                           )
            else:
                if device_setting.activated and device_setting.device_id != device_id:
                    return create_rest_message('The code have been used to activate before', status_code=StatusCode.BAD_REQUEST)
                else:
                    return create_rest_message('Failed to activate', status_code=StatusCode.BAD_REQUEST)
            
        else:
            logger.info('Setting record is not found');
            return create_rest_message('Invalid activate code', status_code=StatusCode.BAD_REQUEST)
    else:
        logger.info('activation_code is empty or device id is empty');
        return create_rest_message('Activation code and device id are required', status_code=StatusCode.BAD_REQUEST)
        
    
@loyalty_api_bp.route('/account-sync', methods=['get'])
def activate():
    activation_code = request.args.get('activation_code') or request.form.get('activation_code') or request.json.get('activation_code')
    logger.info('activation_code=%s', activation_code)
    return getDeviceSetting(activation_code)
    
    
@loyalty_api_bp.route('/activate', methods=['POST'])
def activate_post():
    
    activation_code = request.args.get('activation_code') or request.form.get('activation_code') or request.json.get('activation_code')
    device_id       = request.args.get('device_id') or request.form.get('device_id') or request.json.get('device_id')
    
    logger.info('activation_code=%s', activation_code)
    logger.info('device_id=%s', device_id)
    
    return updateActivationAndGetDeviceSetting(activation_code, device_id)
        
       
    
@loyalty_api_bp.route('/version-sync', methods=['get'])
def version_sync():
    db_client       = create_db_client(caller_info="version_sync")
    
    with db_client.context():
        version =  {
                               
                                'setting'  :[
                                            
                                        ]
                                       
                            }
                                
    
            
    
    return version




 