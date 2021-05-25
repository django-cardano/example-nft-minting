$(document).ready(function() {
  function queryTip() {
    $.ajax({ url: queryTipUrl })
      .done(function(tipInfo) {
        $('#tip-epoch').html(tipInfo.epoch);
        $('#tip-block').html(tipInfo.block);
        $('#tip-slot').html(tipInfo.slot);
      });
  }

  setInterval(queryTip, 5000);
  queryTip();
});
