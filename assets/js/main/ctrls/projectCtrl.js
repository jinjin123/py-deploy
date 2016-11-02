define(['/assets/js/main/ctrls/module.js'],function(fabric){
    fabric.controller('projectCtrl',['$rootScope','$scope','$http','$location', function($rootScope,$scope,$http,$location){

        $('#bootbox-confirm').click(function () {
            bootbox.prompt("What is your name?", function (result) {
					if (result === null) {
						alert("Prompt dismissed");
					}
					else {
						alert("Hi, " + result + "!");
					}
				});
        });

        $scope.add_project = function(){
            if ( !$scope.project.id ){
                $http({
                    method: 'POST',
                    url: '/project/add',
                    params: {
                        'name': $scope.project.name,
                        'desc': $scope.project.desc,
                        'gitaddress': $scope.project.gitaddress ,
                        'localaddress': $scope.project.localaddress ,
                        'remoteaddress': $scope.project.remoteaddress ,
                        'deployaddress': $scope.project.deployaddress ,
                        'gituser': $scope.project.gituser ,
                    }
                }).then( function successCallback(response) {
                    if ( response.data.status == 'success' ) {
                        $('#edit-project').modal('hide');
                        $scope.reload();
                    }
                    if ( response.data.status == 'error' ) {
                        alert(response.data.msg);
                    }
                    if ( response.data.status == 'exception' ) {
                        alert( response.data.msg );
                    }
                    if ( response.data.status == 'logout' ) {
                        window.location.href='/login'
                    }

                }, function errorCallback(response){
                    // 处理不成功

                } );
            } else {
                $http({
                    method: 'POST',
                    url: '/project/edit',
                    params: {
                        'id': $scope.project.id,
                        'name': $scope.project.name,
                        'desc': $scope.project.desc,
                        'gitaddress': $scope.project.gitaddress ,
                        'localaddress': $scope.project.localaddress ,
                        'remoteaddress': $scope.project.remoteaddress ,
                        'deployaddress': $scope.project.deployaddress ,
                        'gituser': $scope.project.gituser ,
                    }
                }).then( function successCallback(response) {
                    if ( response.data.status == 'success' ) {
                        $('#edit-project').modal('hide');
                        $scope.reload();
                    }
                    if ( response.data.status == 'error' ) {
                        alert(response.data.msg);
                    }
                    if ( response.data.status == 'exception' ) {
                        alert( response.data.msg );
                    }
                    if ( response.data.status == 'logout' ) {
                        window.location.href='/login'
                    }

                }, function errorCallback(response){
                    // 处理不成功

                } );

            }
        }

        $scope.reload = function reload(){
            $http({
                method: 'GET',
                url: '/project/list',
                params:{}
            }).then(
                function successCallback( response ) {
                    if ( response.data.status == 'success' ) {
                        $scope.projects = response.data.data;
                    }
                    if ( response.data.status == 'error' ) {
                        alert(response.data.msg);
                    }
                    if ( response.data.status == 'exception' ) {
                        alert( response.data.msg );
                    }
                    if ( response.data.status == 'logout' ) {
                        window.location.href='/login'
                    }

                }
            )
        }
        $scope.reload();

        $scope.add = function(){
            $scope.project = {};
            $scope.title = "添加项目";
            $('#edit-project').modal();
        }

        $scope.edit = function(project_id){
            $http({
                method:'GET',
                url:'/project/' + project_id
            }).then(function successCallback(response){
                if ( response.data.status == 'success' ) {
                    $scope.project = response.data.data;
                    $scope.title = "编辑项目"
                    $('#edit-project').modal();
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login'
                }



            });
        }

        $scope.showerror = function(project_id){
            $http({
                method:'GET',
                url:'/project/' + project_id
            }).then(function successCallback(response){
                if ( response.data.status == 'success' ) {
                    bootbox.dialog(response.data.data.error, [{
	    				"label": "关闭"
		    		}]);
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login'
                }

            });
        }

        $scope.again = function(project_id) {
            $http({
                method: 'POST',
                url: '/project/again',
                params: {
                    'project_id': project_id ,
                }
            }).then( function successCallback(response){
                if ( response.data.status == 'success' ) {
                    $scope.reload();
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login'
                }
            })
        }

        $scope.assignment = function(project_id) {
            $http({
                method: 'GET',
                url: '/project/relation/' + project_id,
            }).then( function successCallback(response){
                if ( response.data.status == 'success' ) {
                    $scope.not_have = response.data.data.not_have
                    $scope.have = response.data.data.have
                    $scope.project_id = project_id
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login'
                }

            })
        }

        $scope.add_machine = function(){
            project = $scope.project_id;
            machine = $scope.select_nothave.join(',');
            $http({
                method: 'POST',
                url: '/project/relation/add',
                params: {
                    'project': project,
                    'machine': machine,
                }
            }).then( function successCallback(response){
                if ( response.data.status == 'success' ) {
                    // 删除节点到左侧
                    $("#select_nothave option:selected").appendTo($("#select_have"))
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login'
                }


            })
        }
        $scope.del_machine = function(){
            project = $scope.project_id;
            machine = $scope.select_have.join(',');
            $http({
                method: 'POST',
                url: '/project/relation/del',
                params: {
                    'project': project,
                    'machine': machine,
                }
            }).then( function successCallback(response){
                if ( response.data.status == 'success' ) {
                    // 删除节点到右侧
                    $("#select_have option:selected").appendTo($("#select_nothave"))
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login'
                }


            })
        }
        



    }]);
});
