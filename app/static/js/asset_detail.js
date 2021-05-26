$(document).ready(function() {
  function updateTxFee() {
    var address = $('#id_address').val();
    var feeField = $('#id_fee');

    if (!address) {
      feeField.val('--------');
      return;
    }

    var form = document.getElementById('mint-nft-form');
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

  var cardContainer = $('.card-container');
  var card = $('.card');

  var imageAspectRatio = assetMetadata.height / assetMetadata.width;
  var paddingBottom = (imageAspectRatio * 100) + '%';
  cardContainer.css('padding-bottom', paddingBottom);

  cardContainer.mouseenter(function() {
    card.css('transform', 'rotateY(180deg)');
  }).mouseleave(function() {
    card.css('transform', '');
  });

  var assetMetadataPre = $('.asset-metadata');
  assetMetadataPre.html(JSON.stringify(assetMetadata, null, 2));

  // card.on('mouseover')
  // $('#id_address').keyup(_.debounce(updateTxFee, 500, {
  //   'leading': false,
  //   'trailing': true,
  // }));
  //
  // updateTxFee();
});
