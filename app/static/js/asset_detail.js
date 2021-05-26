$(document).ready(function() {
  var mintNFTForm = $('#mint-nft-form');
  var feeField = $('#id_fee');

  function updateTxFee(e) {
    if (e) {
      if (e.target.name === 'password') {
        return;
      }
    }
    const form = mintNFTForm[0];

    const mintingPolicyId = form.minting_policy.value;
    const paymentWalletId = form.payment_wallet.value;
    const destinationAddress = form.destination_address.value;

    if (!(mintingPolicyId && paymentWalletId && destinationAddress)) {
      feeField.val('--------');
      return;
    }

    $.ajax({
      url: form.action,
      method: 'post',
      data: {
        minting_policy: mintingPolicyId,
        payment_wallet: paymentWalletId,
        destination_address: destinationAddress,
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

  // ----------------------------------------------------------------
  $('.asset-metadata').html(
    JSON.stringify(assetMetadata, null, 2)
  );

  // ----------------------------------------------------------------
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

  // ----------------------------------------------------------------
  mintNFTForm.on('keyup change', _.debounce(updateTxFee, 500, {
    'leading': false,
    'trailing': true,
  }));

  updateTxFee();
});
