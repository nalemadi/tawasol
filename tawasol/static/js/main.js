console.log("Tawasol main JS file");

$(document).ready(function() {

    var owl_tweets = $("#owl-tweets");

    function catch_new_tweets(tweets) {
        owlInit(owl_tweets)
        var content = ''
        for (var i = tweets.length - 1; i >= 0; i--) {
            var content_item = '<div class="item"><h4>' + tweets[i] + '</h4></div>';
            content += content_item;
        };
        owl_tweets.html(content);
        owl_tweets.owlCarousel({
            items: 4,
            lazyLoad: false,
            margin: 10,
            nav: true,
            autoplay: true,
            dots: false,
            loop: false
        });
    };


    function generate_language_distribution(values) {
        // language distribution
        $('#language_distribution').highcharts({
            chart: {
                type: 'pie',
                height: 250
            },
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            series: [{
                name: 'Used language',
                data: values.language
            }]
        });
    };

    function generate_hashtags(values) {
        var hashtags = values.hashtags;
        $('#hashtag').jQCloud(hashtags, {
            autoResize: true
        });
    }

    function generate_sentiment_chart(values) {
        // Sentiment Chart for Tweets
        $('#chart_sentiment').highcharts({
            colors: ['#27ae60', '#e74c3c', '#7f8c8d'],
            chart: {
                type: 'area',
                height: 350
            },
            title: {
                text: ''
            },
            xAxis: {
                categories: values.categories,
                tickmarkPlacement: 'on',
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Total Number of tweets'
                },
                stackLabels: {
                    enabled: true,
                    style: {
                        fontWeight: 'bold',
                        color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                    }
                }
            },
            legend: {
                align: 'right',
                x: -30,
                verticalAlign: 'top',
                y: 25,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
                borderColor: '#CCC',
                borderWidth: 1,
                shadow: false
            },
            tooltip: {
                headerFormat: '<b>{point.x}</b><br/>',
                pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
            },
            plotOptions: {
                area: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                    }
                }
            },
            series: [{
                name: 'Positive',
                data: values.positive
            }, {
                name: 'Negative',
                data: values.negative
            }, {
                name: 'Neutral',
                data: values.neutral
            }]
        });
    }

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
                text: ''
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
    }

    function generate_happiness_chart(values) {
        // Happiness distribution for tweets
        $('#happiness_distribution').highcharts({
            chart: {
                zoomType: 'x',
                height: 250
            },
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                categories: values.categories
            },
            yAxis: {
                title: {
                    text: 'happiness score'
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
                name: 'happiness score',
                data: values.happiness
            }]
        });
    }

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
        generate_sentiment_chart(values);
        generate_happiness_chart(values);
        generate_language_distribution(values);
        catch_new_tweets(values.tweets)
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

    function generate_map() {
            /*
        ============== MAP ==================
        */
        // Initialize the tile layers (base layers)
        var mapbox_tawasol_apikey = 'MAPBOX_TOKEN_REMOVED',
            mapboxUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}',
            mapboxAttribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,' +
            '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>,' + 'Imagery © <a href="http://mapbox.com">Mapbox</a>',
            dark = L.tileLayer(mapboxUrl, {
                id: 'mapbox.dark',
                attribution: mapboxAttribution,
                accessToken: mapbox_tawasol_apikey
            }),
            light = L.tileLayer(mapboxUrl, {
                id: 'mapbox.light',
                attribution: mapboxAttribution,
                accessToken: mapbox_tawasol_apikey
            }),
            satellite = L.tileLayer(mapboxUrl, {
                id: 'mapbox.satellite',
                attribution: mapboxAttribution,
                accessToken: mapbox_tawasol_apikey
            }),
            streets = L.tileLayer(mapboxUrl, {
                id: 'mapbox.streets',
                attribution: mapboxAttribution,
                accessToken: mapbox_tawasol_apikey
            });

        // initialize the map
        // var map = L.map('map').setView([25.3, 51.3], 10);
        //
        var tweets_markers = L.markerClusterGroup();
        L.AwesomeMarkers.Icon.prototype.options.prefix = 'ion';

        var map = L.map('map', {
            center: [25.3, 51.49],
            zoom: 12,
            layers: [dark]
        });

        // Layer configuration/Management
        var baseMaps = {
            "Grayscale": dark,
            "Light": light,
            "Satellite": satellite,
            "Streets": streets
        };

        var overlayMaps = {
            "Tweets": tweets_markers
        };
        //
        var controller = L.control.layers(baseMaps, overlayMaps);
        controller.addTo(map);
        //

        /*
        ============== END MAP ==================
        */
    };

    ////////////////////////////
    //  Start Here          ///
    ///////////////////////////
    var user_data = $('#my-data').data();
    if (user_data != null) {
        var user_email = user_data.name;
        console.log(user_email);
        generate_charts(user_email);
        generate_map();
    }
});