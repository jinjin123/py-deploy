define(['/assets/js/main/ctrls/module.js'],function(fabric){
    fabric.controller('fabricCtrl',['$rootScope','$scope','$http','$location', function($rootScope,$scope,$http,$location){

        $scope.isShowMachine = true;
        $scope.isNew = true;
        $scope.isTag = true;
        $scope.selected_machine = true;
        if ( $scope.isNew && $scope.isTag ) {
            $scope.isProject = true;
        }

        $scope.reload = function reload(status){
            $http({
                method: 'GET',
                url: '/fabric/list',
                params:{
                    'status': status
                }
            }).then(
                function successCallback( response ) {
                    if ( response.data.status == 'success' ) {
                        $scope.fabric_list = response.data.data;
                    }
                    if ( response.data.status == 'error' ) {
                        alert(response.data.msg);
                    }
                    if ( response.data.status == 'exception' ) {
                        alert( response.data.msg );
                    }
                    if ( response.data.status == 'logout' ) {
                        window.location.href='/login' ;
                    }
                }
            )
        }
        $scope.reload('');

        function _getProjects(status){
            $http({
                method: 'GET',
                url: '/project/list',
                params: {
                    'status': status,
                }
            }).then( function successCallback(response) {
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
                    window.location.href='/login' ;
                }
            }, function errorCallback(response){
                // 处理不成功

            } );
        }

        function _getMachines(project_id) {
            $http({
                method: 'GET',
                url: '/machine/project/' + project_id,
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
                    window.location.href='/login' ;
                }

            }, function errorCallback(response){

            } );
        }

        function _getTags(project_id){
            $http({
                method: 'GET',
                url: '/fabric/tag',
                params: {
                    'project': project_id,
                }
            }).then( function successCallback(response) {
                if ( response.data.status == 'success' ) {
                    $scope.tags = response.data.data;
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login' ;
                }

            }, function errorCallback(response){

            } );

        }

        function _getUsableTag(){
            $http({
                method: 'GET',
                url: '/fabric/usabletag',
            }).then( function successCallback(response) {
                if ( response.data.status == 'success' ) {
                    $scope.fabric.tag = response.data.data.tag;
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login' ;
                }

            }, function errorCallback(response){

            } );

        }

        $scope.getTagsandMachines = function(project_id) {
            if ( $scope.fabric.type == 'tag' ) {
                _getTags(project_id);
            }
            _getUsableTag()
            _getMachines(project_id)
        }


        $scope.fabric_new = function(){
            _getProjects('ready') ;
            $scope.type = "new";
        }

        $scope.fabric_tag = function(){
            _getProjects('ready') ;
            $scope.type = "tag";
        }

        //===================新增发布计划需要的代码=============================
        $scope.add = function(){
            $scope.title = "创建发布计划";
            $scope.fabric = null ;
            $("#add-fabric").modal({
                keyboard: false,
                backdrop: 'static',
            });
        }
        $scope.getProjects = function(status){
            $scope.projects = {} ;
            $scope.fabric.tag = null ;
            $scope.fabric.project_id = null ;
            $scope.machines = null ;
            _getProjects(status)
        }
        //====================新增发布计划需要的代码===========================

        $scope.add_fabric = function(){
            var type = $scope.fabric.type;
            var project_id = $scope.fabric.project_id;
            var desc = $scope.fabric.desc;
            var tag = $scope.fabric.tag;
            var fabric_id = $scope.fabric.id;

            if ( !fabric_id ) {
                var checkok = new Array();
                $('input[name="machine"]:checked').each(function(){
                    checkok.push( this.value )
                })
                if ( checkok[0] == 'on' ) {
                    checkok.shift();
                }
                checked = checkok.join(',');

                $http({
                    method: 'POST',
                    url: '/fabric/add',
                    params: {
                        'type': type,
                        'project': project_id,
                        'desc': desc,
                        'tag': tag,
                        'machine': checked,
                    }
                }).then( function successCallback(response) {
                    if ( response.data.status == 'success' ) {
                        $("#add-fabric").modal('hide');
                        $scope.reload();
                    }
                    if ( response.data.status == 'error' ) {
                        alert(response.data.msg);
                    }
                    if ( response.data.status == 'exception' ) {
                        alert( response.data.msg );
                    }
                    if ( response.data.status == 'logout' ) {
                        window.location.href='/login' ;
                    }

                }, function errorCallback(response){

                } );
            } else {
                $http({
                    method: 'POST',
                    url: '/fabric/edit',
                    params: {
                        'fabric_id': fabric_id,
                        'type': type,
                        'project': project_id,
                        'desc': desc,
                        'tag': tag,
                    }
                }).then( function successCallback(response) {
                    if ( response.data.status == 'success' ) {
                        $("#add-fabric").modal('hide');
                        $scope.reload();
                    }
                    if ( response.data.status == 'error' ) {
                        alert(response.data.msg);
                    }
                    if ( response.data.status == 'exception' ) {
                        alert( response.data.msg );
                    }
                    if ( response.data.status == 'logout' ) {
                        window.location.href='/login' ;
                    }

                }, function errorCallback(response){

                } );
            }


        }

        _fabricInfo = function(fabric_id){
            $http({
                method: 'GET',
                url: '/fabric/'+fabric_id,
            }).then( function successCallback(response) {
                if ( response.data.status == 'success' ) {
                    $scope.fabric = response.data.data;
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login' ;
                }

            }, function errorCallback(response){

            } );
        }

        // ====================编辑发布计划===================
        $scope.edit = function( fabric_id, type, project_id ) {
            $scope.title = "编辑发布计划";
            $scope.fabric = {}
            _getProjects('ready');
            if ( type == 'tag' ) {
                _getTags(project_id);
            }
            _fabricInfo(fabric_id);
            $("#add-fabric").modal();

        }
        // ==================/编辑发布计划================

        $scope.ready = function(fabric_id){
            $http({
                method: 'POST',
                url: '/fabric/ready',
                params: {
                    'fabric': fabric_id,
                }
            }).then( function successCallback(response) {
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
                    window.location.href='/login' ;
                }

            }, function errorCallback(response){

            } );
        }

        $scope.cancel = function(fabric_id){
            $http({
                method: 'POST',
                url: '/fabric/cancel',
                params: {
                    'fabric': fabric_id,
                }
            }).then( function successCallback(response) {
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
                    window.location.href='/login' ;
                }

            }, function errorCallback(response){

            } );
        }

        $scope.deploy = function(fabric_id){
            $http({
                method: 'POST',
                url: '/fabric/deploy',
                params: {
                    'fabric': fabric_id,
                }
            }).then( function successCallback(response) {
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
                    window.location.href='/login' ;
                }
            }, function errorCallback(response){

            } );
        }

        $scope.assignment = function(fabric_id){

            //
            $http({
                method: 'GET',
                url: '/fabric/machine/' + fabric_id
            }).then( function successCallback(response) {
                if ( response.data.status == 'success' ) {
                    $scope.have = response.data.data.have;
                    $scope.not_have = response.data.data.not_have;
                    $scope.fabric_id = response.data.data.fabric_info.id;
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login' ;
                }
            }, function errorCallback(response){

            } );

            $('#assignment').modal();
        }

        $scope.add_machine = function() {
            fabric_id = $scope.fabric_id ;
            machine_id = $scope.select_nothave;

            $http({
                method: 'POST',
                url: '/fabric/addmachine',
                params:{
                    'fabric_id' : fabric_id,
                    'machine_id': machine_id ,
                }
            }).then( function successCallback(response) {
                if ( response.data.status == 'success' ) {
                    // 删除节点到左侧
                    $("#select_nothave option:selected").appendTo($("#select_have"));
                    $scope.reload();
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login' ;
                }
            }, function errorCallback(response){

            } );
        }

        $scope.del_machine = function() {
            fabric_id = $scope.fabric_id ;
            machine_id = $scope.select_have ;
            $http({
                method: 'POST',
                url: '/fabric/delmachine',
                params:{
                    'fabric_id' : fabric_id,
                    'machine_id': machine_id ,
                }
            }).then( function successCallback(response) {
                if ( response.data.status == 'success' ) {
                     // 删除节点到右侧
                    $("#select_have option:selected").appendTo($("#select_nothave"));
                    $scope.reload();
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login' ;
                }
            }, function errorCallback(response){

            } );
        }

        $scope.viewmachine = function(fabric_id) {
            $http({
                method: 'get',
                url: '/fabric/viewmachine/'+fabric_id,
            }).then( function successCallback(response) {
                if ( response.data.status == 'success' ) {
                    $scope.machine_list = response.data.data;
                    $("#machinelist").modal({
                        keyboard: false,
                        backdrop: 'static',
            });
                }
                if ( response.data.status == 'error' ) {
                    alert(response.data.msg);
                }
                if ( response.data.status == 'exception' ) {
                    alert( response.data.msg );
                }
                if ( response.data.status == 'logout' ) {
                    window.location.href='/login' ;
                }
            }, function errorCallback(response){

            } );

        }

        // 显示错误信息
        $scope.show_error = function(fabric_id){
            $http({
                method: 'GET',
                url: '/fabric/'+fabric_id,
            }).then( function successCallback(response) {
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
                    window.location.href='/login' ;
                }

            }, function errorCallback(response){

            } );
        }


    }]);
});




















