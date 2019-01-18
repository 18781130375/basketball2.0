<template>
	<div id="v4force">
	</div>
</template>
<script>
	import * as d3 from 'd3v4'
	export default {
		name: 'v4force',
		data() {
			return {}
		},
		mounted() {
			var nodes = [{
					'name': 'Lillian',
					'sex': 'F'
				},
				{
					'name': 'Gordon',
					'sex': 'M'
				},
				{
					'name': 'Sylvester',
					'sex': 'M'
				},
				{
					'name': 'Mary',
					'sex': 'F'
				},
				{
					'name': 'Helen',
					'sex': 'F'
				},
				{
					'name': 'Jamie',
					'sex': 'M'
				},
				{
					'name': 'Jessie',
					'sex': 'F'
				},
				{
					'name': 'Ashton',
					'sex': 'M'
				},
				{
					'name': 'Duncan',
					'sex': 'M'
				},
				{
					'name': 'Evette',
					'sex': 'F'
				},
				{
					'name': 'Mauer',
					'sex': 'M'
				},
				{
					'name': 'Fray',
					'sex': 'F'
				},
				{
					'name': 'Duke',
					'sex': 'M'
				},
				{
					'name': 'Baron',
					'sex': 'M'
				},
				{
					'name': 'Infante',
					'sex': 'M'
				},
				{
					'name': 'Percy',
					'sex': 'M'
				},
				{
					'name': 'Cynthia',
					'sex': 'F'
				}
			];

			var links = [{
					'source': 'Sylvester',
					'target': 'Gordon',
					'type': 'A'
				},
				{
					'source': 'Sylvester',
					'target': 'Lillian',
					'type': 'A'
				},
				{
					'source': 'Sylvester',
					'target': 'Mary',
					'type': 'A'
				},
				{
					'source': 'Sylvester',
					'target': 'Jamie',
					'type': 'A'
				},
				{
					'source': 'Sylvester',
					'target': 'Jessie',
					'type': 'A'
				},
				{
					'source': 'Sylvester',
					'target': 'Helen',
					'type': 'A'
				},
				{
					'source': 'Helen',
					'target': 'Gordon',
					'type': 'A'
				},
				{
					'source': 'Mary',
					'target': 'Lillian',
					'type': 'A'
				},
				{
					'source': 'Ashton',
					'target': 'Mary',
					'type': 'A'
				},
				{
					'source': 'Duncan',
					'target': 'Jamie',
					'type': 'A'
				},
				{
					'source': 'Gordon',
					'target': 'Jessie',
					'type': 'A'
				},
				{
					'source': 'Sylvester',
					'target': 'Fray',
					'type': 'E'
				},
				{
					'source': 'Fray',
					'target': 'Mauer',
					'type': 'A'
				},
				{
					'source': 'Fray',
					'target': 'Cynthia',
					'type': 'A'
				},
				{
					'source': 'Fray',
					'target': 'Percy',
					'type': 'A'
				},
				{
					'source': 'Percy',
					'target': 'Cynthia',
					'type': 'A'
				},
				{
					'source': 'Infante',
					'target': 'Duke',
					'type': 'A'
				},
				{
					'source': 'Duke',
					'target': 'Gordon',
					'type': 'A'
				},
				{
					'source': 'Duke',
					'target': 'Sylvester',
					'type': 'A'
				},
				{
					'source': 'Baron',
					'target': 'Duke',
					'type': 'A'
				},
				{
					'source': 'Baron',
					'target': 'Sylvester',
					'type': 'E'
				},
				{
					'source': 'Evette',
					'target': 'Sylvester',
					'type': 'E'
				},
				{
					'source': 'Cynthia',
					'target': 'Sylvester',
					'type': 'E'
				},
				{
					'source': 'Cynthia',
					'target': 'Jamie',
					'type': 'E'
				},
				{
					'source': 'Mauer',
					'target': 'Jessie',
					'type': 'E'
				}
			]

			var width = 300;
			var height = 400;
			var svg = d3.select("#v4force")
				.append("svg")
				.attr("width", width)
				.attr("height", height)

			//初始化力学仿真器，通过布局函数格式化数据    
			var simulation = d3.forceSimulation(nodes)
				.force("link", d3.forceLink(links).id((d) => {
					return d.name
				}).distance(60)) //distance设置连线距离
				.force("charge", d3.forceManyBody()) //注1> 
				.force("center", d3.forceCenter(width / 2, height / 2)) //设置力学仿真器的中心
				.on("tick", ticked)

			console.log('nodes', nodes);
			console.log('links', links);

			var color = d3.scaleOrdinal(d3.schemeCategory20); //生成颜色选择器函数，此函数返回颜色数组 (string [])

			//添加group包裹svg元素以进行缩放，目的是在缩放时不会影响整个容器的位置
			var g = svg.append("g")
				.attr("class", "everything");

			// 绘制连线
			var svg_links = g.append('g')
				.selectAll("line")
				.data(links)
				.enter()
				.append("line")
				.style("stroke", "#ccc")
				.style("stroke-width", 3)
				.attr("marker-end", "url(#resolved)");
				
			// 绘制节点    
			var svg_nodes = g.append('g')
				.selectAll("circle")
				.data(nodes)
				.enter()
				.append("circle")
				.attr("r", '10')
				.style("fill", "white")
				.style("stroke", this.circleColor)
				.style("stroke-width", 2)

			//绘制描述节点的文字
			var svg_texts = g.append('g')
				.selectAll("text")
				.data(nodes)
				.enter()
				.append("text")
				.style("fill", "black")
				.attr("dx", -10)
				.attr("dy", -5)
				.text(function(d) {
					return d.name;
				});
			
			var marker =
				svg.append("marker")
				//.attr("id", function(d) { return d; })
				.attr("id", "resolved")
				//.attr("markerUnits","strokeWidth")//设置为strokeWidth箭头会随着线的粗细发生变化
				.attr("markerUnits", "userSpaceOnUse")
				.attr("viewBox", "0 -5 10 10") //坐标系的区域
				.attr("refX", 32) //箭头坐标
				.attr("refY", -1)
				.attr("markerWidth", 5) //标识的大小
				.attr("markerHeight", 10)
				.attr("orient", "auto") //绘制方向，可设定为：auto（自动确认方向）和 角度值
				.attr("stroke-width", 5) //箭头宽度
				.append("path")
				.attr("d", "M0,-5L10,0L0,5") //箭头的路径
				.attr('fill', '#000000'); //箭头颜色
				
			
			//监听拖拽开始    
			function dragstarted(d) {
				if(!d3.event.active) simulation.alphaTarget(0.3).restart(); //alpha是动画的冷却系数，运动过程中会不断减小，直到小于0.005为止，此时动画会停止。
				d.fx = d.x; //fx为固定坐标，x为初始坐标  注3>  
				d.fy = d.y;
			}

			//监听拖拽中  
			function dragged(d) {
				d.fx = d3.event.x; //fevent.x为拖拽移动时的坐标
				d.fy = d3.event.y;
			}

			//监听拖拽结束
			function dragended(d) {
				if(!d3.event.active) simulation.alphaTarget(0);
				d.fx = null; //固定坐标清空
				d.fy = null;
			}

			function zoom_actions() {
				g.attr("transform", d3.event.transform)
			}

			//拖拽时的事件监听器  以实时更新坐标
			function ticked() {
				svg_links.attr("x1", function(d) {
						return d.source.x;
					})
					.attr("y1", function(d) {
						return d.source.y;
					})
					.attr("x2", function(d) {
						return d.target.x;
					})
					.attr("y2", function(d) {
						return d.target.y;
					});

				svg_nodes.attr("cx", function(d) {
						return d.x;
					})
					.attr("cy", function(d) {
						return d.y;
					});

				svg_texts.attr("x", function(d) {
						return d.x;
					})
					.attr("y", function(d) {
						return d.y;
					});
			}
		},
		methods: {
			circleColor(d) {
				if(d.sex === 'M') {
					return 'blue'
				} else {
					return 'pink'
				}
			},
			linkColor(d) {
				if(d.type === 'A') {
					return 'green'
				} else {
					return 'red'
				}
			}
		}
	}
</script>

/*.link line .node circle 节点和线条的样式不能写在
<style scoped></style> 中， 因为 d3 数据是动态渲染的，scoped 中的样式无法控制动态生成的 dom*/
<style>
	.links line {
		stroke: #999;
		stroke-opacity: 0.6;
	}
	
	.nodes circle {
		stroke: #fff;
		stroke-width: 1.5px;
	}
</style>