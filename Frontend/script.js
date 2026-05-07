document.getElementById('ai-form').addEventListener('submit', async function(e) {
    e.preventDefault(); 

    const docType = document.getElementById('doc_type').value;
    const details = document.getElementById('details').value;
    const submitBtn = document.getElementById('submit-btn');
    const loadingDiv = document.getElementById('loading');
    const resultBox = document.getElementById('result-box');
    const aiOutput = document.getElementById('ai-output');

    if (!details.trim()) {
        alert("Please enter your details first!");
        return;
    }

    submitBtn.disabled = true;
    submitBtn.innerText = "Generating...";
    submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
    loadingDiv.classList.remove('hidden');
    resultBox.classList.add('hidden');

    try {
        const response = await fetch('http://127.0.0.1:5000/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                doc_type: docType,
                details: details
            })
        });

        const data = await response.json();

        if (data.success) {
            aiOutput.innerHTML = marked.parse(data.document);
            resultBox.classList.remove('hidden');
        } else {
            alert("Error from AI: " + data.error);
        }
    } catch (error) {
        console.error("Fetch error:", error);
        alert("Cannot connect to Backend. Please make sure your Python app.py is running!");
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = "Generate Resume";
        submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        loadingDiv.classList.add('hidden');
    }
});

// 1. Copy to Clipboard Feature
document.getElementById('copy-btn').addEventListener('click', function() {
    const aiOutputText = document.getElementById('ai-output').innerText;
    const copyBtn = document.getElementById('copy-btn');
    
    navigator.clipboard.writeText(aiOutputText).then(() => {
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = "✅ Copied!";
        setTimeout(() => { copyBtn.innerHTML = originalText; }, 2000);
    }).catch(err => {
        alert("Failed to copy text!");
    });
});

// 2. Download as PDF Feature (ADVANCED PRINT FIX)
document.getElementById('pdf-btn').addEventListener('click', function() {
    const element = document.getElementById('ai-output');
    const pdfBtn = document.getElementById('pdf-btn');
    
    const originalBtnText = pdfBtn.innerHTML;
    pdfBtn.innerHTML = "⏳ Generating PDF...";
    
    // FIX 2: Original element ko cherne ki bajaye uski ek copy (clone) banayen
    const clone = element.cloneNode(true);
    
    // Print ke liye white background aur purely black text set karein
    clone.className = "p-10 bg-white text-black prose max-w-none"; 
    
    // Custom style banayen taake clone ke andar har cheez black ho
    const style = document.createElement('style');
    style.innerHTML = `
        .pdf-mode, .pdf-mode h1, .pdf-mode h2, .pdf-mode h3, .pdf-mode p, .pdf-mode li, .pdf-mode strong { 
            color: black !important; 
        }
    `;
    clone.classList.add('pdf-mode');

    // Clone ko screen ke peeche chhupa dein (taake user ko nazar na aaye)
    const container = document.createElement('div');
    container.style.position = 'absolute';
    container.style.top = '-9999px'; 
    container.appendChild(style);
    container.appendChild(clone);
    document.body.appendChild(container);

    // FIX 3: ScrollY: 0 (Blank space khatam) aur pagebreak (lines na katne ke liye)
    const opt = {
        margin:       0.5,
        filename:     'ResumAI_Document.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2, useCORS: true, scrollY: 0 }, 
        jsPDF:        { unit: 'in', format: 'a4', orientation: 'portrait' },
        pagebreak:    { mode: ['avoid-all', 'css', 'legacy'] }
    };

    html2pdf().set(opt).from(clone).save().then(() => {
        // PDF download hone ke baad hidden copy ko delete kar dein
        document.body.removeChild(container);
        pdfBtn.innerHTML = originalBtnText;
    }).catch(err => {
        console.error("PDF generation error:", err);
        alert("Failed to generate PDF. Check console for details.");
        document.body.removeChild(container);
        pdfBtn.innerHTML = originalBtnText;
    });
});