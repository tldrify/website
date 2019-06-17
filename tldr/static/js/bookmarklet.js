/*
 * Copyright (c) Michael Spector 2015
 * All rights reseved
 */

(function() {
	var callback = function() {
		TLDR.save();
	};
	if (typeof (TLDR) == 'undefined') {
		TLDR = {};
		var sources = [ '//tldrify.com/static/js/ajax-spin.min.js?v20150104-1710',
				'//tldrify.com/static/js/ajaxslt.min.js?v20140205-1504',
				'//cdn.jsdelivr.net/g/json2@0.1(json2.min.js),rangy@1.2.3(rangy-core.js),jquery@2.1.4(jquery.min.js)',
				'//tldrify.com/static/js/tldr.min.js?v20150427-1637' ];

		var loadNextScript = function() {
			if (sources.length > 0) {
				var script = document.createElement('script');
				script.src = sources.shift();
				document.body.appendChild(script);

				var done = false;
				script.onload = script.onreadystatechange = function() {
					if (!done
							&& (!this.readyState || this.readyState == "loaded" || this.readyState == "complete")) {
						done = true;

						// Handle memory leak in IE
						script.onload = script.onreadystatechange = null;

						loadNextScript();
					}
				}
			} else {
				callback();
			}
		}
		loadNextScript();

	} else {
		if (TLDR_spin.show()) {
			callback();
		}
	}
})();
