document.addEventListener('DOMContentLoaded', function() {
    var checkboxes = document.querySelectorAll('.select-checkbox');
    var idInputs = document.querySelectorAll('[id^="ID_"]');

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            var taskId = this.dataset.taskId;
            if (this.checked) {
                idInputs.forEach(function(input) {
                    input.value = taskId;
                });
            } else {
                idInputs.forEach(function(input) {
                    input.value = "";
                });
            }
        });
    });
});
