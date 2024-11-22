/**
 * GitHubLLM 对象 - 处理GitHub仓库内容转换为LLM格式的前端逻辑
 */
const GitHubLLM = {
    // 存储DOM元素引用
    elements: null,

    /**
     * 初始化函数 - 获取DOM元素并绑定事件
     */
    init() {
        console.log('初始化 GitHubLLM...');
        this.elements = {
            repoUrl: document.getElementById('repo-url'),
            processBtn: document.getElementById('process-btn'),
            loading: document.getElementById('loading'),
            progress: document.getElementById('progress'),
            progressText: document.getElementById('progress-text'),
            error: document.getElementById('error'),
            result: document.getElementById('result'),
            preview: document.getElementById('preview'),
            resultFilename: document.getElementById('result-filename'),
            downloadBtn: document.getElementById('download-btn'),
            copyBtn: document.getElementById('copy-btn')
        };

        this.bindEvents();
        console.log('GitHubLLM 初始化完成');
    },

    /**
     * 绑定事件处理函数
     */
    bindEvents() {
        console.log('绑定事件处理函数...');
        this.elements.processBtn.addEventListener('click', () => this.processRepo());
        
        if (this.elements.copyBtn) {
            this.elements.copyBtn.addEventListener('click', () => this.copyContent());
        }
        console.log('事件绑定完成');
    },

    /**
     * 处理仓库内容的主函数
     */
    async processRepo() {
        try {
            // 验证输入
            if (!this.elements.repoUrl.value) {
                this.showError('请输入GitHub仓库URL');
                return;
            }

            this.showLoading();
            console.log('开始请求 /process 接口...');
            const response = await fetch('/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repo_url: this.elements.repoUrl.value })
            });

            if (!response.ok) {
                console.error('请求失败:', response.status, response.statusText);
                throw new Error('网络请求失败');
            }
            console.log('请求成功,开始处理响应流...');

            // 创建响应流读取器
            const reader = response.body
                .pipeThrough(new TextDecoderStream())
                .getReader();
            console.log('响应流读取器创建完成');

            let buffer = ''; // 添加缓冲区
            
            while (true) {
                const {done, value} = await reader.read();
                
                if (done) {
                    // 处理缓冲区中剩余的数据
                    if (buffer.trim()) {
                        try {
                            const data = JSON.parse(buffer);
                            console.log('处理最后的数据:', data);
                            await this.handleProgress(data);
                        } catch (e) {
                            console.error('解析最后数据失败:', e);
                        }
                    }
                    break;
                }
                
                buffer += value;
                const lines = buffer.split('\n');
                buffer = lines.pop() || ''; // 保留最后一个不完整的行
                
                for (const line of lines) {
                    if (line.trim()) {
                        try {
                            const data = JSON.parse(line);
                            console.log('收到事件:', data.type, data);
                            await this.handleProgress(data);
                        } catch (e) {
                            console.error('解析事件失败:', e, line);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('处理过程出错:', error);
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    },

    /**
     * 处理进度更新事件
     * @param {Object} data - 进度数据
     */
    async handleProgress(data) {
        switch (data.type) {
            case 'start':
                console.log('开始处理:', data);
                this.elements.progressText.textContent = `正在处理文件 (0/${data.total})...`;
                this.elements.progress.style.width = '0%';
                break;
                
            case 'progress':
                console.log('处理进度:', data);
                const percent = (data.current / data.total) * 100;
                this.elements.progressText.textContent = 
                    `正在处理 ${data.file} (${data.current}/${data.total})`;
                this.elements.progress.style.width = `${percent}%`;
                break;
                
            case 'error':
                console.error('处理出错:', data);
                break;
                
            case 'complete':
                console.log('处理完成:', data);
                this.showResult(data);
                this.elements.progressText.textContent = 
                    `已完成处理 ${data.total_processed} 个文件`;
                this.elements.progress.style.width = '100%';
                break;
                
            default:
                console.warn('未知事件类型:', data);
        }
    },

    /**
     * 显示加载状态
     */
    showLoading() {
        console.log('显示加载状态...');
        this.elements.loading.classList.remove('hidden');
        this.elements.error.classList.add('hidden');
        this.elements.result.classList.add('hidden');
        this.elements.processBtn.disabled = true;
    },

    /**
     * 隐藏加载状态
     */
    hideLoading() {
        console.log('隐藏加载状态...');
        this.elements.loading.classList.add('hidden');
        this.elements.processBtn.disabled = false;
    },

    /**
     * 显示错误信息
     * @param {string} message - 错误信息
     */
    showError(message) {
        console.error('显示错误:', message);
        this.elements.error.textContent = message;
        this.elements.error.classList.remove('hidden');
        this.hideLoading();
    },

    /**
     * 显示处理结果
     * @param {Object} data - 结果数据
     */
    showResult(data) {
        console.log('显示结果:', data);
        const { filename, content } = data;
        
        // 保存当前文件名
        this.currentFile = filename;
        console.log('设置当前文件名:', this.currentFile);
        
        if (this.elements.resultFilename) {
            this.elements.resultFilename.textContent = filename;
        }
        
        if (this.elements.preview) {
            this.elements.preview.textContent = content;
        }
        
        if (this.elements.result) {
            this.elements.result.classList.remove('hidden');
            this.elements.result.scrollIntoView({ behavior: 'smooth' });
        }
    },

    /**
     * 复制内容到剪贴板
     */
    async copyContent() {
        try {
            await navigator.clipboard.writeText(this.elements.preview.textContent);
            
            // 显示复制成功提示
            const originalText = this.elements.copyBtn.textContent;
            this.elements.copyBtn.textContent = '复制成功！';
            this.elements.copyBtn.classList.add('bg-green-100');
            
            setTimeout(() => {
                this.elements.copyBtn.textContent = originalText;
                this.elements.copyBtn.classList.remove('bg-green-100');
            }, 2000);
        } catch (err) {
            console.error('复制失败:', err);
            this.showError('复制失败，请手动复制');
        }
    },

    async downloadFile() {
        const btn = this.elements.downloadBtn;
        const originalText = btn.textContent;
        
        try {
            // 设置加载状态
            btn.textContent = 'Downloading...';
            btn.disabled = true;
            
            console.log('开始下载文件处理');
            console.log('当前文件:', this.currentFile);
            
            if (!this.currentFile) {
                console.error('没有可下载的文件');
                this.showError('没有可下载的文件');
                return;
            }

            try {
                console.log(`准备下载文件: ${this.currentFile}`);
                const response = await fetch(`/download/${this.currentFile}`);
                console.log('下载请求响应:', response);

                if (!response.ok) {
                    throw new Error(`下载失败: ${response.status} ${response.statusText}`);
                }

                // 获取文件内容并下载
                const blob = await response.blob();
                console.log('获取到文件 blob:', blob);

                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = this.currentFile;
                
                console.log('创建下载链接:', link.href);
                document.body.appendChild(link);
                link.click();
                
                // 清理
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
                console.log('下载流程完成');

            } catch (error) {
                console.error('下载过程出错:', error);
                this.showError(`下载失败: ${error.message}`);
            }
        } catch (error) {
            console.error('下载失败:', error);
            this.showError(`下载失败: ${error.message}`);
        } finally {
            // 恢复按钮状态
            btn.textContent = originalText;
            btn.disabled = false;
        }
    }
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('页面加载完成，初始化 GitHubLLM');
    GitHubLLM.init();
}); 