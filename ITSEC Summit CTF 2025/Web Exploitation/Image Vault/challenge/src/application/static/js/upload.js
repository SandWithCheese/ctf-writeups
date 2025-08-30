
const fileInput = document.getElementById('fileInput');
const uploadArea = document.querySelector('.upload-area');

fileInput.addEventListener('change', handleFiles);
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#667eea';
    uploadArea.style.background = 'rgba(102, 126, 234, 0.1)';
});
uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--glass-border)';
    uploadArea.style.background = 'var(--glass-bg)';
});
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    handleFiles({ target: { files } });
    uploadArea.style.borderColor = 'var(--glass-border)';
    uploadArea.style.background = 'var(--glass-bg)';
});

function handleFiles(e) {
    const files = e.target.files;
    if (files.length === 0) return;

    [...files].forEach(file => {
        if (file.type !== 'image/png') {
            alert(`Only PNG files are allowed.`);
            return;
        }

        const reader = new FileReader();
        reader.onload = () => {
            let base64Data = reader.result.split(',')[1];

            fetch('/api/upload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image: base64Data
                })
            })
            .then(res => res.json())
            .then(data => {
                alert(`Successfully Uploaded`);
                window.location.href = '/home';
            })
            .catch(err => {
                alert(`Failed to upload`);
            });
        };
        reader.readAsDataURL(file);
    });
}