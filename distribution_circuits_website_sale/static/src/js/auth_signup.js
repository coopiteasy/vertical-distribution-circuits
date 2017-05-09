odoo.define('distribution_circuits_website_sale.auth_signup', function (require) {
	"use strict";

	$(document).ready(function () {
	    $(".oe_website_login_container").on('change', "select[name='raliment_point_id']", function (ev) {
	    	$('.oe_website_login_container').find('select[name="delivery_point_id"]').val('');
		});
	    
	    $(".oe_website_login_container").on('change', "select[name='delivery_point_id']", function (ev) {
	    	$('.oe_website_login_container').find('select[name="raliment_point_id"]').val('');
		});
	});
});