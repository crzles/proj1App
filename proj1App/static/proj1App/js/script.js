// DISCUSSION PODS — mic / join / leave


function joinPod(podId) {
    const bar       = document.getElementById('micBar');
    const label     = document.getElementById('micLabel');
    const indicator = document.getElementById('micIndicator');

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                bar.style.display = 'flex';
                label.textContent = 'Mic active — Pod ' + podId;
                indicator.classList.add('active');
                window._activeStream = stream;
            })
            .catch(() => {
                bar.style.display = 'flex';
                label.textContent = 'Mic blocked — joined as listener';
            });
    } else {
        bar.style.display = 'flex';
        label.textContent = 'Joined Pod ' + podId + ' (listener)';
    }
}

function leavePod() {
    if (window._activeStream) {
        window._activeStream.getTracks().forEach(t => t.stop());
        window._activeStream = null;
    }
    const bar       = document.getElementById('micBar');
    const indicator = document.getElementById('micIndicator');
    if (bar)       bar.style.display = 'none';
    if (indicator) indicator.classList.remove('active');
}