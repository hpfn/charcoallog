$(function() {
  // Array with names of inputs
  id_inputs = ['id_date', 'id_money', 'id_description', 'id_category', 'id_payment']
  inputs = ['date', 'money', 'description', 'category', 'payment']
  let url_edit

  // Edit money
  $('.money-edit').on('click', function() {
    let obj = $(this).closest('tr').children('td')
    url_edit = $(this).data('url')

    // get the length of array (obj)
    let totalLen = obj.length

    obj.each(function(i, e) {
      var item_v = $(this).text()
      if (i < totalLen - 1) {
        $(this).empty()
        // If is description the width is large
        if (i == 2) {
          $(this).append('<input type="text" id="' + id_inputs[i] + '" name="' + inputs[i] + '" style="width: 30em;" value="' + item_v + '" />')
        } else {
          $(this).append('<input type="text" id="' + id_inputs[i] + '" name="' + inputs[i] + '" style="width: 6em;" value="' + item_v + '" />')
        }
      // Insert icons on last column
      } else {
        $(this).empty()
        $(this).append('<i class="fa fa-check span-is-link" ></i>')
        $(this).append('<i class="fa fa-close span-is-link" style="color: red"></i>')
      }
    });
  });

  // Update
  $(document).on('click', '.fa-check', function(event) {
    // get all values from inputs
    let date = $('#' + id_inputs[0]).val();
    let money = $('#' + id_inputs[1]).val();
    let description = $('#' + id_inputs[2]).val();
    let category = $('#' + id_inputs[3]).val();
    let payment = $('#' + id_inputs[4]).val();
    console.log(url_edit);
    $.post(
      url_edit,
      {
        date: date,
        money: money,
        description: description,
        category: category,
        payment: payment
      },
      function(response) {
        location.reload()
    });
  });

  // Cancel
  $(document).on('click', '.fa-close', function(event) {
    location.reload()
  });

  // Delete money
  $('.money-delete').on('click', function() {
    let url = $(this).data('url')
    let $this = $(this)
    $.get(url, function(data) {
      $this.parent().parent().remove()
    });
  });
});