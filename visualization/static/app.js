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

        var bars = chart.selectAll(".bar")
            .data(this.data);

        bars.enter().append("rect")
            .attr("class", "bar")
            .attr("transform", "translate(25, 0)")
            .attr("height", function(d) { return height - y(d.value); })
            .attr("width", x.step() - 50)
        .merge(bars)
            .attr("x", function(d) { return x(d.label); })
            .attr("y", function(d) { return y(d.value); });

        bars.exit().remove();
    }
});

Vue.component("post", {
    template: "<div class='post' v-html='message'></div>",
    props: ["message", "sentimentwords", "product", "aspect"],
    mounted: function() {
        var tokens = this.message.split(" ");
        var result = "";

        for(var i = 0; i < tokens.length; i++) {
            token = tokens[i].toLowerCase();

            if(this.sentimentwords.positive.indexOf(token) !== -1) {
                result += "<span class='positive'>" + tokens[i] + "</span> ";
            } else if(this.sentimentwords.negative.indexOf(token) !== -1) {
                result += "<span class='negative'>" + tokens[i] + "</span> ";
            } else if(token === this.product.toLowerCase()) {
                result += "<span class='product'>" + tokens[i] + "</span> ";
            } else if(token === this.aspect.toLowerCase()) {
                result += "<span class='aspect'>" + tokens[i] + "</span> ";
            } else {
                result += token + " "
            }
        }

        this.message = result;
    }
});

new Vue({
    el: "#app",
    data: {
        products: [],
        selectedProduct: {
            product: {}
        },
        sentimentwords: []
    },
    mounted: function() {
        var that = this;
        $.get("http://127.0.0.1:5000", function(data) {
            that.products = _.map(data.products, function(product) {
                return {
                    label: product.name,
                    value: product
                };
            });
            that.selectedProduct = that.products[0].value;
            that.sentimentwords = data.sentimentwords;
        });
    }
})