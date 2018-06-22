function AjaxPing(event) {
  event.preventDefault();
  console.log("executing ajax ping call");
  $(this).parent().parent().find("div.loadingframe").show();
  $.ajax({
    url: $(this).attr('href'),
    context: this,
    success: function (response) {
      console.log('I have received a response');
      var date = new Date(response['sent_time']);
      var datestr = date.toUTCString();
      datestr = datestr.substring(0, datestr.lastIndexOf(" "));

      if (response['received'] > 0) {
        $(this).parent().parent().find("p.results").html("Pinged at " + datestr + '<br />' + response['received'] + "/5 Packets Received <br /> Average RTT: " + response['average'] + ' ms');
      } else {
        $(this).parent().parent().find("p.results").html("Pinged at " + datestr + '<br /> 0/5 Packets Received <br /> Average RTT: N/A');
      }
      $(this).parent().parent().find("div.loadingframe").hide();
      $(this).parent().parent().removeClass("bg-red bg-lime bg-yellow");
      $(this).parent().parent().addClass(response['color']);
      console.log($(this).parent().parent().find("div.loadingframe"));
      console.log(datestr);
    }
  });
  console.log("Ajax call finished");
  return false; // for good measure
}

// Ajax call to ping websites.
$('.ajaxcall').on("click", AjaxPing);

// Toggles add website section
$('#adding').click( function(){
  $('#addform').toggle();
  $('#adding').html($('#adding').html() == ' Add ' ? ' Hide ' : ' Add ');
  return false;
});

// Ajax call handling adding of websites
$("#addform").submit(function(e){
  e.preventDefault();
  console.log("Ajax call to add website")
  $('#addloading').show()
  $.ajax({
    url: $("#addform").attr('action'),
    type: "post",
    data: $("#addform").serialize(),
    success: function(response, status){
      console.log("I have received a response from add website");
      console.log(status);
      $('#addloading').hide();
      if (response['sent'] == 0){
        alert("URL can't be resolved.");
        return false;
      }
      var lastpass = $(".website:last");
      newpass = lastpass.clone();
      newpass.find(".passage").removeClass("bg-red bg-lime bg-yellow");
      newpass.find(".passage").addClass(response['color']);
      newpass.find("p.lead").html("<b class='text-white webname'>" + response['website_name'] + "</b><br />" + response['website_url']);
      newpass.find("b.webname").html(response['website_name']);
      var date = new Date(response['sent_time']);
      var datestr = date.toLocaleString();
      if (response['received'] > 0){
        newpass.find("p.results").html("Pinged at " + datestr + '<br />' + response['received'] + "/5 Packets Received <br /> Average RTT: " + response['average'] + ' ms');
      } else {
        newpass.find("p.results").html("Pinged at " + datestr + '<br /> 0/5 Packets Received <br /> Average RTT: N/A');
      }
      newpass.find(".ajaxcall").attr("href", "/wall/" + response['my_id'] + "/ping");
      newpass.find(".ajaxcall").on("click", AjaxPing)
      newpass.find(".historycall").attr("href", "/wall/" + response['my_id'] + "/history");
      newpass.insertAfter(lastpass);
      return false;
    }
  });
});
