var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});

var popover = new bootstrap.Popover(document.querySelectorAll('.copy_popover'), {
  container: 'body'
})

function show_copied_popover(element) {
  $(element).popover({
    placement: 'right',
    content: 'Skopiowano!',
    trigger: 'click'
  });
}