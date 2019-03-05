console.log("Tawasol main JS file");

$(document).ready(function() {

    function generate_hashtags(values) {
        var hashtags = values.hashtags;
        $('#hashtag').jQCloud(hashtags, {
            autoResize: true
        });
    };

    function generate_users_distribution(values) {
        // User distribution for users
        $('#users_distribution').highcharts({
            chart: {
                zoomType: 'x',
                height: 250
            },
            title: {
                text: ''
            },
            subtitle: {
                text: 'Click to zoom in'
            },
            xAxis: {
                categories: values.categories
            },
            yAxis: {
                title: {
                    text: 'Number of users'
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            series: [{
                type: 'area',
                name: 'Number of users',
                data: values.users
            }]
        });
    };

    function update_tweets_count(tweets_count) {
        $('#tweets_count').text(tweets_count);
    }

    function update_users_count(users_count) {
        $('#users_count').text(users_count);
    }

    function update_date() {
        var current_time = Date.now();
        $('#last_update').text(moment(current_time).format("HH:mm"));
    }

    function generate_stat_nbrs(values) {
        update_tweets_count(values.nbr_tweets);
        update_users_count(values.nbr_users);
        update_date();
        generate_users_distribution(values);
        generate_hashtags(values);
    }

    function generate_charts(user_email) {
        console.log("inside generate");
        var url = '/get_info/'+user_email;
        $.getJSON(url, function(values, responseText, jqXHR) {
            if (jqXHR.status != 204) {
                generate_stat_nbrs(values.twitter);
            }
        });
    };

    ////////////////////////////
    //  Start Here          ///
    ///////////////////////////
    var user_data = $('#my-data').data();
    if (user_data != null) {
        var user_email = user_data.name;
        console.log(user_email);
        generate_charts(user_email);
    }
});