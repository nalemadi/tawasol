console.log("Tawasol main JS file");

$(document).ready(function() {

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
    var user_email = $('#my-data').data();
    if (user_email != null) {
        console.log(user_email);
        generate_charts(user_email);
    }
});