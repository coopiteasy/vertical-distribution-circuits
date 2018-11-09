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
			}); 
			window.location.href = '/shop';
        });
	});
    $("select[name='shipping_id']", oe_website_sale).trigger('change');

    var clickwatch = (function(){
        var timer = 0;
        return function(callback, ms){
          clearTimeout(timer);
          timer = setTimeout(callback, ms);
        };
    })();
    
    $(".oe_website_sale").off("change", ".oe_cart input.js_quantity[data-product-id]").on("change", ".oe_cart input.js_quantity[data-product-id]", function (ev) {
    	ev.preventDefault();
    	var $input = $(this);
    	if ($input.data('update_change')) {
    		return;
    	}
    	var value = parseInt($input.val() || 0, 10);
    	var $dom = $(this).closest('tr');
    	var default_price = parseFloat($dom.find('.text-danger > span.oe_currency_value').text());
    	var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
    	var line_id = parseInt($input.data('line-id'),10);
    	var product_id = parseInt($input.data('product-id'),10);
    	var product_ids = [product_id];
    	clickwatch(function(){

    		$dom_optional.each(function(){
    			$(this).find('.js_quantity').text(value);
    			product_ids.push($(this).find('span[data-product-id]').data('product-id'));
    		});
    		$input.data('update_change', true);

    		ajax.jsonRpc("/shop/cart/update_json", 'call', {
    			'line_id': line_id,
    			'product_id': parseInt($input.data('product-id'),10),
    			'set_qty': value})
    			.then(function (data) {
    				$input.data('update_change', false);
    				if (value !== parseInt($input.val() || 0, 10)) {
    					$input.trigger('change');
    					return;
    				}
    				var $q = $(".my_cart_quantity");
    				if (data.cart_quantity) {
    					$q.parent().parent().removeClass("hidden");
    				}
    				else {
    					$q.parent().parent().addClass("hidden");
    					$('a[href^="/shop/checkout"]').addClass("hidden")
    				}
    				$q.html(data.cart_quantity).hide().fadeIn(600);

    				$input.val(data.quantity);
    				$('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);

    				$(".js_cart_lines").first().before(data['website_sale.cart_lines']).end().remove();

    				if (data.warning) {
    					var cart_alert = $('.oe_cart').parent().find('#data_warning');
    					if (cart_alert.length === 0) {
    						$('.oe_cart').prepend('<div class="alert alert-danger alert-dismissable" role="alert" id="data_warning">'+
    								'<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning + '</div>');
    					}
    					else {
    						cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning);
    					}
    					$input.val(data.quantity);
    				}

    				window.location.href = '/shop/cart';
    			});
    	}, 500);
    });
    
});