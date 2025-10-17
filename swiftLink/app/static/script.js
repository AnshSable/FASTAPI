const API_BASE = '/api/v1';

// DOM Elements
const shortenForm = document.getElementById('shortenForm');
const resultCard = document.getElementById('resultCard');
const loading = document.getElementById('loading');
const errorCard = document.getElementById('errorCard');
const errorMessage = document.getElementById('errorMessage');

// Form submission
shortenForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(shortenForm);
    const data = {
        original_url: formData.get('original_url'),
        custom_code: formData.get('custom_code') || undefined,
        title: formData.get('title') || undefined
    };
    
    await shortenUrl(data);
});

async function shortenUrl(data) {
    showLoading();
    hideError();
    
    try {
        const response = await fetch(`${API_BASE}/shorten`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showResult(result);
        } else {
            showError(result.detail || 'An error occurred');
        }
    } catch (error) {
        showError('Network error. Please try again.');
    } finally {
        hideLoading();
    }
}

function showResult(data) {
    document.getElementById('shortUrlOutput').value = data.short_url;
    document.getElementById('originalUrlOutput').textContent = data.original_url;
    document.getElementById('clicksOutput').textContent = data.clicks;
    document.getElementById('createdAtOutput').textContent = new Date(data.created_at).toLocaleString();
    
    shortenForm.style.display = 'none';
    resultCard.style.display = 'block';
}

function copyToClipboard() {
    const shortUrlInput = document.getElementById('shortUrlOutput');
    shortUrlInput.select();
    document.execCommand('copy');
    
    const copyBtn = document.getElementById('copyBtn');
    const originalText = copyBtn.textContent;
    copyBtn.textContent = 'Copied!';
    copyBtn.style.background = '#28a745';
    
    setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.style.background = '';
    }, 2000);
}

function resetForm() {
    shortenForm.reset();
    shortenForm.style.display = 'block';
    resultCard.style.display = 'none';
    hideError();
}

function showLoading() {
    loading.style.display = 'block';
    document.getElementById('shortenBtn').disabled = true;
}

function hideLoading() {
    loading.style.display = 'none';
    document.getElementById('shortenBtn').disabled = false;
}

function showError(message) {
    errorMessage.textContent = message;
    errorCard.style.display = 'block';
}

function hideError() {
    errorCard.style.display = 'none';
}

// QR Code functionality (optional enhancement)
function generateQRCode(shortUrl) {
    // You can integrate a QR code library here later
    console.log('QR Code for:', shortUrl);
}