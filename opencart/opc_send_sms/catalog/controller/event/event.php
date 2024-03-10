<?php
/**
 * Extension name: Send SMS
 * Descrption: Using this extension we will a send sms via MTS Exolve API after make order.
 * Author: BosonBeard. 
 * 
 */
namespace Opencart\Catalog\Controller\Extension\OpcSendSms\Event;

class Event extends \Opencart\System\Engine\Controller
{
    /**
     * index
     * Event trigger: catalog/model/checkout/order/addHistory/before
     * @param  mixed $route
     * @param  mixed $data
     * @param  mixed $output
     * @return void
     */
    public function index(&$route = false, &$data = array(), &$output = array()): void {

        // get data from OpenCart

        $order_id = "none";
        $this->load->model('setting/setting');

        if (isset($this->session->data['order_id']))
            {
                    $order_id = $this->session->data['order_id'];
            }
        
         // get data from OpenCart
        $customer_phone = $this->customer->getTelephone(); 
 
        // get data from extension opc_send_sms 
        $sender_phone =  $this->config->get('module_opc_send_sms_phone');
        $token =  $this->config->get('module_opc_send_sms_token');
        $text_raw =  $this->config->get('module_opc_send_sms_text');
        
        if (!$text_raw)
        {
            $text_raw = "Order $order_id created.";
        }    
        $text = str_replace('%order_id%',$order_id,$text_raw);

        // send request to MTS Exolve API
        $curl = curl_init();

        curl_setopt_array($curl, array(
        CURLOPT_URL => 'https://api.exolve.ru/messaging/v1/SendSMS',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => '',
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 0,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => 'POST',
        CURLOPT_POSTFIELDS =>'{
        "number": "'.$sender_phone.'",
        "destination": "'.$customer_phone.'",
        "text": "'.$text.'" 
        }
        ',
        CURLOPT_HTTPHEADER => array(
            'Content-Type: application/json',
            "Authorization: Bearer $token"
            ),
        ));
        $response = curl_exec($curl);
        curl_close($curl);
        
    }

    /**
     * getTemplateBuffer
     *
     * @param  mixed $route
     * @param  mixed $event_template_buffer
     * @return string
     */
    protected function getTemplateBuffer($route, $event_template_buffer) {

        // if there already is a modified template from view/*/before events use that one
        if ($event_template_buffer) {
            return $event_template_buffer;
        }
    }
}
