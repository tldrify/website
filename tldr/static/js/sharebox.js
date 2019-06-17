/*
 * Copyright (c) Michael Spector 2015
 * All rights reseved
 */

$(function($) {
	var url = window.tldr_url;
	var title = window.tldr_title;
	var c = $("#share-content-template").clone();
	c.toggleClass("hide", false).attr("id", "share-content");
	c.find("input").attr("id", "share-url");
	c.find("[data-clipboard-target]").attr("id", "clipboard-btn");
	c.find("a.share-mail").attr("href", "mailto:?subject=" + encodeURIComponent(title) + "&body=" + encodeURIComponent(url));
	c.find("a.share-google").attr("href", "https://plus.google.com/share?url=" + encodeURIComponent(title + " - " + url));
	c.find("a.share-twitter").attr("href", "https://twitter.com/?status=" + encodeURIComponent(title + " - " + url));
	c.find("a.share-linkedin").attr("href", "https://www.linkedin.com/shareArticle?mini=true&url=" + encodeURIComponent(url) + "&title=" + encodeURIComponent(title) + "&summary=&source=");
	//c.find("a.share-facebook").attr("href", "https://www.facebook.com/sharer/sharer.php?s=100&p[url]=" + encodeURIComponent(url) + "&p[title]=" + encodeURIComponent(title));

	$("body").popover({
		placement : 'bottom',
		trigger: 'manual',
		html: 'true',
		content : c.html()
	}).popover('show');

	$("#share-url").on("click", function() {
		$(this).select();
	});

	$(".share-buttons a").on("click", function() {
		var url = $(this).attr('href');
		if (url.indexOf('http') === 0) {
			window.open(url, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600');
			return false;
		}
	});

	function createSelection(field, start, end) {
  		if(field.createTextRange) {
			var selRange = field.createTextRange();
			selRange.collapse(true);
			selRange.moveStart('character', start);
			selRange.moveEnd('character', end);
			selRange.select();
			field.focus();
		} else if( field.setSelectionRange ) {
			field.focus();
			field.setSelectionRange(start, end);
		} else if( typeof field.selectionStart != 'undefined' ) {
			field.selectionStart = start;
			field.selectionEnd = end;
			field.focus();
		}
	}

	var has_flash = false;
	try {
		if (new ActiveXObject('ShockwaveFlash.ShockwaveFlash')) {
			has_flash = true;
		}
	} catch(e) {
		if (navigator.mimeTypes ["application/x-shockwave-flash"] != undefined) {
			has_flash = true;
		}
	}
	if (has_flash) {
		var btn = $("#clipboard-btn");
		btn.css({display: ""});

		ZeroClipboard.config({
			'swfPath': '//cdn.jsdelivr.net/zeroclipboard/2.2.0/ZeroClipboard.swf',
			'trustedDomains': ["*"],
			'debug': true
		});

		var clip = new ZeroClipboard(btn);
		clip.on("ready", function() {
			this.on("aftercopy", function(event) {
				var textField = $("#share-url");
				createSelection(textField[0], 0, textField.val().length);
			});
		});
	}
});
