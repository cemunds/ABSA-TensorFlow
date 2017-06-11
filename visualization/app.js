Vue.component("product", {
    template: "#product-template",
    props: {
        product: {
            type: Object,
            required: true
        }
    }
});

Vue.component("sentiment-chart", {
    template:"<svg class='chart'></svg>",
    props: ["data"],
    mounted: function() {
        var margin = {
            top: 20,
            right: 30,
            bottom: 30,
            left: 40
        };

        var width = 420 - margin.left - margin.right;
        var height = 250 - margin.top - margin.bottom;

        var x = d3.scaleBand()
        .domain(this.data.map(function(d) { return d.label; }))
        .rangeRound([0, width], .1);

        var y = d3.scaleLinear()
        .domain([0, d3.max(this.data, function(d) { return d.value; })])
        .range([height, 0]);

        var xAxis = d3.axisBottom().scale(x);
        var yAxis = d3.axisLeft().scale(y);

        var chart = d3.select(this.$el)
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        chart.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        chart.append("g")
            .attr("class", "y axis")
            .call(yAxis);

        chart.selectAll(".bar")
            .data(this.data)
        .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.label); })
            .attr("y", function(d) { return y(d.value); })
            .attr("transform", "translate(25, 0)")
            .attr("height", function(d) { return height - y(d.value); })
            .attr("width", x.step() - 50);
    }
});

new Vue({
    el: "#app",
    data: {
        products: [
            {
                "name": "iPhone",
                "aspects": [
                    {
                        "name": "battery",
                        "sentiments": [
                            {
                                label: "negative",
                                value: 5
                            },
                            {
                                label: "neutral",
                                value: 3
                            },
                            {
                                label: "positive",
                                value: 2
                            }
                        ],
                        "posts": ["[...] the battery does not last long enough [...]"]
                    }
                ]
            }
        ]
    },
    methods: {

    },
    mounted: function() {

    }
})