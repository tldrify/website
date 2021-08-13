/*
 * Copyright (c) Michael Spector 2015
 * All rights reseved
 */

(function() {
  var callback = function() {
    TLDR.save();
  };
  if (typeof(TLDR) == 'undefined') {
    TLDR = {};
    var sources = ['//tldrify.com/static/js/ajax-spin.min.js?v20150104-1710',
      '//tldrify.com/static/js/ajaxslt.min.js?v20140205-1504',
      '//tldrify.com/static/js/rangy-core.min.js?v20200517-0927',
      '//tldrify.com/static/js/jquery.min.js?v20200517-0927',
      '//tldrify.com/static/js/tldr.min.js?v20210813-0707'
    ];

    var loadNextScript = function() {
      if (sources.length > 0) {
        var script = document.createElement('script');
        script.src = sources.shift();
        document.body.appendChild(script);

        var done = false;
        script.onload = script.onreadystatechange = function() {
          if (!done &&
            (!this.readyState || this.readyState == "loaded" || this.readyState == "complete")) {
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
