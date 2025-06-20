let chartInstance;
let chartType = 'bar';

function formatTime() {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function appendMessage(message, sender = 'user') {
  const chatBox = document.getElementById('chat-box');

  const wrapper = document.createElement('div');
  wrapper.classList.add('message-wrapper');

  const avatar = document.createElement('img');
  avatar.classList.add('avatar');
  avatar.src = sender === 'user' ? '/static/images/user-icon.jpg' : '/static/images/bot-icon.jpg';

  const msgBubble = document.createElement('div');
  msgBubble.classList.add('message');
  msgBubble.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
  msgBubble.innerHTML = `${message}<div class="timestamp">${formatTime()}</div>`;

  if (sender === 'user') {
    wrapper.appendChild(msgBubble);
    wrapper.appendChild(avatar);
  } else {
    wrapper.appendChild(avatar);
    wrapper.appendChild(msgBubble);
  }

  chatBox.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
  const msg = document.getElementById('message').value;
  if (!msg.trim()) return;

  appendMessage(msg, 'user');

  fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: msg })
  })
  .then(res => res.json())
  .then(data => {
    appendMessage(data.response, 'bot');
    document.getElementById('message').value = '';
    loadAnalytics();
  });
}

function loadAnalytics() {
  fetch('/analytics')
    .then(res => res.json())
    .then(data => {
      const ctx = document.getElementById('analyticsChart').getContext('2d');
      if (chartInstance) chartInstance.destroy();
      chartInstance = new Chart(ctx, {
        type: chartType,
        data: {
          labels: ['Total', 'Success', 'Failure'],
          datasets: [{
            label: '# of Searches',
            data: [data.total, data.success, data.failure],
            backgroundColor: ['#007bff', '#28a745', '#dc3545'],
            borderRadius: 8,
            borderSkipped: false,
            barPercentage: 0.6,
            categoryPercentage: 0.5
          }]
        },
        options: {
          responsive: true,
          animation: {
            duration: 800,
            easing: 'easeOutBounce'
          },
          plugins: {
            legend: {
              labels: {
                font: {
                  size: 14,
                  family: 'Poppins'
                }
              }
            },
            tooltip: {
              backgroundColor: '#f8f9fa',
              titleColor: '#343a40',
              bodyColor: '#495057',
              borderColor: '#ced4da',
              borderWidth: 1
            }
          },
          scales: chartType === 'bar' ? {
            x: {
              ticks: { font: { size: 13, family: 'Poppins' } },
              grid: { color: 'rgba(0,0,0,0.05)' }
            },
            y: {
              beginAtZero: true,
              ticks: { font: { size: 13, family: 'Poppins' } },
              grid: { color: 'rgba(0,0,0,0.05)' }
            }
          } : {}
        }
      });
    });
}

function toggleChartType() {
  chartType = chartType === 'bar' ? 'pie' : 'bar';
  if (chartInstance) {
    chartInstance.destroy(); // destroy old chart
  }
  loadAnalytics(); // recreate with new type
}

function showChartModal() {
  const modal = new bootstrap.Modal(document.getElementById('analyticsModal'));
  modal.show();
  setTimeout(() => loadAnalytics(), 300); // delay ensures canvas is visible
}

function startVoice() {
  const recognition = new webkitSpeechRecognition();
  recognition.lang = 'en-US';
  recognition.start();
  recognition.onresult = (event) => {
    document.getElementById('message').value = event.results[0][0].transcript;
  };
}

function toggleTheme() {
      const chatBox = document.getElementById('chatContainer');
      chatBox.classList.toggle('dark-mode');
}

window.onload = () => {
  loadAnalytics();
  document.getElementById('toggleChartBtn').addEventListener('click', toggleChartType);
  document.getElementById('showChartBtn').addEventListener('click', showChartModal);
};