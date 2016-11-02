require.config({
	baseUrl: '/assets/',
	// path映射那些不直接放置于baseUrl下的模块名。
	paths:{
		//一些库文件
		"angular":"js/lib/angular/angular",
		"angular-ui-router":"js/lib/angular-ui-router/angular-ui-router",
		"angular-messages":"js/lib/angular-messages/angular-messages.min",
		//js文件
		'bootstrap': "js/main/bootstrap",
		'fabric': "js/main/fabric",
		'router': "js/main/router",
		// 以及其他的js文件
			// 控制器们
		'mainCtrl':"js/main/ctrls/mainCtrl",
			// 指令们
		'mainDirective':"js/main/directives/mainDirective",
			// 服务们
		'mainService':"js/main/services/mainService",
	},
	// 为那些没有使用define()来声明依赖关系、设置模块的"浏览器全局变量注入"型脚本做依赖和导出配置。
	shim:{
		'angular':{
			exports:'angular'
		},
		'angular-ui-router':{
			deps:['angular'],
			exports: 'angular-ui-router'
		},
		'angular-messages':{
			deps:['angular'],
			exports: 'angular-messages'
		},
	},
	// 要先加载bootstrap.js文件
	deps:['bootstrap'],
	// 防止读取缓存，调试用
	urlArgs: "bust=" + (new Date()).getTime(),
	//更新用户缓存一次
	//urlArgs: "bust=" + 63,
	waitSeconds: 0
});