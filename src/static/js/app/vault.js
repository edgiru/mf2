window.Vault = (function($, _, Backbone, Rib, _t){
	"use strict";

	/**
	 * Model
	 */
	var Vault = Backbone.Model.extend({
		
		defaults: {
			name: ''
		},
		
		initialize: function() {
		},
		
		validate: function(attrs) {
		    if (typeof attrs.name !== 'undefined' && !_.isString(attrs.name)) {
				return "'name' must be an String";
			}
			// todo
		}
	});
	
	/**
	 * Collection
	 */
	Vault.Collection = Backbone.Collection.extend({
		model: Vault,
		url: '/api/vault',
		
		initialize: function() {
		}
	});
	
	Vault.Views = {};
	
	/**
	 * Form view
	 */
	Vault.Views.Form = Rib.Views.Form.extend({
		
		className: "vault",
		tmpl: _t('vault.form'),
		
		save: function(){
			this.model.set({
				'name': this.$('.name').val()
			});
			
			this.model.save();
		}
	});
	
	/**
	 * List view
	 */
	Vault.Views.List = Rib.Views.EditableCollection.extend({
		
		tmpl: _t('vault.in-list'),
		
		list_selector: '.list',
		FormView: Vault.Views.Form,
		
		events: {
			'click .text': 'onClickText',
			'click .add': 'addClicked'
		},
		
		initialize: function (args) {
			Rib.Views.EditableCollection.prototype.initialize.call(this);
			
			_.bindAll(this, 'changeName');
			
			this.collection.bind('change:name', this.changeName);
		},
		
		addOne: function(model) {
			Rib.Views.EditableCollection.prototype.addOne.call(this, model);
			
			if(model.isNew()){
				this.edit(model);
			}
		},
		
		onClickText: Rib.U.el2ModelProxy(function(model){
			// todo
		}),
		
		changeName: Rib.U.model2ElProxy(function(el, model) {
			$('.name', el).text(model.get('name'));
		}),
		
		addClicked: function(){
			this.collection.add({});
		}
	});
	
	return Vault;
})(window.jQuery, window._, window.Backbone, window.Rib, window._t);
