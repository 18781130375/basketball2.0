<template>
	<div id="team_event">
	</div>
</template>
<script type="text/javascript">
	import * as d3 from 'd3v4'
	import * as echarts from 'echarts'
	import $ from 'jquery'
	import axios from 'axios'
	import foul from '@/assets/foul.png'
	import free from '@/assets/free.png'
	import Assist from '@/assets/Assist.png'
	import Block from '@/assets/Block.png'
	import miss from '@/assets/miss.png'
	import rebound_defensive from '@/assets/rebound_defensive.png'
	import rebound_offensive from '@/assets/rebound_offensive.png'
	import rebound from '@/assets/rebound.png'
	import Steal from '@/assets/steal.png'
	import sub from '@/assets/sub.png'
	import turnover from '@/assets/turnover.png'
	import violation from '@/assets/violation.png'
	import adv from '@/assets/adv.png'
	import disadv from '@/assets/disadv.png'
	import pt1 from '@/assets/pt1.png'
	import pt2 from '@/assets/pt2.png'
	import pt3 from '@/assets/pt3.png'
	export default {
		data() {
			return {
				foul: foul,
				free: free,
				miss: miss,
				rebound_defensive: rebound_defensive,
				rebound_offensive: rebound_offensive,
				rebound: rebound,
				sub: sub,
				turnover: turnover,
				violation: violation,
				adv: adv,
				disadv: disadv,
				pt1: pt1,
				pt2: pt2,
				pt3: pt3,
				Steal: Steal,
				Block: Block,
				Assist: Assist
			}
		},
		methods: {
			RandomTime() {
				var time = [];
				var temp = 0;
				while(temp <= 720) {
					var t = Math.random(0, 1) * 30;
					time.push([temp, temp + t]);
					temp = temp + t;
				}
				console.log(time);
				return time;
			}
		},
		created() {},
		mounted() {
			var me = this;
			var width = $("#team_event").width(),
				height = $("#team_event").height();

			var svgContainer = d3.select("#team_event")
				.append("svg")
				.attr("id", "eventsvg")
				.attr("width", width)
				.attr("height", height);

			var xscale = d3.scaleLinear()
				.domain([0, 720])
				.range([20, width * 0.9]);

			var imgwid = 22;
			var playerpad = height * 0.7 / 10,
				team1wid = playerpad * 5 * 1.2;

			this.$axios.get('/apis/staff/0,720').then(res => {
				//console.log(res.data);
				DrawEvents(res.data);
				//FilterEvents(515.2, 541.1);
			})

			//获取折线图数据
			this.$axios.get('/apis/attack_time/' + '0' + ',' + '720').then(res => {
				var score = res.data;
				DrawStepLine(score);
			})
			
			//获取步态数据
//			this.$axios.get('/apis/score/' + '0' + ',' + '720').then(res => {
//				var score = res.data;
//				console.log(score)
//			})
//			
			//模拟的步态时间 一个步态 是一个投球
			var time = me.RandomTime();
			for(var i in time) {
				drawMask(time[i][0], time[i][1]);
			}

			//mask层的交互
			function drawMask(st, et) {
				var stepwid = xscale(et) - xscale(st);
				var stephei = height * 0.8;

				var maskrect = svgContainer
					.append('rect')
					.attr("id", "mask_" + st + "_" + et)
					.attr("name", "masks")
					.attr("x", xscale(st))
					.attr("y", 0)
					.attr("width", stepwid)
					.attr("height", stephei)
					.attr("fill", 'rgb(255,255,255)')
					.attr("stroke", "black")
					.attr("stroke-width", 1)
					.style('opacity', 0.1)
					.on('click', function(d) {
						var dom = document.getElementById("mask_" + st + "_" + et);
						if(dom.style.opacity == 0.1) {
							dom.style.opacity = 1;
							FilterClick(st, et);
						} else {
							dom.style.opacity = 0.1;
							FilterClick(st, et);
						}
					});
			}

			//绘制分差曲线
			function DrawStepLine(score) {
				var dataset = [];
				var tempscore = score[0][1];
				var temptime = score[0][0];

				//重构数组 步行折线图的格式
				for(var i in score) {
					var now = score[i];
					//now[1]:现在的分差 now[0]:现在的时间
					if(now[1] != tempscore) dataset.push([now[0], tempscore]);
					dataset.push(now);
					tempscore = now[1];
					temptime = now[0];
				}
				//console.log(dataset);
				var lineyscale = d3.scaleLinear()
					.domain([-10, 10])
					.range([height * 0.8, 20]);

				//折现生成器
				var line = d3.line()
					.x(function(d) {
						return xscale(d[0])
					})
					.y(function(d) {
						return lineyscale(d[1])
					});

				//绘制折线图
				svgContainer.selectAll('path')
					.data(dataset)
					.enter()
					.append('path')
					.attr('stroke-width', 4)
					.attr('d', line(dataset))
					.attr('fill', "none")
					.attr("stroke", "#ccc");
			}

			function DrawEvents(Period1) {
				//console.log(Period1);
				//				var playerpad = 30,
				//					team1wid = 220;
				var team1 = [],
					team2 = [],
					imgpad = 5;
				var advData = []; /*有利数据*/
				var disadvData = []; /*不有利数据*/

				var team1ID = 'GSW',
					team2ID = 'CLE';

				//var hashTeam1 = hashArr(team1);
				//var hashTeam2 = hashArr(team2);

				/*首发球员*/
				var fgpy = [
					['20', 1, 'CLE'],
					['23', 2, 'CLE'],
					['0', 3, 'CLE'],
					['5', 4, 'CLE'],
					['2', 5, 'CLE'],
					['4', 1, 'GSW'],
					['11', 2, 'GSW'],
					['23', 3, 'GSW'],
					['12', 4, 'GSW'],
					['30', 5, 'GSW']
				];
				var subpy = [];
				subset(calpyset(fgpy));

				RenderImg();
				drawPlayerMark();
				DrawAdvMsg();
				DrawDisadvMsg();
				drawIcon();
				subset(subpy);
				//采集時間
				function RenderImg() {
					//	console.log(Period1)
					for(var index in Period1) {
						var item = Period1[index];
						var second = item['time'];
						var team = item['team'];
						var type = item['action'];
						/*暂且为1*/
						//var remaintime = 1; //remaintime
						var player = item['action_player'];
						var line = item['sig'];

						switch(type) {
							//犯規
							case 'Foul':
								if(team == team2ID) {
									var y = line * playerpad;
									DrawImg(xscale(second), y, foul, player + type, "foul");
								} else {
									var y = (line - 5) * playerpad + team1wid;
									DrawImg(xscale(second), y, foul, player + type, "foul");
								}
								break;
								//罚球
							case 'Free':
								if(team == team2ID) {
									var y = line * playerpad;
									//////console.log(y);
									DrawImg(xscale(second), y, pt1, player + type, "pt1");
								} else {
									var y = (line - 5) * playerpad + team1wid;
									//////console.log(y);
									DrawImg(xscale(second), y, pt1, player + type, "pt1");
								}
								break;
							case 'Miss':
								if(team == team2ID) {
									var y = line * playerpad;
									var blockplayer = item['object_player'];
									DrawImg(xscale(second), y, miss, player + type, "miss");
									//DrawEventTime(xscale(second), y, xscale(second - remaintime), y, "miss");

									break;
								} else {
									var y = (line - 5) * playerpad + team1wid;
									var blockplayer = item['object_player'];

									DrawImg(xscale(second), y, miss, player + type, "miss");
									break;
								}
							case 'DefRbd':
								if(team == team2ID) {
									var y = line * playerpad;
									DrawImg(xscale(second), y, rebound_defensive, player + type, "DefRbd");
									//DrawEventTime(xscale(second), y, xscale(second - remaintime), y, 'rbdDefensive');
								} else {
									var y = (line - 5) * playerpad + team1wid;
									DrawImg(xscale(second), y, rebound_defensive, player + type, "DefRbd");
									//DrawEventTime(xscale(second), y, xscale(second - remaintime), y, 'rbdDefensive');
								}
								break;
							case 'OfRed':
								if(team == team2ID) {
									var y = line * playerpad;
									DrawImg(xscale(second), y, rebound_offensive, player + type, "OfRed");
									//DrawEventTime(xscale(second), y, xscale(second - remaintime), y, 'rbdOffensive');
								} else {
									var y = (line - 5) * playerpad + team1wid;
									DrawImg(xscale(second), y, rebound_offensive, player + type, "OfRed");
									//DrawEventTime(xscale(second), y, xscale(second - remaintime), y, 'rbdOffensive');
								}
								break;
							case 'pt2':
								var assistplayer = item['object_player'];
								if(team == team2ID) {
									var y = line * playerpad;
									DrawImg(xscale(second), y, pt2, player + type, "pt2");
									//DrawEventTime(xscale(second), y, xscale(second - remaintime), y, 'pt2');
									/*if(assistplayer != "0") {
										var assY = line * playerpad;
										advData.push(["assist", xscale(second), y, xscale(second), assY]);
									}*/
									break;
								} else {
									var y = (line - 5) * playerpad + team1wid;
									DrawImg(xscale(second), y, pt2, player + type, "pt2");
									//DrawEventTime(xscale(second), y, xscale(second - remaintime), y, 'pt2');

									/*if(assistplayer != "0") {
										var assY = (line - 5) * playerpad + team1wid;
										advData.push(["assist", xscale(second), y, xscale(second), assY]);
									}*/
									break;
								}
							case 'pt3':
								var assistplayer = item['object_player'];
								if(team == team2ID) {
									var y = line * playerpad;
									DrawImg(xscale(second), y, pt3, player + type, "pt3");
									break;
								} else {
									var y = (line - 5) * playerpad + team1wid;
									DrawImg(xscale(second), y, pt3, player + type, "pt3");
									break;
								}
							case 'sub':
								var enterplayer = item['action_player'];
								var num = item['num'];
								if(team == team2ID) {
									var y = line * playerpad;
									//	var objy = line * playerpad;           //被替换的球员
									//DrawImg(xscale(second), y, sub, player + type, "sub");

									subpy.push([num, xscale(second + 15), y, team]);

									break;
								} else {
									var y = (line - 5) * playerpad + team1wid;
									//	var objy = (line-5) * playerpad+team1wid;           //被替换的球员
									//DrawImg(xscale(second), y, sub, player + type, "sub");
									subpy.push([num, xscale(second + 15), y, team]);

									break;
								}
							case 'violation':
								if(team == team2ID) {
									var y = line * playerpad;
									DrawImg(xscale(second), y, violation, player + type, "violation");
									////////console.log(player);
									break;
								} else {
									var y = (line - 5) * playerpad + team1wid;
									DrawImg(xscale(second), y, violation, player + type, "violation");
									////////console.log(player);
									break;
								}
							case 'Turnover':
								if(team == team2ID) {
									var y = line * playerpad;
									DrawImg(xscale(second), y, turnover, player + type, "turnover");
									//DrawEventTime(xscale(second), y, xscale(second - remaintime), y, 'turnover');
									break;
								} else {
									var y = (line - 5) * playerpad + team1wid;
									DrawImg(xscale(second), y, turnover, player + type, "turnover");
									//DrawEventTime(xscale(second), y, xscale(second - remaintime), y, 'turnover');
									break;
								}
							case 'Assist':
								if(team == team2ID) {
									var y = line * playerpad;
									DrawImg(xscale(second), y, Assist, player + type, "Assist");
									break;
								} else {
									var y = (line - 5) * playerpad + team1wid;
									DrawImg(xscale(second), y, Assist, player + type, "Assist");
									break;
								}
							case 'Block':
								if(team == team2ID) {
									var y = line * playerpad;
									DrawImg(xscale(second), y, Block, player + type, "Block");
									break;
								} else {
									var y = (line - 5) * playerpad + team1wid;
									DrawImg(xscale(second), y, Block, player + type, "Block");
									break;
								}
							case 'Steal':
								if(team == team2ID) {
									var y = line * playerpad;
									DrawImg(xscale(second), y, Steal, player + type, "Steal");
									break;
								} else {
									var y = (line - 5) * playerpad + team1wid;
									DrawImg(xscale(second), y, Steal, player + type, "Steal");
									break;
								}
						}
					}
				}

				function calpyset(dataset) {
					//					var playerpad = 30,
					//						team1wid = 220;
					//					var playerpad = height*0.7/10,
					//						team1wid = playerpad*5*1.2;

					var set = [];
					for(var i in dataset) {
						var py = dataset[i];
						var x = 10,
							y;
						if(py[2] == 'CLE') {
							y = py[1] * playerpad;
						} else {
							y = py[1] * playerpad + team1wid;
						}
						set.push([py[0], x, y, py[2]]);
					}
					return set;
				}

				function subset(dataset) {
					//console.log(dataset);
					var cirR = 10;
					let color = ["#EE9572", "#AEEEEE"];
					var ele = svgContainer.selectAll('#pyg')
						.data(dataset);
					var eleEnter = ele.enter()
						.append('g')
						.attr("id", "fgpy")
						.attr("transform", function(d, i) {
							return "translate(" + d[1] + ',' + d[2] + ")";
						});

					var circle = eleEnter.append('circle')
						.attr('r', cirR)
						.attr('stroke', function(d) {
							return d[3] == 'GSW' ? color[0] : color[1];
						})
						.attr('stroke-width', 1)
						.attr('fill', function(d) {
							return d[3] == 'GSW' ? color[0] : color[1];
						})
						.style("opacity", 1);

					eleEnter.append("text")
						.attr("dx", function(d, i) {
							if(d[0] >= 10) return -8;
							else return -4;
						})
						.attr("dy", function(d) {
							return 5;
						})
						.text(function(d) {
							return d[0];
						})
						.style("opacity", 1);

				}

				function drawPlayerMark() {
					/*球员的mark直线*/
					for(var i = 1; i <= 5; i++) {
						DrawMark(0, playerpad * i, width, playerpad * i);
					}
					for(var i = 1; i <= 5; i++) {
						DrawMark(0, playerpad * i + team1wid, width, playerpad * i + team1wid);
					}
				}

				function hashArr(arr) {
					var arrHash = [];
					for(var i = 0; i < arr.length; i++) {
						arrHash[arr[i]] = i;
					}
					return arrHash;
				};

				function removeRepeat(team, ar) {
					var ret = [];
					ret.push(team);
					for(var i = 0, j = ar.length; i < j; i++) {
						if(ret.indexOf(ar[i]) === -1) {
							ret.push(ar[i]);
						}
					}
					return ret;
				};

				function DrawImg(x, y, src, team, name) {
					svgContainer.append('image')
						.attr("id", "img" + team + "_" + x)
						.attr('x', x - 5)
						.attr('y', y - 11)
						.attr('xlink:href', src)
						.attr('width', imgwid)
						.attr('height', imgwid)
						.attr('name', name)
						.attr('class', x)
						.style('opacity', 0.1)
						.style('display', "block");
				};

				function DrawLine(x1, y1, x2, y2, msg) {
					var line = svgContainer.append("line")
						.attr("id", "line" + msg + "_" + x1)
						.attr("x1", x1)
						.attr("y1", y1)
						.attr("x2", x2)
						.attr("y2", y2)
						.attr("stroke", "red")
						.attr("stroke-width", 3);
				};

				function DrawAdvMsg() {
					var line = svgContainer.selectAll("advline")
						.data(advData)
						.enter()
						.append("line")
						.attr("id", "advicon")
						.attr("x1", function(d) {
							return d[1];
						})
						.attr("y1", function(d) {
							return d[2];
						})
						.attr("x2", function(d) {
							return d[3];
						})
						.attr("y2", function(d) {
							return d[4];
						})
						.attr("stroke", "#008B00")
						.attr("stroke-width", 2)
						.attr("name", "adv")
						.style("display", "none");
				};

				function DrawDisadvMsg() {
					var line = svgContainer.selectAll("disadvline")
						.data(disadvData)
						.enter()
						.append("line")
						.attr("id", "advicon")
						.attr("x1", function(d) {
							return d[1];
						})
						.attr("y1", function(d) {
							return d[2];
						})
						.attr("x2", function(d) {
							return d[3];
						})
						.attr("y2", function(d) {
							return d[4];
						})
						.attr("stroke", "red")
						.attr("stroke-width", 2)
						.attr("name", "disadv")
						.style("display", "none");
				}

				function DrawMark(x1, y1, x2, y2) {
					var line = svgContainer.append("line")
						.attr("id", "assist")
						.attr("x1", x1)
						.attr("y1", y1)
						.attr("x2", x2)
						.attr("y2", y2)
						.attr("stroke", "black")
						.attr("stroke-width", 0.2);
				};

				function TeamPlayer(team) {
					var id = 0,
						teamplayer = [];
					for(var index in Period1) {
						if(Period1[index]['team'] == team) {
							teamplayer[id] = Period1[index]['player'];
							id++;
						}
					}
					teamplayer = removeRepeat(team, teamplayer);
					return teamplayer;
				};

				function drawAttribute(MVP1, MVP2, MVP3, MVP4, MVP5) {
					if(hashTeam1[MVP1] != null) {
						DrawRect(width * 0.95, hashTeam1[MVP1] * playerpad - rect1 / 2, rect1, MVP1, "#008B00");
						DrawRect(width * 0.95, hashTeam1[MVP2] * playerpad - (rect1 - d) / 2, rect1 - d, MVP2, "#008B00");
						DrawRect(width * 0.95, hashTeam1[MVP3] * playerpad - (rect1 - 2 * d) / 2, rect1 - 2 * d, MVP3, "#008B00");
						DrawRect(width * 0.95, hashTeam1[MVP4] * playerpad - (rect1 - 3 * d) / 2, rect1 - 3 * d, MVP4, "#008B00");
						DrawRect(width * 0.95, hashTeam1[MVP5] * playerpad - (rect1 - 4 * d) / 2, rect1 - 4 * d, MVP5, "#008B00");
					} else {
						DrawRect(width * 0.95, hashTeam2[MVP1] * playerpad + team1wid - rect1 / 2, rect1, MVP1, "#008B00");
						DrawRect(width * 0.95, hashTeam2[MVP2] * playerpad + team1wid - (rect1 - d) / 2, rect1 - d, MVP2, "#008B00");
						DrawRect(width * 0.95, hashTeam2[MVP3] * playerpad + team1wid - (rect1 - 2 * d) / 2, rect1 - 2 * d, MVP3, "#008B00");
						DrawRect(width * 0.95, hashTeam2[MVP4] * playerpad + team1wid - (rect1 - 3 * d) / 2, rect1 - 3 * d, MVP4, "#008B00");
						DrawRect(width * 0.95, hashTeam2[MVP5] * playerpad + team1wid - (rect1 - 4 * d) / 2, rect1 - 4 * d, MVP5, "#008B00");
					}
				}

				function drawIcon() {
					var strwid = width * 0.3,
						imgwid = 20,
						imgpad = 70;
					var image = [
						[foul, "foul"],
						[miss, "miss"],
						[rebound_defensive, "DefRbd"],
						[rebound_offensive, "OfRed"],
						[sub, "sub"],
						[turnover, "turnover"],
						[pt1, "pt1"],
						[pt2, "pt2"],
						[pt3, "pt3"],
						[Assist, "Assist"],
						[Block, "Block"],
						[Steal, "Steal"]
					];

					var icon = svgContainer.selectAll("#icong")
						.data(image)
						.enter()
						.append("g")
						.attr("transform", function(d, i) {
							return "translate(" + (strwid + imgpad * i) + "," + height * 0.81 + ")";
						});
					var entericon = icon.append("image")
						.attr("width", imgwid)
						.attr("height", imgwid)
						.attr("link:href", function(d) {
							return d['0']
						})
						.attr("id", function(d) {
							return d['1'] + 'icon';
						})
						.attr('name', function(d) {
							return d['1'] + 'icon';
						})
						.style("opacity", function(d) {
							if(d['1'] == 'adv' || d['1'] == 'disadv') {
								return 0.4;
							} else {
								return 1.0;
							}
						})
						.on("click", function(d) {
							clickIcon(d['1']);
						});

					var entertxt = icon.append("text")
						.attr("dx", function(d, i) {
							if(d[1].length > 5) {
								return -5;
							} else if(d[1].length >= 10) {
								return -32;
							} else {
								return -1;
							}
						})
						.attr("dy", function(d) {
							return 40;
						})
						.attr("id", function(d) {
							return d['1'] + 'txt';
						})
						.style("opacity", 1.0)
						.text(function(d) {
							return d['1'];
						})
				}

				function clickIcon(name) {
					var domitem = document.getElementsByName(name);
					var iconitem = document.getElementById(name + 'icon');
					var txt = document.getElementById(name + 'txt');
					var domtime = document.getElementsByName(name + 'line');

					if(iconitem.style.opacity == 1) {
						for(var i = 0; i < domitem.length; i++) {
							domitem[i].style.display = 'none';
						}
						for(var i = 0; i < domtime.length; i++) {
							domtime[i].style.display = 'none';
						}
						iconitem.style.opacity = 0.4;
						txt.style.opacity = 0.4;
					} else {
						for(var i = 0; i < domitem.length; i++) {
							domitem[i].style.display = 'block';
						}
						for(var i = 0; i < domtime.length; i++) {
							domtime[i].style.display = 'block';
						}
						iconitem.style.opacity = 1.0;
						txt.style.opacity = 1.0;
					}
				}

			}
			
			/*FilterEvents 该版本 没有使用*/
			function FilterEvents(st, et) {
				st = xscale(st);
				et = xscale(et);
				var image = [
					[foul, "foul"],
					[miss, "miss"],
					[rebound_defensive, "DefRbd"],
					[rebound_offensive, "OfRed"],
					[sub, "sub"],
					[turnover, "turnover"],
					[pt1, "pt1"],
					[pt2, "pt2"],
					[pt3, "pt3"],
					[Assist, "Assist"],
					[Steal, "Steal"],
					[Block, "Block"]
				];

				for(var j = 0; j < image.length; j++) {
					change(image[j]['1']);
				}

				function change(name) {
					var icon = d3.select("#" + name + 'icon');
					//解除绑定 重新定义
					icon.on("click", null);
					icon.on("click", function(d) {
						var txt = document.getElementById(name + 'txt');
						var pic = document.getElementById(name + 'icon');
						var dom = document.getElementsByName(name);
						if(pic.style.opacity == 1.0) {
							for(var i = 0; i < dom.length; i++) {
								dom[i].style.display = 'none';
							}
							pic.style.opacity = 0.4;
							txt.style.opacity = 0.4;
						} else {
							for(var i = 0; i < dom.length; i++) {
								if(dom[i]['classList'] <= et && dom[i]['classList'] >= st) {
									dom[i].style.display = 'block';
								} else {
									dom[i].style.display = 'none';
								}
							}
							pic.style.opacity = 1.0;
							txt.style.opacity = 1.0;
						}
					})
				}

				for(var j = 0; j < image.length; j++) {
					var dom = document.getElementsByName(image[j]['1']); //img所有动作
					var domicon = document.getElementById(image[j]['1'] + 'icon'); //所有logo
					var maskrect = document.getElementById("mask_" + st + "_" + et); //mask

					console.log(dom);
					for(var i = 0; i < dom.length; i++) {
						var item = dom[i];
						var second = item['classList']['0'];
						if(second >= st && second <= et && domicon.style.opacity == 1) {
							item.style.opacity = 0.8;
						} else {

							item.style.opacity = 0.1;
						}
					}

				}
			}

			function FilterClick(st, et) {
				var image = [
					[foul, "foul"],
					[miss, "miss"],
					[rebound_defensive, "DefRbd"],
					[rebound_offensive, "OfRed"],
					[sub, "sub"],
					[turnover, "turnover"],
					[pt1, "pt1"],
					[pt2, "pt2"],
					[pt3, "pt3"],
					[Assist, "Assist"],
					[Steal, "Steal"],
					[Block, "Block"]
				];
				var selectArrary = [];
				var masks = document.getElementsByName("masks");

				for(var i = 0; i < masks.length; i++) {
					//1:选中 0.1：没被选中
					if(masks[i].style.opacity == 1) {
						var select = masks[i].id.split("_");
						selectArrary.push([select[1], select[2]]);
					}
				}
				//console.log(selectArrary);
				
				//与轨迹图的交互 当前所有选择的时间段的时间
				me.$root.Bus.$emit('trail', selectArrary);
				
				for(var j = 0; j < image.length; j++) {
					var dom = document.getElementsByName(image[j]['1']); //img所有动作
					var domicon = document.getElementById(image[j]['1'] + 'icon'); //所有logo

					var light = 0;
					//	console.log(dom);
					for(var i = 0; i < dom.length; i++) {
						var item = dom[i];
						var second = item['classList']['0'];
						if(domicon.style.opacity == 1) {
							for(var k = 0; k < selectArrary.length; k++) {
								var selectTime=selectArrary[k];
								if(second <= xscale(selectTime[1]) && second >= xscale(selectTime[0])) {
									item.style.opacity = 0.8;
									light = 1;
									break;
								}
							}
							//图标没有按掉 但不在范围内
							if(!light) {
								item.style.opacity = 0.1;
							}
						} else {
							item.style.opacity = 0.1;
						}
					}

				}

			}
		}
	}
</script>