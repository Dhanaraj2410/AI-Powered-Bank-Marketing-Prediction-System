function initModelPerformanceCharts(rocFpr, rocTpr) {
  Chart.defaults.color = '#94a3b8';
  Chart.defaults.font.family = 'Inter, sans-serif';

  // ROC Curve Plot
  const ctxRoc = document.getElementById('chartRocCurve');
  if (ctxRoc && rocFpr && rocTpr) {
    const dataPoints = rocFpr.map((fpr, i) => ({ x: fpr, y: rocTpr[i] }));
    
    new Chart(ctxRoc, {
      type: 'line',
      data: {
        datasets: [
          {
            label: 'ROC Curve (Logistic Regression)',
            data: dataPoints,
            borderColor: '#00b4d8',
            borderWidth: 2,
            pointRadius: 0,
            fill: false
          },
          {
            label: 'Random Classifier (AUC = 0.50)',
            data: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
            borderColor: '#64748b',
            borderWidth: 1,
            borderDash: [5, 5],
            pointRadius: 0,
            fill: false
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            type: 'linear',
            position: 'bottom',
            title: { display: true, text: 'False Positive Rate (FPR)', color: '#cbd5e1' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            min: 0, max: 1
          },
          y: {
            title: { display: true, text: 'True Positive Rate (TPR / Recall)', color: '#cbd5e1' },
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            min: 0, max: 1
          }
        },
        plugins: {
          legend: { position: 'bottom' }
        }
      }
    });
  }
}
