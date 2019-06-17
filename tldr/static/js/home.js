$(function($) {
	var raph, path, fullPath, cur, length, step, delay, oldPath, newPath, arrowPath;
	var steps = 50, startDelay = 30;
	var pathAttr = { 'opacity': .5, 'stroke': '#a60000', 'stroke-width': 5, 'stroke-dasharray': '-'};
	var arrowAttr = { 'opacity': .5, 'stroke': '#a60000', 'stroke-width': 1, 'fill': '#a60000' };
	var drawing = false;

	function startDraw() {
		if (!drawing) {
			drawing = true;

			var buttonX = $(this).offset().left - $(window).scrollLeft();
			var buttonY = $(this).offset().top - $(window).scrollTop();
			var startX = buttonX - 10;
			var startY = buttonY + $(this).height()*3/2;
			var endX = $(window).width()/6, endY = 0;
			var paperWidth = startX - endX;
			var paperHeight = startY - endY;

			$("#paper").toggleClass("hide", false).css({
				position: 'fixed',
				width: paperWidth,
				heigth: paperHeight,
				top: endY,
				left: endX
			});

			cur = 0;
			delay = startDelay;
			path = "M" + paperWidth + " " + (paperHeight-7) + "Q20 " + paperHeight + " 20 15";

			raph = Raphael(document.getElementById('paper'), paperWidth, paperHeight);
			fullPath = raph.path(path);
			fullPath.hide();
			length = fullPath.getTotalLength();
			step = length / steps;
			setTimeout(doDrawStep, delay);
		}
	}

	function doDrawStep() {
		if (drawing) {
			cur += step;
			if (cur > length) {
				cur = length;
			}
			newPath = raph.path(fullPath.getSubpath(0, cur)).attr(pathAttr);
			if (oldPath) {
				oldPath.remove();
			}
			oldPath = newPath;
			if (cur < length) {
				delay = startDelay - (startDelay/2)*(cur/length);
				setTimeout(doDrawStep, delay);
			} else {
				arrowPath = raph.path("M10 15 L30 15 L20 5 L10 15").attr(arrowAttr);
				drawing = false;
			}
		}
	}

	function stopDraw() {
		drawing = false;
		$("#paper").toggleClass("hide", true);
		if (newPath) {
			newPath.remove();
			newPath = null;
		}
		if (oldPath) {
			oldPath.remove();
			newPath = null;
		}
		if (fullPath) {
			fullPath.remove();
			fullPath = null;
		}
		if (arrowPath) {
			arrowPath.remove();
			arrowPath = null;
		}
		raph = null;
	}

	$("#bookmarklet").mouseenter(startDraw).mouseleave(stopDraw);
	$(window).scroll(stopDraw);

	$("#feedback-tab").click(function() {
		$("#feedback-form").toggle("slide").find("form").attr("action", "/feedback");
	});

	$("#feedback-form form").on('submit', function(event) {
		var $form = $(this);
		$.ajax({
			type: $form.attr('method'),
			url: $form.attr('action'),
			data: $form.serialize(),
			success: function() {
				$("#feedback-form").toggle("slide").find("textarea").val('');
			}
		});
		event.preventDefault();
	});
});

