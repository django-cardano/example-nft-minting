$(document).ready(function() {
  function updateTxFee() {
    var address = $('#id_address').val();
    var quantity = $('#id_quantity').val();
    var feeField = $('#id_fee');

    if (!(address && quantity)) {
      feeField.val('--------');
      return;
    }

    var form = document.getElementById('transfer-ada-form');
    $.ajax({
      url: form.action,
      method: 'post',
      data: {
        source_wallet_id: walletId,
        quantity: quantity,
        address: address,
      },
      headers: {
        "X-CSRFToken": form.csrfmiddlewaretoken.value
      }
    }).done(function(data) {
      if (data.fee) {
        var adaFee = data.fee / 1000000;
        feeField.val(adaFee.toFixed(6));
      } else {
        feeField.val('--------');
      }
    });
  }

  $('#id_quantity, #id_address').keyup(_.debounce(updateTxFee, 500, {
    'leading': false,
    'trailing': true,
  }));

  updateTxFee();

  // --------------------------------------------------------------------------
  $('#consolidate-utxos-form').on('submit', function(e) {
    var password = window.prompt('Enter wallet spending password');
    if (password) {
      var form = e.target;
      $.ajax({
        url: form.action,
        method: 'post',
        data: {
          consolidate_tokens_password: password
        },
        headers: {
          "X-CSRFToken": form.csrfmiddlewaretoken.value
        }
      }).done(function(responseData) {
        window.location.href = responseData.transaction_url;
      }).fail(function(xhr) {
        window.alert(xhr.responseJSON.error);
      });
    }

    return false;
  });
});
