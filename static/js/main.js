document.addEventListener('DOMContentLoaded', function () {
  // Initialize Bootstrap Tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Handle Prediction Feedback 👍 / 👎 AJAX Submit
  var feedbackButtons = document.querySelectorAll('.btn-feedback');
  feedbackButtons.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var predId = this.getAttribute('data-pred-id');
      var feedbackVal = this.getAttribute('data-feedback');
      var parentContainer = document.getElementById('feedback-container');

      fetch('/api/predictions/' + predId + '/feedback/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ feedback: feedbackVal })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          if (parentContainer) {
            parentContainer.innerHTML = '<div class="alert alert-success d-inline-block py-2 px-3 mb-0"><i class="fas fa-check-circle me-1"></i> Thank you for your feedback!</div>';
          }
        }
      })
      .catch(err => console.error('Feedback submission error:', err));
    });
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
