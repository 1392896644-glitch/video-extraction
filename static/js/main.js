// 文件上传处理
const uploadArea = document.getElementById('uploadArea');
const videoFile = document.getElementById('videoFile');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const uploadPlaceholder = document.querySelector('.upload-placeholder');
const uploadBtn = document.getElementById('uploadBtn');
const uploadBtnText = document.getElementById('uploadBtnText');
const progressBar = document.getElementById('progressBar');
const progressText = document.getElementById('progressText');
const progressSection = document.getElementById('progressSection');
const resultsSection = document.getElementById('resultsSection');

// 风格标签
const styleLabels = [
    '痛点直击型',
    '情感共鸣型',
    '数据说服型',
    '场景化描述型',
    '简洁有力型'
];

// 风格颜色
const styleColors = [
    'primary',
    'danger',
    'info',
    'warning',
    'success'
];

// 点击上传区域触发文件选择
uploadArea.addEventListener('click', () => {
    videoFile.click();
});

// 文件选择事件
videoFile.addEventListener('change', handleFileSelect);

// 拖拽上传
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        videoFile.files = files;
        handleFileSelect();
    }
});

// 处理文件选择
function handleFileSelect() {
    const file = videoFile.files[0];
    if (!file) return;
    
    // 显示文件信息
    uploadPlaceholder.style.display = 'none';
    fileInfo.style.display = 'block';
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    
    // 启用上传按钮
    uploadBtn.disabled = false;
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// 上传按钮点击事件
uploadBtn.addEventListener('click', async () => {
    const file = videoFile.files[0];
    if (!file) return;
    
    // 禁用按钮，显示加载状态
    uploadBtn.disabled = true;
    uploadBtn.querySelector('.spinner-border').style.display = 'inline-block';
    uploadBtnText.textContent = '处理中...';
    
    // 显示进度条
    progressSection.style.display = 'block';
    resultsSection.style.display = 'none';
    
    // 创建FormData
    const formData = new FormData();
    formData.append('video', file);
    
    try {
        // 模拟进度
        simulateProgress();
        
        // 发送请求
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 显示结果
            displayResults(result.data);
        } else {
            alert('处理失败：' + result.error);
        }
    } catch (error) {
        alert('处理失败：' + error.message);
    } finally {
        // 恢复按钮状态
        uploadBtn.disabled = false;
        uploadBtn.querySelector('.spinner-border').style.display = 'none';
        uploadBtnText.textContent = '开始分析';
        
        // 隐藏进度条
        setTimeout(() => {
            progressSection.style.display = 'none';
        }, 500);
    }
});

// 模拟进度条
function simulateProgress() {
    let progress = 0;
    const steps = [
        { progress: 20, text: '提取视频中...' },
        { progress: 40, text: '分析文案中...' },
        { progress: 60, text: '生成改写文案中...' },
        { progress: 80, text: '写入飞书表格中...' },
        { progress: 100, text: '完成！' }
    ];
    
    let stepIndex = 0;
    
    const interval = setInterval(() => {
        if (stepIndex < steps.length) {
            progressBar.style.width = steps[stepIndex].progress + '%';
            progressText.textContent = steps[stepIndex].text;
            stepIndex++;
        } else {
            clearInterval(interval);
        }
    }, 800);
}

// 显示结果
function displayResults(data) {
    // 隐藏进度，显示结果
    progressSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    // 填充数据
    document.getElementById('extractedText').textContent = data.extracted_text || '提取失败';
    document.getElementById('textSummary').textContent = data.text_summary || '生成失败';
    document.getElementById('textAnalysis').textContent = data.text_analysis || '分析失败';
    
    // 显示5条改写文案
    const rewrittenTextsDiv = document.getElementById('rewrittenTexts');
    rewrittenTextsDiv.innerHTML = '';
    
    if (data.rewritten_texts && data.rewritten_texts.length > 0) {
        data.rewritten_texts.forEach((text, index) => {
            const item = document.createElement('div');
            item.className = 'rewrite-item';
            item.innerHTML = `
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h6>
                            <span class="badge bg-${styleColors[index % styleColors.length]}">改写${index + 1}</span>
                            ${styleLabels[index % styleLabels.length]}
                        </h6>
                        <div class="content">${text || '生成失败'}</div>
                    </div>
                    <button class="btn btn-sm btn-outline-secondary" onclick="copyRewrite(${index})">复制</button>
                </div>
            `;
            rewrittenTextsDiv.appendChild(item);
        });
    } else {
        rewrittenTextsDiv.innerHTML = '<p class="text-muted">改写文案生成失败</p>';
    }
    
    // 设置飞书链接
    const feishuLink = document.getElementById('feishuLink');
    if (data.feishu_url) {
        feishuLink.href = data.feishu_url;
        feishuLink.style.display = 'inline-block';
    } else {
        feishuLink.style.display = 'none';
    }
    
    // 滚动到结果区域
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// 复制文本
function copyText(elementId) {
    const text = document.getElementById(elementId).textContent;
    copyToClipboard(text);
}

// 复制改写文案
window.copyRewrite = function(index) {
    const items = document.querySelectorAll('.rewrite-item .content');
    if (items[index]) {
        const text = items[index].textContent;
        copyToClipboard(text);
    }
}

// 复制到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('已复制到剪贴板！');
    }).catch(err => {
        console.error('复制失败:', err);
        // 降级方案
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        alert('已复制到剪贴板！');
    });
}

// 防止页面刷新丢失文件
window.addEventListener('beforeunload', (e) => {
    if (videoFile.files.length > 0) {
        e.preventDefault();
        e.returnValue = '';
    }
});
