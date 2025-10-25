const API_BASE_URL = 'http://localhost:8000';

// Get token from localStorage
function getToken() {
    return localStorage.getItem('token');
}

// Show message
function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

// Load user data
async function loadUserData() {
    const token = getToken();
    
    if (!token) {
        window.location.href = 'index.html';
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const userData = await response.json();
            document.getElementById('username').textContent = userData.username;
            document.getElementById('userEmail').textContent = userData.email;
            document.getElementById('createdAt').textContent = new Date(userData.created_at).toLocaleDateString();
            
            // Pre-fill update form
            document.getElementById('updateEmail').value = userData.email;
            document.getElementById('updateUsername').value = userData.username;
        } else {
            localStorage.removeItem('token');
            window.location.href = 'index.html';
        }
    } catch (error) {
        showMessage('Error loading user data: ' + error.message, 'error');
    }
}

// Update profile
function updateProfile() {
    document.getElementById('updateForm').style.display = 'block';
}

function hideUpdateForm() {
    document.getElementById('updateForm').style.display = 'none';
}

document.getElementById('updateFormElement').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const updateData = {};
    
    if (formData.get('email')) updateData.email = formData.get('email');
    if (formData.get('username')) updateData.username = formData.get('username');
    if (formData.get('password')) updateData.password = formData.get('password');
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${getToken()}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updateData)
        });
        
        if (response.ok) {
            showMessage('Profile updated successfully!', 'success');
            hideUpdateForm();
            loadUserData(); // Reload user data
        } else {
            const data = await response.json();
            showMessage(data.detail || 'Update failed', 'error');
        }
    } catch (error) {
        showMessage('Network error: ' + error.message, 'error');
    }
});

// Logout
function logout() {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
}

// Check authentication on page load
window.addEventListener('load', () => {
    const token = getToken();
    if (!token) {
        window.location.href = 'index.html';
    } else {
        loadUserData();
    }
});