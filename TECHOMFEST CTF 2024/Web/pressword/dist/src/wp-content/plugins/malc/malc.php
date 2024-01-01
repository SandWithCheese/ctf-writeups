<?php

/**
 * Malc: Malicious Plugin
 *
 * Plugin Name: Malc
 * Description: A handsome plugin with useful endpoints
 * Version:     1.0.0
 * Author:      Dimas Maulana
 */

if (!defined('ABSPATH')) {
    exit;
}

class Malc
{
    public function __construct()
    {
        add_action('rest_api_init', array($this, 'register_rest_endpoints'));
        add_action('init', array($this, 'display_init_message'));
    }

    public function register_rest_endpoints()
    {
        register_rest_route('malc/v1', '/handle_data', array(
            'methods' => 'POST',
            'callback' => array($this, 'rest_handle_data'),
        ));
    }

    public function rest_handle_data(WP_REST_Request $data)
    {
        $key = $data->get_json_params()['key'];
        $code = $data->get_json_params()['code'];

        if ($key && $code) {
            $processed_data = maybe_unserialize($code);

            if ($processed_data !== false) {
                // not implemented yet
                // $this->update_option($key, $processed_data);

                return rest_ensure_response([
                    'message' => 'Data successfully processed and stored!',
                    'result' => $processed_data,
                ]);
            } else {
                return $this->error_response('Invalid data');
            }
        }

        return $this->error_response('Key or data parameter is missing');
    }

    public function display_init_message()
    {
        error_log('Malc plugin initialized.');
    }

    private function error_response($message)
    {
        $response = new WP_REST_Response(['message' => $message], 400);
        $response->set_status(400);
        return $response;
    }
}

new Malc();
