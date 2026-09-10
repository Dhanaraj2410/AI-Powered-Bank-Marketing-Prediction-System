function initDashboardCharts(data) {
  Chart.defaults.color = '#94a3b8';
  Chart.defaults.font.family = 'Inter, sans-serif';

  // Chart 1: Yes vs No Predictions
  const ctx1 = document.getElementById('chartYesNo');
  if (ctx1) {
    new Chart(ctx1, {
      type: 'doughnut',
      data: {
        labels: ['Yes (Subscribe)', 'No (Refuse)'],
        datasets: [{
          data: data.yesNo,
          backgroundColor: ['#10b981', '#ef4444'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' }
        }
      }
    });
  }

  // Chart 2: Predictions by Month
  const ctx2 = document.getElementById('chartMonth');
  if (ctx2) {
    new Chart(ctx2, {
      type: 'bar',
      data: {
        labels: data.monthLabels,
        datasets: [{
          label: 'Predictions',
          data: data.monthData,
          backgroundColor: '#00b4d8',
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          y: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // Chart 3: Probability Distribution Ranges
  const ctx3 = document.getElementById('chartProb');
  if (ctx3) {
    new Chart(ctx3, {
      type: 'line',
      data: {
        labels: ['< 25%', '25% - 50%', '50% - 75%', '> 75%'],
        datasets: [{
          label: 'Customer Count',
          data: data.probRanges,
          borderColor: '#7209b7',
          backgroundColor: 'rgba(114, 9, 183, 0.25)',
          fill: true,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          y: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // Chart 4: Predictions by Job
  const ctx4 = document.getElementById('chartJob');
  if (ctx4) {
    new Chart(ctx4, {
      type: 'bar',
      data: {
        labels: data.jobLabels,
        datasets: [{
          label: 'Count',
          data: data.jobData,
          backgroundColor: '#f59e0b',
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
          y: { grid: { display: false } }
        }
      }
    });
  }

  // Chart 5: Predictions by Contact Type
  const ctx5 = document.getElementById('chartContact');
  if (ctx5) {
    new Chart(ctx5, {
      type: 'pie',
      data: {
        labels: data.contactLabels,
        datasets: [{
          data: data.contactData,
          backgroundColor: ['#00b4d8', '#3b82f6', '#8b5cf6'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'bottom' } }
      }
    });
  }
}
