// variable that keeps all the filter information

var send_data = {}

$(document).ready(function () {
    // reset all parameters on page load

    resetFilters();
    // bring all the data without any filters

    getAPIData();
    // get all program from database via 

    // AJAX call into program select options

    getprogram();
    // get all varities from database via 

    // AJAX call into variert select options

    getstate_of_origin();

    // on selecting the program option


    $('#program').on('change', function () {
        // since program_version and local_govt is dependent 

        // on program select, emty all the options from select input

        $("#program_version").val("all");
        $("#program_specific").val("all");
        send_data['program_version'] = '';
        send_data['program_specific'] = '';

        // update the selected program

        if(this.value == "all")
            send_data['program'] = "";
        else
            send_data['program'] = this.value;

        //get program_version of selected program

        getprogram_version(this.value);
        getprogram_specific(this.value);
        // get api data of updated filters

        getAPIData();
    });

    // on filtering the state_of_origin input

    $('#state_of_origin').on('change', function () {
        // get the api data of updated state_of_origin
        
        $("#local_govt").val("all");

        send_data['local_govt'] = '';
        
        if(this.value == "all")
            send_data['state_of_origin'] = "";
        else
            send_data['state_of_origin'] = this.value;
        
        getlocal_govt(this.value);
        
        getAPIData();
    });

    // on filtering the program_version input

    $('#program_version').on('change', function () {
        // clear the local_govt input 

        // since it is dependent on program_version input

        
        if(this.value == "all")
            send_data['program_version'] = "";
        else
            send_data['program_version'] = this.value;
        
        getAPIData();
    });

    $('#program_specific').on('change', function () {
        // clear the local_govt input 

        // since it is dependent on program_version input

        
        if(this.value == "all")
            send_data['program_specific'] = "";
        else
            send_data['program_specific'] = this.value;
        
        getAPIData();
    });

    // on filtering the local_govt input

    $('#local_govt').on('change', function () {

        if(this.value == "all")
            send_data['local_govt'] = "";
        else
            send_data['local_govt'] = this.value;
        getAPIData();
    });

    // sort the data according to price/points

    $('#sort_by').on('change', function () {
        send_data['sort_by'] = this.value;
        getAPIData();
    });

    // display the results after reseting the filters

    $("#display_all").click(function(){
        resetFilters();
        getAPIData();
    })
})


/**
    Function that resets all the filters   
**/
function resetFilters() {
    $("#program").val("all");
    $("#program_version").val("all");
    $("#program_specific").val("all");
    $("#local_govt").val("all");
    $("#state_of_origin").val("all");
    $("#sort_by").val("none");
    
    //clearing up the program_version and local_govt select box
    getprogram_specific("all");
    getprogram_version("all");
    getlocal_govt("all");
    

    send_data['program'] = '';
    send_data['program_version'] = '';
    send_data['program_specific'] = '';
    send_data['local_govt'] = '';
    send_data['state_of_origin'] = '';
    send_data["sort_by"] = '',
    send_data['format'] = 'json';
}

/**.
    Utility function to showcase the api data 
    we got from backend to the table content
**/
function putTableData(result) {
    // creating table row for each result and

    // pushing to the html cntent of table body of listing table

    let row;
    if(result["results"].length > 0){
        $("#no_results").hide();
        $("#list_data").show();
        $("#listing").html(""); 
        var count = 1;
        fem = 0
        mal = 0
        row = result["results"].map(function (b) {
            
            
            if (b.gender=='Female') {
                female_count = ++fem
            } else if (b.gender !=='Female') {
                female_count = fem
            }
            
            if (b.gender=='Male'){
                male_count = ++mal
            } else if (b.gender !=='Male'){
                male_count = mal
            }
            
            
            return "<tr> <td>" + count++ + "</td>" +
                "<td>" + b.unique_id + "</td>"+
                "<td> <a href = 'student_detail/'> " + b.surname + "</a></td>" +
                "<td>" + b.firstname + "</td>" +
                "<td>" + b.middlename + "</td>" +
                "<td>" + b.gender + "</td>" +
                "<td>" + b.program + "</td>" +
                "<td>" + b.program_version + "</td>" +
                "<td>" + b.program_specific + "</td>" +
                "<td>" + b.roll_no + "</td>" +
                "<td>" + b.state_of_origin + "</td>" +
                "<td>" + b.local_govt + "</td>" +
                "<td>" + b.email + "</td>" +
                "<td>" + b.phone_no + "</td></tr>";
            
        });
        
        $("#listing").append(row);   
    }
    else{
        // if no result found for the given filter, then display no result

        $("#no_results h5").html("No results found");
        $("#list_data").hide();
        $("#no_results").show();
    }
    // setting previous and next page url for the given result

    let prev_url = result["previous"];
    let next_url = result["next"];
    // disabling-enabling button depending on existence of next/prev page. 

    if (prev_url === null) {
        $("#previous").addClass("disabled");
        $("#previous").prop('disabled', true);
    } else {
        $("#previous").removeClass("disabled");
        $("#previous").prop('disabled', false);
    }
    if (next_url === null) {
        $("#next").addClass("disabled");
        $("#next").prop('disabled', true);
    } else {
        $("#next").removeClass("disabled");
        $("#next").prop('disabled', false);
    }
    // setting the url

    $("#previous").attr("url", result["previous"]);
    $("#next").attr("url", result["next"]);
    // displaying result count

    $("#result-count span").html(result["count"]);
    $("#total_number h3").html(result["count"]);
    $("#female h4").html(female_count);
    $("#male h4").html(male_count);
}

function getAPIData() {
    let url = $('#list_data').attr("url")
    $.ajax({
        method: 'GET',
        url: url,
        data: send_data,
        beforeSend: function(){
            $("#no_results h5").html("Loading data...");
        },
        success: function (result) {
            let count = 0
            result['results'].forEach(element => {
                element.sn = ++count 
            });

            putTableData(result);
        },
        error: function (response) {
            $("#no_results h5").html("Something went wrong");
            $("#list_data").hide();
        }
    });
}

$("#next").click(function () {
    // load the next page data and 

    // put the result to the table body

    // by making ajax call to next available url

    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (result) {
            putTableData(result);
        },
        error: function(response){
            console.log(response)
        }
    });
})

$("#previous").click(function () {
    // load the previous page data and 

    // put the result to the table body 

    // by making ajax call to previous available url

    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (result) {
            putTableData(result);
        },
        error: function(response){
            console.log(response)
        }
    });
})

function getprogram() {
    // fill the options of program by making ajax call

    // obtain the url from the program select input attribute

    let url = $("#program").attr("url");

    // makes request to getprogram(request) method in views

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {

            program_option = "<option value='all' selected>All Programs</option>";
            $.each(result["program"], function (a, b) {
                program_option += "<option>" + b + "</option>"
            });
            $("#program").html(program_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getstate_of_origin() {
    // fill the options of varities by making ajax call

    // obtain the url from the varities select input attribute

    let url = $("#state_of_origin").attr("url");
    // makes request to getstate_of_origin(request) method in views

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            state_options = "<option value='all' selected>All States</option>";
            $.each(result["state_of_origin"], function (a, b) {
                state_options += "<option>" + b + "</option>"
            });
            $("#state_of_origin").html(state_options)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getprogram_version(program) {
    // fill the options of program_versions by making ajax call

    // obtain the url from the program_versions select input attribute

    let url = $("#program_version").attr("url");
    // makes request to getprogram_version(request) method in views

    let program_version_option = "<option value='all' selected>All Program Versions</option>";
    $.ajax({
        method: 'GET',
        url: url,
        data: {
            "program": program
        },
        success: function (result) {
            $.each(result["program_version"], function (a, b) {
                program_version_option += "<option>" + b + "</option>"
            });
            $("#program_version").html(program_version_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getprogram_specific(program) {
    // fill the options of program_versions by making ajax call

    // obtain the url from the program_versions select input attribute

    let url = $("#program_specific").attr("url");
    // makes request to getprogram_version(request) method in views

    let program_specific_option = "<option value='all' selected>All Courses</option>";
    $.ajax({
        method: 'GET',
        url: url,
        data: {
            "program": program
        },
        success: function (result) {
            $.each(result["program_specific"], function (a, b) {
                program_specific_option += "<option>" + b + "</option>"
            });
            $("#program_specific").html(program_specific_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getlocal_govt(state_of_origin) {
    // fill the options of local_govt by making ajax call

    // obtain the url from the local_govt select input attribute

    let url = $("#local_govt").attr("url");
    // makes request to getlocal_govt(request) method in views

    let local_govt_option = "<option value='all' selected>All LGAs</option>";
    $.ajax({
        method: 'GET',
        url: url,
        data: {
            "state_of_origin": state_of_origin,
        },
        success: function (response) {
            $.each(response["local_govt"], function (a, b) {
                local_govt_option += "<option>" + b + "</option>"
            });
            $("#local_govt").html(local_govt_option);
        },
        error: function(response){
            console.log(response)
        }
    });
}

