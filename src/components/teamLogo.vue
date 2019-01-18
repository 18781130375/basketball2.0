<template>
	<div>
		<div id="logo" height="100%" width="100%">
			<div id="team2players" style="width: 50%;height: 80px;"></div>
			<div id="IconExplain"></div>
			<div id="team1players" style="width: 50%;height:80px;"></div>
		</div>
		<Modal v-model="modal11" draggable scrollable title="LeBron James">
			<div id="LeBronJames"></div>
		</Modal>
		<Modal v-model="modal12" draggable scrollable title="Mo Williams">
			<div id="MoWilliams"></div>
		</Modal>
		<Modal v-model="modal13" draggable scrollable title="James Jones">
			<div id="JamesJones"></div>
		</Modal>
		<Modal v-model="modal14" draggable scrollable title="J.R. Smith">
			<div id="J.R.Smith"></div>
		</Modal>
		<Modal v-model="modal15" draggable scrollable title="Kevin Love">
			<div id="KevinLove"></div>
		</Modal>
		<Modal v-model="modal16" draggable scrollable title="Brandon Rush">
			<div id="BrandonRush"></div>
		</Modal>
		<Modal v-model="modal17" draggable scrollable title="Andrew Bogut">
			<div id="AndrewBogut"></div>
		</Modal>
		<Modal v-model="modal18" draggable scrollable title="Andre Iguodala">
			<div id="AndreIguodala"></div>
		</Modal>
		<Modal v-model="modal19" draggable scrollable title="Shaun Livingston">
			<div id="ShaunLivingston"></div>
		</Modal>
		<Modal v-model="modal110" draggable scrollable title="Leandro Barbosa">
			<div id="LeandroBarbosa"></div>
		</Modal>
		<Modal v-model="modal111" draggable scrollable title="Marreese Speights">
			<div id="MarreeseSpeights"></div>
		</Modal>
		<Modal v-model="modal112" draggable scrollable title="Stephen Curry">
			<div id="StephenCurry"></div>
		</Modal>
		<Modal v-model="modal113" draggable scrollable title="Timofey Mozgov">
			<div id="TimofeyMozgov"></div>
		</Modal>
		<Modal v-model="modal114" draggable scrollable title="Kyrie Irving">
			<div id="KyrieIrving"></div>
		</Modal>
		<Modal v-model="modal115" draggable scrollable title="Tristan Thompson">
			<div id="TristanThompson"></div>
		</Modal>
		<Modal v-model="modal116" draggable scrollable title="Klay Thompson">
			<div id="KlayThompson"></div>
		</Modal>
		<Modal v-model="modal117" draggable scrollable title="Iman Shumpert">
			<div id="ImanShumpert"></div>
		</Modal>
		<Modal v-model="modal118" draggable scrollable title="Festus Ezeli">
			<div id="FestusEzeli"></div>
		</Modal>
		<Modal v-model="modal119" draggable scrollable title="Draymond Green">
			<div id="DraymondGreen"></div>
		</Modal>
		<Modal v-model="modal120" draggable scrollable title="Matthew Dellavedova">
			<div id="MatthewDellavedova"></div>
		</Modal>
		<Modal v-model="modal121" draggable scrollable title="Ian Clark">
			<div id="IanClark"></div>
		</Modal>
		<Modal v-model="modal122" draggable scrollable title="James Michael McAdoo">
			<div id="JamesMichaelMcAdoo"></div>
		</Modal>
	</div>
</template>
<script>
	//require("../../static/index.css")
	import GSW from '@/assets/GSW.png'
	import CLE from '@/assets/CLE.png'
	import * as echarts from 'echarts'
	require("../../static/js/d3v3.js")
	export default {
		data() {
			return {
				GSW: GSW,
				CLE: CLE,
				modal11: false,
				modal12: false,
				modal13: false,
				modal14: false,
				modal15: false,
				modal16: false,
				modal17: false,
				modal18: false,
				modal19: false,
				modal110: false,
				modal111: false,
				modal112: false,
				modal113: false,
				modal114: false,
				modal115: false,
				modal116: false,
				modal117: false,
				modal118: false,
				modal119: false,
				modal120: false,
				modal121: false,
				modal122: false
			}
		},
		methods: {
			RadarChart(id, data, options) {
				var cfg = {
					w: 600, //Width of the circle
					h: 600, //Height of the circle
					margin: {
						top: 10,
						right: 10,
						bottom: 10,
						left: 10
					}, //The margins of the SVG
					levels: 3, //How many levels or inner circles should there be drawn
					maxValue: 0, //What is the value that the biggest circle will represent
					labelFactor: 1.25, //How much farther than the radius of the outer circle should the labels be placed
					wrapWidth: 60, //The number of pixels after which a label needs to be given a new line
					opacityArea: 0.35, //The opacity of the area of the blob
					dotRadius: 4, //The size of the colored circles of each blog
					opacityCircles: 0.1, //The opacity of the circles of each blob
					strokeWidth: 2, //The width of the stroke around each blob
					roundStrokes: false, //If true the area and stroke will follow a round path (cardinal-closed)
					color: d3.scale.category10() //Color function
				};

				//Put all of the options into a variable called cfg
				if('undefined' !== typeof options) {
					for(var i in options) {
						if('undefined' !== typeof options[i]) {
							cfg[i] = options[i];
						}
					} //for i
				} //if

				//If the supplied maxValue is smaller than the actual one, replace by the max in the data
				var maxValue = Math.max(cfg.maxValue, d3.max(data, function(i) {
					return d3.max(i.map(function(o) {
						return o.value;
					}))
				}));

				var allAxis = (data[0].map(function(i, j) {
						return i.axis
					})), //Names of each axis
					total = allAxis.length, //The number of different axes
					radius = Math.min(cfg.w / 2, cfg.h / 2), //Radius of the outermost circle
					Format = d3.format('%'), //Percentage formatting
					angleSlice = Math.PI * 2 / total; //The width in radians of each "slice"

				//Scale for the radius
				var rScale = d3.scale.linear()
					.range([0, radius])
					.domain([0, maxValue]);

				/////////////////////////////////////////////////////////
				//////////// Create the container SVG and g /////////////
				/////////////////////////////////////////////////////////

				//Remove whatever chart with the same id/class was present before
				d3.select(id).select("svg").remove();

				//Initiate the radar chart SVG
				var svg = d3.select(id).append("svg")
					.attr("width", cfg.w + cfg.margin.left + cfg.margin.right)
					.attr("height", cfg.h + cfg.margin.top + cfg.margin.bottom)
					.attr("class", "radar" + id);

				//Append a g element        
				var g = svg.append("g")
					.attr("transform", "translate(" + (cfg.w / 2 + cfg.margin.left) + "," + (cfg.h / 2 + cfg.margin.top) + ")");

				/////////////////////////////////////////////////////////
				////////// Glow filter for some extra pizzazz ///////////
				/////////////////////////////////////////////////////////

				//Filter for the outside glow
				var filter = g.append('defs').append('filter').attr('id', 'glow'),
					feGaussianBlur = filter.append('feGaussianBlur').attr('stdDeviation', '2.5').attr('result', 'coloredBlur'),
					feMerge = filter.append('feMerge'),
					feMergeNode_1 = feMerge.append('feMergeNode').attr('in', 'coloredBlur'),
					feMergeNode_2 = feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

				/////////////////////////////////////////////////////////
				/////////////// Draw the Circular grid //////////////////
				/////////////////////////////////////////////////////////

				//Wrapper for the grid & axes
				var axisGrid = g.append("g").attr("class", "axisWrapper");

				//Draw the background circles
				axisGrid.selectAll(".levels")
					.data(d3.range(1, (cfg.levels + 1)).reverse())
					.enter()
					.append("circle")
					.attr("class", "gridCircle")
					.attr("r", function(d, i) {
						return radius / cfg.levels * d;
					})
					.style("fill", "#CDCDCD")
					.style("stroke", "#CDCDCD")
					.style("fill-opacity", cfg.opacityCircles)
					.style("filter", "url(#glow)");

				//Text indicating at what % each level is
				axisGrid.selectAll(".axisLabel")
					.data(d3.range(1, (cfg.levels + 1)).reverse())
					.enter().append("text")
					.attr("class", "axisLabel")
					.attr("x", 4)
					.attr("y", function(d) {
						return -d * radius / cfg.levels;
					})
					.attr("dy", "0.4em")
					.style("font-size", "10px")
					.attr("fill", "#737373")
					.text(function(d, i) {
						return Format(maxValue * d / cfg.levels);
					});

				/////////////////////////////////////////////////////////
				//////////////////// Draw the axes //////////////////////
				/////////////////////////////////////////////////////////

				//Create the straight lines radiating outward from the center
				var axis = axisGrid.selectAll(".axis")
					.data(allAxis)
					.enter()
					.append("g")
					.attr("class", "axis");
				//Append the lines
				axis.append("line")
					.attr("x1", 0)
					.attr("y1", 0)
					.attr("x2", function(d, i) {
						return rScale(maxValue * 1.1) * Math.cos(angleSlice * i - Math.PI / 2);
					})
					.attr("y2", function(d, i) {
						return rScale(maxValue * 1.1) * Math.sin(angleSlice * i - Math.PI / 2);
					})
					.attr("class", "line")
					.style("stroke", "white")
					.style("stroke-width", "2px");

				//Append the labels at each axis
				axis.append("text")
					.attr("class", "legend")
					.style("font-size", "11px")
					.attr("text-anchor", "middle")
					.attr("dy", "0.35em")
					.attr("x", function(d, i) {
						return rScale(maxValue * cfg.labelFactor) * Math.cos(angleSlice * i - Math.PI / 2);
					})
					.attr("y", function(d, i) {
						return rScale(maxValue * cfg.labelFactor) * Math.sin(angleSlice * i - Math.PI / 2);
					})
					.text(function(d) {
						return d
					})
					.call(wrap, cfg.wrapWidth);

				/////////////////////////////////////////////////////////
				///////////// Draw the radar chart blobs ////////////////
				/////////////////////////////////////////////////////////

				//The radial line function
				var radarLine = d3.svg.line.radial()
					.interpolate("linear-closed")
					.radius(function(d) {
						return rScale(d.value);
					})
					.angle(function(d, i) {
						return i * angleSlice;
					});

				if(cfg.roundStrokes) {
					radarLine.interpolate("cardinal-closed");
				}

				//Create a wrapper for the blobs    
				var blobWrapper = g.selectAll(".radarWrapper")
					.data(data)
					.enter().append("g")
					.attr("class", "radarWrapper");

				//Append the backgrounds    
				blobWrapper
					.append("path")
					.attr("class", "radarArea")
					.attr("d", function(d, i) {
						return radarLine(d);
					})
					.style("fill", function(d, i) {
						return cfg.color(i);
					})
					.style("fill-opacity", cfg.opacityArea)
					.on('mouseover', function(d, i) {
						//Dim all blobs
						d3.selectAll(".radarArea")
							.transition().duration(200)
							.style("fill-opacity", 0.1);
						//Bring back the hovered over blob
						d3.select(this)
							.transition().duration(200)
							.style("fill-opacity", 0.7);
					})
					.on('mouseout', function() {
						//Bring back all blobs
						d3.selectAll(".radarArea")
							.transition().duration(200)
							.style("fill-opacity", cfg.opacityArea);
					});

				//Create the outlines    
				blobWrapper.append("path")
					.attr("class", "radarStroke")
					.attr("d", function(d, i) {
						return radarLine(d);
					})
					.style("stroke-width", cfg.strokeWidth + "px")
					.style("stroke", function(d, i) {
						return cfg.color(i);
					})
					.style("fill", "none")
					.style("filter", "url(#glow)");

				//Append the circles
				blobWrapper.selectAll(".radarCircle")
					.data(function(d, i) {
						return d;
					})
					.enter().append("circle")
					.attr("class", "radarCircle")
					.attr("r", cfg.dotRadius)
					.attr("cx", function(d, i) {
						return rScale(d.value) * Math.cos(angleSlice * i - Math.PI / 2);
					})
					.attr("cy", function(d, i) {
						return rScale(d.value) * Math.sin(angleSlice * i - Math.PI / 2);
					})
					.style("fill", function(d, i, j) {
						return cfg.color(j);
					})
					.style("fill-opacity", 0.8);

				/////////////////////////////////////////////////////////
				//////// Append invisible circles for tooltip ///////////
				/////////////////////////////////////////////////////////

				//Wrapper for the invisible circles on top
				var blobCircleWrapper = g.selectAll(".radarCircleWrapper")
					.data(data)
					.enter().append("g")
					.attr("class", "radarCircleWrapper");

				//Append a set of invisible circles on top for the mouseover pop-up
				blobCircleWrapper.selectAll(".radarInvisibleCircle")
					.data(function(d, i) {
						return d;
					})
					.enter().append("circle")
					.attr("class", "radarInvisibleCircle")
					.attr("r", cfg.dotRadius * 1.5)
					.attr("cx", function(d, i) {
						return rScale(d.value) * Math.cos(angleSlice * i - Math.PI / 2);
					})
					.attr("cy", function(d, i) {
						return rScale(d.value) * Math.sin(angleSlice * i - Math.PI / 2);
					})
					.style("fill", "none")
					.style("pointer-events", "all")
					.on("mouseover", function(d, i) {
						newX = parseFloat(d3.select(this).attr('cx')) - 10;
						newY = parseFloat(d3.select(this).attr('cy')) - 10;

						tooltip
							.attr('x', newX)
							.attr('y', newY)
							.text(Format(d.value))
							.transition().duration(200)
							.style('opacity', 1);
					})
					.on("mouseout", function() {
						tooltip.transition().duration(200)
							.style("opacity", 0);
					});

				//Set up the small tooltip for when you hover over a circle
				var tooltip = g.append("text")
					.attr("class", "tooltip")
					.style("opacity", 0);

				/////////////////////////////////////////////////////////
				/////////////////// Helper Function /////////////////////
				/////////////////////////////////////////////////////////

				//Taken from http://bl.ocks.org/mbostock/7555321
				//Wraps SVG text    
				function wrap(text, width) {
					text.each(function() {
						var text = d3.select(this),
							words = text.text().split(/\s+/).reverse(),
							word,
							line = [],
							lineNumber = 0,
							lineHeight = 1.4, // ems
							y = text.attr("y"),
							x = text.attr("x"),
							dy = parseFloat(text.attr("dy")),
							tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em");

						while(word = words.pop()) {
							line.push(word);
							tspan.text(line.join(" "));
							if(tspan.node().getComputedTextLength() > width) {
								line.pop();
								tspan.text(line.join(" "));
								line = [word];
								tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
							}
						}
					});
				} //wrap    

			}
		},
		mounted() {
			let me = this;
			//radar();

			var datasetpy ={'Andre Iguodala': [[{'axis': '得分', 'value': 0.8751671122994653}, {'axis': '场均盖帽数', 'value': 1.7030303030303031}, {'axis': '场均抢断数', 'value': 0.8923444976076554}, {'axis': '场均篮板球数', 'value': 1.2982635342185904}, {'axis': '场均助攻数', 'value': 0.9763124199743918}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Andrew Bogut': [[{'axis': '得分', 'value': 0.8163435828877006}, {'axis': '场均盖帽数', 'value': 1.7030303030303031}, {'axis': '场均抢断数', 'value': 0.8923444976076554}, {'axis': '场均篮板球数', 'value': 1.2982635342185904}, {'axis': '场均助攻数', 'value': 0.9763124199743918}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Brandon Rush': [[{'axis': '得分', 'value': 0.7722259358288771}, {'axis': '场均盖帽数', 'value': 0.8363636363636364}, {'axis': '场均抢断数', 'value': 0.7870813397129186}, {'axis': '场均篮板球数', 'value': 0.7926455566905005}, {'axis': '场均助攻数', 'value': 0.765044814340589}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Draymond Green': [[{'axis': '得分', 'value': 1.1325200534759359}, {'axis': '场均盖帽数', 'value': 1.5696969696969698}, {'axis': '场均抢断数', 'value': 1.4186602870813396}, {'axis': '场均篮板球数', 'value': 1.5791624106230846}, {'axis': '场均助攻数', 'value': 1.6946222791293213}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Festus Ezeli': [[{'axis': '得分', 'value': 0.8751671122994653}, {'axis': '场均盖帽数', 'value': 1.3696969696969699}, {'axis': '场均抢断数', 'value': 0.8397129186602871}, {'axis': '场均篮板球数', 'value': 1.1409601634320734}, {'axis': '场均助攻数', 'value': 0.7509603072983355}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Ian Clark': [[{'axis': '得分', 'value': 0.7501671122994653}, {'axis': '场均盖帽数', 'value': 0.7696969696969698}, {'axis': '场均抢断数', 'value': 0.7870813397129186}, {'axis': '场均篮板球数', 'value': 0.6241062308478038}, {'axis': '场均助攻数', 'value': 0.793213828425096}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Iman Shumpert': [[{'axis': '得分', 'value': 0.8310494652406417}, {'axis': '场均盖帽数', 'value': 0.9030303030303031}, {'axis': '场均抢断数', 'value': 1.1555023923444976}, {'axis': '场均篮板球数', 'value': 0.9387129724208375}, {'axis': '场均助攻数', 'value': 0.8918053777208707}], [{'axis': '得分', 'value': 1.031784759358289}, {'axis': '场均盖帽数', 'value': 0.8963636363636365}, {'axis': '场均抢断数', 'value': 1.013397129186603}, {'axis': '场均篮板球数', 'value': 1.0196118488253318}, {'axis': '场均助攻数', 'value': 1.0129321382842509}]], 'J.R. Smith': [[{'axis': '得分', 'value': 1.0736965240641712}, {'axis': '场均盖帽数', 'value': 0.8363636363636364}, {'axis': '场均抢断数', 'value': 1.208133971291866}, {'axis': '场均篮板球数', 'value': 0.8263534218590398}, {'axis': '场均助攻数', 'value': 0.8918053777208707}], [{'axis': '得分', 'value': 1.031784759358289}, {'axis': '场均盖帽数', 'value': 0.8963636363636365}, {'axis': '场均抢断数', 'value': 1.013397129186603}, {'axis': '场均篮板球数', 'value': 1.0196118488253318}, {'axis': '场均助攻数', 'value': 1.0129321382842509}]], 'James Jones': [[{'axis': '得分', 'value': 0.7538435828877006}, {'axis': '场均盖帽数', 'value': 0.7696969696969698}, {'axis': '场均抢断数', 'value': 0.7344497607655502}, {'axis': '场均篮板球数', 'value': 0.6241062308478038}, {'axis': '场均助攻数', 'value': 0.6946222791293214}], [{'axis': '得分', 'value': 1.031784759358289}, {'axis': '场均盖帽数', 'value': 0.8963636363636365}, {'axis': '场均抢断数', 'value': 1.013397129186603}, {'axis': '场均篮板球数', 'value': 1.0196118488253318}, {'axis': '场均助攻数', 'value': 1.0129321382842509}]], 'James Michael McAdoo': [[{'axis': '得分', 'value': 0.7244318181818182}, {'axis': '场均盖帽数', 'value': 0.7696969696969698}, {'axis': '场均抢断数', 'value': 0.7344497607655502}, {'axis': '场均篮板球数', 'value': 0.669050051072523}, {'axis': '场均助攻数', 'value': 0.7087067861715749}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Kevin Love': [[{'axis': '得分', 'value': 1.2060494652406417}, {'axis': '场均盖帽数', 'value': 0.9696969696969697}, {'axis': '场均抢断数', 'value': 1.0502392344497609}, {'axis': '场均篮板球数', 'value': 1.6241062308478038}, {'axis': '场均助攻数', 'value': 0.9903969270166453}], [{'axis': '得分', 'value': 1.031784759358289}, {'axis': '场均盖帽数', 'value': 0.8963636363636365}, {'axis': '场均抢断数', 'value': 1.013397129186603}, {'axis': '场均篮板球数', 'value': 1.0196118488253318}, {'axis': '场均助攻数', 'value': 1.0129321382842509}]], 'Klay Thompson': [[{'axis': '得分', 'value': 1.4303141711229947}, {'axis': '场均盖帽数', 'value': 1.0363636363636364}, {'axis': '场均抢断数', 'value': 1.0502392344497609}, {'axis': '场均篮板球数', 'value': 0.9387129724208375}, {'axis': '场均助攻数', 'value': 0.9481434058898848}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Kyrie Irving': [[{'axis': '得分', 'value': 1.3384024064171123}, {'axis': '场均盖帽数', 'value': 0.8363636363636364}, {'axis': '场均抢断数', 'value': 1.208133971291866}, {'axis': '场均篮板球数', 'value': 0.8488253319713994}, {'axis': '场均助攻数', 'value': 1.3143405889884763}], [{'axis': '得分', 'value': 1.031784759358289}, {'axis': '场均盖帽数', 'value': 0.8963636363636365}, {'axis': '场均抢断数', 'value': 1.013397129186603}, {'axis': '场均篮板球数', 'value': 1.0196118488253318}, {'axis': '场均助攻数', 'value': 1.0129321382842509}]], 'LeBron James': [[{'axis': '得分', 'value': 1.547961229946524}, {'axis': '场均盖帽数', 'value': 1.0363636363636364}, {'axis': '场均抢断数', 'value': 1.3660287081339713}, {'axis': '场均篮板球数', 'value': 1.3432073544433094}, {'axis': '场均助攻数', 'value': 1.6101152368758003}], [{'axis': '得分', 'value': 1.031784759358289}, {'axis': '场均盖帽数', 'value': 0.8963636363636365}, {'axis': '场均抢断数', 'value': 1.013397129186603}, {'axis': '场均篮板球数', 'value': 1.0196118488253318}, {'axis': '场均助攻数', 'value': 1.0129321382842509}]], 'Leandro Barbosa': [[{'axis': '得分', 'value': 0.8531082887700535}, {'axis': '场均盖帽数', 'value': 0.7030303030303031}, {'axis': '场均抢断数', 'value': 0.9449760765550239}, {'axis': '场均篮板球数', 'value': 0.7027579162410623}, {'axis': '场均助攻数', 'value': 0.821382842509603}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Marreese Speights': [[{'axis': '得分', 'value': 0.8788435828877006}, {'axis': '场均盖帽数', 'value': 0.9696969696969697}, {'axis': '场均抢断数', 'value': 0.7870813397129186}, {'axis': '场均篮板球数', 'value': 0.8825331971399387}, {'axis': '场均助攻数', 'value': 0.765044814340589}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Matthew Dellavedova': [[{'axis': '得分', 'value': 0.8935494652406417}, {'axis': '场均盖帽数', 'value': 0.7030303030303031}, {'axis': '场均抢断数', 'value': 0.9449760765550239}, {'axis': '场均篮板球数', 'value': 0.7477017364657814}, {'axis': '场均助攻数', 'value': 1.2720870678617158}], [{'axis': '得分', 'value': 1.031784759358289}, {'axis': '场均盖帽数', 'value': 0.8963636363636365}, {'axis': '场均抢断数', 'value': 1.013397129186603}, {'axis': '场均篮板球数', 'value': 1.0196118488253318}, {'axis': '场均助攻数', 'value': 1.0129321382842509}]], 'Mo Williams': [[{'axis': '得分', 'value': 0.9192847593582888}, {'axis': '场均盖帽数', 'value': 0.7030303030303031}, {'axis': '场均抢断数', 'value': 0.7870813397129186}, {'axis': '场均篮板球数', 'value': 0.713993871297242}, {'axis': '场均助攻数', 'value': 0.9903969270166453}], [{'axis': '得分', 'value': 1.031784759358289}, {'axis': '场均盖帽数', 'value': 0.8963636363636365}, {'axis': '场均抢断数', 'value': 1.013397129186603}, {'axis': '场均篮板球数', 'value': 1.0196118488253318}, {'axis': '场均助攻数', 'value': 1.0129321382842509}]], 'Shaun Livingston': [[{'axis': '得分', 'value': 0.8494318181818182}, {'axis': '场均盖帽数', 'value': 0.8363636363636364}, {'axis': '场均抢断数', 'value': 0.9976076555023923}, {'axis': '场均篮板球数', 'value': 0.7589376915219612}, {'axis': '场均助攻数', 'value': 1.0749039692701665}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Stephen Curry': [[{'axis': '得分', 'value': 1.7244318181818183}, {'axis': '场均盖帽数', 'value': 0.7696969696969698}, {'axis': '场均抢断数', 'value': 1.7344497607655502}, {'axis': '场均篮板球数', 'value': 1.118488253319714}, {'axis': '场均助攻数', 'value': 1.5960307298335468}], [{'axis': '得分', 'value': 0.9735127005347595}, {'axis': '场均盖帽数', 'value': 1.0863636363636362}, {'axis': '场均抢断数', 'value': 0.9888357256778307}, {'axis': '场均篮板球数', 'value': 0.9836567926455566}, {'axis': '场均助攻数', 'value': 0.9892232180964576}]], 'Timofey Mozgov': [[{'axis': '得分', 'value': 0.8494318181818182}, {'axis': '场均盖帽数', 'value': 1.1696969696969697}, {'axis': '场均抢断数', 'value': 0.7870813397129186}, {'axis': '场均篮板球数', 'value': 1.0061287027579162}, {'axis': '场均助攻数', 'value': 0.7087067861715749}], [{'axis': '得分', 'value': 1.031784759358289}, {'axis': '场均盖帽数', 'value': 0.8963636363636365}, {'axis': '场均抢断数', 'value': 1.013397129186603}, {'axis': '场均篮板球数', 'value': 1.0196118488253318}, {'axis': '场均助攻数', 'value': 1.0129321382842509}]], 'Tristan Thompson': [[{'axis': '得分', 'value': 0.9045788770053477}, {'axis': '场均盖帽数', 'value': 1.0363636363636364}, {'axis': '场均抢断数', 'value': 0.8923444976076554}, {'axis': '场均篮板球数', 'value': 1.5229826353421858}, {'axis': '场均助攻数', 'value': 0.765044814340589}], [{'axis': '得分', 'value': 1.031784759358289}, {'axis': '场均盖帽数', 'value': 0.8963636363636365}, {'axis': '场均抢断数', 'value': 1.013397129186603}, {'axis': '场均篮板球数', 'value': 1.0196118488253318}, {'axis': '场均助攻数', 'value': 1.0129321382842509}]]}


			var teampy = ['LeBron James', 'Mo Williams',
				'James Jones', 'J.R. Smith', 'Kevin Love',
				'Timofey Mozgov', 'Kyrie Irving', 'Tristan Thompson',
				'Iman Shumpert', 'Matthew Dellavedova', 'Leandro Barbosa',
				'Shaun Livingston', 'Andre Iguodala', 'Andrew Bogut', 'Brandon Rush',
				'Marreese Speights', 'Stephen Curry', 'Klay Thompson', 'Festus Ezeli',
				'Draymond Green', 'Ian Clark', 'James Michael McAdoo'
			]

			for(var i in teampy) {
				var item = teampy[i];
				var name = item.split(' ');
				var divname = "";
				for(var j = 0; j < name.length; j++) {
					divname += name[j];
				}
				////console.log(divname);
				radar(datasetpy[item], "#" + divname);
			}

			logo();

			function logo() {
				var team2d = [
						['LeBron James', 'CLE', 23, 1],
						['Mo Williams', 'CLE', 52, 2],
						['James Jones', 'CLE', 1, 3],
						['J.R. Smith', 'CLE', 5, 4],
						['Kevin Love', 'CLE', 0, 5],
						['Timofey Mozgov', 'CLE', 20, 6],
						['Kyrie Irving', 'CLE', 2, 7],
						['Tristan Thompson', 'CLE', 13, 8],
						['Iman Shumpert', 'CLE', 4, 9],
						['Matthew Dellavedova', 'CLE', 8, 10]
					],
					team1d = [
						['Leandro Barbosa', 'GSW', 19, 1],
						['Shaun Livingston', 'GSW', 34, 2],
						['Andre Iguodala', 'GSW', 9, 3],
						['Andrew Bogut', 'GSW', 12, 4],
						['Brandon Rush', 'GSW', 4, 5],
						['Marreese Speights', 'GSW', 5, 6],
						['Stephen Curry', 'GSW', 30, 7],
						['Klay Thompson', 'GSW', 11, 8],
						['Festus Ezeli', 'GSW', 31, 9],
						['Draymond Green', 'GSW', 23, 10],
						['Ian Clark', 'GSW', 21, 11],
						['James Michael McAdoo', 'GSW', 20, 12]
					];

				DrawCir("team1players", team1d, "GSW");
				DrawCir("team2players", team2d, "CLE");
				//Drawlogo(150, 50, "#team1logo", GSW, "team1logo");
				//Drawlogo(150, 50, "#team2logo", CLE, "team1logo");

				function Drawlogo(x, y, set, src, name) {
					d3.select(set).append('img')
						.attr("id", name)
						.attr('x', x)
						.attr('y', y)
						.attr('src', src)
						.attr('width', 100)
						.attr('height', 100);
				};

				function DrawCir(divname, dataset, team) {
					var cirR = 10;
					let color = ["#EE9572", "#AEEEEE"];
					var width = $("#" + divname).width(),
						height = $("#" + divname).height();
					var pad=0;
					if(team=="GSW") pad=width*0.8;
					var svg = d3.select("#" + divname).append('svg')
						.attr('width', width)
						.attr('height', height);
					//////console.log(svg)
					var ele = svg.selectAll('g')
						.data(dataset);
					var eleEnter = ele.enter()
						.append('g')
						.attr("id", function(d) {
							return d[0];
						})
						.attr("transform", function(d, i) {
							if(i <= 4) return "translate(" + ((i + 1) * 25+pad) + ",20)";
							else if(i <= 9) return "translate(" + ((i - 4) * 25+pad) + ",60)";
							else return "translate(" + ((i - 9) * 25+pad) + ",100)";
						});

					var circle = eleEnter.append('circle')
						.attr('r', cirR)
						.attr('stroke', function(d) {
							return team == 'GSW' ? color[0] : color[1];
						})
						.attr('stroke-width', 1)
						.attr('fill', function(d) {
							return team == 'GSW' ? color[0] : color[1];
						})
						.on("click", function(d) {
							switch(d[0]) {
								case 'LeBron James':
									me.modal11 = true;
									break;
								case 'Mo Williams':
									me.modal12 = true;
									break;
								case 'James Jones':
									me.modal13 = true;
									break;
								case 'J.R. Smith':
									me.modal14 = true;
									break;
								case 'Kevin Love':
									me.modal15 = true;
									break;
								case 'Brandon Rush':
									me.modal16 = true;
									break;
								case 'Andrew Bogut':
									me.modal17 = true;
									break;
								case 'Andre Iguodala':
									me.modal18 = true;
									break;
								case 'Shaun Livingston':
									me.modal19 = true;
									break;
								case 'Leandro Barbosa':
									me.modal110 = true;
									break;
								case 'Marreese Speights':
									me.modal111 = true;
									break;
								case 'Stephen Curry':
									me.modal112 = true;
									break;
								case 'Timofey Mozgov':
									me.modal113 = true;
									break;
								case 'Kyrie Irving':
									me.modal114 = true;
									break;
								case 'Tristan Thompson':
									me.modal115 = true;
									break;
								case 'Klay Thompson':
									me.modal116 = true;
									break;
								case 'Iman Shumpert':
									me.modal117 = true;
									break;
								case 'Festus Ezeli':
									me.modal118 = true;
									break;
								case 'Draymond Green':
									me.modal119 = true;
									break;
								case 'Matthew Dellavedova':
									me.modal120 = true;
									break;
								case 'Ian Clark':
									me.modal121 = true;
									break;
								case 'James Michael McAdoo':
									me.modal122 = true;
									break;
							}
						});
					eleEnter.append("text")
						.attr("dx", function(d, i) {
							if(d[2] >= 10) return -8;
							else return -4;
						})
						.attr("dy", function(d) {
							return 5;
						})
						.text(function(d) {
							return d[2];
						})
						.on("click", function(d) {
							switch(d[0]) {
								case 'LeBron James':
									me.modal11 = true;
									break;
								case 'Mo Williams':
									me.modal12 = true;
									break;
								case 'James Jones':
									me.modal13 = true;
									break;
								case 'J.R. Smith':
									me.modal14 = true;
									break;
								case 'Kevin Love':
									me.modal15 = true;
									break;
								case 'Brandon Rush':
									me.modal16 = true;
									break;
								case 'Andrew Bogut':
									me.modal17 = true;
									break;
								case 'Andre Iguodala':
									me.modal18 = true;
									break;
								case 'Shaun Livingston':
									me.modal19 = true;
									break;
								case 'Leandro Barbosa':
									me.modal110 = true;
									break;
								case 'Marreese Speights':
									me.modal111 = true;
									break;
								case 'Stephen Curry':
									me.modal112 = true;
									break;
								case 'Timofey Mozgov':
									me.modal113 = true;
									break;
								case 'Kyrie Irving':
									me.modal114 = true;
									break;
								case 'Tristan Thompson':
									me.modal115 = true;
									break;
								case 'Klay Thompson':
									me.modal116 = true;
									break;
								case 'Iman Shumpert':
									me.modal117 = true;
									break;
								case 'Festus Ezeli':
									me.modal118 = true;
									break;
								case 'Draymond Green':
									me.modal119 = true;
									break;
								case 'Matthew Dellavedova':
									me.modal120 = true;
									break;
								case 'Ian Clark':
									me.modal121 = true;
									break;
								case 'James Michael McAdoo':
									me.modal122 = true;
									break;
							}
						});

				}
			}

			function radar(dataset, divname) {
				var margin = {
						top: 100,
						right: 100,
						bottom: 100,
						left: 100
					},
					width = Math.min(400, window.innerWidth - 10) - margin.left - margin.right,
					height = Math.min(width, window.innerHeight - margin.top - margin.bottom - 20);

				////console.log(dataset);

				var color = d3.scale.ordinal()
					.range(["#EDC951", "#CC333F"]);

				var radarChartOptions = {
					w: width,
					h: height,
					margin: margin,
					maxValue: 0.5,
					levels: 5,
					roundStrokes: true,
					color: color
				};
				//Call function to draw the Radar chart
				me.RadarChart(divname, dataset, radarChartOptions);
			}

		}
	}
</script>

<style>
	#team1players,#IconExplain{
		float: right;
	}
	#team2players{
		float: left;
	}
</style>
