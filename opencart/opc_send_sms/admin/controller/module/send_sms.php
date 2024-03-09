<?php
/**
 * Extension name: Send SMS
 * Descrption: Using this extension we will a send sms via MTS Exolve API after make order.
 * Author: BosonBeard. 
 * 
 */
namespace Opencart\Admin\Controller\Extension\OpcSendSms\Module;

use \Opencart\System\Helper AS Helper;

class SendSMS extends \Opencart\System\Engine\Controller {    
    
   /**
   * index
   *
   * @return void
   */
   public function index(): void {
      $this->load->language('extension/opc_send_sms/module/send_sms');
      $this->document->setTitle($this->language->get('heading_title'));

      $data['breadcrumbs'] = [];

      $data['breadcrumbs'][] = [
         'text' => $this->language->get('text_home'),
         'href' => $this->url->link('common/dashboard','user_token='    
         .$this->session->data['user_token'])
      ];

      $data['breadcrumbs'][] = [
         'text' => $this->language->get('text_extension'),
         'href' => $this->url->link('marketplace/extension','user_token='
         .$this->session->data['user_token'] . '&type=module')
      ];

      if (!isset($this->request->get['module_id'])) {
         $data['breadcrumbs'][] = [
            'text' => $this->language->get('heading_title'),
            'href' => $this->url->link('extension/opc_send_sms/module/send_sms','user_token='. 
            $this->session->data['user_token'])
      ];
      } else {
         $data['breadcrumbs'][] = [
            'text' => $this->language->get('heading_title'),
            'href' => $this->url->link('extension/opc_send_sms/module/send_sms','user_token='.
             $this->session->data['user_token'] . '&module_id=' . $this->request->get['module_id'])
      ];
      }
         
      // configuration save URL
      $data['save'] = $this->url->link('extension/opc_send_sms/module/send_sms.save', 'user_token=' . $this->session->data['user_token']);
         
      // back to previous page URL
      $data['back'] = $this->url->link('marketplace/extension', 'user_token=' . $this->session->data['user_token'] . '&type=module');

      // getting settings fields from extension configuration
      $data['module_opc_send_sms_status'] = $this->config->get('module_opc_send_sms_status');
      $data['module_opc_send_sms_token'] = $this->config->get('module_opc_send_sms_token');
      $data['module_opc_send_sms_phone'] = $this->config->get('module_opc_send_sms_phone');
      $data['module_opc_send_sms_text'] = $this->config->get('module_opc_send_sms_text');



      $data['header'] = $this->load->controller('common/header');
      $data['column_left'] = $this->load->controller('common/column_left');
      $data['footer'] = $this->load->controller('common/footer');

      $this->response->setOutput($this->load->view('extension/opc_send_sms/module/send_sms', $data));
   }
      
   /**
   * save method
   *
   * @return void
   */
   public function save(): void {
      $this->load->language('extension/opc_send_sms/module/send_sms');
      $json = [];

      if (!$this->user->hasPermission('modify', 'extension/opc_send_sms/module/send_sms')) {
      $json['error']['warning'] = $this->language->get('error_permission');
      }

      if (!isset($this->request->post['module_opc_send_sms_token'])) {
         $json['error']['api-key'] = $this->language->get('error_api_token');
      }
      if (!isset($this->request->post['module_opc_send_sms_phone'])) {
         $json['error']['api-key'] = $this->language->get('error_api_phone');
      }

   if (!$json) {
      $this->load->model('setting/setting');
      
      // saving configuration
      $this->model_setting_setting->editSetting('module_opc_send_sms_status', $this->request->post);
      $this->model_setting_setting->editSetting('module_opc_send_sms_token', $this->request->post);
      $this->model_setting_setting->editSetting('module_opc_send_sms_phone', $this->request->post);
      $this->model_setting_setting->editSetting('module_opc_send_sms_text', $this->request->post);

      $json['success'] = $this->language->get('text_success');
   }

   $this->response->addHeader('Content-Type: application/json');
   $this->response->setOutput(json_encode($json));
   }
   
   /**
   * install method
   *
   * @return void
   */
   public function install() {
      // registering events to show menu
      $this->__registerEvents();
   }

   /**
   * __registerEvents
   *
   * @return void
   */
   protected function __registerEvents() {
      // events array
     $events   = array();
     $events[] = array(
       'code'        => "SendCheckoutSmsMtsExolve_",
       'trigger'     => "catalog/model/checkout/order/addHistory/before",
       'action'      => "extension/opc_send_sms/event/event",
       'description' => "Send SMS after checkout via MTS Exolve",
       'status'      => 1,
       'sort_order'  => 0,
    );
    
      // loading event model
    $this->load->model('setting/event');
    foreach($events as $event){

           // registering events in DB
            $this->model_setting_event->addEvent($event);
    }
  }

}
