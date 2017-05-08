odoo.define('distribution_circuits_website_sale.website_sale', function (require) {
	"use strict";
	
	var ajax = require('web.ajax');
    var oe_website_sale = this;
    
    require('website_sale.website_sale');
    
    $(".oe_website_sale").on('change', "select[name='selected_time_frame']", function (ev) {
		var selected_time_frame = $('.oe_website_sale').find('select[name="selected_time_frame"]').val();
		ajax.jsonRpc("/shop/set_current_time_frame", 'call', {
  			'time_frame_id': selected_time_frame
  		})
  		.then(function (data) {
			$.each(data, function(i, obj) {
				//alert(obj);
			}); 
        });
	});
    $("select[name='shipping_id']", oe_website_sale).trigger('change');;
});