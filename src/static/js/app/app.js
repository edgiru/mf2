/*global $ _ Rib _t __ core Tag Payment Vault Filter*/

window.AppView = (function(){
	"use strict";
	
	var AppView = Rib.View.extend({
		
		events: {
		},
		
		initialize: function() {
			_.bindAll(this, 'hideDialog', 'openDialog');
			
			var appView = this;
			
			Rib.U.bind('need_dialog', appView.openDialog);
			
			core.coll(function(cc){
				appView.childViews = {
					vaults:   new Vault   .Views.List({collection: cc.Vaults,   el: appView.$('#vaults-block')}),
					filters:  new Filter  .Views.List({collection: cc.Filters,  el: appView.$('#filters-block')}),
					payments: new Payment .Views.List({collection: cc.Payments, el: appView.$('#payments-list')}),
					tags:     new Tag     .Views.List({collection: cc.Tags,     el: appView.$('#tags-block')}),
					settings: new Settings.View({/*model: cc.Settings,*/ el: appView.$('#settings')})
				};
			});
		},
		
		showDialog: function(content) {
			this.$("#modal-dialog").empty().append(content).show();
		},
		
		hideDialog: function() {
			this.$("#modal-dialog").hide();
			this.dialogView = null;
		},
		
		openDialog: function(view) {
			
			this.dialogView = view;
			
			view.bind('close', this.hideDialog);
			this.showDialog(view.render().el);
		},
		
		closeDialog: function() {
			if (this.dialogView) {
				this.dialogView.cancel();
			}
		}
	});
	
	return AppView;
	
})();
