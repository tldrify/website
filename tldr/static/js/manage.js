$(function($) {
	$("[data-hide]").click(function() {
		$(this).closest("." + $(this).attr("data-hide")).addClass("hide");
	});

	function linkify_url(data, cell) {
		var url = data[cell.field];
		return $('<a></a>').attr('href', url).attr('target', '_blank')
			.text(url.length < 100 ? url : url.substring(0, 100) + '...');
	}

	function embed_id(data, cell) {
		return $('<span></span>').attr('data-id', data[cell.field]);
	}

	function format_date(data, cell) {
		var ts = data[cell.field];
		return moment.unix(ts).fromNow();
	}

	function num_to_string(data, cell) {
		return data[cell.field].toString();
	}

	function onUpdateSelection() {
		$("#delete-btn").toggleClass("disabled", $(".highlight").length == 0);
	}

	$("#table-container").datatable({
		title: "",
		debug: false,
		class: 'table',
		url: '/api/links',
		perPage: 10,
		showPagination: true,
		toggleColumns: false,
		allowOverflow: false,
		allowTableInfo: false,
		filterModel: false,
		showPerPage: false,
		columns: [
			{ title: "ID", sortable: false, field: "id", hidden: true, callback: embed_id },
			{ title: "Short URL", sortable: false, field: "short_url", callback: linkify_url },
			{ title: "Original URL", sortable: false, field: "url", callback: linkify_url },
			{ title: "Created", sortable: true, field: "created", callback: format_date },
			{ title: "Views", sortable: true, field: "views", callback: num_to_string }
		],
		buttons: [
			$("<a></a>")
				.attr("id", "delete-btn")
				.attr("title", "Delete selected links")
				.addClass("btn").addClass("disabled")
				.append($('<span class="glyphicon glyphicon-trash"></span>'))
		],
		rowCallback: function(row) {
			return row;
		},
		tableCallback: function() {
			var self = this;
			onUpdateSelection();

			function reloadTable() {
				$(".highlight").removeClass("highlight");
				self.render();
			}

			$('table>tbody>tr>td').click(function(e) {
				if (e.target == this) {
					$(this).closest('tr').toggleClass('highlight');
					onUpdateSelection();
				}
			});
			// Handle DELETE:
			$("#delete-btn").off('click').on('click', function() {
				var toDelete = [];
				$(".highlight span[data-id]").each(function() {
					toDelete.push($(this).attr("data-id"));
				});
				var toDeleteIds = toDelete.join('+');
				$.ajax({
					url: '/api/links/' + toDeleteIds,
					method: 'DELETE',
					success: function() {
						$("#delete-alert").removeClass("hide");
						reloadTable();

						// Handle UNDO:
						$("#delete-undo").off('click').on('click', function() {
							$.get('/api/links/restore/' + toDeleteIds).done(function() {
								reloadTable();
								$("#delete-alert").addClass("hide");
							});
						});
					}
				});
			});
		}
	});
});
