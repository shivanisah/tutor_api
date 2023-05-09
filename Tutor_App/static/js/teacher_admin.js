(function ($) {
    $(document).ready(function () {
      // Get the select elements
      var classSelect = $('#id_teaching_grades');
      var subjectSelect = $('#id_subjects');
  
      // Disable the subject select initially
      subjectSelect.prop('disabled', true);
  
      // Handle the onchange event of the class select
      classSelect.on('change', function () {
        var selectedClass = classSelect.val();
        if (selectedClass) {
          // Make an AJAX request to get the subjects for the selected class
          $.ajax({
            url: '/get_subjects/',
            type: 'GET',
            data: { class_id: selectedClass },
            success: function (data) {
              // Clear the current options in the subject select
              subjectSelect.empty();
  
              // Add the new options to the subject select
              $.each(data.subjects, function (index, subject) {
                subjectSelect.append('<option value="' + subject.id + '">' + subject.name + '</option>');
              });
  
              // Enable the subject select
              subjectSelect.prop('disabled', false);
            }
          });
        } else {
          // If no class is selected, disable the subject select and clear its options
          subjectSelect.prop('disabled', true);
          subjectSelect.empty();
        }
      });
    });
  })(django.jQuery);
  