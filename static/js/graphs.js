function coursesstats() {
    var data = []
    var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance 
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText);

            var width = 300,
                height = 300,
                radius = Math.min(width, height) / 2;
            var color = d3.scaleOrdinal(d3.schemeCategory10);
            var pie = d3.pie().value(function(d) {
                return d.amount;
            })(data);
            var arc = d3.arc().outerRadius(radius - 10).innerRadius(0);
            var labelArc = d3.arc().outerRadius(radius - 40).innerRadius(radius - 40);
            var svg = d3.select("#coursestats").append("svg").attr("width", width).attr("height", height).append("g")
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

            var g = svg.selectAll("arc").data(pie).enter().append("g")
                .attr("class", "arc");
            g.append("path").attr("d", arc).style("fill", function(d) {
                return color(d.data.course);
            });

            g.append("text").attr("transform", function(d) {
                    return "translate(" + labelArc.centroid(d) + ")";
                }).text(function(d) {
                    return d.data.course;
                })
                .style("fill", "#fff");

        }
    };
    xmlhttp.open("GET", "/coursestats", true);
    xmlhttp.send();
}

function ingredientstats() {
    var data = []
    var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance 
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText);





            var margin = {
                    top: 20,
                    right: 20,
                    bottom: 30,
                    left: 40
                },
                width = 360 - margin.left - margin.right,
                height = 300 - margin.top - margin.bottom;

            var color = d3.scaleOrdinal(d3.schemeCategory10);
            var x = d3.scaleBand()
                .range([0, width])
                .padding(0.1);
            var y = d3.scaleLinear()
                .range([height, 0]);


            var svg = d3.select("#ingredientstats").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");




            x.domain(data.map(function(d) {
                return d.ingredient;
            }));
            y.domain([0, d3.max(data, function(d) {
                return d.amount;
            })]);

            // append the rectangles for the bar chart
            svg.selectAll(".bar")
                .data(data)
                .enter().append("rect")
                .attr("class", "bar")
                .attr("x", function(d) {
                    return x(d.ingredient);
                })
                .attr("width", x.bandwidth())
                .attr("y", function(d) {
                    return y(d.amount);
                })
                .attr("height", function(d) {
                    return height - y(d.amount);
                })
                .attr("fill", function(d) {
                    return color(data.ingredient);
                });


            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));



            svg.append("g")
                .call(d3.axisLeft(y).ticks(1));

        };
    }

    xmlhttp.open("GET", "/ingredientstats", true);
    xmlhttp.send();
}

function type(d) {
    d.amount = +d.amount;
    return d;
}

function countrystats() {
    var data = []
    var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance 
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText);

            var text = "";

            var width = 260;
            var height = 260;
            var thickness = 40;
            var duration = 750;

            var radius = Math.min(width, height) / 2;
            var color = d3.scaleOrdinal(d3.schemeCategory10);

            var svg = d3.select("#chart")
                .append('svg')
                .attr('class', 'pie')
                .attr('width', width)
                .attr('height', height);

            var g = svg.append('g')
                .attr('transform', 'translate(' + (width / 2) + ',' + (height / 2) + ')');

            var arc = d3.arc()
                .innerRadius(radius - thickness)
                .outerRadius(radius);

            var pie = d3.pie()
                .value(function(d) {
                    return d.amount;
                })
                .sort(null);

            var path = g.selectAll('path')
                .data(pie(data))
                .enter()
                .append("g")
                .on("mouseover", function(d) {
                    let g = d3.select(this)
                        .style("cursor", "pointer")
                        .style("fill", "black")
                        .append("g")
                        .attr("class", "text-group");

                    g.append("text")
                        .attr("class", "name-text")
                        .text(`${d.data.country}`)
                        .attr('text-anchor', 'middle')
                        .attr('dy', '-1.2em');

                    g.append("text")
                        .attr("class", "value-text")
                        .text(`${d.data.amount}`)
                        .attr('text-anchor', 'middle')
                        .attr('dy', '.6em');
                })
                .on("mouseout", function(d) {
                    d3.select(this)
                        .style("cursor", "none")
                        .style("fill", color(this._current))
                        .select(".text-group").remove();
                })
                .append('path')
                .attr('d', arc)
                .attr('fill', (d, i) => color(i))
                .on("mouseover", function(d) {
                    d3.select(this)
                        .style("cursor", "pointer")
                        .style("fill", "black");
                })
                .on("mouseout", function(d) {
                    d3.select(this)
                        .style("cursor", "none")
                        .style("fill", color(this._current));
                })
                .each(function(d, i) {
                    this._current = i;
                });


            g.append('text')
                .attr('text-anchor', 'middle')
                .attr('dy', '.35em')
                .text(text);

        }
    }
    xmlhttp.open("GET", "/countrystats", true);
    xmlhttp.send();
}


function doload() {
    coursesstats();
    ingredientstats();
    countrystats();
}