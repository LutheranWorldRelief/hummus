new Vue({
	el:'#vue-app',
	data:{
		imports:[]
	},
	methods:{
		importData:function (imp) {
			console.log(imp);
			$.post(imp.url, {class:imp.id})
				.done(function(data){
					console.log(data);
				})
				.fail(function(data){
					console.log(data);
					alertify.alert(data.responseText);
				});
		}
	},
	mounted:function () {
		var self = this;
		var options = JSON.parse($('#vue-options').text());
		for(attr in options){
			self[attr] = options[attr];
		}
	}
});