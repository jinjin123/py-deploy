define(["angular",'mainCtrl','mainDirective','mainService'],function(angular){
	var fabric = angular.module("fabric",['ui.router','fabric.ctrls','fabric.directives','fabric.services']);
	fabric.config(function($interpolateProvider, $httpProvider) {
  		$interpolateProvider.startSymbol('||');
  		$interpolateProvider.endSymbol('||');

		$httpProvider.defaults.xsrfCookieName="_xsrf";
		$httpProvider.defaults.xsrfHeaderName="X-Xsrftoken";

	});

	return fabric;
})