
async function toggleCode(username) {
    const codeEl = document.getElementById(`code-${username}`);
    const currentContent = codeEl.textContent;
    if (currentContent !== '••••••••') {
        codeEl.textContent = '••••••••';
        return;
    }
    try {
        const res = await fetch(`/api/invite-code/${username}`);
        const data = await res.json();
        if (res.ok) {
        codeEl.textContent = data.invite_code.code;
        } else {
        alert(data.message || 'Failed to fetch code.');
        }
    } catch (err) {
        console.error(err);
        alert('Server error.');
    }
    }

    document.getElementById('inviteForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const responseBox = document.getElementById('inviteResponse');
    responseBox.innerHTML = '';

    try {
        const res = await fetch('/api/add-invite-code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username })
        });

        const data = await res.json();
        if (res.ok) {
        responseBox.innerHTML = `
            <div class="alert alert-success" data-aos="fade-down">
            Invite code successfully created</code>
            </div>
        `;
        } else {
        responseBox.innerHTML = `
            <div class="alert alert-danger" data-aos="fade-down">
            ${data.message || 'Failed to generate invite.'}
            </div>
        `;
        }
    } catch (err) {
        console.error(err);
        responseBox.innerHTML = `
        <div class="alert alert-danger" data-aos="fade-down">
            Server error. Please try again later.
        </div>
        `;
    }
});