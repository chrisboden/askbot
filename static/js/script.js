
$(function () {
    // Send GET request to /list_of_books endpoint on page load
    $.get("/mentors", function (data) {
        // Insert returned data into the #results element
        $("#mentors").html(data);
    });

    // Submit form via AJAX
    $("#search-form").submit(function (event) {
        event.preventDefault();

        // Show loading spinner
        $("#loading-spinner").show();

        // Get form data
        var formData = $(this).serialize();

        // Send POST request to /search endpoint
        $.ajax({
            type: "POST",
            url: "/search",
            data: formData,
            success: function (response) {
                // Split response by new line characters
                var lines = response["choices"][0]["text"].split("\n");
                // Iterate over each line
                lines.forEach(function (line) {
                    // Create a p element for each line
                    var p = $("<div class=\"result-item\"><p></p></div>").text(line);
                    // Append the p element to the results container
                    $("#results").append(p).scrollTop($("#results")[0].scrollHeight);
                    // Hide loading spinner
                    $("#loading-spinner").hide();
                    $(".robot-says").show();
                });
            }
        });
    });
});

$(function () {
    // Send GET request to /get-prompt endpoint on modal show event
    $("#promptmodal").on("show.bs.modal", function () {
        $.get("/get-prompt", function (data) {
            // Insert returned prompt text into the #promptedit textarea
            $("#promptedit").val(data);
        });
    });

    // Submit form via AJAX when the form is submitted
    $("#edit-prompt-form").submit(function (event) {
        event.preventDefault();
        // Get form data
        var formData = $(this).serialize();
        // Send POST request to /save-prompt endpoint
        $.ajax({
            type: "POST",
            url: "/save-prompt",
            data: formData,
            success: function (response) {
                // Show success alert
                $("#alert-container").html(
                    '<div class="alert alert-success alert-dismissible fade show" role="alert">' +
                    response +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span>' +
                    "</button>" +
                    "</div>"
                );
                // Close the modal
                $("#promptmodal").modal("hide");
            },
            error: function () {
                // Show error alert
                $("#alert-container").html(
                    '<div class="alert alert-danger alert-dismissible fade show" role="alert">Error saving prompt text.' +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span>' +
                    "</button>" +
                    "</div>"
                );
            }
        });
    });
});