/**
 * This is the pie chart for the statistics on the amount of different courses in the database.
 * This method uses AJAX to retrieve the course statistics from the backend as json format
 * and then formats it to javascript data structure and uses it to form a pie chart using d3
 */
function coursesstats() {
    // The data held in javascript
    var data = []
    // AJAX http request
    var xmlhttp = new XMLHttpRequest();
    
    // Callback function for successfull AJAX request

    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // Retrieved JSON content successful. Now parse to native javascript format
            data = JSON.parse(this.responseText);

            // Use adequate size for all devices and calculate radius
            var width = 300,
                height = 300,
                radius = Math.min(width, height) / 2;

            // Allocate random colouring scheme for different course items
            var color = d3.scaleOrdinal(d3.schemeCategory10);

            // Supply the data for the pie chart
            var pie = d3.pie().value(function (d) {
                return d.amount;
            })(data);

            // Generate arc
            var arc = d3.arc().outerRadius(radius - 10).innerRadius(0);
            
            // Generate label for arc
            var labelArc = d3.arc().outerRadius(radius - 40).innerRadius(radius - 40);
            
            // Generate SVG item and transform and translate it.
            var svg = d3.select("#coursestats").append("svg").attr("width", width).attr("height", height).append("g")
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

            var g = svg.selectAll("arc").data(pie).enter().append("g")
                .attr("class", "arc");

            // Fill the specific course item with a colour
            g.append("path").attr("d", arc).style("fill", function (d) {
                return color(d.data.course);
            });

            // Add the text label
            g.append("text").attr("transform", function (d) {
                return "translate(" + labelArc.centroid(d) + ")";
            }).text(function (d) {
                return d.data.course;
            })
                .style("fill", "#fff");

        }
    };
    // Retrieve AJAX stats from backend
    xmlhttp.open("GET", "/coursestats", true);
    xmlhttp.send();
}

/**
 * This is a bar chart for the amount of allergen ingredients included in the recipes
 * This method uses AJAX to retrieve the allergen statistics from the backend as json format
 * and then formats it to javascript data structure and uses it to form a bar chart using d3
 */
function ingredientstats() {
    // The data held in javascript
    var data = []
    // The AJAX request
    var xmlhttp = new XMLHttpRequest();

    // Callback function for successfull AJAX request
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // Retrieved JSON content successful. Now parse to native javascript format
            data = JSON.parse(this.responseText);

            // The margin for the bar chart
            var margin = {
                top: 20,
                right: 20,
                bottom: 30,
                left: 40
            },
            
            // Calculate the width and height using an adequate size for all devices
            width = 360 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

            // Random colour scheme
            var color = d3.scaleOrdinal(d3.schemeCategory10);
            
           
            var x = d3.scaleBand()
                .range([0, width])
                .padding(0.1);
            var y = d3.scaleLinear()
                .range([height, 0]);

            // Calculate SVG item transform and translate it.
            var svg = d3.select("#ingredientstats").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

            // The data for the x axis
            x.domain(data.map(function (d) {
                return d.ingredient;
            }));

            // The data for the y axis
            y.domain([0, d3.max(data, function (d) {
                return d.amount;
            })]);

            // append the rectangles for the bar chart
            svg.selectAll(".bar")
                .data(data)
                .enter().append("rect")
                .attr("class", "bar")
                .attr("x", function (d) {
                    return x(d.ingredient);
                })
                .attr("width", x.bandwidth())
                .attr("y", function (d) {
                    return y(d.amount);
                })
                .attr("height", function (d) {
                    return height - y(d.amount);
                })
                .attr("fill", function (d) {
                    return color(data.ingredient);
                });

            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            svg.append("g")
                .call(d3.axisLeft(y).ticks(1));

        };
    }
    // AJAX Request
    xmlhttp.open("GET", "/ingredientstats", true);
    xmlhttp.send();
}

// Helper function
function type(d) {
    d.amount = +d.amount;
    return d;
}

/**
 * This is the donut chart for the statistics on the amount of different countries in the database
 * for the total of recipes.
 * This method uses AJAX to retrieve the country statistics from the backend as json format
 * and then formats it to javascript data structure and uses it to form a donut chart using d3
 */
function countrystats() {
    // The data held in javascript
    var data = []
    // The AJAX request
    var xmlhttp = new XMLHttpRequest(); 
    xmlhttp.onreadystatechange = function () {
        // Function to process response
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText);

            var text = "";
            // dimension variables
            var width = 260;
            var height = 260;
            var thickness = 40;
            var duration = 750;
            // radius of donut chart
            var radius = Math.min(width, height) / 2;
            // random colour scheme
            var color = d3.scaleOrdinal(d3.schemeCategory10);

            // Select the chart to create
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

            // Give the chart the data to process with
            var pie = d3.pie()
                .value(function (d) {
                    return d.amount;
                })
                .sort(null);

            // Create the 'donut' variant of the pie chart
            // with mouseover functions
            var path = g.selectAll('path')
                .data(pie(data))
                .enter()
                .append("g")
                .on("mouseover", function (d) {
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
                .on("mouseout", function (d) {
                    d3.select(this)
                        .style("cursor", "none")
                        .style("fill", color(this._current))
                        .select(".text-group").remove();
                })
                .append('path')
                .attr('d', arc)
                .attr('fill', (d, i) => color(i))
                .on("mouseover", function (d) {
                    d3.select(this)
                        .style("cursor", "pointer")
                        .style("fill", "black");
                })
                .on("mouseout", function (d) {
                    d3.select(this)
                        .style("cursor", "none")
                        .style("fill", color(this._current));
                })
                .each(function (d, i) {
                    this._current = i;
                });

            // The Text in the middle
            g.append('text')
                .attr('text-anchor', 'middle')
                .attr('dy', '.35em')
                .text(text);

        }
    }
    // The AJAX requet opened and sent
    xmlhttp.open("GET", "/countrystats", true);
    xmlhttp.send();
}

/**
 * Function for when the body loads to generate all the graphs
 */
function doload() {
    coursesstats();
    ingredientstats();
    countrystats();
}