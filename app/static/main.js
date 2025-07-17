const socket = io();

// Skor güncellenince
socket.on('update_data', data => {
    document.getElementById('team1_name').innerText = data.team1_name;
    document.getElementById('team2_name').innerText = data.team2_name;
    document.getElementById('team1_score').innerText = data.team1_score;
    document.getElementById('team2_score').innerText = data.team2_score;
});

// Süre güncellenince
socket.on('update_time', data => {
    const m = String(data.minute).padStart(2, '0');
    const s = String(data.second).padStart(2, '0');
    document.getElementById('timer').innerText = `${m}:${s}`;
});

// Her saniyede zaman iste
setInterval(() => {
    socket.emit('get_time');
}, 1000);