define(["fabric"],function(app){

	return app.config(function ($stateProvider, $urlRouterProvider) {

	 $urlRouterProvider.otherwise('/dashboard');

     $stateProvider
         .state("/", {
            url: "/dashboard",
            templateUrl: "/dashboard/view/index",
			controller: 'dashboardCtrl',
			resolve:{
				loaded:function($rootScope){
					$rootScope.pageLoaded = false;
				}
			}
        }).state("machine", {
            url: "/machine",
            templateUrl: "/machine/view/index",
			controller: 'machineCtrl',
			resolve:{
				loaded:function($rootScope){
					$rootScope.pageLoaded = false;
				}
			}
        }).state("machine.list", {
            url: "/list/:id",
            views: {
                machine_list: {
                    templateUrl: "/machine/view/list",
			        controller: 'machinelistCtrl',
                }
            }

        }).state("project", {
            url: "/project",
            templateUrl: "/project/view/index",
			controller: 'projectCtrl',
			resolve:{
				loaded:function($rootScope){
					$rootScope.pageLoaded = false;
				}
			}
        }).state("components", {
            url: "/components",
            templateUrl: "/components/view/index",
			controller: 'componentsCtrl',
			resolve:{
				loaded:function($rootScope){
					$rootScope.pageLoaded = false;
				}
			}
        }).state("fabric", {
            url: "/fabric",
            templateUrl: "/fabric/view/index",
			controller: 'fabricCtrl',
            resolve:{
				loaded:function($rootScope){
					$rootScope.pageLoaded = false;
				}
			}
        });

    })
});