console.log("Tawasol main JS file");

$(document).ready(function() {

    var map_tweets = [];

    function owlInit(owl) {
        owl.trigger('destroy.owl.carousel');
        owl.html(owl.find('.owl-stage-outer').html()).removeClass('owl-loaded');
    }

    var owl_tweets = $("#owl-tweets");
    var owl_top_tweets = $("#owl-top-tweets");

    function catch_new_tweets(tweets) {
        owlInit(owl_tweets);
        var content = '';
        for (var i = tweets.length - 1; i >= 0; i--) {
            var array = tweets[i].split("\n");
            var last_item = array.splice(-1, 1);
            if (parseInt(last_item) != -1) {
                console.log("tweet with coordinates");
                map_tweets.push(tweets[i])
            }
            var tweet_text = array.join("\n");
            var content_item = '<div class="item"><h4>' + tweet_text + '</h4></div>';
            content += content_item;
        }
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
    }

    function generate_gender_distribution(values) {
        // gender distribution
        $('#gender_distribution').highcharts({
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
                name: 'Gender',
                data: values.gender
            }],
            colors:['#EA74E5', '#5DC0F6']
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
    }

    function generate_hashtags(values) {
        var hashtags = values.hashtags;
        $('#hashtag').jQCloud(hashtags, {
            autoResize: true
        });
    }

    function generate_sentiment_chart(values, categories) {
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
                categories: categories,
                tickmarkPlacement: 'on',
                labels: {
                    rotation: 30,
                    style: {
            	        fontSize:'6pt'
                    }
            }
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

    function generate_users_distribution(values, categories) {
        // User distribution for users
        $('#users_distribution').highcharts({
            colors: ['#FF8A33'],
            chart: {
                type: 'area',
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
                categories: categories,
                labels: {
                    rotation: 30,
                    style: {
            	        fontSize:'6pt'
                    }
            }
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
                    /*fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]*/
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
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
                data: values.users,
                color: '#FF8A33'
            }]
        });
    }

    function generate_happiness_chart(values, categories) {
        // Happiness distribution for tweets
        $('#happiness_distribution').highcharts({
            colors: ['#40ccb5'],
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
                categories: categories,
                labels: {
                    rotation: 30,
                    style: {
            	        fontSize:'6pt'
                    }
            }
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
                    /*fillColor: {
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
                    },*/
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
                data: values.happiness,
                color: '#40ccb5'
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

    function generate_top_users(top_users) {
        $('#owl-top-users').jQCloud(top_users, {
            autoResize: true
        });
    }

    function generate_top_tweets(top_tweets) {
        console.log("===== top tweets ====");
        //owlInit(owl_top_tweets);
        var content = '';
        for (var i = 0; i < top_tweets.length; i++) {
            var tweet_text = top_tweets[i]["text"];
            var tweet_weight = top_tweets[i]["weight"];
            //var content_item = '<div class="item"><h4>' + tweet_text + '</h4></div>';
            var content_item = '<div class="row"><div class="col-xs-1" align="center"><h4>' + tweet_weight + '</h4></div><div class="col-xs-10"><h4>' + tweet_text + '</h4></div></div>';
            content += content_item;
        }
        owl_top_tweets.html(content);
        /*owl_top_tweets.owlCarousel({
            items: 4,
            lazyLoad: false,
            margin: 10,
            nav: true,
            autoplay: true,
            dots: false,
            loop: false
        });*/
    }

    function generate_top_mentions(top_mentions) {
        $('#owl-top-mentions').jQCloud(top_mentions, {
            autoResize: true
        });
    }

    function update_categories_format(categories) {
        //console.log(categories);
        var up_categories = [];
        console.log(categories);
        const months = ["JAN", "FEB", "MAR","APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
        for (var i=0; i<categories.length; i++) {
            var category = categories[i];
            //var cat_date = Date.parse(category);
            var d= new Date(category);
            //console.log(d);
            var dday = ("0"+(d.getDate())).slice(-2);
            var dhour = ("0"+(d.getHours())).slice(-2);
            var dminutes = ("0"+(d.getMinutes())).slice(-2);
            var dmonth = months[d.getMonth()];
            var new_date = dday+"-"+dmonth+" "+dhour+":"+dminutes;
            up_categories.push(new_date);
        }
        return up_categories
    }

    function generate_stat_nbrs(values) {
        // change categories format
        var categories = update_categories_format(values.categories);
        update_tweets_count(values.nbr_tweets);
        update_users_count(values.nbr_users);
        update_date();
        generate_users_distribution(values, categories);
        generate_hashtags(values);
        generate_sentiment_chart(values, categories);
        generate_happiness_chart(values, categories);
        generate_language_distribution(values);
        generate_gender_distribution(values);
        catch_new_tweets(values.tweets);
        generate_top_users(values.top_users);
        generate_top_mentions(values.top_mentions);
        generate_top_tweets(values.top_tweets);
    }

    function processMapTweets() {
        console.log("map tweets length");
        console.log(map_tweets.length);
        //
        for (var i = map_tweets.length - 1; i >= 0; i--) {
            var array = map_tweets[i].split("\n");
            var last_item = array.splice(-1, 1);
            var broken = last_item[0].split(",");
            var lng = parseInt(broken[0]);
            var lat = parseInt(broken[1]);
            var lightgreenMarker = L.AwesomeMarkers.icon({
                icon: 'flame',
                markerColor: 'lightgreen'
            });
            var marker = L.marker([lat, lng], {
                icon: lightgreenMarker
            });
            //
            var tweet_text = array.join("\n");
            var content_item = '<div class="item"><h4>' + tweet_text + '</h4></div>';
            //
            marker.bindPopup(content_item);
            tweets_markers.addLayer(marker);
            tweets_markers.addTo(map);
        }
        //
    }

    function generate_charts(user_email) {
        console.log("inside generate");
        var url = '/get_info/' + user_email;
        $.getJSON(url, function(values, responseText, jqXHR) {
            if (jqXHR.status != 204) {
                generate_stat_nbrs(values.twitter);
            }
        });
    }

    var map;
    var tweets_markers;

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
        tweets_markers = L.markerClusterGroup();
        L.AwesomeMarkers.Icon.prototype.options.prefix = 'ion';

        map = L.map('map', {
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
        processMapTweets();
        /*
        ============== END MAP ==================
        */
    }

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