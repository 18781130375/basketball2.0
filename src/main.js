// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import echarts from 'echarts'
import axios from 'axios'
import $ from 'jquery'
import { Button, Table, Modal } from 'iview';
import 'iview/dist/styles/iview.css';

Vue.component('Button', Button);
Vue.component('Table', Table);
Vue.component('Modal', Modal);

Vue.config.productionTip = false
Vue.prototype.$echarts = echarts
Vue.prototype.$axios = axios
Vue.prototype.$Modal = Modal;
/* eslint-disable no-new */

// 设置axios请求的token
axios.defaults.headers.common['token'] = 'f4c902c9ae5a2a9d8f84868ad064e706'
//设置请求头
axios.defaults.headers.post["Content-type"] = "application/json"

new Vue({
	el: '#app',
	data: {
		Bus: new Vue()
	},
	components: {
		App
	},
	template: '<App/>'
})