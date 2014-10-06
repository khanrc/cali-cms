
var Common = {
	"htmlspecialchars": function(str) {
		if(str instanceof Object)
			str = str.toString();
		else
			return "";

		str = str.replace(/&/g, "&amp;");
		str = str.replace(/</g, "&lt;");
		str = str.replace(/>/g, "&gt;");
		str = str.replace(/"/g, "&quot;");
		str = str.replace(/'/g, "&#039;");

		return str;
	},
	"get_iso_date": function(date) {
		var str = date.getFullYear();
		str += "-" + ("0" + (date.getMonth() + 1)).substr(-2);
		str += "-" + ("0" + date.getDate()).substr(-2);

		return str;
	},
	"add_day": function(old_date, delta_day) {
		var new_date = new Date();

		new_date.setTime(old_date.getTime() + (1000 * 60 * 60 * 24 * Number(delta_day)));

		return new_date;
	},
	"cya": function(url, data, success) {
		$.ajax({
			"type": "POST",
			"url": url + "?z=" + (new Date().getTime()),
			"data": data,
			"dataType": "json",
			"async": false,
			"success": function(json) {
				if(json.ec != 0)
					alert(json.em);
				else if(typeof(success) === "function") {
					arguments[0] = json.d;
					success.apply(this, arguments);
				}
			},
			"error": function() {
				alert("Unknown error");
			}
		});
	}
};

