define(['/assets/js/main/ctrls/module.js'],function(fabric){
    fabric.controller('machineCtrl',['$rootScope','$scope','$http','$location','$state','$stateParams', function($rootScope,$scope,$http,$location,$state,$stateParams){

        $scope.reload = function reload(){
            $http({
                methon: 'GET',
                url: '/machine/list',
                params: {
                    'project' : $stateParams.id ,
                }
            }).then( function successCallback(response) {
                if ( response.data.status == 'success' ) {
                    $scope.machines = response.data.data;
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
            }, function errorCallback(response) {

            }
            );
        }

        $scope.reload();

        $scope.add_machine = function(){
            if( ! $scope.machine.id ) {
                $http({
                    method: 'POST',
                    url: '/machine/add',
                    params: {
                        'name': $scope.machine.name,
                        'account': $scope.machine.account,
                        'password': $scope.machine.password,
                        'desc': $scope.machine.desc,
                        'ip': $scope.machine.ip,
                        'auth_type': $scope.machine.auth_type
                    }
                }).then(function successCallback(response) {
                    // coding...
                    if (response.data.status == 'success') {
                        $('#add-machine').modal('hide');
                        $scope.reload();
                    }
                    if (response.data.status == 'error') {
                        alert(response.data.msg);
                    }
                    if (response.data.status == 'exception') {
                        alert(response.data.msg);
                    }
                    if (response.data.status == 'logout') {
                        window.location.href = '/login'
                    }
                }, function errorCallback(response) {
                    // 处理不成功
                });
            }
            if ( $scope.machine.id ) {
                // 编辑操作
                $http({
                    method: 'POST',
                    url: '/machine/edit',
                    params: {
                        'id': $scope.machine.id,
                        'name': $scope.machine.name,
                        'account': $scope.machine.account,
                        'password': $scope.machine.password,
                        'desc': $scope.machine.desc,
                        'ip': $scope.machine.ip,
                        'auth_type': $scope.machine.auth_type
                    }
                }).then(function successCallback(response) {
                    // coding...
                    if (response.data.status == 'success') {
                        $('#add-machine').modal('hide');
                        $scope.reload();
                    }
                    if (response.data.status == 'error') {
                        alert(response.data.msg);
                    }
                    if (response.data.status == 'exception') {
                        alert(response.data.msg);
                    }
                    if (response.data.status == 'logout') {
                        window.location.href = '/login'
                    }
                }, function errorCallback(response) {
                    // 处理不成功
                });
            }
        }

        $scope.add_machine_button = function(){
            $('#add-machine').modal();
            $scope.machine = {} ;
            $scope.machine.auth_type = 'password';
            $scope.title = '添加机器';
        }

        $scope.delete = function(machine_id){
            $http({
                method: 'POST',
                url: '/machine/del',
                params: {
                    'machine': machine_id ,
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

            }

            );
        }
        
        $scope.edit = function( machine_id ) {
            $http({
                method: 'GET',
                url: '/machine/'+ machine_id,
            }).then( function successCallback(response){
                if ( response.data.status == 'success' ) {
                    $scope.machine = response.data.data;
                    $scope.title = '修改信息';
                    $('#add-machine').modal();
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

            );
        }



    }]);
});
