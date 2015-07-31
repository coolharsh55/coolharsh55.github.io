/**
 * jQuery Implied Cookie Policy Message Plugin v1.0
 * Compatibility: >= jQuery v1.2.6
 * 
 * Author: Ashley Dawson <ashley@ashleydawson.co.uk>
 */
( function($) {
	
	var methods = {
		
		init: function() {
			for(var setting in $.settings) {
				if(setting != 'message') {
					var message = $.settings.message;
					$.settings.message = message.replace('%' + setting + '%', $.settings[setting]);
				}
			}
		}
		
		, _setCookie: function(c_name, value, exdays) {
			var exdate = new Date();
			exdate.setDate(exdate.getDate() + exdays);
			var c_value = escape(value) + ((exdays == null) ? "" : "; expires=" + exdate.toUTCString());
			document.cookie = c_name + "=" + c_value;
		}
		
		, _getCookie: function(c_name) {
			var i, x, y, ARRcookies = document.cookie.split(";");
			for(i=0; i < ARRcookies.length; i++) {
				x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
				y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
				x = x.replace(/^\s+|\s+$/g, "");
				if(x == c_name) {
					return unescape(y);
				}
			}
			return null;
		}
		
		, _getMarkup: function() {
			return '<div class="cp-wrapper ' + $.settings.extra_class + '"><div class="cp-inner"><p>' + $.settings.message +
				   '</p><button class="cp-button cp-button-close" title="' + $.settings.close_button_title + '"><span>' 
				   + $.settings.close_button_text + '</span></button></div></div>';
		}
	}
	
	$.fn.cookiepolicy = function(options) {
		
		$.settings = $.extend({
			 message: 'Our cookies give you an awesome online experience. If you continue to use this site, ' + 
				 'we\'ll assume you are happy for your web browser to receive cookies from us. ' + 
				 'See our <a href="%cookie_policy_url%">cookie policy</a> for more information on cookies.'
			, extra_class: ''
			, cookie_policy_url: 'http://www.example.com/cookie-policy.html'
			, close_button_text: 'Close'
			, close_button_title: 'Close this cookie policy message box'
			, cookie_name: 'hide_cookie_policy_message'
			, cookie_expire_days: 10
			, on_open: function() { }
			, on_close: function() { }
			, on_closed: function() { }
		}, options);
		
		var base_node = this;
		
		methods.init();
		
		var hide_message = methods._getCookie($.settings.cookie_name);
		
		if(hide_message === null) {
			base_node.prepend(methods._getMarkup());
			$.settings.on_open();
			base_node.find('.cp-button-close').click(function(e) {
				e.preventDefault();
				base_node.find('.cp-wrapper').slideUp();
				methods._setCookie($.settings.cookie_name, true, $.settings.cookie_expire_days);
				$.settings.on_close();
			});
		} else {
			$.settings.on_closed();
		}
		
	}
	
} )( jQuery );
