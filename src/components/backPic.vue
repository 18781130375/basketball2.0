<template>
	<div id="backPic">
		<div class="force1" style="width:200px;height: 46rem;"></div>
		<div class="baseketball-flied">
			<div class="baseketball-flied-circle">
				<div class="rect">
					<div class="rect-line"></div>
				</div>
			</div>
			<div class="baseketball-flied-circle-1">
				<div class="rect">
					<div class="rect-line-1"></div>
				</div>
			</div>
			<div class="mid-line" id="courtMidLine"></div>
			<div class="courtcir" id="courtcir"></div>
			<div class="baseket"></div>
			<div class="baseket1"></div>
		</div>
		<v4force class="force2"></v4force>
	</div>
</template>

<script>
	import * as echarts from 'echarts'
	import * as $ from 'jquery'
	import * as d3 from 'd3v4'
	import court from '@/assets/court.jpg'
	import CLE from '@/assets/CLE.png'
	import GSW from '@/assets/GSW.png'
	import axios from 'axios'
	import v4force from './v4force'
	export default {
		name: 'backPic',
		components: {
			v4force
		},
		data() {
			return {
				court: court,
				CLE: CLE,
				GSW: GSW
			}
		},
		methods: {
			Init() {
				//////console.log($("#backPic"));
				var width = $(".baseketball-flied").width();
				var height = $(".baseketball-flied").height();
				var svg = d3.select(".baseketball-flied")
					.append("svg")
					.attr("id", "trailsvg")
					.attr("width", width)
					.attr("height", height);

				var infosvg = d3.select('.force1')
					.append("svg")
					.attr("id", "infosvg")
					.attr("width", "200px")
					.attr("height", "46rem")

			},
			DrawTrial(data) {
				if(data.length == 0) {
					//console.log("error");
					return;
				}
				//console.log(data)
				var svgloc = d3.select("#trailsvg");
				var width = $(".baseketball-flied").width();
				var height = $(".baseketball-flied").height();
				let color = ["#EE9572", "#AEEEEE"];

				////////console.log(data);
				dtrail();

				function dtrail() {
					svgloc.selectAll("#loc")
						.data(data)
						.enter()
						.append("path")
						.attr("name", function(d) {
							return d['2'] + 'loc';
						})
						.attr("id", function(d) {
							return d['4'] + 'loc';
						})
						.attr("transform", function(d) {
							return 'translate(' + d[0] + ',' + d[1] + ')';
						})
						.attr("d", d3.symbol().type(function(d) {
							return d3.symbols[d[5]];
						}))
						.attr('stroke', "none")
						.attr("fill", function(d) {
							return d['2'] == 'GSW' ? color[0] : color[1];
						})
						.style("opacity", function(d) {
							return d[5] == 1 ? 1 : 0;
						});
				}
			},
			drect(team) {
				var left = 10,
					top = 10,
					rectw = 20,
					ciry = top + rectw * 1.5;
				var svginfo=d3.select('#infosvg');
				var width=svginfo["_groups"]["0"]["0"].attributes[1].value;
				
				//*10 是rem 转换成px
				var height=parseInt(svginfo["_groups"]["0"]["0"].attributes[2].value)*10+"px";

				var midhei = parseInt(height)/2;
				var midw =  parseInt(width) / 2;
				
				console.log(midhei)
				
				let color = ["#EE9572", "#AEEEEE"];
				var rectdata = [
					[left, top, color[0], "GSW", "GSW球队轨迹"],
					[left, top + midhei, color[1], "CLE", "CLE球队轨迹"]
				];
				console.log(rectdata)
				console.log(team);
				svginfo.selectAll("#iconrect")
					.data(rectdata)
					.enter()
					.append("rect")
					.attr("id", function(d) {
						return d[3] + 'icon';
					})
					.attr("x", function(d) {
						return d[0];
					})
					.attr("y", function(d) {
						return d[1];
					})
					.attr("width", rectw)
					.attr("height", rectw)
					.attr("fill", function(d) {
						return d[2]
					})
					.style("opacity", 1)
					.on("click", function(d) {
						clickme(d[3], team);
					});

				svginfo.selectAll("iconTxt")
					.data(rectdata)
					.enter()
					.append("text")
					.attr("id", function(d) {
						return d[3] + 'text';
					})
					.attr("x", function(d) {
						return d[0];
					})
					.attr("y", function(d) {
						return d[1];
					})
					.attr("dx", rectw)
					.attr("dy", rectw / 1.5)
					.attr("stroke", function(d) {
						return 'none';
					})
					.attr("font-size", 15)
					.style("opacity", 1)
					.text(function(d) {
						return d[4]
					});

				
				svginfo.selectAll("#iconCir")
					.data(team)
					.enter()
					.append("circle")
					.attr("id", function(d) {
						return d[0] + "iconpy";
					})
					.attr("cx", function(d) {
						return d[1] > 3 ? midw : left;
					})
					.attr("cy", function(d) {
						var index = d[1];
						if(d[1] > 3) index = d[1] - 3;
						return d[2] == 'GSW' ? ciry + index * 20 : midhei + top + (index + 1) * 20;
					})
					.attr('r', function(d) {
						return rectw / 2;
					})
					.attr('stroke', "none")
					.attr("fill", function(d) {
						return d[2] == 'GSW' ? color[0] : color[1];
					})
					.style("opacity", function(d) {
						if(d[1] == 1) return 1;
						else return 0.3;
					});

				svginfo.selectAll("#playertxt")
					.data(team)
					.enter()
					.append("text")
					.attr("id", function(d) {
						return d[0] + "icontext";
					})
					.attr("x", function(d) {
						return d[1] > 3 ? midw : left;
					})
					.attr("y", function(d) {
						var index = d[1];
						if(d[1] > 3) index = d[1] - 3;
						return d[2] == 'GSW' ? ciry + index * 20 : midhei + top + (index + 1) * 20;
					})
					.attr('dx', function(d) {
						return -rectw / 2.5;
					})
					.attr('dy', rectw / 3)
					.attr("stroke", function(d) {
						return 'none';
					})
					.attr("font-size", 15)
					.style("opacity", 1)
					.text(function(d) {
						return d['3'];
					})
					.on("click", function(d) {
						clickpy(d[2], d[0])
					});

				svginfo.selectAll("#symbol")
					.data(team)
					.enter()
					.append("path")
					.attr("transform", function(d) {
						var x = left + 20,
							index = d[1],
							y;
						if(d[1] > 3) {
							x = midw + 20;
							index = d[1] - 3;
						}
						if(d[2] == 'GSW') {
							y = ciry + index * 20;
						} else {
							y = midhei + top + (index + 1) * 20
						}
						//							////console.log(x);
						//							////console.log(y);
						return 'translate(' + x + ',' + y + ')';
					})
					.attr("d", d3.symbol().type(function(d, i) {
						//////console.log(d);
						return d3.symbols[d[1]];
					}))
					.attr('stroke', "none")
					.attr("fill", function(d) {
						return d[2] == 'GSW' ? color[0] : color[1];
					});

				function clickpy(tname, id) {
					var tgroups = document.getElementsByName(tname + "loc");
					var icon = document.getElementById(id + "iconpy");
					for(var i in tgroups) {
						var group = tgroups[i];
						if(group.id == id + 'loc') {
							if(icon.style.opacity == 1) {
								group.style.opacity = 0;
							} else {
								group.style.opacity = 1;
							}
						}
					}
					if(icon.style.opacity == 1) icon.style.opacity = 0.3;
					else icon.style.opacity = 1.0;
				}

				function clickme(name, team) {
					var dom = document.getElementsByName(name + "loc");
					var iconrect = document.getElementById(name + "icon");
					//////console.log(name);
					for(var i in team) {
						if(team[i][2] == name) {
							var pyicon = document.getElementById(team[i][0] + "iconpy");
							if(iconrect.style.opacity == 1) {
								pyicon.style.opacity = 0.3;
							} else {
								pyicon.style.opacity = 1;
							}
						}
					}

					if(iconrect.style.opacity == 1) {
						for(var i = 0; i < dom.length; i++) {
							dom[i].style.opacity = 0;
						}
						iconrect.style.opacity = 0.4;
					} else {
						iconrect.style.opacity = 1;
						for(var i = 0; i < dom.length; i++) {
							if(i != "length") {
								dom[i].style.opacity = 1;
							}
						}
					}
				}
			},

			HeatCourt(GetScoreData) {
				var svgloc = d3.select("#trailsvg");
				var width = $(".baseketball-flied").width(),
					height = $(".baseketball-flied").height();

				//col:列 wid  row：行：hei
				var colscale = d3.scaleLinear()
					.domain([0, 94])
					.range([0, width]);
				var rowscale = d3.scaleLinear()
					.domain([0, 50])
					.range([0, height]);

				//rows:行方向上网格的个数 cols:列方向上网格的个数 ell表示大小
				var rows = 50,
					cols = 50;
				var colcell = width / cols;
				var rowcell = height / rows;

				//统计数组
				var scoreCnt = new Array();
				for(var i = 0; i < rows; i++) {
					scoreCnt[i] = new Array();
					for(var j = 0; j < cols; j++) {
						scoreCnt[i][j] = 0;
					}
				}
				////console.log(scoreCnt)

				//绘制网格
				for(var i = 0; i < rows; i++) {
					for(var j = 0; j < cols; j++) {
						var x = i * colcell;
						var y = j * rowcell;

						svgloc.append("rect")
							.attr("id", 'cell_' + i + "_" + j)
							.attr('x', x)
							.attr('y', y)
							.attr('width', colcell)
							.attr('height', rowcell)
							.attr("fill", 'rgb(255,255,255)')
							//.attr("stroke", "black")
							//.attr("stroke-width", 0.001)
							.style('opacity', 0.8);
					}
				}

				//随机生成投球数据
//				var GetScoreData = [];
//				for(var i = 0; i < 3000; i++) {
//					var x = Math.random(0, 1) * 94;
//					var y = Math.random(0, 1) * 15;
//					var miss = Math.random(0, 1);
//					if(miss > 0.5) GetScoreData.push([x, y, 1]);
//					else GetScoreData.push([x, y, -1]);
//				}
//				for(var i = 0; i < 3000; i++) {
//					var x = Math.random(0, 1) * 94;
//					var y = Math.random(0, 1) * 15 + 35;
//					var miss = Math.random(0, 1);
//					if(miss > 0.5) GetScoreData.push([x, y, 1]);
//					else GetScoreData.push([x, y, -1]);
//				}
//				console.log(GetScoreData);

				//处理判断生成的数据在哪个cell里面
				for(var i = 0; i < GetScoreData.length; i++) {

					var ScoreData = GetScoreData[i];
					var x = colscale(ScoreData[0]);
					var y = rowscale(ScoreData[1]);
					var yIndex = parseInt(y / colcell);
					var xIndex = parseInt(x / rowcell);
					
					//1:得分 -1：失球
					if(ScoreData[2] == 1) scoreCnt[yIndex][xIndex] += 1;
					else scoreCnt[yIndex][xIndex] -= 1;
				}
				////console.log(scoreCnt)

				//渐变色
				var interpolatorUp = d3.interpolateRgb("white", "red");
				var interpolatorDown = d3.interpolateRgb("#3182bd", "white")
				////console.log(interpolator(1));

				//热力图绘制
				//最大最小的得分区域数值
				var max = largestOfFour(scoreCnt);
				var min = smallstOfFour(scoreCnt);
//				console.log(max)
//				console.log(min)

				for(var i = 0; i < cols; i++) {
					for(var j = 0; j < rows; j++) {
						var cnt = scoreCnt[i][j];
						if(cnt >= 0) {
							d3.select('#cell_' + i + "_" + j)["_groups"]["0"]["0"].attributes[5].value = interpolatorUp(cnt / max);
						} else {
							d3.select('#cell_' + i + "_" + j)["_groups"]["0"]["0"].attributes[5].value = interpolatorDown((-cnt) / min);
						}
					}
				}

				//找二维数组的最大值
				function largestOfFour(arr) {
					var newArray = arr.join(",").split(",");
					return Math.max.apply({}, newArray);
				}

				function smallstOfFour(arr) {
					var newArray = arr.join(",").split(",");
					return Math.min.apply({}, newArray);
				}
			},
			//绘制球场
			DrawCourt() {
				var svgloc = d3.select("#trailsvg");
				var width = $(".baseketball-flied").width(),
					height = $(".baseketball-flied").height();
				var pie = d3.pie();

				var piedata = pie([10]);

				var outerRadius = 30; //外半径
				var innerRadius = 28; //内半径，为0则中间没有空白

				var arc = d3.arc() //弧生成器
					.innerRadius(innerRadius) //设置内半径
					.outerRadius(outerRadius); //设置外半径

				var arcs = svgloc.selectAll("g")
					.data(piedata)
					.enter()
					.append("g")
					.attr("transform", "translate(" + (width / 2) + "," + (height / 2) + ")");

				arcs.append("path")
					.attr("fill", "black")
					.attr("d", function(d) {
						return arc(d);
					});
			},
			DrawTeamInfo() {
				var svgloc = d3.select("#trailsvg");
				var width = $(".baseketball-flied").width(),
					height = $(".baseketball-flied").height();
				//				svgloc.append("image")
				//					.attr("id", "basketimg")
				//					.attr('xlink:href', CLE)
				//					.attr('width', 100)
				//					.attr('height', 100)
				//					.attr("transform", "translate(" + (width / 2) + "," + height / 2.5 + ")");
				svgloc.append("image")
					.attr("id", "basketimg")
					.attr('xlink:href', GSW)
					.attr('width', 150)
					.attr('height', 150)
					.attr("transform", "translate(" + (width / 2.3) + "," + height / 3 + ")");
					console.log(document.getElementById('courtcir').style.display);
			},
			DisplayMidCir(){
				document.getElementById('courtcir').style.display='block';
				document.getElementById('courtMidLine').style.display='block';
			}
		},
		mounted() {
			document.getElementById('courtcir').style.display='none';
			document.getElementById('courtMidLine').style.display='none';
			let me = this;
			me.Init();
		
			me.$axios.get('/apis/result_pos/0,720')
					.then(res => {
						//console.log(res.data);
						me.HeatCourt(res.data);
						//绘制logo
						me.DrawTeamInfo();
					})
			

			me.$root.Bus.$on('trail', function(selectRange) {
				var str = "";
				for(var i = 0; i < selectRange.length; i++) {
					str += selectRange[i][0] + "," + selectRange[i][1] + ";";
				}
				////console.log(str);
				getData(str);
			});

			function Usedata(traildata) {
				var player = {
					2544: ['LeBron James', 'CLE', 23],
					2571: ['Leandro Barbosa', 'GSW', 19],
					2590: ['Mo Williams', 'CLE', 52],
					2592: ['James Jones', 'CLE', 1],
					2733: ['Shaun Livingston', 'GSW', 34],
					2738: ['Andre Iguodala', 'GSW', 9],
					2747: ['J.R. Smith', 'CLE', 5],
					101106: ['Andrew Bogut', 'GSW', 12],
					201567: ['Kevin Love', 'CLE', 0],
					201575: ['Brandon Rush', 'GSW', 4],
					201578: ['Marreese Speights', 'GSW', 5],
					201939: ['Stephen Curry', 'GSW', 30],
					202389: ['Timofey Mozgov', 'CLE', 20],
					202681: ['Kyrie Irving', 'CLE', 2],
					202684: ['Tristan Thompson', 'CLE', 13],
					202691: ['Klay Thompson', 'GSW', 11],
					202697: ['Iman Shumpert', 'CLE', 4],
					203105: ['Festus Ezeli', 'GSW', 31],
					203110: ['Draymond Green', 'GSW', 23],
					203521: ['Matthew Dellavedova', 'CLE', 8],
					203546: ['Ian Clark', 'GSW', 21],
					203949: ['James Michael McAdoo', 'GSW', 20]
				};

				var width = $(".baseketball-flied").width();
				var height = $(".baseketball-flied").height();
				var xScale = d3.scaleLinear()
					.domain([0, 94])
					.range([0, width]);
				var yScale = d3.scaleLinear()
					.domain([0, 50])
					.range([0, height]);

				var loc = [];
				var team = [];
				var team_Id = [];
				var hspy = {};
				var cnt1 = 1,
					cnt2 = 1;
				getset(loc);

				function getset(array) {
					for(var i = 0; i < traildata.length; i++) {
						for(var m = 0; m < traildata[i].length; m++) {
							var domdata = traildata[i][m];
							for(var key in player) {
								var x1 = domdata[key + '_x'];
								if(x1 != 10000) {
									var x = xScale(x1);
									var y = yScale(domdata[key + '_y']);
									var msg = player[key];
									if(team.indexOf(key) == -1 && msg['1'] == 'GSW') {
										team.push(key);
										team_Id.push([key, cnt1, "GSW", msg['2']]);
										hspy[key] = cnt1;
										cnt1++;
									}
									if(team.indexOf(key) == -1 && msg['1'] == 'CLE') {
										team.push(key);
										team_Id.push([key, cnt2, "CLE", msg['2']]);
										hspy[key] = cnt2;
										cnt2++;
									}
									/*x,y,球队,球号*/
									loc.push([x, y, msg['1'], parseInt(msg['2']), key, hspy[key]]);
									////////console.log(x);
								}
							
}
						}
					}
					//console.log(loc);
				}
				//sort 二维数组排序
				//loc.sort(function(x,y){ return x[3]>y[3]?1:-1;})
				//////console.log(loc);
				//							var loc1 = loc.filter(function(d, i) {
				//								return i % 3 == 0;
				//							})
				
				console.log(loc)
				me.DisplayMidCir();
				$("#trailsvg").empty();
				me.DrawTrial(loc);
				me.drect(team_Id);
			}

			function getData(str) {
				me.$axios.get('/apis/Some_Time_player_position/' + str)
					.then(res => {
						//console.log(res.data);
						Usedata(res.data);
					})
			}
		}
	}
</script>

<style>
	* {
		font-size: 10px;
	}
	
	.baseketball-flied {
		width: 86rem;
		height: 46rem;
		border: .2rem solid black;
		position: relative;
		overflow: hidden;
		float: left;
	}
	
	.baseketball-flied,
	.force1,
	.force2 {
		float: left;
	}
	
	.baseketball-flied-circle {
		width: 43rem;
		height: 36.2rem;
		border-radius: 18.1rem;
		position: absolute;
		top: 4.76rem;
		left: -18.1rem;
		border: .2rem solid black;
	}
	
	.baseketball-flied-circle .rect {
		width: 38rem;
		height: 14.48rem;
		border: .2rem solid black;
		position: absolute;
		top: 10.86rem;
		left: 0px;
		border-radius: 8rem;
	}
	
	.baseketball-flied-circle-1 {
		width: 43rem;
		height: 36.2rem;
		border-radius: 18.1rem;
		position: absolute;
		top: 4.76rem;
		right: -18.1rem;
		overflow: hidden;
		border: .2rem solid black;
	}
	
	.baseketball-flied-circle-1 .rect {
		width: 38rem;
		height: 14.48rem;
		border: .2rem solid black;
		position: absolute;
		top: 10.86rem;
		right: 0rem;
		border-radius: 8rem;
	}
	
	.mid-line {
		width: .15rem;
		background: black;
		height: 46.1rem;
		position: absolute;
		left: 43rem;
		display: none;
	}
	
	.courtcir {
		width: 12rem;
		height: 12rem;
		border: .2rem solid black;
		border-radius: 6rem;
		position: absolute;
		left: 37rem;
		top: 17rem;
		display: none;
	}
	
	.rect .rect-line {
		width: .2rem;
		height: 14.48rem;
		background: black;
		position: absolute;
		left: 32rem;
	}
	
	.rect .rect-line-1 {
		width: .2rem;
		height: 14.48rem;
		background: black;
		position: absolute;
		right: 32rem;
	}
	
	.baseket {
		width: 4rem;
		height: 4rem;
		border-radius: 4rem;
		border: .2rem solid black;
		position: absolute;
		top: 21rem;
		left: -2rem;
	}
	
	.baseket1 {
		width: 4rem;
		height: 4rem;
		border-radius: 4rem;
		border: .2rem solid black;
		position: absolute;
		top: 21rem;
		right: -2rem;
	}
</style>