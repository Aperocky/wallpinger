// Ajax call to ping websites.
$('.ajaxcall').click(function(event) {
    event.preventDefault();
    console.log("executing ajax call");
    $(this).parent().parent().find("div.loadingframe").show();
    $.ajax({
        url: $(this).attr('href'),
        context: this,
        success: function(response) {
          console.log('I have received a response');
          var date = new Date(response['sent_time']);
          var datestr = date.toLocaleString();

          if (response['received'] > 0){
            $(this).parent().parent().find("p.results").html("Pinged at " + datestr + '<br />' + response['received'] + "/5 Packets Received <br /> Average RTT: " + response['average'] + ' ms');
          } else {
            $(this).parent().parent().find("p.results").html("Pinged at " + datestr + '<br /> 0/5 Packets Received <br /> Average RTT: N/A');
          }
          $(this).parent().parent().find("div.loadingframe").hide();
          console.log($(this).parent().parent().find("div.loadingframe"))
          console.log(datestr);
        }
    });
    console.log("Ajax call finished");
    return false; // for good measure
});
