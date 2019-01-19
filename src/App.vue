<template>
	<div id="app">
		<div class="header">
			<teamLogo></teamLogo>
		</div>
		<div class="main">
			<backPic></backPic>
		</div>
		<div class="footer">
			<teamEvent></teamEvent>
		</div>
	</div>
</template>
<script>
	import teamEvent from './components/team1Event'
	import backPic from './components/backPic'
	import teamLogo from './components/teamLogo'
//	import leftGird from './components/leftGrid'
//	import v4force from './components/v4force'
	import * as d3 from 'd3v4'
	export default {
		name: 'App',
		components: {
			backPic,
			teamEvent,
			teamLogo,
//			leftGird,
//			v4force
		},
		data() {
			return {}
		},
		mounted() {
			//	var app=document.getElementById("app");
			//	console.log(this.$refs.app.style)
		}
	}
</script>
<style>
	#app {
		width: 100%;
		height: 100%;
		/*background-color:#c7c7c7;*/
		position: fixed;
		/*相对于窗口定位*/
	}
	
	.header {
		width: 100%;
		height: 10%;
		border: solid 1px black;
	}
	
	.main {
		width: 100%;
		height: 46rem;
		border: solid 1px black;
	}
	
	.footer {
		width: 100%;
		height: 38%;
		border: solid 1px black;
	}
	
	#backPic {
		width: 100%;
		height: 46rem;
		float: left;
	}
	
	#team_event {
		height: 100%;
	}
	
	.leftGrid,
	.rightGrid {
		/*border: solid 1px black;*/
		float: left;
	}
	
	.leftGrid{
		width: 20%;
		height: 100%;
	}
	* {
		margin: 0px;
		padding: 0px;
		box-sizing: border-box;
	}
</style>